import pylab as pl
import sciris as sc

sc.options(dpi=200)

class Antsim:
    ''' Simulation of ants randomly walking '''    
    
    def makeants(self, num_ants=50):
        ''' Initialize the ants '''
        # Initialize the number of ants
        self.numants = num_ants

        # Initialize the x and y coordinates: an array of zeros of length num_ants
        self.x = pl.zeros(num_ants)
        self.y = pl.zeros(num_ants)
    
    def plotants(self, timesteps=150, stepsize=0.03):
        ''' Plot the ants '''
        pl.figure()
        # For each timestep in the configured number of timesteps
        for t in range(timesteps):
            pl.clf()
            # Increment the x and y position of each ant by an amount stepsize*randn()
            self.x += stepsize*pl.randn(self.numants)
            self.y += stepsize*pl.randn(self.numants)
            # Scatter x vs y
            pl.scatter(self.x, self.y)
            # Set the x and y limits to (-1,1)
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            # Set the plot title to show the current step and total # of timesteps
            pl.title('t = %i / %i' % (t+1, timesteps))
            pl.pause(1e-3)
            

# Create and run the simulation
sim = Antsim()
sim.makeants(num_ants=100)
# Plot the ants
sim.plotants()
