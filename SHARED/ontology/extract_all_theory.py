#!/usr/bin/env python3
"""
Extract ALL theoretical constructs from papers and notes into Ontology
Processes each paper to find equations, theorems, definitions, predictions, etc.
"""
import json, re, os, sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

PAPERS_DIR = Path("/home/delorien/vaults/nexus-dscn/papers")
NOTES_DIR = Path("/home/delorien/vaults/nexus-dscn/ontology/notes")
GRAPH_PATH = Path("~/.openclaw/workspace/memory/ontology/graph.jsonl").expanduser()

sys.path.insert(0, str(Path("~/.openclaw/workspace/skills/ontology/scripts").expanduser()))
from ontology import create_entity, create_relation, append_op, load_graph, generate_id

def extract_equations(content: str, paper_id: str) -> List[Dict]:
    """Extract equations from paper content"""
    equations = []
    
    # Pattern: "Ecuación N" or "Equation N" or "Ec. N"
    eq_patterns = [
        r'(?:Ecuaci[oó]n|Equation|Ec\.)\s*(\d+)\s*[—:-]\s*([^\n]+)',
        r'(?:Ec\.\s*)?(\d+)\s*[—:-]\s*([^\n]+(?:\\omega|\\phi|\\beta|\\gamma|\\alpha|\\lambda|\\kappa|\\theta|\\rho|\\sigma|\\eta|\\Delta|\\nabla|\\sum|\\prod|\\int|\\partial|\\times|\\cdot|\\leq|\\geq|\\neq|\\approx|\\sim|\\propto|\\in|\\subset|\\cup|\\cap|\\forall|\\exists|\\rightarrow|\\leftarrow|\\leftrightarrow|\\Rightarrow|\\Leftrightarrow|\\pm|\\mp|\\times|\\div|\\sqrt|\\frac|\\sum|\\prod|\\lim|\\log|\\exp|\\sin|\\cos|\\tan|\\max|\\min|\\inf|\\sup))',
        r'\$\$([^$]+)\$\$',
        r'\$([^$]+)\$',
    ]
    
    # Simple line-based extraction for numbered equations
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Match patterns like "### Ecuación 1 — ..." or "**Ecuación 1**"
        m = re.search(r'(?:Ecuaci[oó]n|Equation|Ec\.)\s*(\d+)', line, re.IGNORECASE)
        if m:
            eq_num = m.group(1)
            # Get description from next lines
            desc_lines = []
            for j in range(i+1, min(i+10, len(lines))):
                if lines[j].strip() and not lines[j].startswith('#'):
                    desc_lines.append(lines[j].strip())
                elif lines[j].startswith('##'):
                    break
            desc = ' '.join(desc_lines[:5])
            
            # Try to find formula in nearby lines
            formula = ""
            for j in range(i, min(i+15, len(lines))):
                if '$' in lines[j] or '\\' in lines[j]:
                    formula = lines[j].strip()
                    break
            
            equations.append({
                'number': eq_num,
                'name': f"Equation {eq_num}",
                'formula': formula or desc[:200],
                'description': desc[:500],
                'paper_id': paper_id
            })
    
    return equations

def extract_theorems(content: str, paper_id: str) -> List[Dict]:
    """Extract theorems from paper content"""
    theorems = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        m = re.search(r'(?:Teorema|Theorem)\s+(\d+[\.\d]*)\s*[—:-]?\s*(.*)', line, re.IGNORECASE)
        if m:
            thm_num = m.group(1)
            title = m.group(2).strip()
            
            # Get proof/content
            proof_lines = []
            for j in range(i+1, min(i+30, len(lines))):
                if lines[j].strip() and not lines[j].startswith('##'):
                    proof_lines.append(lines[j].strip())
                elif lines[j].startswith('##'):
                    break
            
            theorems.append({
                'number': thm_num,
                'name': title or f"Theorem {thm_num}",
                'statement': ' '.join(proof_lines[:10]),
                'paper_id': paper_id
            })
    
    return theorems

def extract_definitions(content: str, paper_id: str) -> List[Dict]:
    """Extract definitions from paper content"""
    definitions = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        m = re.search(r'(?:Definici[oó]n|Definition)\s+(\d+[\.\d]*)\s*[—:-]?\s*(.*)', line, re.IGNORECASE)
        if m:
            def_num = m.group(1)
            title = m.group(2).strip()
            
            def_lines = []
            for j in range(i+1, min(i+20, len(lines))):
                if lines[j].strip() and not lines[j].startswith('##'):
                    def_lines.append(lines[j].strip())
                elif lines[j].startswith('##'):
                    break
            
            definitions.append({
                'number': def_num,
                'name': title or f"Definition {def_num}",
                'statement': ' '.join(def_lines[:8]),
                'paper_id': paper_id
            })
    
    return definitions

def extract_predictions(content: str, paper_id: str) -> List[Dict]:
    """Extract predictions from paper content"""
    predictions = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        m = re.search(r'(?:Predicci[oó]n|Prediction)\s+([A-Z]\d+)\s*[—:-]?\s*(.*)', line, re.IGNORECASE)
        if m:
            pred_id = m.group(1)
            title = m.group(2).strip()
            
            pred_lines = []
            for j in range(i+1, min(i+20, len(lines))):
                if lines[j].strip() and not lines[j].startswith('##'):
                    pred_lines.append(lines[j].strip())
                elif lines[j].startswith('##'):
                    break
            
            predictions.append({
                'id': pred_id,
                'name': title or f"Prediction {pred_id}",
                'statement': ' '.join(pred_lines[:10]),
                'paper_id': paper_id
            })
    
    return predictions

def extract_conjectures(content: str, paper_id: str) -> List[Dict]:
    """Extract conjectures from paper content"""
    conjectures = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        m = re.search(r'(?:Conjetura|Conjecture)\s+([A-Z]\d+)\s*[—:-]?\s*(.*)', line, re.IGNORECASE)
        if m:
            conj_id = m.group(1)
            title = m.group(2).strip()
            
            conj_lines = []
            for j in range(i+1, min(i+20, len(lines))):
                if lines[j].strip() and not lines[j].startswith('##'):
                    conj_lines.append(lines[j].strip())
                elif lines[j].startswith('##'):
                    break
            
            conjectures.append({
                'id': conj_id,
                'name': title or f"Conjecture {conj_id}",
                'statement': ' '.join(conj_lines[:10]),
                'paper_id': paper_id
            })
    
    return conjectures

def process_paper(filepath: Path, existing_entities: Dict) -> Dict:
    """Process a single paper file"""
    content = filepath.read_text(encoding='utf-8')
    paper_id = generate_id('paper')
    
    # Extract all constructs
    equations = extract_equations(content, paper_id)
    theorems = extract_theorems(content, paper_id)
    definitions = extract_definitions(content, paper_id)
    predictions = extract_predictions(content, paper_id)
    conjectures = extract_conjectures(content, paper_id)
    
    return {
        'paper_id': paper_id,
        'title': filepath.stem,
        'equations': equations,
        'theorems': theorems,
        'definitions': definitions,
        'predictions': predictions,
        'conjectures': conjectures
    }

def main():
    print("Loading existing graph...")
    entities, _ = load_graph(str(GRAPH_PATH))
    print(f"Existing entities: {len(entities)}")
    
    all_extracted = []
    
    # Process papers
    print("\nProcessing papers...")
    for paper_dir in PAPERS_DIR.iterdir():
        if not paper_dir.is_dir():
            continue
        for paper_file in paper_dir.glob("*.md"):
            print(f"  Processing {paper_file.name}...")
            try:
                extracted = process_paper(paper_file, entities)
                all_extracted.append(extracted)
                
                # Create entities in ontology
                for eq in extracted['equations']:
                    eid = generate_id('equation')
                    create_entity('Equation', {
                        'number': eq['number'],
                        'name': eq['name'],
                        'formula': eq['formula'],
                        'description': eq['description'],
                        'domain': 'core',
                        'verified': False,
                        'verification_method': 'theoretical'
                    }, str(GRAPH_PATH), eid)
                    create_relation(eid, 'references_paper', extracted['paper_id'], {}, str(GRAPH_PATH))
                
                for thm in extracted['theorems']:
                    tid = generate_id('theorem')
                    create_entity('Theorem', {
                        'number': thm['number'],
                        'name': thm['name'],
                        'statement': thm['statement'],
                        'proof_sketch': '',
                        'verified': False,
                        'verification_details': '',
                        'seeds_tested': 0,
                        'steps_tested': 0,
                        'empirical_result': ''
                    }, str(GRAPH_PATH), tid)
                    create_relation(tid, 'references_paper', extracted['paper_id'], {}, str(GRAPH_PATH))
                
                for d in extracted['definitions']:
                    did = generate_id('definition')
                    create_entity('Definition', {
                        'number': d['number'],
                        'name': d['name'],
                        'statement': d['statement'],
                        'domain': 'core'
                    }, str(GRAPH_PATH), did)
                    create_relation(did, 'references_paper', extracted['paper_id'], {}, str(GRAPH_PATH))
                
                for p in extracted['predictions']:
                    pid = generate_id('prediction')
                    create_entity('Prediction', {
                        'id': p['id'],
                        'name': p['name'],
                        'statement': p['statement'],
                        'domain': 'computational',
                        'level': 1,
                        'falsification_criterion': '',
                        'status': 'proposed',
                        'key_variables': []
                    }, str(GRAPH_PATH), pid)
                    create_relation(pid, 'references_paper', extracted['paper_id'], {}, str(GRAPH_PATH))
                
                for c in extracted['conjectures']:
                    cid = generate_id('conjecture')
                    create_entity('Conjecture', {
                        'id': c['id'],
                        'name': c['name'],
                        'statement': c['statement'],
                        'status': 'open',
                        'evidence': ''
                    }, str(GRAPH_PATH), cid)
                    create_relation(cid, 'references_paper', extracted['paper_id'], {}, str(GRAPH_PATH))
                
            except Exception as e:
                print(f"    Error: {e}")
    
    # Process notes
    print("\nProcessing Obsidian notes...")
    for note_file in NOTES_DIR.glob("*.md"):
        print(f"  Processing {note_file.name}...")
        try:
            content = note_file.read_text(encoding='utf-8')
            # Extract from notes too
            equations = extract_equations(content, generate_id('note'))
            theorems = extract_theorems(content, generate_id('note'))
            definitions = extract_definitions(content, generate_id('note'))
            predictions = extract_predictions(content, generate_id('note'))
            conjectures = extract_conjectures(content, generate_id('note'))
            
            # Create entities (simplified for notes)
            for eq in equations:
                eid = generate_id('equation')
                create_entity('Equation', {
                    'number': eq['number'],
                    'name': eq['name'],
                    'formula': eq['formula'],
                    'description': eq['description'],
                    'domain': 'core',
                    'verified': False,
                    'verification_method': 'theoretical'
                }, str(GRAPH_PATH), eid)
            
        except Exception as e:
            print(f"    Error: {e}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()