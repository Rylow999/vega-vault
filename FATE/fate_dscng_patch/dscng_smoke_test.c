#include <stdio.h>
#include <math.h>
#include "fate_engine.h"

static double sphere(const double *phase, int dim, void *ctx) {
    (void)ctx;
    double s = 0.0;
    for (int i = 0; i < dim; i++) {
        double x = phase[i] - M_PI; // optimum at phase[i] == pi
        s += x * x;
    }
    return 1.0 / (1.0 + s);
}

int main(void) {
    FateConfig cfg;
    fate_config_default(&cfg, 16, sphere, NULL);
    cfg.seed = 42;
    cfg.max_evals = 4000;
    cfg.pop_size = 40; // > DSCNG_MAX_NODES? no, 40 < 64, fine
    cfg.verbose = 0;

    FateEngine *e = fate_create(&cfg);
    if (!e) { fprintf(stderr, "fate_create failed\n"); return 1; }

    FateState st;
    int done = 0;
    int era = 0;
    while (!done) {
        done = fate_step(e);
        era++;
        if (era % 20 == 0 || done) {
            fate_get_state(e, &st);
            printf("era=%4d evals=%5llu champ_fit=%.4f R=%.4f mean_V=%.4f prunes=%d pop=%d\n",
                   era, (unsigned long long)st.eval_count, st.champion_fitness,
                   st.dscng_phase_coherence, st.dscng_mean_vitality, st.dscng_prunes, st.pop_size);
            if (isnan(st.dscng_phase_coherence) || isnan(st.dscng_mean_vitality)) {
                fprintf(stderr, "NaN detected!\n");
                return 2;
            }
        }
    }
    fate_destroy(e);
    printf("OK\n");
    return 0;
}
