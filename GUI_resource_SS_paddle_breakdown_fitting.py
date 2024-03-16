
#fitting and plotting file for SS paddle --GUI file source

import SS_paddle_breakpoint_fitting as SS

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy as sp
from scipy.interpolate import interp1d
import os
from time import time


#Priliminary test with plot temp read from pyrometer via serial port
#plot for threads
# Function to plot data
    


#add fitting and plot based received photodiode current
def f(PDcurrent_point):
   fitted_T=SS.fitting_region_split(PDcurrent_point)
   return fitted_T

#print(f(1e-17))