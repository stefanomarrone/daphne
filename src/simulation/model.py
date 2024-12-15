from scipy.integrate import odeint
import numpy as np
import math
from pde import CartesianGrid

grid = CartesianGrid([64, 64])                 # generate grid
state = pde.ScalarField.random_uniform(grid)  # generate initial condition

eq = pde.DiffusionPDE(diffusivity=0.1)
for x in range(10,30):
    result = eq.solve(state, t_range=x)  # solve the pde
    result.plot()  # plot the resulting field


