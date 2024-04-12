# Solution for tutorial 4.5 in Python

import numpy as np
import sciris as sc
import starsim as ss
import pylab as pl

# EXERCISE: find parameters that match the data
beta = 0.35 # NB: best-fitting beta is not the same as in simple_abm!
dur_inf = 10 # However, dur_inf is
seed = 1

pars = sc.objdict(
    n_agents = 200,
    start = 0,
    end = 20,
    dt = 0.2,
    diseases = dict(
        type = 'sir',
        beta = beta,
        dur_inf = ss.expon(scale=dur_inf),
        init_prev = 5/200,
        p_death = 0,
    ),
    networks = dict(
        type = 'static',
        n_contacts = 5,
    ),
    rand_seed = seed,
)

# Define the data
data = np.array(
[ 6,  11,  14,  15,  17,  20,  25,  31,  40,  47,  52,  57,  66,
 75,  85,  93,  99, 100, 107, 111, 112, 118, 123, 117, 120, 122,
122, 123, 123, 125, 122, 120, 119, 110, 112, 117, 115, 118, 117,
113, 115, 112, 111, 107, 105, 103, 101,  99, 100,  99,  98,  97,
 94,  93,  92,  91,  89,  88,  88,  87,  86,  83,  81,  80,  78,
 76,  76,  73,  72,  71,  71,  71,  69,  68,  67,  65,  61,  58,
 57,  56,  56,  54,  52,  51,  51,  49,  49,  47,  46,  46,  46,
 46,  45,  45,  45,  43,  43,  40,  37,  36]
)
time = np.arange(len(data))*pars.dt


# Define the plotting function
def plot_results(sim):
    # Pull out results
    res = sim.diseases.sir.results
    time = sim.yearvec[0:len(data)]
    model = res.n_infected[0:len(data)]
    mismatch = np.mean(abs(data - model))
    df = sc.dataframe(
        time=time,
        Data=data,
        Model=model
    )

    pl.scatter(df.time, df.Data, label='Data', color='black')
    pl.plot(df.time, df.Model, label='Model', color='red')
    pl.title('Number of people infected')
    pl.xlabel('Time')
    pl.ylabel('Number infected')
    pl.legend()
    pl.show()

# Create and run the simulation
sim = ss.Sim(pars)
sim.run()
plot_results(sim)