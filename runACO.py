# -*- coding: utf-8 -*-
"""
@author: ofersh@telhai.ac.il
"""
from ACO import AntforTSP as ACO
import numpy as np


if __name__ == "__main__" :
   
    #Running for 120 groups
    fname120 = open("rotterdam_120groups.dat.txt")
    data120 = []
    for line in fname120:
        data120.append(int(line))
    n120 = len(data120)
    Niter = 10**2
    Nant = 120
    ant_colony_120 = ACO(data120,Nant, Niter, rho=0.95, beta=5)
    shortest_path_120 = ant_colony_120.run()
    print("shotest_path_120: {}".format(shortest_path_120), ' ', len(shortest_path_120[0]))
    
    #Running for 250 groups
    fname250 = open("roskilde_250groups.dat.txt")
    data250 = []
    Niter = 10**2
    Nant = 250
    for line in fname250:
        data250.append(int(line))
    n250 = len(data250)
    ant_colony_250 = ACO(data250,Nant, Niter, rho=0.95, beta=10)
    shortest_path_250 = ant_colony_250.run()
    print("shotest_path_250: {}".format(shortest_path_250), ' ', len(shortest_path_250[0]))
    
    