import sciris as sc
import numpy as np
import pylab as pl
import starsim as ss

data_baseline = np.array([
 10,  20,  30,  49,  80, 135, 218, 303, 373, 428, 452, 463, 465,
446, 411, 374, 323, 270, 244, 222, 214, 214, 227, 246, 260, 271,
265, 257, 254, 243, 232, 214, 191, 161, 137, 110,  98,  83,  67,
 62,  51,  47,  45,  42,  47,  49,  48,  48,  52,  57,  67,  77,
 89,  96, 117, 129, 148, 176, 191, 209, 233, 248, 252, 253, 253,
245, 234, 214, 199, 183, 159, 145, 129, 118, 109,  97,  94,  94,
 83,  82,  79,  75,  82,  91,  99, 104, 104, 113, 129, 146, 153,
163, 175, 193, 197, 208, 208, 213, 215, 203, 204])

data_vaccine = np.array([
 10,  20,  30,  49,  80,  92, 102, 110, 119, 118, 124, 118, 115,
96,  79,  72,  65,  61,  51,  37,  36,  28,  21,  22,  15,  15,
11,  10,  11,   9,  10,   6,   6,   6,   7,   5,   7,   6,   6,
 7,   6,   7,   7,   7,   9,   8,   6,   7,  10,   8,   7,   9,
 9,   7,   8,   8,  11,  12,  11,  10,   8,  10,  14,  18,  21,
20,  22,  23,  25,  27,  25,  24,  28,  28,  28,  27,  27,  27,
27,  28,  25,  25,  19,  20,  21,  21,  24,  26,  28,  33,  43,
54,  65,  82,  92, 115, 133, 170, 199, 222, 250])


# EXERCISE: plot data
# pl.figure()
# pl.plot(data_baseline, label='Baseline')
# pl.plot(data_vaccine, label='Vaccine')

#%%


class Vaccine(ss.Intervention):
    def __init__(self, ti=7, p=0.5, boost=2.0):
        super().__init__()
        self.ti = ti
        self.p = p
        self.boost = boost
    
    def apply(self, sim):
        if sim.ti == self.ti:
            sis = sim.diseases.sis
            eligible_ids = sim.people.uid[sis.susceptible]
            n_eligible = len(eligible_ids)
            is_vacc = np.random.rand(n_eligible) < self.p
            vacc_ids = eligible_ids[is_vacc]
            sis.immunity[vacc_ids] += self.boost


def make_run_sim(beta=0.05, waning=0.05, seed=1, vaccine=False, ti=10, p=0.5, boost=2.0):
    pars = dict(
        n_agents = 500,
        start = 0,
        end = 100,
        dt = 1.0,
        rand_seed = seed,
        networks = 'random',
        diseases = dict(
            type = 'sis',
            beta = beta,
            waning = waning,
        )
    )
    
    # Define "baseline" and "intervention" sims without and with the vaccine
    if vaccine:
        vx = Vaccine(ti=ti, p=p, boost=boost)
        sim = ss.Sim(pars, interventions=vx)
    else:
        sim = ss.Sim(pars)
    
    # Run the simulation
    sim.run()
    results = sc.objdict()
    results.time = sim.yearvec
    results.n_infected = sim.results.sis.n_infected
    return results


def plot(results, label=''):
    pl.title('Number of people infected')
    pl.plot(results.time, results.n_infected, 'o-', label=label)
    pl.legend()
    sc.figlayout()
    pl.show()
    

# Make, run, and plot the simulation
sc.options(dpi=200)
pars = dict(beta=0.08, waning=0.03, seed=15)
res1 = make_run_sim(**pars)
plot(res1, 'Baseline')
res2 = make_run_sim(**pars, vaccine=True, ti=4, p=0.8, boost=10)
plot(res2, 'Vaccine')

# Save data
print(repr(res1.n_infected.astype(int)))
print(repr(res2.n_infected.astype(int)))

