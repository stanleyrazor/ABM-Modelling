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
Person <- function() {
  self <- list(
    S = 1,  # People start off susceptible
    I = 0,
    R = 0
  )
  
  self$infect <- function(self) {
    self$S <- 0
    self$I <- 1
    return(self)
  }
  
  self$recover <- function(self) {
    self$I <- 0
    self$R <- 1
    return(self)
  }
  
  self$check_infection <- function(self, other) {
    if (self$S & other$I & runif(1) < beta / (N * contact_rate) * dt) {
      self <- self$infect(self)
    }
    return(self)
  }
  
  self$check_recovery <- function(self) {
    if (self$I & (runif(1) < (gamma * dt))) {
      self <- self$recover(self)
    }
    return(self)
  }
  
  return(self)
}

# Define Sim class
Sim <- function() {
  # Create arrays
  self <- list(
    x = seq(0, npts - 1),
    S = rep(0, npts),
    I = rep(0, npts),
    R = rep(0, npts)
  )
  self$people <- list()
  for (i in 1:N) {
    self$people[[i]] <- Person()
  }
  
  for (i in 1:I0) {
    self$people[[i]] <- self$people[[i]]$infect(self$people[[i]])
  }
  
  self$time = self$x * dt
  
  self$count <- function(self) {
    S = 0
    I = 0
    R = 0
    for (i in 1:N) {
      S = S + self$people[[i]]$S
      I = I + self$people[[i]]$I
      R = R + self$people[[i]]$R
    }
    return(list(S = S, I = I, R = R))
  }
  
  self$check_infections <- function(self) {
    for (i in 1:N) {
      contacts <- sample(1:N, size = floor(N * contact_rate))
      for (contact in contacts) {
        person1 <- self$people[[i]]
        person2 <- self$people[[contact]]
        self$people[[i]] <- person1$check_infection(person1, person2)
      }
    }
    return(self)
  }
  
  self$check_recoveries <- function(self) {
    for (i in 1:N) {
      person = self$people[[i]]
      self$people[[i]] <- person$check_recovery(person)
    }
    return(self)
  }
  
  self$run <- function(self) {
    for (t in self$x) {
      self <- self$check_infections(self)
      self <- self$check_recoveries(self)
      
      # Update results
      counts <- self$count(self)
      self$S[[t + 1]] <- counts$S
      self$I[[t + 1]] <- counts$I
      self$R[[t + 1]] <- counts$R
    }
    
    cat("Run finished\n")
    return(self)
  }
  
  self$plot <- function(self) {
    plot(self$time, self$S, type = "l", col = "blue", lwd = 2, xlab = "Time", ylab = "Number of people", main = "SIR Model")
    lines(self$time, self$I, type = "l", col = "red", lwd = 2)
    lines(self$time, self$R, type = "l", col = "green", lwd = 2)
    legend("topleft", legend = c("Susceptible", "Infectious", "Recovered"), fill = c("blue", "red", "green"))
  }
  
  return(self)
}

# Run the simulation
sim <- Sim()
sim <- sim$run(sim)
sim$plot(sim)