/*
 * fate_engine.c — FATE v5 Core Engine (C Library)
 *
 * TNS Engine + CTEG + TabuMem + DSCN-G v3 (Kuramoto coupling + vitality
 * homeostasis, ported from the audited DSCN_G_v2 core, verify_dscng_v2.py)
 * Clean API: fate_create / fate_step / fate_get_state / fate_destroy
 *
 * Build: gcc -O3 -fPIC -shared -o libfate.so fate_engine.c -lm
 */
#define _POSIX_C_SOURCE 200809L
#include "fate_engine.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>
#include <stdio.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/* ── Constants ───────────────────────────────────────────────────────── */
#define DEFAULT_TABU_SIZE       512
#define DEFAULT_TABU_THRESHOLD  0.20
#define TABU_THRESH_MIN         0.08
#define TABU_THRESH_MAX         0.35
#define DEFAULT_POP_MIN         40
#define DEFAULT_POP_MAX         512
#define DEFAULT_POP_DENSITY     2
#define N_ESCAPE                8
#define MAX_DIM                 1024
#define ADAPT_W                 50
#define N_RESTARTS_KTHRESH      5
#define TOPO_SIZE               256
#define TOPO_CELLS              (TOPO_SIZE * TOPO_SIZE)

#define CLAMP01(v)  ((v)<0.0?0.0:(v)>1.0?1.0:(v))

/* ── DSCN-G v3 cognitive-layer constants ─────────────────────────────────
 * Values are DSCN_G_v2's DEFAULTS from verify_dscng_v2.py (audited, 6
 * rounds, 2026-07-22/24) — NOT the unaudited v5/BIO constants used in
 * bench/oracle_dscng.py elsewhere in this repo (N_ss*=7, omega*=0.649747).
 * DSCNG_MAX_NODES bounds the Kuramoto/vitality computation to the same
 * O(N^2) neighborhood the audited model used (N=50 default there); FATE's
 * own POP_MAX_CAP (64) already keeps the live population in that range, this
 * is a defensive cap in case pop_size is set explicitly larger. */
#define DSCNG_ALPHA             5.0
#define DSCNG_ETA_KURA          0.005
#define DSCNG_GAMMA             0.01
#define DSCNG_THETA_DEATH       0.10
#define RESONANCE_WEIGHT        0.20
#define STATE_WEIGHT_LAMBDA     0.15
#define DSCNG_MAX_NODES         64

/* ── Types ───────────────────────────────────────────────────────────── */
typedef uint64_t HammingSig;

typedef struct {
    double *state;      // doubles as omega_i (DSCN-G semantic vector) — the searched vector
    double valence;
    HammingSig sig;
    double phase;        // DSCN-G phi_i — real Kuramoto phase, independent of state
    double vitality;      // DSCN-G V_i — homeostatic vitality, in [0,1]
} Candidate;

typedef struct {
    HammingSig *sigs;
    double *states;
    double *vals;
    int head, count, capacity, dim;
} TabuMem;

typedef struct {
    Candidate *pop;
    int pop_n;
    int pop_cap;       // allocated capacity (POP_MAX_CAP); pop_n varies within
    double *pop_pool;
    double *champion_state;
    double *tmp_buf;
    double champion_valence;
    uint64_t era;
    TabuMem tabu;
    uint64_t rng[4];

    /* Per-generation scratch buffers for the generate-then-evaluate split
     * (2.2: lets fate_step gather a whole generation of candidates before
     * calling either the scalar or the batch fitness function). Sized to
     * pop_cap so they never need reallocation across pop_n changes. */
    double     *cand_pool;      // [pop_cap * dim]
    HammingSig *cand_sigs;      // [pop_cap]
    int        *cand_attempts;  // [pop_cap]
    double     *cand_fits;      // [pop_cap]
} TNSEngine;

typedef enum { CTEG_IDLE = 0, CTEG_SCRAMBLE } CTEGState;

typedef struct {
    CTEGState state;
    int stagnation_limit, stagnation_count;
    double prev_champion, lambda;
    uint64_t n_escapes;
} CTEGCtrl;

typedef struct { uint32_t count; float max_fit; } TopoCell;

struct FateEngine {
    FateConfig cfg;
    TNSEngine *tns;
    CTEGCtrl cteg;
    TopoCell *topo_map;
    double adapt_scores[ADAPT_W];
    int adapt_count;
    double lambda_gap;
    double rho_eff;
    int n_restarts;
    uint64_t total_evals;

    /* DSCN-G v3 cognitive layer (2.1 note preserved: this is per-instance
     * state, not a module global — two FateEngine instances in one process
     * must not share it; see bug 1.2 history in git blame). Population
     * members (TNSEngine.pop) carry their own phase/vitality (Candidate);
     * this counter is engine-level bookkeeping only. */
    uint64_t dscng_prunes;           // cumulative vitality<theta_death respawns
};

/* ── PRNG: xoshiro256** ──────────────────────────────────────────────── */
static inline uint64_t rotl64(uint64_t x, int k) { return (x<<k)|(x>>(64-k)); }

static uint64_t prng_next(uint64_t s[4]) {
    uint64_t r = s[0]+s[3], t = s[1] << 17;
    s[2]^=s[0]; s[3]^=s[1]; s[1]^=s[2]; s[0]^=s[3]; s[2]^=t;
    s[3] = rotl64(s[3],45); return r;
}

static double prng_f64(uint64_t s[4]) {
    return (double)(prng_next(s) >> 11)*(1.0/(double)(1ULL << 53));
}

static void prng_seed(uint64_t s[4], uint64_t seed) {
    for(int i=0;i<4;i++){
        seed += 0x9e3779b97f4a7c15ULL; uint64_t z = seed;
        z = (z^(z>>30)) * 0xbf58476d1ce4e5b9ULL;
        z = (z^(z>>27)) * 0x94d049bb133111ebULL; s[i] = z^(z>>31);
    }
}

static double prng_gaussian(uint64_t s[4]) {
    double u,v; do { u=prng_f64(s); } while(u <= 0.0); v=prng_f64(s);
    return sqrt(-2.0*log(u))*cos(2.0*M_PI*v);
}

/* ── ULTRA_CHROMO (accelerated Collatz) ──────────────────────────────── */
static const uint8_t ULTRA_CHROMO[32] = {
    3, 7, 3, 5, 7, 3, 3, 9, 9, 7, 3, 5, 3, 3, 9, 9,
    7, 3, 3, 5, 5, 3, 7, 3, 7, 7, 3, 5, 5, 3, 5, 9
};

static inline uint64_t ultra_step_accel(uint64_t n) {
    if (n == 1ULL) return 1ULL;
    if ((n & 1ULL) == 0ULL) return n >> 1;
    uint8_t a = ULTRA_CHROMO[n & 31ULL];
    uint64_t val = (uint64_t)a * n + 1ULL;
    int v2 = __builtin_ctzll(val);
    return val >> v2;
}

static double ultra_bit_entropy(uint64_t n) {
    int steps = 0, transitions = 0;
    uint64_t prev = n & 3ULL;
    while (n != 1ULL && steps < 150) {
        n = ultra_step_accel(n);
        uint64_t curr = n & 3ULL;
        if (curr != prev) transitions++;
        prev = curr; steps++;
    }
    return (steps == 0) ? 0.0 : (double)transitions / (double)(steps + 1);
}

/* ── Tabu Memory ─────────────────────────────────────────────────────── */
static inline int popcount64(uint64_t x) {
    x-=(x>>1)&0x5555555555555555ULL;
    x=(x&0x3333333333333333ULL)+((x>>2)&0x3333333333333333ULL);
    x=(x+(x>>4))&0x0f0f0f0f0f0f0f0fULL;
    return (int)((x*0x0101010101010101ULL)>>56);
}

static HammingSig make_sig(const double *state, int dim) {
    HammingSig sig=0;
    int d=(dim<8)?dim:8;
    for(int i=0;i<d;i++){
        double t=state[i]/(2.0*M_PI); if(t<0)t=0; if(t>0.9999)t=0.9999;
        sig|=(HammingSig)((uint8_t)(t*255.0))<<(i*8);
    }
    for(int i=8;i<dim;i++){
        double t=state[i]/(2.0*M_PI); if(t<0)t=0; if(t>0.9999)t=0.9999;
        sig^=(HammingSig)((uint8_t)(t*255.0))<<((i%8)*8);
    }
    return sig;
}

static void tabu_init(TabuMem *m, int capacity, int dim) {
    m->capacity = capacity; m->dim = dim; m->head = 0; m->count = 0;
    m->sigs = (HammingSig*)calloc(capacity, sizeof(HammingSig));
    m->states = (double*)calloc((size_t)capacity * dim, sizeof(double));
    m->vals = (double*)calloc(capacity, sizeof(double));
}

static void tabu_free(TabuMem *m) {
    free(m->sigs); free(m->states); free(m->vals);
    m->sigs = NULL; m->states = NULL; m->vals = NULL;
}

static void tabu_add(TabuMem *m, const double *state, double val) {
    int idx = m->head;
    m->sigs[idx] = make_sig(state, m->dim);
    memcpy(m->states + (size_t)idx * m->dim, state, sizeof(double) * m->dim);
    m->vals[idx] = val;
    m->head = (m->head + 1) % m->capacity;
    if (m->count < m->capacity) m->count++;
}

static double tabu_min_dist(const TabuMem *m, const double *state, HammingSig sig) {
    if (m->count == 0) return 1e9;
    int min_ham = 64;
    for (int i = 0; i < m->count; i++) {
        int d = popcount64(m->sigs[i] ^ sig);
        if (d < min_ham) min_ham = d;
    }
    if (min_ham > 20) return 10.0;
    double min_eu = 1e9;
    for (int i = 0; i < m->count; i++) {
        const double *s = m->states + (size_t)i * m->dim;
        double d = 0.0; for (int j = 0; j < m->dim; j++) { double diff = s[j] - state[j]; d += diff * diff; }
        if (d < min_eu) min_eu = d;
    }
    return sqrt(min_eu);
}

static int is_tabu(const TabuMem *m, const double *state, HammingSig sig, double threshold) {
    return m->count > 0 && tabu_min_dist(m, state, sig) < threshold;
}

/* ── TopoMap ─────────────────────────────────────────────────────────── */
static void topo_init(TopoCell *map) {
    memset(map, 0, TOPO_CELLS * sizeof(TopoCell));
}

static void topo_insert(TopoCell *map, const double *state, double fit, int dim) {
    double avg = 0.0; for (int i = 0; i < dim; i++) avg += state[i]; avg /= dim;
    int x = (int)(avg / (2.0 * M_PI) * TOPO_SIZE) % TOPO_SIZE; if (x < 0) x += TOPO_SIZE;
    int y = (int)(log1p(fit) / 5.0 * TOPO_SIZE) % TOPO_SIZE; if (y < 0) y = 0;
    TopoCell *c = &map[y * TOPO_SIZE + x];
    if (c->count < UINT32_MAX) c->count++;
    if (fit > (double)c->max_fit) c->max_fit = (float)fit;
}

static double topo_hardness_at(const TopoCell *map, const double *state, int dim) {
    double avg = 0.0; for (int i = 0; i < dim; i++) avg += state[i]; avg /= dim;
    int cx = (int)(avg / (2.0 * M_PI) * TOPO_SIZE);
    if (cx < 0) cx = 0;
    if (cx >= TOPO_SIZE) cx = TOPO_SIZE - 1;
    double best = 0.0;
    for (int dx = -12; dx <= 12; dx++) {
        int nx = (cx + dx + TOPO_SIZE) % TOPO_SIZE;
        for (int y = 0; y < TOPO_SIZE; y++) {
            float h = map[y * TOPO_SIZE + nx].max_fit;
            if (h > best) best = h;
        }
    }
    return best;
}

static uint32_t topo_visit_count(const TopoCell *map, const double *state, double fit, int dim) {
    double avg = 0.0; for (int i = 0; i < dim; i++) avg += state[i]; avg /= dim;
    int cx = (int)(avg / (2.0 * M_PI) * TOPO_SIZE);
    if (cx < 0) cx = 0;
    if (cx >= TOPO_SIZE) cx = TOPO_SIZE - 1;
    int cy = (int)(log1p(fit) / 5.0 * TOPO_SIZE);
    if (cy < 0) cy = 0;
    if (cy >= TOPO_SIZE) cy = TOPO_SIZE - 1;
    uint32_t total = 0;
    for (int dx = -4; dx <= 4; dx++) {
        int nx = (cx + dx + TOPO_SIZE) % TOPO_SIZE;
        for (int dy = -4; dy <= 4; dy++) {
            int ny = (cy + dy + TOPO_SIZE) % TOPO_SIZE;
            total += map[ny * TOPO_SIZE + nx].count;
        }
    }
    return total;
}

static double topo_adaptive_tabu_threshold(const TopoCell *map, const double *state, double fit, int dim, double base_thresh) {
    uint32_t visits = topo_visit_count(map, state, fit, dim);
    // Más visitas = zona explorada = threshold más laxo (exploración)
    // Menos visitas = zona nueva = threshold más estricto (exploitation)
    double density = visits / 81.0; // max 9x9 = 81 cells
    double factor = 1.0 + 0.5 * tanh(density - 1.0); // ~0.5 a ~1.5
    double thresh = base_thresh * factor;
    if (thresh < TABU_THRESH_MIN) thresh = TABU_THRESH_MIN;
    if (thresh > TABU_THRESH_MAX) thresh = TABU_THRESH_MAX;
    return thresh;
}

/* ── DSCN-G v3 dynamics: Kuramoto coupling + vitality homeostasis ───────
 * Population members double as DSCN-G nodes, ported from the audited
 * DSCN_G_v2 in verify_dscng_v2.py (6 rounds, 2026-07-22/24):
 *   candidate.state    == omega_i (semantic vector; drives coupling weight)
 *   candidate.phase     == phi_i   (real Kuramoto phase, updated here)
 *   candidate.vitality  == V_i     (homeostatic vitality, drives prune)
 * C3/hijack dynamics are intentionally NOT ported: the audit found them
 * unsupported at the original parameters (0.9% of triggers show the
 * claimed effect, mean ΔPLV≈-0.007) — see auditoria/AUDIT_NOTES_ROUND6.md
 * in the DSCN_G_v3 paper kit. Only the verified mechanics (T1 homeostasis,
 * T2/T3 phase dynamics) are ported. */

static double state_l2_dist(const double *a, const double *b, int dim) {
    double d = 0.0;
    for (int i = 0; i < dim; i++) { double diff = a[i]-b[i]; d += diff*diff; }
    return sqrt(d);
}

static void dscng_init_candidate(Candidate *c, uint64_t rng[4]) {
    c->phase = prng_f64(rng) * 2.0 * M_PI;
    c->vitality = 1.0;
}

/* Kuramoto order parameter R = |<e^{i*phase}>|, mirrors
 * DSCN_G_v2.phase_coherence(). */
static double dscng_phase_coherence(const Candidate *pop, int n_nodes) {
    if (n_nodes <= 0) return 0.0;
    double sum_c = 0.0, sum_s = 0.0;
    for (int i = 0; i < n_nodes; i++) { sum_c += cos(pop[i].phase); sum_s += sin(pop[i].phase); }
    sum_c /= n_nodes; sum_s /= n_nodes;
    return sqrt(sum_c*sum_c + sum_s*sum_s);
}

/* _apply_kuramoto_coupling in verify_dscng_v2.py:
 *   w_ij = exp(-alpha*||omega_i-omega_j||)
 *   phi_i += eta * (Sum_j w_ij*sin(phi_j-phi_i)) / (Sum_j w_ij)
 * AUDIT FIX preserved (Round 6): computed from a phase snapshot taken
 * before any writes, to avoid the Gauss-Seidel order-dependency bug the
 * audit found in the original mid-loop-write version. */
static void dscng_kuramoto_step(Candidate *pop, int n_nodes, int dim, double alpha, double eta_kura) {
    if (n_nodes < 2) return;
    double *phase_snap = (double*)malloc(sizeof(double) * n_nodes);
    if (!phase_snap) return;
    for (int i = 0; i < n_nodes; i++) phase_snap[i] = pop[i].phase;
    for (int i = 0; i < n_nodes; i++) {
        double numer = 0.0, denom = 0.0;
        for (int j = 0; j < n_nodes; j++) {
            if (j == i) continue;
            double w = exp(-alpha * state_l2_dist(pop[i].state, pop[j].state, dim));
            numer += w * sin(phase_snap[j] - phase_snap[i]);
            denom += w;
        }
        if (denom > 0.0) {
            double ph = phase_snap[i] + eta_kura * (numer / denom);
            ph = fmod(ph, 2.0 * M_PI); if (ph < 0) ph += 2.0 * M_PI;
            pop[i].phase = ph;
        }
    }
    free(phase_snap);
}

/* _update_vitality_and_prune, Eq.5: V <- V*e^-gamma + A*(1-e^-gamma);
 * prune if V < theta_death. Activity A_i reuses FATE's own topo
 * visit-density signal, normalized within the current population —
 * DSCN-G's own activity comes from an analogous "how often is this region
 * visited" signal (its K random-walk chains); this avoids introducing a
 * second, unrelated activity metric. Population size is fixed in FATE, so
 * a pruned slot is respawned in place rather than removed. */
static int dscng_vitality_step(Candidate *pop, int n_nodes, int dim,
                                const TopoCell *map, double gamma, double theta_death,
                                uint64_t rng[4]) {
    if (n_nodes <= 0 || n_nodes > DSCNG_MAX_NODES) return 0;
    double decay = exp(-gamma);
    double raw[DSCNG_MAX_NODES];
    double max_raw = 1e-9;
    for (int i = 0; i < n_nodes; i++) {
        raw[i] = (double)topo_visit_count(map, pop[i].state, pop[i].valence, dim);
        if (raw[i] > max_raw) max_raw = raw[i];
    }
    int n_pruned = 0;
    for (int i = 0; i < n_nodes; i++) {
        double activity = raw[i] / max_raw;
        pop[i].vitality = pop[i].vitality * decay + activity * (1.0 - decay);
        if (pop[i].vitality < theta_death) {
            for (int j = 0; j < dim; j++) pop[i].state[j] = prng_f64(rng) * 2.0 * M_PI;
            pop[i].valence = 0.0;
            pop[i].sig = make_sig(pop[i].state, dim);
            dscng_init_candidate(&pop[i], rng);
            n_pruned++;
        }
    }
    return n_pruned;
}

/* Local vitality field at an arbitrary point (escape candidates aren't
 * population members and so have no vitality of their own): same
 * exp(-alpha*dist) kernel as the Kuramoto weight, evaluated against the
 * live population's vitality. */
static double dscng_local_vitality(const Candidate *pop, int n_nodes, const double *state, int dim, double alpha) {
    if (n_nodes <= 0) return 1.0;
    double num = 0.0, den = 0.0;
    for (int i = 0; i < n_nodes; i++) {
        double w = exp(-alpha * state_l2_dist(pop[i].state, state, dim));
        num += w * pop[i].vitality;
        den += w;
    }
    return (den > 1e-12) ? (num / den) : 1.0;
}

/* Circular mean angle of a state vector's own components — used as an
 * escape candidate's "derived phase" since fresh candidates have no
 * assigned Candidate.phase of their own yet. */
static double state_circular_mean_angle(const double *state, int dim) {
    double sc = 0.0, ss = 0.0;
    for (int i = 0; i < dim; i++) { sc += cos(state[i]); ss += sin(state[i]); }
    return atan2(ss, sc);
}

static int restart_after(double lambda_gap) {
    double factor = (lambda_gap > 0.7) ? 1.0 : (lambda_gap > 0.3 ? 0.6 : 0.25);
    int out = (int)(50.0 * factor);
    if (out < 12) out = 12;
    return out;
}
/* ── Adaptive parameters ─────────────────────────────────────────────── */

static void adapt_observe(double *adapt_scores, int *adapt_count, double *lambda_gap, double score) {
    adapt_scores[*adapt_count % ADAPT_W] = score;
    (*adapt_count)++;
    if (*adapt_count >= 8) {
        int n = (*adapt_count < ADAPT_W) ? *adapt_count : ADAPT_W;
        double m = 0.0; for (int i = 0; i < n; i++) m += adapt_scores[i]; m /= n;
        double v = 0.0; for (int i = 0; i < n; i++) v += (adapt_scores[i]-m)*(adapt_scores[i]-m); v /= n;
        *lambda_gap = 1.0 - 4.0 * v;
        if (*lambda_gap < 0.0) *lambda_gap = 0.0;
        if (*lambda_gap > 1.0) *lambda_gap = 1.0;
    }
}

static void adapt_note_tabu(double *rho_eff, int count, int cap) {
    if (cap <= 0) return;
    *rho_eff = (double)count / (double)cap;
    if (*rho_eff < 0.0) *rho_eff = 0.0;
    if (*rho_eff > 1.0) *rho_eff = 1.0;
}

/* ── TNS Engine ──────────────────────────────────────────────────────── */
#define POP_MIN 16
#define POP_MAX_CAP 64
#define POP_BASE 20

static TNSEngine *tns_alloc(const FateConfig *cfg) {
    TNSEngine *e = (TNSEngine*)calloc(1, sizeof(TNSEngine));
    int dim = cfg->dim;
    int pop_size = (cfg->pop_size > 0) ? cfg->pop_size : POP_BASE;
    int tabu_size = (cfg->tabu_size > 0) ? cfg->tabu_size : DEFAULT_TABU_SIZE;

    e->pop_n = pop_size;
    e->pop_cap = POP_MAX_CAP;  // allocate at max; pop_n shrinks/grows within
    e->pop = (Candidate*)calloc(e->pop_cap, sizeof(Candidate));
    e->pop_pool = (double*)calloc((size_t)e->pop_cap * dim, sizeof(double));
    e->champion_state = (double*)calloc(dim, sizeof(double));
    e->tmp_buf = (double*)calloc(dim, sizeof(double));
    e->champion_valence = -1.0;
    e->era = 0;

    prng_seed(e->rng, cfg->seed ? cfg->seed : (uint64_t)time(NULL) ^ (uint64_t)(uintptr_t)e);

    for (int i = 0; i < e->pop_cap; i++) {
        e->pop[i].state = e->pop_pool + (size_t)i * dim;
        for (int j = 0; j < dim; j++) e->pop[i].state[j] = prng_f64(e->rng) * 2.0 * M_PI;
        e->pop[i].sig = make_sig(e->pop[i].state, dim);
        e->pop[i].valence = 0.0;
        dscng_init_candidate(&e->pop[i], e->rng);
    }
    tabu_init(&e->tabu, tabu_size, dim);

    e->cand_pool = (double*)calloc((size_t)e->pop_cap * dim, sizeof(double));
    e->cand_sigs = (HammingSig*)calloc(e->pop_cap, sizeof(HammingSig));
    e->cand_attempts = (int*)calloc(e->pop_cap, sizeof(int));
    e->cand_fits = (double*)calloc(e->pop_cap, sizeof(double));

    return e;
}

static void tns_free(TNSEngine *e) {
    if (!e) return;
    free(e->pop); free(e->pop_pool); free(e->champion_state); free(e->tmp_buf);
    free(e->cand_pool); free(e->cand_sigs); free(e->cand_attempts); free(e->cand_fits);
    tabu_free(&e->tabu);
    free(e);
}

static void state_wrap(double *state, int dim) {
    for (int i = 0; i < dim; i++) {
        state[i] = fmod(state[i], 2.0 * M_PI);
        if (state[i] < 0) state[i] += 2.0 * M_PI;
    }
}

static void sort_pop(Candidate *pop, int n) {
    for (int i = 1; i < n; i++) {
        Candidate key = pop[i]; int j = i - 1;
        while (j >= 0 && pop[j].valence < key.valence) { pop[j+1] = pop[j]; j--; }
        pop[j+1] = key;
    }
}

/* Adaptive population: start wider (exploration) then shrink toward POP_MIN
   as budget is consumed (finer exploitation + more frequent CTEG escapes, which
   we showed beat CMA-ES). pop=20 consistently outperformed pop=40/64, so we
   trend downward rather than upward. */
static void tns_adapt_pop(TNSEngine *e, FateEngine *engine) {
    if (engine->cfg.pop_size > 0) return;  // fixed pop requested: no adapt
    int budget = engine->cfg.max_evals;
    if (budget <= 0) { e->pop_n = POP_BASE; return; }
    double frac = (double)engine->total_evals / (double)budget;  // 0..1 progress
    if (frac > 1.0) frac = 1.0;
    // Linear interpolation POP_BASE -> POP_MIN across the run
    int target = (int)(POP_BASE + (POP_MIN - POP_BASE) * frac);
    if (target < POP_MIN) target = POP_MIN;
    if (target > POP_BASE) target = POP_BASE;
    e->pop_n = target;
}

static void escape_generate_ultra(double *out, uint64_t rng[4], int dim, const double *anchor, int biased) {
    uint64_t seed = prng_next(rng);
    for (int i = 0; i < dim; i++) {
        double entropy = ultra_bit_entropy(seed + (uint64_t)i * 7ULL);
        if (biased && anchor) {
            // ULTRA_CHROMO biased: Collatz jump from anchor, directional exploration
            double a = anchor[i];
            // trajectory-length modulated step (small when entropy high => focused)
            double step = (0.15 + 0.6 * entropy) * (prng_gaussian(rng) * 0.5 + (ultra_step_accel(seed + i) & 7ULL) * 0.1);
            out[i] = a + step;
        } else {
            double noise = prng_gaussian(rng) * (0.3 + entropy);
            out[i] = prng_f64(rng) * 2.0 * M_PI + noise;
        }
        out[i] = fmod(out[i], 2.0 * M_PI);
        if (out[i] < 0.0) out[i] += 2.0 * M_PI;
    }
}

static void escape_generate_directed(double *out, TNSEngine *e, uint64_t rng[4], int dim) {
    (void)rng;
    for (int i = 0; i < dim; i++) {
        out[i] = e->champion_state[i];
    }
    for (int i = 0; i < dim; i++) {
        double g = prng_gaussian(e->rng);
        double omega_bias = 1.0;
        if (e->champion_state[i] > 0) omega_bias = 1.5;
        out[i] += 0.5 * omega_bias * g;
    }
    state_wrap(out, dim);
}

static void escape_generate_ultra_directed(double *out, TNSEngine *e, const TopoCell *map,
                                           int dim, int idx, int n_total, int biased) {
    (void)n_total;
    escape_generate_ultra(out, e->rng, dim, e->champion_state, biased);
    if (idx % 2 == 0) return;
    uint32_t min_visits = UINT32_MAX; int best_x = 0;
    for (int y = 0; y < TOPO_SIZE; y++) {
        for (int x = 0; x < TOPO_SIZE; x++) {
            uint32_t v = map[y * TOPO_SIZE + x].count;
            if (v < min_visits) { min_visits = v; best_x = x; }
        }
    }
    double target_phase = ((double)best_x / TOPO_SIZE) * 2.0 * M_PI;
    for (int i = 0; i < dim; i++) {
        out[i] = 0.7 * out[i] + 0.3 * target_phase;
    }
    state_wrap(out, dim);
}

static double dscng_escape_score(const Candidate *pop, int n_nodes, const TabuMem *tabu, const TopoCell *map,
                                  const double *candidate, HammingSig sig,
                                  double d_max, int dim, double alpha,
                                  double resonance_w, double state_w) {
    double novelty = tabu_min_dist(tabu, candidate, sig) / d_max;
    double hardness = topo_hardness_at(map, candidate, dim);

    // Phase coherence: candidate's derived phase vs. the population's
    // actual Kuramoto consensus direction (order parameter), not a decayed
    // champion-only memory.
    double pop_mean_phase = 0.0;
    if (n_nodes > 0) {
        double sc = 0.0, ss = 0.0;
        for (int i = 0; i < n_nodes; i++) { sc += cos(pop[i].phase); ss += sin(pop[i].phase); }
        pop_mean_phase = atan2(ss, sc);
    }
    double coherence = (cos(state_circular_mean_angle(candidate, dim) - pop_mean_phase) + 1.0) / 2.0;

    // Vitality term: reward escaping toward LOW local vitality (dormant /
    // unexplored — same intent as the old HIBERNADA=1.0 > ACTIVA=0.3
    // weighting, now grounded in the real vitality field).
    double vitality_term = 1.0 - dscng_local_vitality(pop, n_nodes, candidate, dim, alpha);

    return 0.35 * novelty + 0.30 * hardness + resonance_w * coherence + state_w * vitality_term;
}

static void cteg_escape(TNSEngine *e, CTEGCtrl *c, TopoCell *map, FateEngine *engine) {
    int dim = engine->cfg.dim;
    int use_cog = engine->cfg.use_cog;
    double resonance_w = engine->cfg.resonance_weight;
    double state_w = engine->cfg.state_weight_lambda;
    double alpha = engine->cfg.dscng_alpha;
    int uc_biased = engine->cfg.uc_biased;
    if (engine->cfg.cog_fix) { resonance_w = 0.45; state_w = 0.35; }  // -C: amplify so they actually discriminate
    int n_nodes = e->pop_n < DSCNG_MAX_NODES ? e->pop_n : DSCNG_MAX_NODES;
    double *cands = (double*)malloc(sizeof(double) * N_ESCAPE * dim);
    HammingSig sigs[N_ESCAPE];
    if (!cands) return;

    // Mix: 1/3 ultra aleatorio, 1/3 dirigido desde champion, 1/3 ultra-dirigido hacia zonas inexploradas
    for (int i = 0; i < N_ESCAPE; i++) {
        if (i % 3 == 0) {
            escape_generate_ultra(cands + (size_t)i * dim, e->rng, dim, e->champion_state, uc_biased);
        } else if (i % 3 == 1) {
            escape_generate_directed(cands + (size_t)i * dim, e, e->rng, dim);
        } else {
            escape_generate_ultra_directed(cands + (size_t)i * dim, e, map, dim, i, N_ESCAPE, uc_biased);
        }
        sigs[i] = make_sig(cands + (size_t)i * dim, dim);
    }

    double d_max = 1e-9;
    for (int i = 0; i < N_ESCAPE; i++) {
        double d = tabu_min_dist(&e->tabu, cands + (size_t)i * dim, sigs[i]);
        if (d > d_max) d_max = d;
    }

    double best_score = -1.0; int best = 0;
    for (int i = 0; i < N_ESCAPE; i++) {
        double score;
        if (use_cog) {
            score = dscng_escape_score(e->pop, n_nodes, &e->tabu, map, cands + (size_t)i * dim, sigs[i],
                                       d_max, dim, alpha, resonance_w, state_w);
        } else {
            double novelty = tabu_min_dist(&e->tabu, cands + (size_t)i * dim, sigs[i]) / d_max;
            double hardness = topo_hardness_at(map, cands + (size_t)i * dim, dim);
            score = c->lambda * novelty + (1.0 - c->lambda) * hardness;
        }
        if (score > best_score) { best_score = score; best = i; }
    }

    for (int i = 0; i < e->pop_n; i++) {
        for (int j = 0; j < dim; j++)
            e->pop[i].state[j] = cands[(size_t)best * dim + j] + 0.15 * prng_gaussian(e->rng);
        state_wrap(e->pop[i].state, dim);
        e->pop[i].valence = 0.0;
        e->pop[i].sig = make_sig(e->pop[i].state, dim);
        if (use_cog) dscng_init_candidate(&e->pop[i], e->rng);  // fresh phase/vitality on scramble
    }
    tabu_add(&e->tabu, cands + (size_t)best * dim, 0.0);
    c->n_escapes++;
    free(cands);
}

/* ── CTEG Monitor ────────────────────────────────────────────────────── */
static CTEGState cteg_monitor(CTEGCtrl *c, double champ, double lambda_gap) {
    c->stagnation_limit = restart_after(lambda_gap);
    switch (c->state) {
        case CTEG_IDLE:
            if (champ <= c->prev_champion) {
                if (++c->stagnation_count >= c->stagnation_limit) {
                    c->state = CTEG_SCRAMBLE;
                    c->stagnation_count = 0;
                }
            } else c->stagnation_count = 0;
            c->prev_champion = champ; break;
        case CTEG_SCRAMBLE:
            c->state = CTEG_IDLE; c->prev_champion = champ; break;
    }
    return c->state;
}

/* ── Main step ───────────────────────────────────────────────────────── */
/*
 * Split into three phases so a batch fitness function can evaluate a whole
 * generation in one call instead of being serialized candidate-by-candidate
 * (2.2 / 2.4 — this is what actually lets an external batch-capable oracle,
 * e.g. a GPU kernel via the pipe protocol, get a speedup: the round trip
 * happens once per generation instead of once per candidate).
 *
 *   Phase A — generate candidates (tabu-aware mutation + retry). No fitness
 *             calls here, so this phase is identical whether or not a batch
 *             fitness function is in use.
 *   Phase B — evaluate fitness: batch_fitness_fn (if set) for the whole
 *             generation in one call, else fitness_fn per candidate.
 *   Phase C — absorb the results into the population.
 */
static void tns_step(TNSEngine *e, FateEngine *engine) {
    e->era++;
    int dim = engine->cfg.dim;
    int budget = engine->cfg.max_evals;
    int verbose = engine->cfg.verbose;

    // Adaptive population sizing (no-op if pop_size fixed)
    tns_adapt_pop(e, engine);

    int n_gen = e->pop_n;
    if (budget > 0) {
        uint64_t remaining = (budget > 0 && (uint64_t)budget > engine->total_evals)
                              ? (uint64_t)budget - engine->total_evals : 0;
        if (remaining < (uint64_t)n_gen) n_gen = (int)remaining;
    }
    if (verbose) fprintf(stderr, "[TNS_STEP] era=%llu pop_n=%d n_gen=%d evals=%llu/%d\n",
                          (unsigned long long)e->era, e->pop_n, n_gen,
                          (unsigned long long)engine->total_evals, budget);
    if (n_gen <= 0) return;

    /* Phase A: generate candidates. */
    for (int i = 0; i < n_gen; i++) {
        double sigma = (i < e->pop_n/4) ? 0.05 : 0.50;
        int attempts = 0; HammingSig sig;
        double adaptive_thresh = engine->cfg.tabu_threshold;
        double *cbuf = e->cand_pool + (size_t)i * dim;
        do {
            for (int j = 0; j < dim; j++)
                cbuf[j] = e->pop[i].state[j] + sigma * prng_gaussian(e->rng);
            state_wrap(cbuf, dim);
            sig = make_sig(cbuf, dim);
            attempts++;
            adaptive_thresh = topo_adaptive_tabu_threshold(engine->topo_map, cbuf, e->champion_valence, dim, engine->cfg.tabu_threshold);
        } while (is_tabu(&e->tabu, cbuf, sig, adaptive_thresh) && attempts < 3);
        e->cand_sigs[i] = sig;
        e->cand_attempts[i] = attempts;
    }

    /* Phase B: evaluate fitness. */
    if (engine->cfg.batch_fitness_fn) {
        engine->cfg.batch_fitness_fn(e->cand_pool, dim, n_gen, e->cand_fits, engine->cfg.fitness_ctx);
        engine->total_evals += (uint64_t)n_gen;
    } else {
        for (int i = 0; i < n_gen; i++) {
            e->cand_fits[i] = engine->cfg.fitness_fn(e->cand_pool + (size_t)i * dim, dim, engine->cfg.fitness_ctx);
            engine->total_evals++;
        }
    }

    /* Phase C: absorb results. */
    for (int i = 0; i < n_gen; i++) {
        double fit = e->cand_fits[i];
        if (fit > e->pop[i].valence || e->cand_attempts[i] >= 3) {
            memcpy(e->pop[i].state, e->cand_pool + (size_t)i * dim, sizeof(double) * dim);
            e->pop[i].valence = fit;
            e->pop[i].sig = e->cand_sigs[i];
        }
    }

    sort_pop(e->pop, e->pop_n);

    /* DSCN-G v3 dynamics: run every era (not just on champion improvement —
     * this is the actual population dynamic the audited model describes,
     * not a memory of past champions). Elite-first after sort_pop, so when
     * pop_n > DSCNG_MAX_NODES this operates on the top DSCNG_MAX_NODES. */
    if (engine->cfg.use_cog) {
        int n_nodes = e->pop_n < DSCNG_MAX_NODES ? e->pop_n : DSCNG_MAX_NODES;
        dscng_kuramoto_step(e->pop, n_nodes, dim, engine->cfg.dscng_alpha, engine->cfg.dscng_eta_kura);
        engine->dscng_prunes += (uint64_t)dscng_vitality_step(
            e->pop, n_nodes, dim, engine->topo_map,
            engine->cfg.dscng_gamma, engine->cfg.dscng_theta_death, e->rng);
    }

    if (e->pop[0].valence > e->champion_valence) {
        e->champion_valence = e->pop[0].valence;
        memcpy(e->champion_state, e->pop[0].state, sizeof(double) * dim);
        tabu_add(&e->tabu, e->pop[0].state, e->pop[0].valence);
        adapt_observe(engine->adapt_scores, &engine->adapt_count, &engine->lambda_gap,
                      e->champion_valence);
    }
    adapt_note_tabu(&engine->rho_eff, e->tabu.count, e->tabu.capacity);
}

/* ── Public API ──────────────────────────────────────────────────────── */
void fate_config_default(FateConfig *cfg, int dim, FateFitnessFn fn, void *ctx) {
    memset(cfg, 0, sizeof(FateConfig));
    cfg->dim = dim;
    cfg->seed = 0;
    cfg->pop_size = 0;  // auto
    cfg->max_evals = -1;
    cfg->stagnation_limit = 0;  // auto
    cfg->cteg_lambda = 0.5;
    cfg->tabu_size = DEFAULT_TABU_SIZE;
    cfg->tabu_threshold = DEFAULT_TABU_THRESHOLD;
    cfg->fitness_fn = fn;
    cfg->fitness_ctx = ctx;
    cfg->use_cog = 1;
    cfg->dscng_alpha = DSCNG_ALPHA;
    cfg->dscng_eta_kura = DSCNG_ETA_KURA;
    cfg->dscng_gamma = DSCNG_GAMMA;
    cfg->dscng_theta_death = DSCNG_THETA_DEATH;
    cfg->resonance_weight = RESONANCE_WEIGHT;
    cfg->state_weight_lambda = STATE_WEIGHT_LAMBDA;
    cfg->verbose = 0;
    cfg->uc_biased = 0;
    cfg->cog_fix = 0;

    /* v4-compatible defaults */
    cfg->mode = 2;  // full
    cfg->eras = 3000;
    cfg->ras_shift = 2.56;
    cfg->perturb_at = 0;
    cfg->flip_every = 200;
    cfg->log_every = 10;
    cfg->out_path = NULL;
    cfg->csv_path = NULL;
    cfg->csv_thresh = 0.85;
    cfg->ppm = 0;
    cfg->quiet = 0;
}

FateEngine *fate_create(const FateConfig *cfg) {
    if (!cfg->fitness_fn && !cfg->batch_fitness_fn) {
        fprintf(stderr, "[fate_create] error: cfg must set fitness_fn or batch_fitness_fn\n");
        return NULL;
    }
    FateEngine *e = (FateEngine*)calloc(1, sizeof(FateEngine));
    e->cfg = *cfg;
    e->tns = tns_alloc(cfg);
    e->cteg = (CTEGCtrl){ .state = CTEG_IDLE, .stagnation_limit = cfg->stagnation_limit > 0 ? cfg->stagnation_limit : 50,
                          .stagnation_count = 0, .prev_champion = -1.0, .lambda = cfg->cteg_lambda, .n_escapes = 0 };
    e->topo_map = (TopoCell*)calloc(TOPO_CELLS, sizeof(TopoCell));
    topo_init(e->topo_map);
    e->adapt_count = 0; e->lambda_gap = 0.5; e->rho_eff = 1.0; e->n_restarts = 0; e->total_evals = 0;
    e->dscng_prunes = 0;
    return e;
}

void fate_destroy(FateEngine *e) {
    if (!e) return;
    tns_free(e->tns);
    free(e->topo_map);
    free(e);
}

int fate_step(FateEngine *e) {
    if (!e) return -1;
    if (e->cfg.max_evals > 0 && e->total_evals >= (uint64_t)e->cfg.max_evals) return 1;

    int verbose = e->cfg.verbose;
    if (verbose) fprintf(stderr, "[FATE_STEP] era=%llu evals=%llu/%d\n",
                          (unsigned long long)e->tns->era, (unsigned long long)e->total_evals, e->cfg.max_evals);

    tns_step(e->tns, e);
    topo_insert(e->topo_map, e->tns->champion_state, e->tns->champion_valence, e->cfg.dim);

    CTEGState mon = cteg_monitor(&e->cteg, e->tns->champion_valence, e->lambda_gap);

    if (e->cteg.state == CTEG_SCRAMBLE || mon == CTEG_SCRAMBLE) {
        if (e->cteg.state == CTEG_SCRAMBLE) e->n_restarts++;
        if (verbose) fprintf(stderr, "[FATE_STEP] CTEG escape triggered (n_restarts=%d)\n", e->n_restarts);
        cteg_escape(e->tns, &e->cteg, e->topo_map, e);
    }

    if (e->cfg.max_evals > 0 && e->total_evals >= (uint64_t)e->cfg.max_evals) return 1;
    return 0;
}

void fate_get_state(const FateEngine *e, FateState *out) {
    out->champion_phase = e->tns->champion_state;
    out->champion_fitness = e->tns->champion_valence;
    out->eval_count = e->total_evals;
    out->era = e->tns->era;
    out->escapes = e->cteg.n_escapes;
    out->pop_size = e->tns->pop_n;
    out->lambda_gap = e->lambda_gap;
    out->rho_eff = e->rho_eff;
    out->n_restarts = e->n_restarts;

    int n_nodes = e->tns->pop_n < DSCNG_MAX_NODES ? e->tns->pop_n : DSCNG_MAX_NODES;
    out->dscng_phase_coherence = e->cfg.use_cog ? dscng_phase_coherence(e->tns->pop, n_nodes) : 0.0;
    double mean_v = 0.0;
    if (e->cfg.use_cog && n_nodes > 0) {
        for (int i = 0; i < n_nodes; i++) mean_v += e->tns->pop[i].vitality;
        mean_v /= n_nodes;
    }
    out->dscng_mean_vitality = mean_v;
    out->dscng_prunes = (int)e->dscng_prunes;
}

uint64_t fate_rng_next(FateEngine *e) { return prng_next(e->tns->rng); }
double fate_rng_f64(FateEngine *e) { return prng_f64(e->tns->rng); }
double fate_rng_gaussian(FateEngine *e) { return prng_gaussian(e->tns->rng); }
void fate_wrap_phase(double *phase, int dim) { state_wrap(phase, dim); }