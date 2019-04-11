"""
Kriging meta-models
"""
# import matplotlib.pyplot as plt
import numpy as np
from pyDOE import lhs
from math import pi, cos
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

def likelihood(x):
    global x_exp
    global y_exp

    x = [1]

    theta = [10 ** i for i in x]
    n = len(x_exp)
    one = [1] * n
    PSI = [[0] * n] * n
    eps = np.spacing(1) * 100
    x_exp = [x_exp]
    y_exp = [y_exp]

    for i in range(n):
        for j in range(n):
            for k in range(len(theta)):
                PSI[i][j] = PSI[i][j] + np.exp(-theta[k] * (x_exp[k][i] - x_exp[k][j]) ** 2)

    # for i in range(n):
    #     PSI = np.matrix(PSI) + np.transpose(np.matrix(PSI))
    try:
        [U, p] = np.linalg.cholesky(PSI)
        LnDetPsi = 2 * np.sum(np.log(abs(np.diag(U))))
        mu = (np.matmul(np.transpose(one), np.matmul(np.invert(np.matrix(PSI)), np.array(y_exp))))
        var = np.matmul(np.transpose(np.array(y_exp[0]) - np.matmul(one, mu)),
                        np.matmul((np.invert(np.matrix(PSI)), np.array(y_exp[0]) - np.matmul(one, mu)))) / float(n)
        NegLnLike = -1 * (-n / 2.0) * np.log(var) - 0.5 * LnDetPsi

    except:
        NegLnLike = 1e4

    return NegLnLike, PSI, U


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

    f = a * (x2 - b * x1 ** 2 + c * x1 - r) ** 2 + s * (1.0 - t) * np.cos(x1) + s
    return f


def objectiveFunction(x_i, x_j, parms, theta, p):
    d = 0
    y = 0
    for i in range(parms):
        d = d + theta * abs(x_i[i] - x_j[i]) ** p
        y = y + abs(x_i[i] - x_j[i])
    return d, y


def correlation(d):
    return np.exp(-d)

lhd = lhs(2, 21, 'Maximin') # sampling data
lhd_full = lhd
lhd = lhd[1:] # removing one value to allow for cross model validation
x1 = []
x2 = []
y = []
y1 = []
d, d1 = [], []
cor, cor1 = [], []
one_bar = np.array([1] * len(lhd))
ranges = [[-5.0,10.0],[0,10.0]]
x_1_range = ranges[0]
x_2_range = ranges[1]

# Creation of initial Kriging model
for i in lhd:
    x1.append(i[0] * (x_1_range[1] - x_1_range[0]) + x_1_range[0])
    x2.append(i[1] * (x_2_range[1] - x_2_range[0]) + x_2_range[0])
    y.append(Branin(x1[-1], x2[-1]))
    cor_tmp = []
    for j in lhd:
        a, b = objectiveFunction([x1[-1], x2[-1]], j[:2], 2, 0.01, 2)
        cor_tmp.append(correlation(a))
    cor.append(cor_tmp)

cor = np.array(cor)
cor_inv = np.linalg.inv(cor)
y = np.array(y)
mu_bar = (np.matmul(np.matmul(np.transpose(one_bar), cor_inv), y)) / (
    np.matmul(np.matmul(np.transpose(one_bar), cor_inv), one_bar))
sig_2 = (np.matmul(np.matmul(np.transpose(y - (one_bar * mu_bar)), cor_inv),
                   np.transpose(y - (one_bar * mu_bar)))) / len(lhd)

max_likelihood = -mu_bar/2.0*np.
print("mu_bar: {}".format(mu_bar))
print("s_2: {}".format(sig_2))

########################################################
# Plotting of Branin function with initial sampled points for visualization purposes
x1 = np.linspace(-5.0, 10.0, 10)
x2 = np.linspace(0.0, 15.0, 10)
X, Y = np.meshgrid(x1, x2)
Z = Branin(X, Y)

data = []
for i in range(len(x1)):
    for j in range(len(x2)):
        data.append([x1[i], x2[j], Z[i][j]])

fig = plt.figure(1)
ax = fig.gca(projection='3d')
ax.contour(X, Y, Z, 40)
ax.scatter(x1, x2, y)
plt.show()
########################################################

# Kringing prediction
new_point = lhd_full[0]
r_newpnt = []
for i in range(len(lhd)):
    a_new, b_new = objectiveFunction(new_point, [x1[i], x2[i]], 2, 0.01, 2)
    r_newpnt.append(correlation(a_new))

y_bar = mu_bar + np.matmul(np.matmul(np.transpose(np.array(r_newpnt)), cor_inv), np.transpose(y - (one_bar * mu_bar)))
print("y predictor: {}".format(y_bar))

sqr_error = sig_2*(1.0 - np.matmul(np.matmul(np.transpose(r_newpnt), cor_inv), r_newpnt) + (
            1.0 - np.matmul(np.matmul(np.transpose(one_bar), cor_inv), r_newpnt) ** 2) / (
                      np.matmul(np.matmul(np.transpose(one_bar), cor_inv), r_newpnt)))
print("Mean square error of predictor: {}".format(sqr_error))
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
