"""
Creation of genetic algorithm to solve for either minimixzation of maximization of a function
Example: finding minima of teh function log(1 + 100*(x_1^2-x_2)^2 + (1-x_1)^2)
"""
import numpy as np
from math import pi
from pyDOE import lhs
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def f(x_1, x_2=0):
    # Test function
    # result = np.log10(1 + 100*(x_1**2-x_2)**2 + (1-x_1)**2)

    # Branin function
    a = 1.0
    b = 5.1 / (4 * pi ** 2)
    c = 5.0 / pi
    r = 6.0
    s = 10.0
    t = 1.0 / (8.0 * pi)

    result = a * (x_2 - b * x_1 ** 2 + c * x_1 - r) ** 2 + s * (1.0 - t) * np.cos(x_1) + s

    # result = x_1**3 +3*x_1**2 -9*x_1 +7

    return result

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
        random_value = np.random.uniform(-.5,0.5,1)
        random_parm = np.random.randint(0,offspring_crossover.shape[1],1)
        offspring_crossover[idx,random_parm] = offspring_crossover[idx, random_parm] + random_value # mutation added to last, could be any index

    return offspring_crossover

def plottingSurface(figure_num,x_vals,y_vals,z_vals):
    global ranges
    x_1_range = ranges[0]
    x_2_range =ranges[1]
    x = np.linspace(x_1_range [0], x_1_range [1], 20)
    y = np.linspace(x_2_range[0], x_2_range[1], 20)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    fig = plt.figure(figure_num)
    ax = fig.gca(projection='3d')
    ax.contour(X, Y, Z, 100)
    ax.scatter(x_vals,y_vals,z_vals,color='r')
    plt.show()


def GA(parms,parms_range, individuals, num_gen, plot):

    x_1_range = parms_range[0]
    x_2_range = parms_range[1]

    # plot function for visualization purposes
    # plottingSurface(100,[],[])

    # Create individuals (done here using latin hyper cube)
    # parms = 2
    # individuals = 20
    population = lhs(int(parms), individuals, 'Maximin')
    fx = []
    for i in range(len(population)):
        population[i] = [population[i][0]*(x_1_range[-1]-x_1_range[0])+x_1_range[0],population[i][1]*(x_2_range[-1]-x_2_range[0])+x_2_range[0]]
        tmp = []
        tmp.append(f(population[i][0],population[i][1]))
        fx.append(tmp)
    fx = np.array(fx)
    # plottingSurface(0,np.array(population[:,0]),np.array(population[:,1]),np.array(fx[:,2]))

    # num_gen = 1000
    graphs = [1,3,4,5,6,7,8,9,10]
    fx_mean = []
    fx_min = []
    for k in range(num_gen):
        fx_old = fx
        fx = []
        for i in population:
            fx.append([i[0],i[1],f(i[0],i[1])])
        fx.sort(key=lambda x: x[-1], reverse=True)
        fx = np.array(fx)
        parents = fx[np.uint8(len(population)*0.5):,:-1]
        offspring_crossover = crossover(np.array(parents), np.array([len(fx)- len(parents),parms]))
        offspring_mutation = mutation(offspring_crossover)
        # print(offspring_mutation)
        new_pop = np.zeros((parents.shape[0]+ offspring_mutation.shape[0],parms))
        new_pop[:parents.shape[0],:] = parents
        new_pop[parents.shape[0]:,:] = offspring_mutation
        population = new_pop
        if abs(np.mean(fx[-1,1:])-min(fx[-1,:]))<10e-6:
        # if abs(min(fx_old[-1,:])-min(fx[-1,:]))<10e-9:
            print("Mean function value {}".format(np.mean(fx_old[-1,:])))
            print("Minimzation function value : {}".format(fx_old[-1,-1]))
            print("Best parameters in current population: {}".format(fx_old[-1,:-1]))
            print("After {} generations".format(k+1))
            break
        if plot:
            if k in graphs:
                plottingSurface(k+1, fx_old[:,0], fx_old[:,1], fx_old[:,2])
        fx_mean.append(np.mean(fx[-1,:]))
        fx_min.append(min(fx[-1,:]))

    if k+1 == num_gen:
        print("Mean function value {}".format(np.mean(fx_old[-1,:])))
        print("Minimzation function value : {}".format(fx_old[-1,-1]))
        print("Best parameters in current population: {}".format(fx_old[-1,:-1]))
        print("After {} generations".format(k+1))

    [x_value, y_value, z_value] = fx_old[-1,:]
    plottingSurface(num_gen+3,fx[:,0], fx[:,1],fx[:,2])
    plottingSurface(num_gen+2,[x_value], [y_value], [z_value])
    return fx_old, k

ranges = [[-5.0,10.0],[0,10.0]]
GA(2,ranges,100,1000, plot = 1)
# fig = plt.figure(num_gen+4)
# ax = fig.gca()
# ax.scatter(list(range(k+1)),fx_min)
# ax.plot(list(range(k+1)),[min(fx[-1,:])]*len(fx_min))

# ax.scatter(x_value, y_value, color='r')

# plt.show()