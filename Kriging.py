"""
Kriging meta-models
"""
# import matplotlib.pyplot as plt
import numpy as np
from pyDOE import lhs
from math import pi, cos
import copy
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# Import experimental data
def loaddisplacementData(Filename):
    wd = '/home/cerecam/Desktop/Crack_Models'
    with open(wd + Filename, 'r') as file:
        data = file.readlines()

    x = []
    y = []
    for line in data[3:-1]:
        x.append(float(line.split()[0]))
        y.append(float(line.split()[1]))

    return x, y


#  def back_sub(A,b):
#      pass
# #     # Performs back-substitution i.e. A\b = x
# #     n = len(A)
# #     # print('n is:', n)
# #     x = [0]*n
# #     for i in range(n-1,-1,-1): #this refers to the rows; i goes 2,1,0
# #         for j in range(i+1,n): #j goes 1,2 @ i = 0
# #                                #j goes 2   @ i = 1
# #             b[i] = b[i] - A[i,j]*x[j]
# #         x[i] = b[i]/A[i,i]
# #
#      return

# def likelihood(x):
    # global x_exp
    # global y_exp
    #
    # x = [1]
    #
    # theta = [10 ** i for i in x]
    # n = len(x_exp)
    # one = [1] * n
    # PSI = [[0] * n] * n
    # eps = np.spacing(1) * 100
    # x_exp = [x_exp]
    # y_exp = [y_exp]
    #
    # for i in range(n):
    #     for j in range(n):
    #         for k in range(len(theta)):
    #             PSI[i][j] = PSI[i][j] + np.exp(-theta[k] * (x_exp[k][i] - x_exp[k][j]) ** 2)
    #
    # # for i in range(n):
    # #     PSI = np.matrix(PSI) + np.transpose(np.matrix(PSI))
    # try:
    #     [U, p] = np.linalg.cholesky(PSI)
    #     LnDetPsi = 2 * np.sum(np.log(abs(np.diag(U))))
    #     mu = (np.matmul(np.transpose(one), np.matmul(np.invert(np.matrix(PSI)), np.array(y_exp))))
    #     var = np.matmul(np.transpose(np.array(y_exp[0]) - np.matmul(one, mu)),
    #                     np.matmul((np.invert(np.matrix(PSI)), np.array(y_exp[0]) - np.matmul(one, mu)))) / float(n)
    #     NegLnLike = -1 * (-n / 2.0) * np.log(var) - 0.5 * LnDetPsi
    #
    # except:
    #     NegLnLike = 1e4
    #
    # return NegLnLike, PSI, U


def Branin(x1, x2):
    """
    Branin function: a(x2 - b*x1² + c*x1 - r)² + s(1-t)cos(x1) + s

    :param x1: dimension 1
    :param x2: dimension 2
    """
    # Recommended function values

    a = 1.0
    b = 5.1 / (4 * pi ** 2)
    c = 5.0 / pi
    r = 6.0
    s = 10.0
    t = 1.0 / (8.0 * pi)
    # Original
    f = a * (x2 - b * x1 ** 2 + c * x1 - r) ** 2 + s * (1.0 - t) * np.cos(x1) + s

    # Modified
    # f = a * (x2 - b * x1 + c * x1 - r) ** 2 + s * ((1.0 - t) * np.cos(x1)+1) + s*x1
    return f


def objectiveFunction(x_i, x_j, parms, theta, p):
    d = 0
    y = 0
    for i in range(parms):
        d = d + theta[i] * (abs(x_i[i] - x_j[i]) ** p)
        y = y + abs(x_i[i] - x_j[i])
        # print(d)
    return d, y


def correlation(d):
    return np.exp(-d)

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
        random_value = np.random.uniform(-.05,0.05,1)
        random_parm = np.random.randint(0,offspring_crossover.shape[1],1)
        offspring_crossover[idx,random_parm] = offspring_crossover[idx, random_parm] + random_value # mutation added to last, could be any index

    return offspring_crossover

def likelihood(x_data, theta, p=2):
    global data_points
    x1 = []
    x2 = []
    cor = np.zeros(((data_points - 1), (data_points - 1)))
    y = np.zeros((data_points - 1))
    for idx,i in enumerate(theta):
        theta[idx] = 10**i

    for idx1, i in enumerate(x_data):
        x1.append(i[0])
        x2.append(i[1])
        X_i = [x1[-1], x2[-1]]
        y[idx1] = Branin(X_i[0], X_i[1])
        dif = np.zeros((data_points - 1))
        objFunc = np.zeros((data_points - 1))
        for idx2, j in enumerate(x_data):
            X_j = [j[0], j[1]]
            a, b = objectiveFunction(X_i, X_j, 2, theta, p)
            dif[idx2] = b
            objFunc[idx2] = a
            cor[idx1, idx2] = correlation(a)
    # print()
    cor = cor + np.eye(data_points-1)+ np.eye(data_points-1)*0.000001
    cor_inv = np.linalg.inv(cor)

    mu_bar = (np.matmul(np.transpose(one_bar), np.matmul(cor_inv, y))) / (
              np.matmul(np.transpose(one_bar), np.matmul(cor_inv, one_bar)))
    sig_2 = (np.matmul(np.transpose(y - (one_bar * mu_bar)), np.matmul(cor_inv,
                                   (y - (one_bar * mu_bar))))) / (
        (data_points - 1))
    # print("Condition number: {}".format(np.linalg.cond(cor)))
    if np.linalg.det(cor) <= 0:
        print("***** Ill conditioned matrix!")
        likelihood = 10000
    else:
        lnDetCor = 2*np.sum(np.log(abs(np.diag(cor))))
        likelihood = -1 * (-((data_points-1) / 2.0) * np.log((sig_2)) - (1.0 / 2.0) * lnDetCor)


    return cor, mu_bar, sig_2, likelihood

def f(param_set):
    global  lhd
    # for i in param_set:
    cor,mu,sig,lnLikeli = likelihood(lhd,param_set)
    return lnLikeli

def GA(parms,parms_range, individuals=100, num_gen=500):
    global lhd

    # Create individuals (done here using latin hyper cube)
    population = lhs(int(parms), individuals, 'Maximin')
    nonscaled_pop = copy.copy(population)
    fx = []
    for i in range(len(population)):
        population_tmp = []
        tmp = []
        for k in range(parms):
            population_tmp.append(population[i][k] * (parms_range[k][-1] - parms_range[k][0]) + parms_range[k][0])
        population[i] = population_tmp
        # tmp = list(population[i])
        tmp.append(f(population_tmp))
        fx.append(tmp)
    fx = np.array(fx)
    fx_mean = []
    fx_min = []
    for k in range(num_gen):
        fx_old = fx
        fx = []
        for i in population:
            fx_tmp = []
            for val in i:
                fx_tmp.append(val)
            fx_tmp.append(f(i))
            fx.append(fx_tmp)
        fx.sort(key=lambda x: x[-1], reverse=True)
        fx = np.array(fx)
        parents = fx[np.uint8(len(population) * 0.5):, :-1]
        if parms > 1:
            offspring_crossover = crossover(np.array(parents), np.array([len(fx) - len(parents), parms]))
            offspring_mutation = mutation(offspring_crossover)
        else:
            # print(fx)
            # print(parents)
            offspring_mutation = mutation(np.array(parents))
            # print(offspring_mutation)

        # print(offspring_mutation)
        new_pop = np.zeros((parents.shape[0] + offspring_mutation.shape[0], parms))
        new_pop[:parents.shape[0], :] = parents
        new_pop[parents.shape[0]:, :] = offspring_mutation
        population = copy.copy(new_pop)

        # print("generation number: {}".format(k+1))
        # print("Minimzation function value : {}".format(fx_old[-1, -1]))
        # print("Best parameters in current population: {}".format(fx_old[-1, :-1]))
        test = []
        for i in range(parms):
            test.append(abs(np.mean(fx[:, i]) - fx[-1, i]) < 10e-5)
        if all(test):
            # if abs(min(fx_old[-1,:])-min(fx[-1,:]))<10e-9:
            # print("Mean function value {}".format(np.mean(fx_old[-1, :])))
            print("Minimzation function value : {}".format(fx_old[-1, -1]))
            # print("Best parameters in current population: {}".format([10 ** (e) for e in fx_old[-1, :-1]]))
            print("After {} generations".format(k + 1))
            break
        fx_mean.append(np.mean(fx[:, :-1], axis=0))
        fx_min.append(fx[-1, :])

    if k + 1 == num_gen:
        # print("Mean function value {}".format(np.mean(fx_old[-1, :])))
        print("Minimzation function value : {}".format(fx_old[-1, -1]))
        # print("Best parameters in current population: {}".format([10 ** (e) for e in fx_old[-1, :-1]]))
        print("After {} generations".format(k + 1))

    return fx_old, k

def plottingSurface(figure_num,x_vals,y_vals,z_vals):
    global ranges
    x_1_range = ranges[0]
    x_2_range =ranges[1]
    x = np.linspace(x_1_range [0], x_1_range [1], 20)
    y = np.linspace(x_2_range[0], x_2_range[1], 20)
    X, Y = np.meshgrid(x, y)
    Z = Branin(X, Y)
    fig = plt.figure(figure_num)
    ax = fig.gca(projection='3d')
    ax.contour(X, Y, Z, 100)
    ax.scatter(x_vals,y_vals,z_vals,color='r')
    plt.show()

ranges = [[-5.0,10.0],[0,10.0]]
# ranges = [[-5.0,10.0],[0,15.0]]
x_1_range = ranges[0]
x_2_range = ranges[1]
data_points = 21
one_bar = np.array([1] * (data_points-1))
lhd = lhs(2, data_points, 'Maximin') # sampling data

for count, i in enumerate(lhd):
    lhd[count] = [i[0] * (x_1_range[1] - x_1_range[0]) + x_1_range[0],i[1] * (x_2_range[1] - x_2_range[0]) + x_2_range[0]]
lhd_full = copy.copy(lhd)
lhd = lhd[1:] # removing one value to allow for cross model validation

# Calibration of initial Kriging model for parameter theta, assuming p = 2 (exponent in weighted residual)
# theta value refers to ln of this number so theta 2 is actually a value of 10^2, approximated range betweeen 10^-3 and 10^2

# parms = 2
# parms_range = [[-3,2],[-3,2]]
# individuals =100
# num_gen=500

num_parms = 2
range_parms = [[-3,2],[-3,2]]
num_individ=20
generations=100

theta_tmp = []
for iter in range(5):
    Results = GA(num_parms,range_parms, num_individ, generations)
    values = Results[0][-1, :]
    theta_tmp.append(np.array([10**i for i in values[:-1]]))
theta_vals = np.mean(theta_tmp,axis=0)
print("Best parameters in current population: {}".format(theta_vals))

# Kringing prediction
test_points = [lhd_full[0], lhd_full[1]]
lhd_new = lhs(2, 21,'Maximin')
new_y = []
for new_point in lhd_new:
    x1 = []
    x2 = []
    cor = np.zeros(((data_points - 1), (data_points - 1)))
    y = np.zeros((data_points - 1))
    r_newpnt = np.zeros((data_points - 1))
    for idx1, i in enumerate(lhd):
        x1.append(i[0])
        x2.append(i[1])
        X_i = [x1[-1], x2[-1]]
        y[idx1] = Branin(X_i[0], X_i[1])
        a_new, b_new = objectiveFunction(new_point, X_i, 2, theta_vals, 2)
        r_newpnt[idx1] = correlation(a_new)
        # dif = np.zeros((data_points - 1))
        # objFunc = np.zeros((data_points - 1))
        for idx2, j in enumerate(lhd):
            X_j = [j[0], j[1]]
            a, b = objectiveFunction(X_i, X_j, 2, theta_vals, 2)
            # dif[idx2] = b
            # objFunc[idx2] = a
            cor[idx1, idx2] = correlation(a)
    # print()
    # cor = cor + np.eye(data_points-1)+ np.eye(data_points-1)*0.000001
    cor_inv = np.linalg.inv(cor)

    mu_bar = (np.matmul(np.transpose(one_bar), np.matmul(cor_inv, y))) / (
              np.matmul(np.transpose(one_bar), np.matmul(cor_inv, one_bar)))

    predictor = mu_bar+np.matmul(np.transpose(r_newpnt),np.matmul(cor_inv,(y-one_bar*mu_bar)))
    new_y.append(predictor)
    sig_2 = (np.matmul(np.transpose(y - (one_bar * mu_bar)), np.matmul(cor_inv,
                                   (y - (one_bar * mu_bar))))) / (
        (data_points - 1))
    t1 = np.matmul(np.transpose(r_newpnt),np.matmul(cor_inv,r_newpnt))
    t2_num = (1.0-np.matmul(np.transpose(one_bar),np.matmul(cor_inv,r_newpnt)))**2
    t2_den = np.matmul(np.transpose(one_bar),np.matmul(cor_inv,one_bar))
    mean_sqr_err = sig_2*(1.0-t1+(t2_num/t2_den))

    print("Predictor: {}".format(predictor))
    print("Mean squared error of uncertainity: {}".format(mean_sqr_err))
    print("Regression RMSE: {}".format(np.sqrt(sig_2)))
    print("RMSE (0 < RMSE < Regres RMSE: {}".format(np.sqrt(abs(mean_sqr_err))))

x_vals = [i[0] for i in lhd_new]
y_vals = [i[1] for i in lhd_new]
plottingSurface(1,x_vals,y_vals,new_y)

#
# y_bar = mu_bar + np.matmul(np.matmul(np.transpose(np.array(r_newpnt)), cor_inv), np.transpose(y - (one_bar * mu_bar)))
# print("y predictor: {}".format(y_bar))
#
# sqr_error = sig_2*(1.0 - np.matmul(np.matmul(np.transpose(r_newpnt), cor_inv), r_newpnt) + (
#             1.0 - np.matmul(np.matmul(np.transpose(one_bar), cor_inv), r_newpnt) ** 2) / (
#                       np.matmul(np.matmul(np.transpose(one_bar), cor_inv), r_newpnt)))
# print("Mean square error of predictor: {}".format(sqr_error))

########################################################
# Plotting of Branin function with initial sampled points for visualization purposes
# x1 = np.linspace(-5.0, 10.0, 10)
# x2 = np.linspace(0.0, 15.0, 10)
# X, Y = np.meshgrid(x1, x2)
# Z = Branin(X, Y)
#
# data = []
# for i in range(len(x1)):
#     for j in range(len(x2)):
#         data.append([x1[i], x2[j], Z[i][j]])
#
# fig = plt.figure(1)
# ax = fig.gca(projection='3d')
# ax.contour(X, Y, Z, 40)
# ax.scatter(x1, x2, y)
# plt.show()
# ########################################################
#

# y.sort()
# y1.sort()
# d.sort()
# d1.sort()
# cor = [correlation(i) for i in y]
# cor2 = [correlation(i) for i in y1]

# fig = plt.figure(2)
# ax = fig.gca()
# ax.plot(d,cor)
# ax.plot(d1,cor2)
# plt.show()

# ax.scatter(x1,x2)
# Z = Branin(X,Y)
# fx = []
# for y in lhd:
#     y1 = y[0]*(10.0+5.0)-5.0
#     y2 = y[1]*(15.0-0.0)-0.0
#     print(x1[-1],y2)
#     fx.append(Branin(x1[-1],y2))
# braninFunction.append(fx)

# ax.contour(np.array(x1),np.array(x2),Z)
# ax.contour(np.array(x1),np.array(x2),Z)
# ax.contour(np.array(x1),np.array(x2),Z, zdir='z', offset=0)
# ax.contour(np.array(x1),np.array(x2),Z, zdir='x', offset=-5, cmap=cm.coolwarm)
# ax.contour(np.array(x1),np.array(x2),Z, zdir='y', offset=-15, cmap=cm.coolwarm)
# # X, Y = np.meshgrid(x1,x2)
# # Z = np.array(braninFunction)
# ax.plot_surface(x1, x2, Z, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)
# def latinHyperCube(n, k, population, iterations):
#     """
#     Generates optimized LH optimizing Morris Mitchel criterion for a range of exponents and plots frist 2 dimeniosn of current hypercube
#
#     :param n: number of data points required
#     :param k: number of design variables/ parameters
#     :param population: number of inidividuals in evolutionary oper
#     :param iterations:
#     :return:
#     """
#
#     return x
# plt.figure()
# plt.plot(x_exp,y_exp,x_num,y_num)
# plt.show()
# plt.plot(x_num,y_num)
