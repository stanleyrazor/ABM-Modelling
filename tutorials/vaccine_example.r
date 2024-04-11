# Clear all variables and load the needed libraries
rm(list=ls())
library(reticulate)
library(ggplot2)

# Import libraries from Python (note: do NOT create a new environment if asked)
vacc_ex <- import('vaccine_example')
ss <- import('starsim')

make_run_sim <- function(beta=0.05, waning=0.05, seed=1, vaccine=FALSE, ti=10, p=0.5, boost=2.0) {
    pars <- list(
        n_agents = 500,
        start = 0,
        end = 100,
        dt = 1.0,
        rand_seed = as.integer(seed),
        networks = 'random',
        diseases = list(
            type = 'sis',
            beta = beta,
            waning = waning
        )
    )
    
    # Define "baseline" and "intervention" sims without and with the vaccine
    if (vaccine) {
        vx <- vacc_ex$Vaccine(ti=ti, p=p, boost=boost)
        sim <- ss$Sim(pars, interventions=vx)
    } else {
        sim <- ss$Sim(pars)
    }
    
    # Run the simulation
    sim$run()
    results <- list(time=sim$yearvec, n_infected=sim$results$sis$n_infected)
    return(results)
}


res_plot <- function(results, label='') {
    lines(results$time, results$n_infected, type='l', main='Number of people infected', xlab='Time', ylab='Number of Infected')
    legend('topright', legend=label, lwd=2)
}

# res_plot(res1, 'Baseline')
# res_plot(res2, 'Vaccine')
    

# Make, run, and plot the simulation
res1 <- make_run_sim(beta=0.08, waning=0.03, seed=15)
res2 <- make_run_sim(beta=0.08, waning=0.03, seed=15, vaccine=TRUE, ti=4, p=0.8, boost=10)

# Combine the data into a single data frame
df <- data.frame(
    time=res1$time,
    Baseline=res1$n_infected, 
    Vaccine=res2$n_infected
)
res1$label <- 'Baseline'
res2$label <- 'Vaccine'

# Define the plotting function
res_plot <- ggplot(df, aes(x = time)) +
    geom_line(aes(y = Baseline, color = 'Baseline')) +
    geom_line(aes(y = Vaccine, color = 'Vaccine')) +
    labs(title = 'Number of people infected', x = 'Time', y = 'Number of Infected') +
    scale_color_manual(values = c('Baseline' = 'blue', 'Vaccine' = 'red'))
print(res_plot)