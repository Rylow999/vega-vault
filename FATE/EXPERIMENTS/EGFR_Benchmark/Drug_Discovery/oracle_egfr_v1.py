#!/usr/bin/env python3
"""
Oracle EGFR v1 — Similarity-based inhibitor prediction.

Protocol:
1. Load ChEMBL EGFR dataset (IC50 values, SMILES)
2. Precompute Morgan fingerprints for all compounds
3. For each candidate phase vector:
   a. Decode phase → fingerprint sintético (1024 bits)
   b. Find nearest neighbor in ChEMBL by Tanimoto similarity
   c. Return pIC50 normalizado como fitness [0, 1]

Fitness = pIC50 / 9.0
  - IC50 = 1nM → pIC50 = 9.0 → fitness = 1.0
  - IC50 = 1μM → pIC50 = 6.0 → fitness = 0.67
  - IC50 = 1mM → pIC50 = 3.0 → fitness = 0.33
"""
import json
import numpy as np
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem
from collections import defaultdict

# — Config —
DATA_PATH = Path(r"C:/Users/lucas/repos/nexus-vault/experiments/EGFR_Drug_Discovery/data/chembl_egfr_ic50_1000.json")
FINGERPRINT_RADIUS = 2
FINGERPRINT_NBITS = 1024
CHUNK_SIZE = 256  # Batch size for GPU-style evaluation


class EGFROracle:
    def __init__(self, data_path=DATA_PATH):
        """Load and precompute ChEMBL EGFR dataset."""
        self.compounds = []
        self.fingerprints = []
        self.pic50_values = []
        
        if not data_path.exists():
            raise FileNotFoundError(f"ChEMBL data not found at {data_path}. Please download first.")
        
        print(f"[EGFR Oracle] Loading data from {data_path}...")
        with open(data_path) as f:
            data = json.load(f)
        
        activities = data.get("activities", [])
        print(f"[EGFR Oracle] Found {len(activities)} activities")
        
        # Deduplicate: keep best (lowest) IC50 per unique SMILES
        smiles_to_best = {}
        for act in activities:
            smiles = act.get("canonical_smiles", "")
            ic50_nm = act.get("standard_value")  # in nM (may be string)
            if not smiles or ic50_nm is None:
                continue
            
            # Convert to float (API returns strings sometimes)
            try:
                ic50_nm = float(ic50_nm)
            except (ValueError, TypeError):
                continue
            
            if ic50_nm <= 0:
                continue
            
            # Calculate pIC50 = -log10(IC50[M]) = -log10(IC50[nM] / 1e9) = 9 - log10(IC50[nM])
            pic50 = 9.0 - np.log10(ic50_nm)
            
            if smiles not in smiles_to_best or pic50 > smiles_to_best[smiles]:
                smiles_to_best[smiles] = pic50
        
        # Build compound database
        print(f"[EGFR Oracle] Processing {len(smiles_to_best)} unique compounds...")
        for smiles, pic50 in smiles_to_best.items():
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                continue
            
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, FINGERPRINT_RADIUS, nBits=FINGERPRINT_NBITS)
            fp_array = np.array(fp, dtype=np.uint8)
            
            self.compounds.append(smiles)
            self.fingerprints.append(fp_array)
            self.pic50_values.append(pic50)
        
        # Convert to numpy arrays for fast similarity search
        self.fps_matrix = np.array(self.fingerprints, dtype=np.uint8)
        self.pic50_array = np.array(self.pic50_values, dtype=np.float32)
        
        print(f"[EGFR Oracle] Loaded {len(self.compounds)} compounds")
        print(f"[EGFR Oracle] pIC50 range: {self.pic50_array.min():.2f} - {self.pic50_array.max():.2f}")
        print(f"[EGFR Oracle] FPS matrix shape: {self.fps_matrix.shape}")
    
    def phase_to_fingerprint(self, phase):
        """
        Decode phase vector → 1024-bit fingerprint.
        
        Each phase dimension controls 1024/len(phase) bits.
        phase[i] in [0, 2π] → determines which bits to set in that segment.
        """
        dim = len(phase)
        bits_per_dim = FINGERPRINT_NBITS // dim
        fp = np.zeros(FINGERPRINT_NBITS, dtype=np.uint8)
        
        for i in range(dim):
            p = phase[i] % (2.0 * np.pi)
            # Map phase to bit positions in this segment
            num_bits = max(1, int((p / (2.0 * np.pi)) * bits_per_dim) + 1)
            start_bit = i * bits_per_dim
            
            # Set consecutive bits based on phase
            for b in range(min(num_bits, bits_per_dim)):
                fp[start_bit + b] = 1
        
        return fp
    
    def tanimoto_similarity(self, fp1, fp2):
        """Calculate Tanimoto similarity between two fingerprints."""
        intersection = np.sum(fp1 & fp2)
        union = np.sum(fp1) + np.sum(fp2) - intersection
        return intersection / union if union > 0 else 0.0
    
    def find_nearest(self, candidate_fp):
        """
        Find nearest neighbor in ChEMBL by Tanimoto similarity.
        Returns (smiles, pIC50, similarity).
        """
        # Batch computation of Tanimoto for all compounds
        intersections = np.sum(self.fps_matrix & candidate_fp, axis=1)
        unions = np.sum(self.fps_matrix, axis=1) + np.sum(candidate_fp) - intersections
        
        # Handle division by zero
        similarities = np.where(unions > 0, intersections / unions, 0.0)
        
        # Find best match
        best_idx = np.argmax(similarities)
        best_sim = similarities[best_idx]
        best_pic50 = self.pic50_array[best_idx]
        best_smiles = self.compounds[best_idx]
        
        return best_smiles, best_pic50, best_sim
    
    def evaluate(self, phase):
        """
        Evaluate fitness for a single phase vector.
        
        Returns:
          - fitness: float in [0, 1] (normalized pIC50)
          - info: dict with details (nearest_smiles, similarity, pIC50, etc.)
        """
        # Phase → fingerprint
        candidate_fp = self.phase_to_fingerprint(phase)
        
        # Find nearest in ChEMBL
        nearest_smiles, nearest_pic50, similarity = self.find_nearest(candidate_fp)
        
        # Fitness = pIC50 / 9.0 (normalize to [0, 1])
        # pIC50=9 (IC50=1nM) → fitness=1.0
        # pIC50=3 (IC50=1mM) → fitness=0.33
        fitness = nearest_pic50 / 9.0
        fitness = min(1.0, max(0.0, fitness))  # Clamp to [0, 1]
        
        info = {
            "nearest_smiles": nearest_smiles,
            "similarity": float(similarity),
            "pIC50": float(nearest_pic50),
            "IC50_nM": float(10 ** (9.0 - nearest_pic50)),
            "fitness": float(fitness),
        }
        
        return fitness, info
    
    def evaluate_batch(self, phases):
        """
        Evaluate fitness for multiple phase vectors (batch mode).
        
        Args:
          phases: np.array of shape (n_candidates, dim)
        
        Returns:
          fitnesses: np.array of shape (n_candidates,)
          infos: list of dicts
        """
        n_candidates = len(phases)
        fitnesses = np.zeros(n_candidates, dtype=np.float32)
        infos = []
        
        for i, phase in enumerate(phases):
            fp = self.phase_to_fingerprint(phase)
            nearest_smiles, nearest_pic50, similarity = self.find_nearest(fp)
            
            fitness = nearest_pic50 / 9.0
            fitness = min(1.0, max(0.0, fitness))
            
            fitnesses[i] = fitness
            infos.append({
                "nearest_smiles": nearest_smiles,
                "similarity": float(similarity),
                "pIC50": float(nearest_pic50),
                "IC50_nM": float(10 ** (9.0 - nearest_pic50)),
            })
        
        return fitnesses, infos


# — Oracle API for FATE-v5 pipe mode —
def main():
    """
    Run as pipe oracle for FATE-v5.
    
    Input (stdin): JSON lines with {"req": [phase_vector]}
    Output (stdout): JSON lines with {"fit": fitness, "info": {...}}
    """
    import sys
    
    # Load oracle
    try:
        oracle = EGFROracle()
    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
    
    print(f"[EGFR Oracle] Ready, waiting for requests...", file=sys.stderr)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        
        if "req" not in obj:
            continue
        
        phase = obj["req"]
        if isinstance(phase, list) and len(phase) > 0 and isinstance(phase[0], list):
            # Batch mode: [[phase1], [phase2], ...]
            phases = [np.array(p, dtype=np.float64) for p in phase]
            fitnesses, infos = oracle.evaluate_batch(phases)
            # For batch, return array of fitnesses
            output = {"fit": fitnesses.tolist(), "infos": infos}
        else:
            # Scalar mode: [p1, p2, ...]
            phase = np.array(phase, dtype=np.float64)
            fitness, info = oracle.evaluate(phase)
            output = {"fit": fitness, "info": info}
        
        print(json.dumps(output))
        sys.stdout.flush()


if __name__ == "__main__":
    main()