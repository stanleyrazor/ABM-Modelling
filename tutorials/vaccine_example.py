import sciris as sc
import numpy as np
import pylab as pl
import starsim as ss


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
    pl.plot(results.time, results.n_infected, label=label)
    pl.legend()
    sc.figlayout()
    

if __name__ == '__main__':
    
    # Make, run, and plot the simulation
    pars = dict(beta=0.08, waning=0.03, seed=15)

    res1 = make_run_sim(**pars)
    res2 = make_run_sim(**pars, vaccine=True, ti=4, p=0.8, boost=10)

    plot(res1, 'Baseline')
    plot(res2, 'Vaccine')

    pl.show()

