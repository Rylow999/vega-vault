/*
 * fate_engine.h — FATE v5 C API (Library Interface)
 *
 * Clean separation: core FATE engine as a reusable library.
 * No CLI, no JSONL, no file I/O — just pure optimization logic.
 *
 * Build: gcc -O3 -fPIC -shared -o libfate.so fate_engine.c -lm
 * Link:  gcc -O3 -o main_v5 main_v5.c chembl_oracle.c -L. -lfate -lm
 */
#ifndef FATE_ENGINE_H
#define FATE_ENGINE_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* — Forward declarations — */
typedef struct FateEngine FateEngine;
typedef struct FateConfig FateConfig;
typedef struct FateState FateState;

/* — Fitness function signature (scalar) —
 * User provides: phase vector (dim doubles in [0, 2π)) → scalar fitness [0,1]
 * Context pointer passed through from FateConfig.
 */
typedef double (*FateFitnessFn)(const double *phase, int dim, void *ctx);

/* — Fitness function signature (batch) —
 * Evaluates n_candidates phase vectors in one call: phases is a flat
 * [n_candidates * dim] array (candidate i occupies phases[i*dim .. i*dim+dim-1]),
 * out_fitness is a caller-allocated [n_candidates] array to fill in.
 * Lets an external oracle (e.g. a GPU kernel) evaluate a whole generation
 * at once instead of being serialized one candidate per round-trip.
 * If FateConfig.batch_fitness_fn is set, the engine prefers it over
 * fitness_fn and gathers a full generation of candidates before calling it.
 */
typedef void (*FateBatchFitnessFn)(const double *phases, int dim, int n_candidates,
                                    double *out_fitness, void *ctx);

/* — Configuration — */
struct FateConfig {
    int dim;                     // Problem dimension (required)
    uint64_t seed;               // RNG seed (0 = random from time)
    int pop_size;                // Population size (0 = auto: dim/2 clamped [40,512])
    int max_evals;               // Total fitness evaluation budget (-1 = unlimited)
    int stagnation_limit;        // CTEG stagnation threshold (0 = auto-adaptive)
    double cteg_lambda;          // CTEG novelty/hardness tradeoff [0,1]
    int tabu_size;               // Tabu memory capacity (default 512)
    double tabu_threshold;       // Tabu distance threshold (default 0.2)
    FateFitnessFn fitness_fn;    // scalar fitness fn; REQUIRED unless batch_fitness_fn is set
    FateBatchFitnessFn batch_fitness_fn; // optional; if set, takes priority over fitness_fn
    void *fitness_ctx;           // Opaque context passed to fitness_fn / batch_fitness_fn

    /* Cognitive features (USE_COG equivalent) — DSCN-G v3 audited dynamics.
     * Population members are treated as DSCN-G nodes: candidate.state doubles
     * as omega_i (semantic vector, used for Kuramoto coupling weight), and
     * each candidate carries a real phase_i and vitality_i (see Candidate).
     * Replaces the old omega_root/EWMA + 3-bucket topo ACTIVE/HIBERNATE
     * heuristic, which had no actual relationship to DSCN-G despite the
     * naming. Defaults below are DSCN_G_v2's DEFAULTS (audited, 6 rounds,
     * 2026-07-22/24) — NOT the unaudited v5/BIO constants used elsewhere
     * in this repo's oracle_dscng.py (N_ss*=7, omega*=0.649747). */
    int use_cog;                 // 1 = enable Kuramoto coupling + vitality homeostasis
    double dscng_alpha;          // Kuramoto coupling-weight sharpness (default 5.0)
    double dscng_eta_kura;       // Kuramoto coupling strength, basal (default 0.005)
    double dscng_gamma;          // vitality decay rate (default 0.01)
    double dscng_theta_death;    // vitality prune threshold (default 0.10)
    double resonance_weight;     // λ₃ — weight of phase-coherence term in escape score (default 0.20)
    double state_weight_lambda;  // λ₄ — weight of vitality term in escape score (default 0.15)
    int verbose;                 // debug output to stderr (default 0)

    /* ULTRA_CHROMO enhancements */
    int uc_biased;               // 1 = Collatz-jump biased toward champion (default 0)
    int cog_fix;                 // 1 = fix cognitive: always-update omega_root, stronger weights

    /* v4-compatible parameters */
    int mode;                    // 0=random, 1=tns, 2=full (default 2)
    int eras;                    // eras if no budget (default 3000)
    double ras_shift;            // shift after perturbation (default 2.56)
    int perturb_at;              // eval of perturbation activation (default 0)
    int flip_every;              // evals between flips (default 200)
    int log_every;               // log frequency (default 10)
    const char *out_path;        // JSONL output path
    const char *csv_path;        // CSV landscape path
    double csv_thresh;           // CSV threshold (default 0.85)
    int ppm;                     // export PPMs
    int quiet;                   // suppress stderr progress
};

/* Initialize config with sensible defaults.
 * fn may be NULL if the caller is going to set cfg->batch_fitness_fn instead. */
void fate_config_default(FateConfig *cfg, int dim, FateFitnessFn fn, void *ctx);

/* — Engine lifecycle —
 * fate_create returns NULL if neither cfg->fitness_fn nor cfg->batch_fitness_fn
 * is set. */
FateEngine *fate_create(const FateConfig *cfg);
void        fate_destroy(FateEngine *e);

/* Single optimization step (one generation).
 * Returns 1 if budget exhausted, 0 otherwise.
 * Call repeatedly until returns 1 or manual stop.
 */
int fate_step(FateEngine *e);

/* — State inspection — */
struct FateState {
    double *champion_phase;      // [dim] best phase vector found
    double  champion_fitness;    // best fitness value
    uint64_t eval_count;         // total fitness evaluations
    uint64_t era;                // generation count
    uint64_t escapes;            // CTEG escape events
    int     pop_size;            // current population size
    double  lambda_gap;          // spectral gap estimate (adaptive)
    double  rho_eff;             // tabu density (count/capacity)
    int     n_restarts;          // CTEG restarts triggered

    /* DSCN-G v3 observability (only meaningful if use_cog=1) */
    double  dscng_phase_coherence; // Kuramoto order parameter R = |<e^{i*phase}>| over population
    double  dscng_mean_vitality;   // mean vitality V_i over population
    int     dscng_prunes;          // cumulative candidates pruned+respawned (vitality < theta_death)
};

void fate_get_state(const FateEngine *e, FateState *out);

/* — RNG access (for external samplers that need correlated noise) — */
uint64_t fate_rng_next(FateEngine *e);
double   fate_rng_f64(FateEngine *e);
double   fate_rng_gaussian(FateEngine *e);

/* — Utility — */
void fate_wrap_phase(double *phase, int dim);  // wrap [0, 2π)

#ifdef __cplusplus
}
#endif

#endif /* FATE_ENGINE_H */