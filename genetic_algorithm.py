# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Based loosely here: https://github.com/gmichaelson/GA_in_python , https://www.youtube.com/watch?v=uCXm6avugCo and here: https://medium.com/@becmjo/genetic-algorithms-and-the-travelling-salesman-problem-d10d1daf96a1
import os
# since i run code in spyder, i use os.chdir to quickly change the working directory
os.chdir(r'C:\Users\The Risk Chief\Documents\GitHub\examples\genetic_algorithm')

import numpy as np
import random
import copy
import matplotlib.pyplot as plt

def initialize(p_zero, N):
#    First thing is to create the map you're trying to navigate. I will do this randomly
#    This will ne the from of a adjacency matrix
#    In other words, an NxN matrix whre each row and column correspond to an intersection on a map
#    X_ij, then is equal to the amount of the time that it takes to got from position i to position j
#    could alse be considered as a distance measure
#    practically, then we need a matric that has numeric values in it..
#    the should be some path that don't exist. I will assign these a 0
#   For instance if you cant get directly from i to j, then X_ij = 0

#    The initialization needs some tuning parameters. One is the proportion of  0's in the final result

    the_map = np.zeros((N,N))
    for i in range(0, N):
        for j in range(0,i):
            if random.random()> p_zero:
                the_map[i][j] = random.random() * 100
                the_map[j][i] = the_map[i][j]
    return the_map
                    
def create_starting_population(size, the_map):
#    This just creates a population of different routes of a fixed size. Pretty straightforward

    population = []
    
    for i in range (0, size):
        population.append(create_new_member(the_map))
        
    return population

def fitness(route, the_map):
    score = 0
    for i in range(1, len(route)):
        if (the_map[route[i-1]][route[i]] == 0) and i != len(the_map)-1:
            print("WARNING: INVALID ROUTE")
            print(route)
            print(the_map)
        score = score + the_map[route[i-1]][route[i]]
    return score

def crossover(a, b):

    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(a))
    geneB = int(random.random() * len(a))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(a[i])
        
    childP2 = [item for item in b if item not in childP1]

    child = childP1 + childP2
#    child = np.array(child)
    return child       
#    return (new_a, new_b)

def mutate(route, probability, the_map):
       
    for i in range(len(route)):
        if(random.random() < probability):
            swap_with = int(random.random()*len(route))
            city1 = route[i]
            city2 = route[swap_with]
            
            route[i] = city2
            route[swap_with] = city1
            
    return new_route

#   Creates a new member
def create_new_member(the_map):    
    route = np.random.choice(len(the_map), len(the_map), replace=False)
#    print(route)
    return route

def score_population(population, the_map):
    
    scores = []
    
    for i in range(0, len(population)):
        scores += [fitness(population[i], the_map)]
        
    return scores
    
def pick_mate(scores):

    array = np.array(scores)
    temp = array.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(array))

    fitness = [len(ranks) - x for x in ranks]
    
    cum_scores = copy.deepcopy(fitness)
    
    for i in range(1,len(cum_scores)):
        cum_scores[i] = fitness[i] + cum_scores[i-1]
        
    probs = [x / cum_scores[-1] for x in cum_scores]
    
    rand = random.random()
    
    for i in range(0, len(probs)):
        if rand < probs[i]:
            
            return i
    
def main():
    
# parameters
sparseness_of_map = 0.95
size_of_map = 10
population_size = 50
number_of_iterations = 1000
number_of_couples = 9
mutation_probability = 0.05
number_of_winners_to_keep = 2
number_of_groups = 1

# initialize the map and save it
the_map = initialize(0, size_of_map)
# create the starting population
population = create_starting_population(population_size, the_map)

last_distance = 1000000000
# for a large number of iterations do:
best_of_alltime = population[0]    
for i in range(0,number_of_iterations):
    new_population = []
#    print(i)
    # evaluate the fitness of the current population
    scores = score_population(population, the_map)    
    best = population[np.argmax(scores)]
    
    number_of_moves = len(best)
    distance = fitness(best, the_map)
    
    if distance != last_distance:
        print('Iteration %i: Best so far is %i steps for a distance of %f' % (i, number_of_moves, distance))

    if(fitness(best, the_map) > fitness(best_of_alltime, the_map)):
        best_of_alltime= best
        best_score_of_alltime = fitness(best_of_alltime, the_map)
        print("best of alltime has changed, it is: ", best_score_of_alltime)
    
    # allow members of the population to breed based on their relative score; 
        # i.e., if their score is higher they're more likely to breed
#    for j in range(0, number_of_couples):  
#        new_1, new_2 = crossover(population[pick_mate(scores)], population[pick_mate(scores)])
#        new_population = new_population + [new_1, new_2]

    for j in range(0, number_of_couples):  
#        new_route = crossover(population[0], population[17])
        new_route = crossover(population[pick_mate(scores)], population[pick_mate(scores)])
        new_population.append(new_route)
  
    # mutate
    for j in range(0, len(new_population)):
        new_population[j] = np.copy(mutate(new_population[j], mutation_probability, the_map))
        
    # keep members of previous generation
    new_population += [population[np.argmax(scores)]]
    for j in range(1, number_of_winners_to_keep):
        keeper = pick_mate(scores)            
        new_population += [population[keeper]]
        
    # add new random members
    while len(new_population) < population_size:
        new_population += [create_new_member(the_map)]
        
    #replace the old population with a real copy
    population = copy.deepcopy(new_population)
            
    last_distance = distance
    
    # plot the results
    
