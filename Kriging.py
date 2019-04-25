"""
Kriging meta-models
"""
# import matplotlib.pyplot as plt
import numpy as np
import sys
import numpy.matlib
import scipy
from pyDOE import lhs
from math import pi, erf, cos
import copy
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# Import experimental data
def loaddisplacementData(Filename):
    global cwd
    with open(cwd + Filename, 'r') as file:
        data = file.readlines()

    displacement = []
    load = []
    for line in data:
        dataline = [float(i) for i in line.strip().split(',')]
        load.append(dataline[0])
        displacement.append(dataline[-1])

    return displacement, load

def Branin(x,y):
    """
    Branin function: function: a(x2 - b*x1² + c*x1 - r)² + s(1-t)cos(x1) + s
    :param x: dim 1
    :param y: dim 2
    :return: evaluated function
    """
    a = 1.0
    b = 5.1 / (4 * pi ** 2)
    c = 5.0 / pi
    r = 6.0
    s = 10.0
    t = 1.0 / (8.0 * pi)
    # Original
    return  a * (y - b * x ** 2 + c * x - r) ** 2 + s * (1.0 - t) * np.cos(x) + s

def modBranin(x,y):
    """
    Branin function: function: a(x2 - b*x1² + c*x1 - r)² + s(1-t)cos(x1) + s
    :param x: dim 1
    :param y: dim 2
    :return: evaluated function
    """
    a = 1.0
    b = 5.1 / (4 * pi ** 2)
    c = 5.0 / pi
    r = 6.0
    s = 10.0
    t = 1.0 / (8.0 * pi)
    # Original
    return  a * (y - b * x + c * x - r) ** 2 + s * ((1.0 - t) * np.cos(x)+1) + s*x

def objectiveFunction(x1, x2):
    """
    objective Function

    :param x1: dimension 1
    :param x2: dimension 2
    """
    global xy_data
    global exp_xy_data

    # Original Branin function
    # f = Branin(x1,x2)

    # Modified Branin
    # f = modBranin(x1,x2)

    #Quadratic test example:
    # f = (2.0 - x1) * (0.1 - x2 - 0.1 * x1) + 0.3

    # Damage parameter aclibation objective function
    # First entry is the experimental load (y) and diaplcement value (x)
    y_num = xy_data[x1][1]
    x_num = xy_data[x1][0]
    l_exp = exp_xy_data[x1][1]

    # num, den = 0, 0
    # for i in range(1,len(y_num)):
    #     num = num + ((l_exp[i] - y_num[i])**2)*(x_num[i]-x_num[i-1])
    #     den = den + (l_exp[i]**2)*(x_num[i]-x_num[i-1])
    # f = num/den

    num, den1, den2 = 0, 0, 0
    for i in range(1, len(y_num)):
        num = num + ((l_exp[i] - y_num[i]) ** 2) * (x_num[i] - x_num[i - 1])
        den1 = den1 + (l_exp[i] ** 2) * (x_num[i] - x_num[i - 1])
        den2 = den2 + (y_num[i] ** 2) * (x_num[i] - x_num[i - 1])
    f = np.sqrt(num / min([den1, den2]))


    return f

def weightedDistance(x_i, x_j, parms, theta, p):
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
        random_value = np.random.uniform(-.075,0.075,1)
        random_parm = np.random.randint(0,offspring_crossover.shape[1],1)
        offspring_crossover[idx,random_parm] = offspring_crossover[idx, random_parm] + random_value # mutation added to last, could be any index

    return offspring_crossover

def likelihood(x_data, theta, p=1):
    global data_points
    x1 = []
    x2 = []
    cor = np.zeros(((data_points), (data_points)))
    y = np.zeros((data_points))
    one_bar = np.array([1] * (len(x_data)))
    for idx,i in enumerate(theta):
        theta[idx] = 10**i

    for idx1, i in enumerate(x_data):
        x1.append(i[0])
        x2.append(i[1])
        X_i = [x1[-1], x2[-1]]
        y[idx1] = objectiveFunction(X_i[0], X_i[1])
        dif = np.zeros((data_points))
        objFunc = np.zeros((data_points))
        for idx2, j in enumerate(x_data):
            X_j = [j[0], j[1]]
            a, b = weightedDistance(i, j, len(theta), theta, p)
            dif[idx2] = b
            objFunc[idx2] = a
            cor[idx1, idx2] = correlation(a)
    # print()
    cor = cor + np.eye(data_points)+ np.eye(data_points)*0.000001
    cor_inv = np.linalg.inv(cor)

    mu_bar = (np.matmul(np.transpose(one_bar), np.matmul(cor_inv, y))) / (
              np.matmul(np.transpose(one_bar), np.matmul(cor_inv, one_bar)))
    sig_2 = (np.matmul(np.transpose(y - (one_bar * mu_bar)), np.matmul(cor_inv,
                                   (y - (one_bar * mu_bar))))) / (
        (data_points))
    # print("Condition number: {}".format(np.linalg.cond(cor)))
    if np.linalg.det(cor) <= 0:
        print("***** Ill conditioned matrix!")
        likelihood = 10000
    else:
        lnDetCor = 2*np.sum(np.log(abs(np.diag(cor))))
        likelihood = -1 * (-((data_points) / 2.0) * np.log((sig_2)) - (1.0 / 2.0) * lnDetCor)


    return cor, mu_bar, sig_2, likelihood

def f(param_set):
    global  lhd
    # for i in param_set:
    cor,mu,sig,lnLikeli = likelihood(lhd,param_set)


    return lnLikeli

def GA(parms,parms_range, individuals=200, num_gen=500):
    print("Running genetic algorithm")
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
    fx_old = []
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
            # test.append(abs(np.mean(fx[:, i]) - fx[0, i]) < 10e-5)
            test.append(abs(np.mean(fx[:, i]) - fx[-1, i]) < 10e-4)
        if all(test):
            # if abs(min(fx_old[-1,:])-min(fx[-1,:]))<10e-9:
            # print("Mean function value {}".format(np.mean(fx_old[-1, :])))
            # print("Minimzation function value : {:.5f}".format(fx_old[-1, -1]))
            # print("Best parameters in current population: {}".format([10 ** (e) for e in fx_old[-1, :-1]]))
            # print("After {} generations".format(k + 1))
            break
        fx_mean.append(np.mean(fx[:, :-1], axis=0))
        fx_min.append(fx[-1, :])

    # if k + 1 == num_gen:
        # print("Mean function value {}".format(np.mean(fx_old[-1, :])))
        # print("Minimzation function value : {:.5f}".format(fx_old[-1, -1]))
        # print("Best parameters in current population: {}".format([10 ** (e) for e in fx_old[-1, :-1]]))
        # print("After {} generations".format(k + 1))
    # if k+1 == num_gen:
    #     print("Maximum number of generations created ({} generations)".format(num_gen))
    return fx_old, k

def y_Predictor(new_lhd,old_lhd,theta):
    new_y = []
    mu_bar = []
    predictor = []
    sig_2 = []
    mean_sqr_err = []
    cor_all = []
    r = []
    one_bar = np.array([1] * len(old_lhd))
    for new_point in new_lhd:
        # x1 = []
        # x2 = []
        cor = np.zeros(((data_points), (data_points)))
        y = np.zeros((data_points))
        r_newpnt = np.zeros((data_points ))
        for idx1, i in enumerate(old_lhd):
            # x1.append(i[0])
            # x2.append(i[1])
            X_i = [i[0], i[1]]
            y[idx1] = objectiveFunction(X_i[0], X_i[1])
            a_new, b_new = weightedDistance(new_point, i, len(theta), theta, p =1)
            r_newpnt[idx1] = correlation(a_new)
            # dif = np.zeros((data_points))
            # objFunc = np.zeros((data_points ))
            for idx2, j in enumerate(old_lhd):
                X_j = [j[0], j[1]]
                a, b = weightedDistance(i, j, len(theta), theta, p=1)
                # dif[idx2] = b
                # objFunc[idx2] = a
                cor[idx1, idx2] = correlation(a)
        # print()
        # cor = cor + np.eye(data_points)+ np.eye(data_points)*0.000001
        r.append(r_newpnt)
        cor_all.append(cor)
        cor_inv = np.linalg.inv(cor)

        mu_bar.append((np.matmul(np.transpose(one_bar), np.matmul(cor_inv, y))) / (
            np.matmul(np.transpose(one_bar), np.matmul(cor_inv, one_bar))))

        predictor = mu_bar[-1] + np.matmul(np.transpose(r_newpnt), np.matmul(cor_inv, (y - one_bar * mu_bar[-1])))
        new_y.append(predictor)
        sig_2.append((np.matmul(np.transpose(y - (one_bar * mu_bar[-1])), np.matmul(cor_inv,
                                                                           (y - (one_bar * mu_bar[-1]))))) / (
                    (data_points )))
        t1 = np.matmul(np.transpose(r_newpnt), np.matmul(cor_inv, r_newpnt))
        t2_num = (1.0 - np.matmul(np.transpose(one_bar), np.matmul(cor_inv, r_newpnt))) ** 2
        t2_den = np.matmul(np.transpose(one_bar), np.matmul(cor_inv, one_bar))
        mean_sqr_err.append(sig_2[-1] * (1.0 - t1 + (t2_num / t2_den)))
    new_y = np.array(new_y)
    return new_y, mu_bar, sig_2, mean_sqr_err, cor_all, r

def expectedImprovement(lhd_new, lhd_old, f_min, theta, B_out=0):

    B = y_Predictor([lhd_new], lhd_old, theta)  # A = [new_y [0], mu_bar [1], sig_2 [2], mean_sqr_err [3], cor_all [4], r [5]]
    new_predictor = B[0][0]
    s_2 = B[3][0]
    s = np.sqrt(abs(s_2))

    # EGO
    # Using CMA-ES (lambda and mu ES) want to maximize te hexpected improvement of a point

    CDF = 0.5 + 0.5 * erf((f_min - new_predictor) / (s * np.sqrt(2.0)))
    PDF = 1.0 / (np.sqrt(2.0 * pi)) * np.exp(-((f_min - new_predictor) ** 2) / (2.0 * s_2))

    EI = (f_min - new_predictor) * CDF + s * PDF
    if B_out:
        return EI, B
    else:
        return EI

def plottingSurface(figure_num,x_vals,y_vals,z_vals):
    global ranges
    x_1_range = ranges[0]
    x_2_range =ranges[1]
    x = np.linspace(x_1_range [0], x_1_range [1], 20)
    y = np.linspace(x_2_range[0], x_2_range[1], 20)
    X, Y = np.meshgrid(x, y)
    Z = objectiveFunction(X, Y)
    fig = plt.figure(figure_num)
    ax = fig.gca()
    ax.contour(X, Y, Z, 100)
    ax.scatter(x_vals,y_vals,color='r')

    fig = plt.figure(figure_num+10)
    ax = fig.gca(projection='3d')
    ax.contour(X, Y, Z, 100)
    ax.scatter(x_vals, y_vals,z_vals, color='r')

def frosenbrock(x):
    f = 0
    for i in range(int(len(x)-1)):
        f += 100*(x[(i+1)] - x[i]**2)**2 + (1.0-x[i])**2
    return f

def fsphere(x):
    f = 0
    for i in x:
        f += i**2
    return f

def CMA_ES(n,xstart,y_min):
    print("Running CMA_ES algorithm")
    global lhd
    global theta_vals
    global ranges
    # x_fes = []
    # for x in ranges:
    #     x_fes.append(x[0]+ (x[-1]-x[0])/2.0)
    # x_fes = np.array(x_fes)
    flag = 0

    # n = design_parms # number of design variables
    # n = 2  # number of design variables
    stopfitness = 1e-8
    # xmean = xstart # initial value of design variables
    xmean = np.random.rand(n)
    for count,x in enumerate(ranges):
        xmean[count] = xmean[count]*(x[-1]-x[0])+x[0]
    # CMA_sig = 0.5 # associated RMSE
    # xmean = lhd_new  # initial value of design variables
    CMA_sig = 0.5

    # Parameter setting
    # Selection and recombination parameters:
    lam = int(4.0 + np.floor(3.0 * np.log(n)))
    mu = lam / 2.0
    w = [np.log(mu + 1.0 / 2.0) - np.log(i + 1) for i in range(int(mu))]
    mu = np.floor(mu)
    w = np.array([x / sum(w) for x in w])
    mu_eff = sum((i) ** 2 for i in w) ** (-1)

    # Step size control parameters:
    c_sig = (mu_eff + 2.0) / (n + mu_eff + 5.0)
    d_sig = 1.0 + 2.0 * max(0.0, np.sqrt(
        (mu_eff - 1.0) / (n + 1.0)) - 1.0) + c_sig  # 1 + 2*max(0, sqrt((mueff-1)/(N+1))-1) + cs

    # Covariance matrix adaptation parameters:
    c_c = (4.0 + mu_eff / n) / (n + 4.0 + 2.0 * mu_eff / n)
    c_1 = 2.0 / ((n + 13.0 / 10.0) ** 2 + mu_eff)
    c_mu = min(1 - c_1, 2 * ((mu_eff - 2.0 + 1.0 / mu_eff) / ((n + 2) ** 2 + 2.0 * mu_eff / 2.0)))

    E_norm = np.sqrt(n) * (1.0 - 1.0 / (4 * n) + 1.0 / (21 * (n ** 2)))  # Expectation of || N(0,I) ||

    # Initialization
    p_c = np.zeros(n)
    p_sig = np.zeros(n)
    B = np.eye(n)
    D = np.ones(n)
    C_mat = np.matmul(B, np.matmul(np.diag(D ** 2), np.transpose(B)))
    invsqrtC = np.matmul(B, np.matmul(np.diag(D ** (-1)), np.transpose(B)))
    eigenval = 0

    z_i = np.zeros((n, lam))
    x_i = np.zeros((n, lam))
    EI = np.zeros(lam)

    gen_num = 250
    outx = []
    out = []
    xmin = 0.0
    ranges = np.array(ranges)
    for g in range(gen_num):

        # generate and evaluate lambda offspring
        alpha = 1e-04
        for i in range(lam):
            z_i[:, i] = np.random.multivariate_normal(np.zeros(n), np.eye(n))
            x_i_tmp = np.matmul(B, np.matmul(np.diag(D), z_i[:, i]))
            x_i[:, i] = xmean + CMA_sig * x_i_tmp  # Mutation to offspring
            x_og = x_i[:,i]
            for k in range(x_i.shape[0]):
                if x_i[k,i]>ranges[k,-1]:
                    x_i[k,i]=ranges[k,-1]
                if x_i[k,i]<ranges[k,0]:
                    x_i[k,i]=ranges[k,0]

            # EI[i]= objectiveFunction(x_i[:,i][0],x_i[:,i][1])-0.397887
            # EI[i]= fsphere(x_i[:,i])
            # EI[i]= frosenbrock(x_i[:,i])
            EI[i] = -1 * expectedImprovement(x_i[:, i], lhd, y_min,
                                             theta_vals)  + alpha*np.linalg.norm(x_og-x_i[:,i])**2 # Evaluation of fitness function for offspring i
            # EI[i], values = -1 * expectedImprovement(x_i[:, i], lhd, y_min,
            #                                  theta_vals, B_out=1)  # Evaluation of fitness function for offspring i
        # # Application of constraints on bounds
        # for check in range(lam):
        #     f_max = max(EI)
        #     EI[check] = f_max + np.linalg.norm(x_i[:, check]- x_fes)

        # Sort by fitness
        idx = sorted(range(len(EI)), key=EI.__getitem__)
        EI = sorted(EI)

        x_old = xmean
        xmean = np.matmul(x_i[:, idx[0:int(mu)]], w)  # Recombination
        zmean = np.matmul(z_i[:, idx[0:int(mu)]], w)

        # Cumulation: update evolution paths
        p_sig = (1.0 - c_sig) * p_sig + np.sqrt(c_sig * (2.0 - c_sig) * mu_eff) * np.matmul(invsqrtC,
                                                                                            (xmean - x_old) / CMA_sig)
        h_check = (sum(p_sig ** 2.0) / (1.0 - (1.0 - c_sig) ** (2 * (g + 1)))) / n < (2.0 + 4.0 / (n + 1.0))
        if h_check:
            h_sig = 1.0
        else:
            h_sig = 0.0
        p_c = (1.0 - c_c) * p_c + h_sig * np.sqrt(c_c * (2.0 - c_c) * mu_eff) * ((xmean - x_old) / CMA_sig)

        t_end = (x_i[:, idx[0:int(mu)]] - np.transpose(np.array([x_old[0:int(mu)]] * int(mu)))) / CMA_sig
        C_mat = (1.0 - c_1 - c_mu) * C_mat + \
                c_1 * (np.matmul(np.ndarray(shape=(n, 1), buffer=p_c),
                                 np.transpose(np.ndarray(shape=(n, 1), buffer=p_c))) + (1.0 - h_sig) * c_c * (
                                   2.0 - c_c) * C_mat) + \
                c_mu * np.matmul(t_end, np.matmul(np.diag(w), np.transpose(t_end)))

        # Step-size adaptation (sigma)
        CMA_sig = CMA_sig * np.exp((c_sig / d_sig) * ((np.linalg.norm(p_sig)) / (E_norm) - 1.0))
        if ((g + 1) * lam) - eigenval > lam / (c_1 + c_mu) / n / 10:
            eigenval = (g + 1) * lam
            C_mat = np.triu(C_mat) + np.transpose(np.triu(C_mat, 1))
            invsqrtC = np.matmul(B, np.matmul(np.diag(D ** (-1)), np.transpose(B)))
            D, B = np.linalg.eig(C_mat)
            D = np.sqrt(D)

        # Break if fitness is good enough
        if g > 10:
            if abs(EI[0] - out[-1][0]) <= stopfitness:
                if abs(outx[-1] - xmean)[0] <= stopfitness * 100 and abs(outx[-1] - xmean)[1] <= stopfitness * 100:
                    xmin = x_i[:, idx[0]]
                    outx.append(xmean)
                    out.append([EI[0], CMA_sig])
                    break

        # Break if fitness is good enough
        if max(D) > 1e7 * min(D):
            xmin = x_i[:, idx[0]]
            outx.append(xmean)
            out.append([EI[0], CMA_sig])
            print('Ill-conditioned D matrix :(')
            flag = 1
            break

        if abs(EI[0]) == EI[int(np.ceil(0.7 * lam))]:
            CMA_sig = CMA_sig * np.exp(0.2 + c_sig * d_sig)
            print("Warning: Flat fitness, consider reformulating the objective")
        if not (g + 1) % 100:
            print('{}: EI: {:.5f}, parameters: {}'.format(g + 1, EI[0], x_i[:, idx[0]]))

        xmin = x_i[:, idx[0]]
        outx.append(xmean)
        out.append([EI[0], CMA_sig])

    return xmin, outx, out, flag

####################################################################
####################################################################

# 'Design of Experiment (DOE)', selecting smapling points (i.e picking random parameters)

design_parms = 3
# design_parms = 2
# ranges = [[-5.0,10.0],[0,15.0]]
# ranges = [[0.1,1.5],[0.25,0.9]]
ranges = [[0.5, 3.0], [0.1,1.5], [0.25,0.9]]
# ranges = [[0.5, 3.0], [0.25,0.9]]
if len(ranges)< design_parms:
    sys.exit("*****ERROR: Not enough range values given for the design parameters to be determined!")
# x_1_range = ranges[0]
# x_2_range = ranges[1]
#
### RANDOM lHD DATA
# data_points = 20
# lhd = lhs(design_parms, data_points+1, 'Maximin') # sampling data
# for count, i in enumerate(lhd):
#     val_tmp = []
#     for j in range(design_parms):
#         val_tmp.append(i[j]*(ranges[j][1] - ranges[j][0])+ranges[j][0])
#     lhd[count] = val_tmp
# lhd_full = copy.copy(lhd)
# validationPoint = lhd[0]
# lhd = lhd[1:] # removing one value to allow for cross model validation
########################################################################

## DOE LHD Data
lhd = []
cwd = '/home/cerecam/Desktop/Crack_Models/'
xy_data = {}
exp_xy_data = {}
with open(cwd + 'Parameters3.txt','r') as pfile:
    used_test = list(range(1,22))
    count = 0
    for line in pfile:
        count +=1
        if count in used_test:
            newline = [float(i.strip()) for i in line.split(',')]
            lhd.append(newline)
            x,y = loaddisplacementData('CalibrationData_P3' + str(count) + '.txt')
            xy_data[newline[0]] = [x,y]
            exp_x, exp_y = loaddisplacementData('ExpData_P3' + str(count) + '.txt')
            exp_xy_data[newline[0]] = [exp_x,exp_y]
        else:
            pass
y_orig = []

lhd_full = copy.deepcopy(lhd)
validationPoint = lhd.pop(11)
y_validationpoint = objectiveFunction(validationPoint[0],validationPoint[1])
for x in lhd:
    y_orig.append(objectiveFunction(x[0],x[1]))

data_points = len(used_test)-1
#################################################################################

add_points = 0
max_EI = False
CMA_again = 0
curr_EI = 1
# while abs(curr_EI)>0.01:

    ####################################################################
    ####################################################################
    # Calibration of initial Kriging model for parameter theta, assuming p = 2 (exponent in weighted residual)
    # theta value refers to ln of this number so theta 2 is actually a value of 10^2, approximated range betweeen 10^-3 and 10^2

range_parms = [[-3,2]]*design_parms
num_individ=20
generations=100
iterations = 2
if not CMA_again:
    theta_tmp = []
    for iter in range(iterations):
        Results = GA(design_parms,range_parms, num_individ, generations)
        values = Results[0][-1, :]
        theta_tmp.append(np.array([10**i for i in values[:-1]]))
        # theta_vals = theta_tmp[-1]
        print("Genetic algorithm converged after {} generations".format(Results[-1]+1))
        print("Theta values for iteration {}: {}".format(iter+1, theta_tmp[iter]))
    theta_vals = np.mean(theta_tmp,axis=0)
    print("Best theta values for Kriging model in current population with ({} datapoints): {}".format(data_points,theta_vals))

    # Get predictor values of the meta model with calibrated theta parameters at our known points
    k_data = y_Predictor(lhd,lhd,theta_vals)
    f_vals = k_data[0]
    f_min = min(f_vals)
    # if add_points == 0:
    #     x_vals = [i[0] for i in lhd]
    #     y_vals = [i[1] for i in lhd]
        # plottingSurface(1, x_vals, y_vals, f_vals)
CMA_again = 0
####################################################################
####################################################################
# Kriging model validation (cross validation)
crossVal_data = y_Predictor([validationPoint], lhd, theta_vals)
crossVal_y = crossVal_data[0]
crossVal_rmse = crossVal_data[3]
crossVal_Residual = 0

CI = (objectiveFunction(validationPoint[0],validationPoint[1])-crossVal_y) / np.sqrt(crossVal_rmse)
print(CI)
if abs(CI[0])>3.0:
    print("Model Invalid!")
curr_EI = 0.0
"""
####################################################################
####################################################################
# Kringing prediction

# lhd_new = lhs(2, 3,'Maximin')
# # lhd_new = lhd
#
# for count, i in enumerate(lhd_new):
#     lhd_new[count] = [i[0] * (x_1_range[1] - x_1_range[0]) + x_1_range[0],i[1] * (x_2_range[1] - x_2_range[0]) + x_2_range[0]]
#
# A = y_Predictor(lhd_new,lhd, theta_vals) # A = [new_y [0], mu_bar [1], sig_2 [2], mean_sqr_err [3], cor_all [4], r [5]]
#
# print("Regression RMSE: {}".format(np.sqrt(A[2][-1])))
# for i in range(len(A[0])):
#     y_bar, mu, sig_2, mean_sqr_err = A[0][i], A[1][i], A[2][i], A[3][i]
#     print("RMSE (0 < RMSE < Regres RMSE: {}".format(np.sqrt(abs(mean_sqr_err))))
#     if np.sqrt(abs(mean_sqr_err)) > np.sqrt(sig_2):
#         print("***** Bad prediction: RMSE> regression RMSE!")
#         print("Predictor: {}".format(y_bar))
#         print("Mean squared error of uncertainity: {}".format(mean_sqr_err))
#
# x_vals = [i[0] for i in lhd_new]
# y_vals = [i[1] for i in lhd_new]
# plottingSurface(1,x_vals,y_vals,A[0])

####################################################################
####################################################################
# Kriging model update

lhd_new = lhs(design_parms, 1)
for count, i in enumerate(lhd_new):
    val_tmp = []
    for j in range(design_parms):
        val_tmp.append(i[j]*(ranges[j][1] - ranges[j][0])+ranges[j][0])
    lhd_new[count] = val_tmp
lhd_new = lhd_new[0]

new_pnt = y_Predictor([lhd_new],lhd, theta_vals)

x_1 = [i[0] for i in lhd]
x_2 = [i[1] for i in lhd]
# # x_3 = [i[2] for i in lhd]
# X1, X2 = np.meshgrid(x_1,x_2)
# lhd_2para = [i for i in lhd]
# z = np.array([[0.0]*len(x_1)]*len(x_2))
# y_vals = []
# for i in lhd:

# for idx1,i in enumerate(x_1):
#     for idx2,j in enumerate(x_2):
#         new_data = y_Predictor([[i,j]],lhd_2para,theta_vals)
#         z[idx2,idx1] = new_data[0]
# fig = plt.figure(2)
# ax = fig.gca()
# # ax.contourf(X1, X2, z)
# ax.scatter(x_1,x_2,f_vals, color='r')
# # ax.imshow(z)
# plt.show()

print('New point created at {}'.format(lhd_new))

para_vals, out1, out2, flag = CMA_ES(design_parms,lhd_new,f_min)

if flag:
    plt.show()
    # break
outx = np.array(out1)
out = np.array(out2)
print('Generation: {}, EI of {:.5f}, new point: {}'.format(len(outx), out[-1,0], para_vals))
curr_EI = out[-1,0]

range_check = True
for c,k in enumerate(para_vals):
    if range_check:
        if (k<ranges[c][0]) or (k>ranges[c][-1]):
            range_check=False
            print(k)
            print((k<ranges[c][0]))
            print((k>ranges[c][-1]))
            break
    else:
        break

if not range_check:
    print("EI point {} out of range, running CMA_ES again".format(para_vals))
    CMA_again = 1

else:
    add_points += 1

    EI_pnt = y_Predictor([para_vals],lhd, theta_vals)
    print('f_value at new point: {}'.format(EI_pnt[0]))
    fig = plt.figure(1)
    ax = fig.gca()
    # ax.scatter(para_vals[0],para_vals[1],EI_pnt[0],color='b', marker='s')
    ax.scatter(para_vals[0],para_vals[1],color='b', marker='s')
    plt.show()


    fig = plt.figure(1+10)
    ax = fig.gca()
    ax.scatter(para_vals[0],para_vals[1],EI_pnt[0],color='b', marker='s')
    # ax.scatter(para_vals[0],para_vals[1],color='b', marker='s')
    plt.show()

    if abs(out[-1, 0]) <= 0.01:
        max_EI = True
        print("Maximum expected improvment less than 1%, metal model fully developed")
        print("{} additional points were created".format(add_points))
        # break

    lhd = np.concatenate((lhd,[para_vals]))
    data_points += 1

    ##
    # Run new tensile test simulation using props of new lhd point
    ##


if not max_EI:
    print("{} additional points were created".format(add_points))

final_vals = []
k_data = y_Predictor(lhd,lhd,theta_vals)
f_vals = k_data[0]
f_min = min(f_vals)

# fig = plt.figure(3)
# ax = fig.gca()
# for i in range(outx.shape[1]):
#     plt.plot(list(range(len(outx[:,i]))), outx[:,i])
# plt.xlabel('iterations')
# plt.grid()
# plt.show()
#
# fig = plt.figure(4)
# ax = fig.gca()
# plt.semilogy(list(range(len(out[:,0]))), abs(out[:,0]), label = 'fitness')
# plt.semilogy(list(range(len(out[:,0]))), out[:,0]-out[-1,0], label = 'difference fitness')
# plt.semilogy(list(range(len(out[:,1]))), abs(out[:,1]), label = 'sigma')
# plt.xlabel('iterations')
# plt.legend(loc='best')
# plt.grid()
# plt.show()
"""