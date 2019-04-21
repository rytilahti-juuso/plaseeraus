# -*- coding: utf-8 -*-
# Based loosely here: https://github.com/gmichaelson/GA_in_python , https://www.youtube.com/watch?v=uCXm6avugCo and here: https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
import os
# since I run code in spyder, i use os.chdir to quickly change the working directory
os.chdir(r'C:\Users\The Risk Chief\Documents\GitHub\examples\genetic_algorithm')

import numpy as np
import random
import copy
import matplotlib.pyplot as plt

def generate_table_group(dummy_participant_count, i):
    table_group= []
    probability = random.randint(0,9)
#    print(probability)
    if(probability >=2):
        table_group.append(random.randint(0,dummy_participant_count))
        if(probability >=4):
            table_group.append(random.randint(0,dummy_participant_count))
            if(probability>=6):
                table_group.append(random.randint(0,dummy_participant_count))
    if i in table_group:
            table_group.remove(i)
    return table_group

# one element contains(name, table_group, gender, boolean isAlreadySorted)
def generate_all_dummy_data(dummy_participant_count):    
    all_data = []
    for i in range(dummy_participant_count):
    #    data for single person stored in array
        person_data = []        
        person_data.append(i)
    #    people wanted in the same table group
        table_group = generate_table_group(dummy_participant_count-1, i)
        person_data.append(table_group)
    #    persons gender
        person_data.append(random.randint(0,1))
        person_data.append(False)
        all_data.append(person_data)
        print(i)
    return all_data
    
def create_score_table(table_order):
    N = len(table_order)
    score_table = np.zeros((N,N))
    for i in range(N):
#        Add friend score
        for z in range(len(table_order[i][1])):
                print(table_order[i][1][z])
                wished_number = table_order[i][1][z]
                score_table[i][wished_number] +=2
        for j in range(N):
                                    
            if(i == j):
                continue
##            if different gender
            if(table_order[j][2] != table_order[i][2]):
                score_table[i][j] += 10
            elif(table_order[j][2] == table_order[i][2]):
                score_table[i][j] += 9

    return score_table

def validate_that_desire_to_table_group_is_mutual(score_table):
    N = len(score_table)
    new_table = []
    for i in range(N):
        for j in range(N):
            if(score_table[j][i] == score_table[i][j] and score_table[j][i] >= 11):
                new_table.append(j)  
    return new_table
    
    
def initialize(p_zero, N):

    score_table = np.zeros((N,N))
    for i in range(0, N):
        for j in range(0,i):
            if random.random()> p_zero:
                score_table[i][j] = random.random() * 100
                score_table[j][i] = score_table[i][j]
    return score_table
                    
def create_starting_population(size, score_table):
#    This just creates a population of different sitting_orders of a fixed size. Pretty straightforward

    population = []
    
    for i in range (0, size):
        population.append(create_new_member(score_table))
        
    return population

def fitness(sitting_order, score_table):
    score = 0
    for i in range(1, len(sitting_order)):
        if (score_table[sitting_order[i-1]][sitting_order[i]] == 0) and i != len(score_table)-1:
            print("WARNING: INVALID sitting_order")
            print(sitting_order)
            print(score_table)
        score = score + score_table[sitting_order[i-1]][sitting_order[i]]
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

def mutate(sitting_order, probability, score_table):
       
    for i in range(len(sitting_order)):
        if(random.random() < probability):
            swap_with = int(random.random()*len(sitting_order))
            city1 = sitting_order[i]
            city2 = sitting_order[swap_with]
            
            sitting_order[i] = city2
            sitting_order[swap_with] = city1
            
    return new_sitting_order

#   Creates a new member
def create_new_member(score_table):    
    sitting_order = np.random.choice(len(score_table), len(score_table), replace=False)
#    print(sitting_order)
    return sitting_order

def score_population(population, score_table):
    
    scores = []
    
    for i in range(0, len(population)):
        scores += [fitness(population[i], score_table)]
        
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
    
#def main():
    
# parameters
sparseness_of_map = 0.95
size_of_map = 20
population_size = 50
number_of_iterations = 1000
number_of_couples = 9
mutation_probability = 0.05
number_of_winners_to_keep = 2
number_of_groups = 1

#added from participant_organizer for testing purposes
all_data = generate_all_dummy_data(10)
score_table = create_score_table(all_data)
validate_that_desire_to_table_group_is_mutual(score_table)
# initialize the map and save it
#score_table = initialize(0, size_of_map)
# create the starting population
population = create_starting_population(population_size, score_table)

last_distance = 0
# for a large number of iterations do:
best_of_alltime = population[0]    
for i in range(0,number_of_iterations):
    new_population = []
#    print(i)
    # evaluate the fitness of the current population
    scores = score_population(population, score_table)    
    best = population[np.argmax(scores)]
    
    number_of_moves = len(best)
    distance = fitness(best, score_table)
    
    if distance != last_distance:
        print('Iteration %i: Best so far is %i steps for a distance of %f' % (i, number_of_moves, distance))

    if(fitness(best, score_table) > fitness(best_of_alltime, score_table)):
        best_of_alltime= best
        best_score_of_alltime = fitness(best_of_alltime, score_table)
        print("best of alltime has changed, it is: ", best_score_of_alltime)
    
    # allow members of the population to breed
    for j in range(0, number_of_couples):  
#        new_sitting_order = crossover(population[0], population[17])
        new_sitting_order = crossover(population[pick_mate(scores)], population[pick_mate(scores)])
        new_population.append(new_sitting_order)
  
    # mutate
    for j in range(0, len(new_population)):
        new_population[j] = np.copy(mutate(new_population[j], mutation_probability, score_table))
        
    # keep members of previous generation
    new_population += [population[np.argmax(scores)]]
    for j in range(1, number_of_winners_to_keep):
        keeper = pick_mate(scores)            
        new_population += [population[keeper]]
        
    # add new random members
    while len(new_population) < population_size:
        new_population += [create_new_member(score_table)]
        
    #replace the old population with a real copy
    population = copy.deepcopy(new_population)
            
    last_distance = distance
    
    # plot the results
    
