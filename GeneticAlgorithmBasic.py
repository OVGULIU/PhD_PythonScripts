"""
Genetic algorithm tutorial from https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6
2 April 2019

Equation = yw1x1 + w2x2 + w3x3 + w4x4 + w5x5 + w6x6
w1 = weighting, xi = inputs (i = 1,2,...6)
"""
import numpy as np

def cal_popFitness(equation_inputs, pop):
    #Fitness function calculates teh sum of teh products between each input and its corresponding weight
    fitness = np.sum(pop*equation_inputs,axis=1)
    return fitness

def select_mating_pool(new_population, fitness, num_parents):
    parents = np.empty((num_parents, new_population.shape[1]))

    for parent_num in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num,:] = new_population[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
        return parents

def crossover(parents, offspring_size):
    offspring = np.empty(offspring_size)
    crossover_point = np.uint8(offspring_size[1]/2)
    for k in range(offspring_size[0]):
        parent1_idx = k%parents.shape[0]
        parent2_idx = (k+1)%parents.shape[0]
        offspring[k,0:crossover_point] = parents[parent1_idx,0:crossover_point]
        offspring[k,crossover_point:] = parents[parent2_idx,crossover_point:]
        return offspring

def mutation(offspring_crossover):

    for idx in range(offspring_crossover.shape[0]):
        random_value = np.random.uniform(-1.0,1.0,1)
        offspring_crossover[idx,-1] = offspring_crossover[idx, -1] + random_value # mutation added to index 4, caould be any index

        return offspring_crossover

equation_inputs = [4, -2, 3.5, 5, 11, -4.7]
num_weights = 6

sol_per_pop = 8
num_parents_mating = 4

pop_size = (sol_per_pop, num_weights)

new_population = np.random.uniform(low=-4.0, high=4.0, size=pop_size) # generates matrix of pop_size (8,6) corresponds to weight values
num_generation = 4
for i in range(num_generation):
    fitness = cal_popFitness(equation_inputs,new_population)
    parents = select_mating_pool(new_population,fitness, num_parents_mating)
    offspring_crossover = crossover(parents,offspring_size=(pop_size[0]-parents.shape[0], num_weights))
    offspring_mutation = mutation(offspring_crossover)

    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:,: ] = offspring_mutation

    # The best result in the current iteration.
    print("Best result : ", np.max(np.sum(new_population * equation_inputs, axis=1)))

fitness = cal_popFitness(equation_inputs,new_population)

best_match_idx = np.where(fitness == np.max(fitness))
print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])