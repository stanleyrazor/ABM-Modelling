library(R6)
rm(list=ls())

# Define parameters
beta <- 2.5  # Infection rate
gamma <- 1.0  # Recovery rate
contact_rate <- 0.5  # Fraction of population each person connects to
I0 <- 5  # Number of people initially infected
N <- 100  # Total population size
maxtime <- 10  # How long to simulate for
npts <- 100  # Number of time points during the simulation
dt <- maxtime / npts  # Timestep length

# Define Person class
Person <- R6Class("Person",
  public = list(
    S = 1,  # People start off susceptible
    I = 0,
    R = 0,
    
    infect = function() {
      self$S <- 0
      self$I <- 1
      return(self)
    },
    
    recover = function() {
      self$I <- 0
      self$R <- 1
      return(self)
    },
    
    check_infection = function(other) {
      if (self$S & other$I & runif(1) < beta / (N * contact_rate) * dt) {
        self <- self$infect()
      }
      return(self)
    },
    
    check_recovery = function() {
      if (self$I & (runif(1) < (gamma * dt))) {
        self <- self$recover()
      }
      return(self)
    }
  )
)

# Define Sim class
Sim <- R6Class("Sim",
  public = list(
    x = seq(0, npts - 1),
    S = rep(0, npts),
    I = rep(0, npts),
    R = rep(0, npts),
    time = NULL,
    people = list(),
    
    initialize = function() {
      for (i in 1:N) {
        self$people[[i]] <- Person$new()
      }
      
      for (i in 1:I0) {
        self$people[[i]]$infect()
      }
      
      self$time = self$x * dt
    },
    
    count = function() {
      S = 0
      I = 0
      R = 0
      for (i in 1:N) {
        S = S + self$people[[i]]$S
        I = I + self$people[[i]]$I
        R = R + self$people[[i]]$R
      }
      return(list(S = S, I = I, R = R))
    },
    
    check_infections = function() {
      for (i in 1:N) {
        contacts <- sample(1:N, size = floor(N * contact_rate))
        for (contact in contacts) {
          person1 <- self$people[[i]]
          person2 <- self$people[[contact]]
          self$people[[i]]$check_infection(person2)
        }
      }
      return(self)
    },
    
    check_recoveries = function() {
      for (i in 1:N) {
        person = self$people[[i]]
        self$people[[i]]$check_recovery()
      }
      return(self)
    },
    
    run = function() {
      for (t in self$x) {
        self$check_infections()
        self$check_recoveries()
        
        # Update results
        counts <- self$count()
        self$S[[t + 1]] <- counts$S
        self$I[[t + 1]] <- counts$I
        self$R[[t + 1]] <- counts$R
      }
      
      cat("Run finished\n")
      return(self)
    },
    
    plot = function() {
      plot(self$time, self$S, type = "l", col = "blue", lwd = 2, xlab = "Time", ylab = "Number of people", main = "SIR Model")
      lines(self$time, self$I, type = "l", col = "red", lwd = 2)
      lines(self$time, self$R, type = "l", col = "green", lwd = 2)
      legend("topleft", legend = c("Susceptible", "Infectious", "Recovered"), fill = c("blue", "red", "green"))
    }
  )
)

# Run the simulation
sim <- Sim$new()
sim$run()
sim$plot()
