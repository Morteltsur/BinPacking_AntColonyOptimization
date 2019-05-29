# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 09:42:08 2018

@author: ofersh@telhai.ac.il
Based on code by <github/Akavall>
"""
import numpy as np

"""
A class for defining an Ant Colony Optimizer for TSP-solving.
The c'tor receives the following arguments:
    Graph: TSP graph 
    Nant: Colony size
    Niter: maximal number of iterations to be run
    rho: evaporation constant
    alpha: pheromones' exponential weight in the nextMove calculation
    beta: heuristic information's (\eta) exponential weight in the nextMove calculation
    seed: random number generator's seed
    we consider a general solution for best packing with ACO
"""
class AntforTSP(object) :
    def __init__(self, Items, Nant, Niter, rho, beta=1, seed=None):
        self.Items = Items
        self.Nant = Nant
        self.Niter = Niter
        self.rho = rho
        self.beta = beta
        self.pheromone = np.ones([max(self.Items)+1, max(self.Items)+1])*20
        self.local_state = np.random.RandomState(seed)

    def run(self) :
        #Book-keeping: best tour ever        
        shortest_path = None
        best_path = ("TBD", 0)
        for i in range(self.Niter):
            all_paths = self.constructColonyPaths()
            print
            self.pheromone * self.rho  #evaporation 
            shortest_path = max(all_paths, key=lambda x: x[1])   
            if i % 5 == 0 and i != 0:
                self.depositPheronomes(best_path)
            else:
                self.depositPheronomes(shortest_path)           
            print(i+1, ": ", len(shortest_path[0]), " ", shortest_path[0])
            if shortest_path[1] > best_path[1]:
                best_path = shortest_path            
        return best_path

    def depositPheronomes(self, best_ant) :
        best_ant_packing = best_ant[0]
        best_fitness = best_ant[1]
        for _bin in best_ant_packing:
            for i in range(0, len(_bin)):
                for j in range(i+1, len(_bin)):
                    self.pheromone[_bin[i]][_bin[j]] += best_fitness #dist
                    self.pheromone[_bin[j]][_bin[i]] += best_fitness #dist

    def constructColonyPaths(self) :
        all_paths = []
        for i in range(self.Nant):
            path = self.constructSolution()
            #constructing pairs: first is the tour, second is its length
            all_paths.append((path, self.evalTour(path))) 
        return all_paths   
    
    def evalTour(self, path) :
        sum_bins = 0
        C = 150
        k=2
        for _bin in path:
            F = 0
            for item in _bin:
                F += item
            sum_bins += (F/C)**k               
        return sum_bins/len(path)           
    
    def constructSolution(self) :#TO DO
        items = list(np.copy(self.Items))
        path = []
        for i in range(len(self.Items)) :
            row = self.fillRow(items)
            path.append(row)
            if len(items) == 0: break
        return path
           
    def fillBin(self, items):
        bin_items = []
        _bin = 0
        max_bin = 150
        while len(items) != 0 and (max_bin - _bin) > min(items):
            for item in items:
                if self.ifToAddItem(max_bin - _bin, item, bin_items, items):
                    bin_items.append(item)
                    _bin += item
                    items.remove(item)
                    break
                if len(items) == 0 or (max_bin - _bin) < min(items) :
                    break
        return bin_items
           
    def ifToAddItem(self, bin_left_space, item, bin_items, items):
        if item > bin_left_space: 
            return False
        denom = 0
        for i in items:
           if i <= bin_left_space:
                denom += self.binTao(i, bin_items)*(i**self.beta)
        nume = self.binTao(item, bin_items)*item**self.beta
        return self.local_state.uniform() < (nume/denom)
    
    def binTao(self, item, bin_items):
        phero_sum = 0
        if len(bin_items) == 0: 
            return 1
        for i in bin_items:
            phero_sum += self.pheromone[i][item]
        return phero_sum/len(bin_items)    
    
        
    