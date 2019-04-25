import os
import matplotlib.pyplot as plt
import copy
import numpy as np


cwd = '/home/cerecam/Desktop/Crack_Models/'
# filenames = ['TensileTests_a','TensileTests_b','TensileTests_c','TensileTests_d','TensileTests_e','TensileTests_f']
# filenames = ['TensileTests_d','TensileTests_e','TensileTests_f']
# filenames = ['TensileTests_a','TensileTests_b','TensileTests_c']
# filenames = ['Tensile']
# filenames = ['TensileTests_new_P312', 'TensileTests_new_P322']
filenames = ['TensileTests_new_P31', 'TensileTests_new_P322', 'TensileTests_new_P33', 'TensileTests_new_P34', 'TensileTests_new_P35',
             'TensileTests_new_P36', 'TensileTests_new_P37', 'TensileTests_new_P38', 'TensileTests_new_P39', 'TensileTests_new_P310',
             # 'TensileTests_new_P311', 'TensileTests_new_P312', 'TensileTests_new_P314', 'TensileTests_new_P315',
             'TensileTests_new_P311', 'TensileTests_new_P312', 'TensileTests_new_P313', 'TensileTests_new_P314', 'TensileTests_new_P315',
             'TensileTests_new_P316', 'TensileTests_new_P317', 'TensileTests_new_P318', 'TensileTests_new_P319', 'TensileTests_new_P320',
             'TensileTests_new_P321','TensileTests_new_P322']
# filenames = ['TensileTests_new_P21', 'TensileTests_new_P22', 'TensileTests_new_P23', 'TensileTests_new_P24', 'TensileTests_new_P25',
#              'TensileTests_new_P26', 'TensileTests_new_P27', 'TensileTests_new_P28', 'TensileTests_new_P29', 'TensileTests_new_P210',
#              # 'TensileTests_new_P211', 'TensileTests_new_P212', 'TensileTests_new_P214', 'TensileTests_new_P215',
#              'TensileTests_new_P211', 'TensileTests_new_P212', 'TensileTests_new_P213', 'TensileTests_new_P214', 'TensileTests_new_P215',
#              'TensileTests_new_P216', 'TensileTests_new_P217', 'TensileTests_new_P218', 'TensileTests_new_P219', 'TensileTests_new_P220',
#              'TensileTests_new_P221']
# # filenames = ['Tensile']
# filenames = ['TensileTests_P31', 'TensileTests_P32', 'TensileTests_P33', 'TensileTests_P34', 'TensileTests_P35',
# # filenames = ['TensileTests_P31', 'TensileTests_P32', 'TensileTests_P34',
#              'TensileTests_P38', 'TensileTests_P39', 'TensileTests_P310',
#              'TensileTests_P311', 'TensileTests_P312', 'TensileTests_P314', 'TensileTests_P315',
#              'TensileTests_P311', 'TensileTests_P312', 'TensileTests_P313', 'TensileTests_P314', 'TensileTests_P315',
#              'TensileTests_P316', 'TensileTests_P317', 'TensileTests_P318', 'TensileTests_P319', 'TensileTests_P320',
#              'TensileTests_P321']
flag=0
frac_pnts = []

RF = {}
UL = {}
UH = {}
U = {}

for odbname in filenames:
    dict_key = odbname.split('_')[-1]
    dataFname = 'LD_' + odbname + '.txt'
    ULnode = '8'
    UHnode = '14'
    # if odbname==filenames[-1]:
    #     flag = os.system("abaqus viewer noGUI=/home/cerecam/Desktop/GIT/PhD_PythonScripts/ExtractFDcurve.py -- "+ ULnode + " " +UHnode + " " + dataFname  + " " + odbname + " " + cwd)
        #
    if flag ==0:
        with open(cwd + dataFname, 'r') as inputF:
            RF_tmp, UL_tmp, UH_tmp, U_tmp = [], [], [], []
            for line in inputF:
                if line == '\n':
                    break
                else:
                    dataline = [float(i.strip()) for i in line.split(',')]
                    RF_tmp.append(-1*dataline[0])
                    UL_tmp.append(dataline[1])
                    UH_tmp.append(dataline[2])
                    # U.append(dataline[2]-dataline[1])
                    U_tmp.append(dataline[3])

            RF[dict_key] = RF_tmp
            UL[dict_key] = UL_tmp
            UH[dict_key] = UH_tmp
            # U.append(dataline[2]-dataline[1])
            U[dict_key] = U_tmp
        RF_neg1 = [i+10 for i, x in enumerate(RF[dict_key][10:]) if x < 0]
        RF_max = RF[dict_key].index(max(RF[dict_key][:RF_neg1[0]]))
        RF_neg = [i+RF_max for i, x in enumerate(RF[dict_key][RF_max:]) if x < 10000]
        # if not RF_neg:
        #     fracP = max(UL[dict_key]) + 3
        # else:
        #     fracP = min([max(UL[dict_key]) + 3, RF_neg[0] - 1])

        m = (RF[dict_key][RF_neg[0]-1]-RF[dict_key][RF_neg[0]])/(U[dict_key][RF_neg[0]-1]-U[dict_key][RF_neg[0]])
        U_end = ((10000.0-RF[dict_key][RF_neg[0]-1])/m) + U[dict_key][RF_neg[0]-1]
        # frac_pnts.append([dict_key, RF_neg[0]])
        RF[dict_key] = RF[dict_key][:RF_neg[0]] + [10000.0]
        UL[dict_key] = UL[dict_key][:RF_neg[0]]
        UH[dict_key] = UH[dict_key][:RF_neg[0]]
        # U.append(dataline[2]-dataline[1])
        U[dict_key] = U[dict_key][:RF_neg[0]] + [U_end]

    else:
        print("Abaqus data extraction Failed")

# frac_pnts.sort(key=lambda x:x[-1])
# RF_frac = frac_pnts[-1]

exp_key = 'P312'
x_frac_exp = U[exp_key][-1]
U_orig = {}
RF_orig = {}
for key in RF.keys():
    x_exp = U[exp_key]
    y_exp = RF[exp_key]
    exp_change = 0
    if x_frac_exp < U[key][-1]:
        print("Experimental fracture before numerical")
        x_ind = [i for i, x in enumerate(U[key]) if x > x_exp[-1]][0]
        x_exp = x_exp + U[key][x_ind:]
        y_exp = y_exp + [10000]*(len(U[key])-x_ind)
        exp_change = 1
    elif U[key][-1] < x_frac_exp:
        print("Numerical fracture before experimental")
        x_ind = [i for i,x in enumerate(x_exp) if x>U[key][-1]][0]
        U[key] = U[key] + x_exp[x_ind:]
        RF[key] = RF[key] + [10000]*(len(x_exp)-x_ind)
    U_idx = [i for i,x in enumerate(U[key]) if x>0.0923][0]
    U_exp_idx = [i for i,x in enumerate(x_exp) if x>0.0923][0]

    # Interpolation of data which has the lower smapling rate
    if key==exp_key:
        pass
    elif len(U[key]) < len(x_exp): # Interpolation of sim data needed
        print('Interpolating simulation data')
        U_orig[key] = copy.deepcopy(U[key])
        RF_orig[key] = RF[key]
        RF_tmp = []
        for x_pnt in x_exp:
            for idx in range(len(U_orig[key][:-1])):
                if x_pnt == U_orig[key][idx]:
                    RF_tmp.append(RF_orig[key][idx])
                    if x_pnt == x_exp[-1]:
                        RF_tmp.append(RF_orig[key][-1])
                    break
                elif (x_pnt>U_orig[key][idx] and x_pnt<U_orig[key][idx+1]):
                    m = (RF_orig[key][idx]-RF_orig[key][idx+1])/(U_orig[key][idx]-U_orig[key][idx+1])
                    RF_tmp.append( m*(x_pnt-U_orig[key][idx])+RF_orig[key][idx])
                    break
                elif x_pnt==U_orig[key][-1]:
                    RF_tmp.append(RF_orig[key][-1])
                    break
        if len(RF_tmp) != len(x_exp):
            print("PROBLEM")

        U[key] = x_exp
        RF[key] = RF_tmp
            

    elif len(U[key][U_idx:]) > len(x_exp[U_exp_idx:]): # Interpolation of exp data needed
        print('Interpolating experimental data')
        U_orig[key] = copy.deepcopy(U[key])
        RF_tmp = []
        for x_pnt in U_orig[key]:
            for idx in range(len(x_exp[:-1])):
                if x_pnt == x_exp[idx]:
                    RF_tmp.append(y_exp[idx])
                    if x_pnt == U_orig[key][-1]:
                        RF_tmp.append(y_exp[-1])
                    break
                elif (x_pnt > x_exp[idx] and x_pnt < x_exp[idx + 1]):
                    m = (y_exp[idx] - y_exp[idx + 1]) / (x_exp[idx] - x_exp[idx + 1])
                    RF_tmp.append(m * (x_pnt - x_exp[idx]) + y_exp[idx])
                    break
                elif x_pnt == x_exp[-1]:
                    RF_tmp.append(y_exp[-1])
                    break
        if len(RF_tmp) != len(U_orig[key]):
            print("PROBLEM")

        x_exp = U[key] 
        y_exp = RF_tmp


    with open(cwd + 'CalibrationData_' + key + '.txt', 'w') as fwrite:
        for i in range(U_idx, len(U[key])):
            fwrite.write(', \t'.join([str(RF[key][i]),str(U[key][i])]) + '\n')
    with open(cwd + 'ExpData_' + key + '.txt', 'w') as fwrite:
        for i in range(U_exp_idx, len(x_exp)):
            fwrite.write(', \t'.join([str(y_exp[i]),str(x_exp[i])]) + '\n')


    fig = plt.figure(1)
    ax = fig.gca()
    if key==exp_key:
        p = ax.plot(U[key][U_idx:], RF[key][U_idx:], ':', label='Experimental')
    else:
        p = ax.plot(U[key][U_idx:], RF[key][U_idx:], label=key)
    if exp_change:
        lineColour = p[0].get_color()
        ax.plot(x_exp[U_exp_idx:], y_exp[U_exp_idx:], ':', color=lineColour)
        # ax.scatter(x_exp[-1], y_exp[-1], label=key + 'Exp', color=lineColour)

    plt.ylim(bottom=0.0)


    # U_idx = U.index([i for i in U if i>0.09][0])
    # fig=plt.figure(2)
    # ax = fig.gca()
    # ax.plot(U[U_idx:], RF[U_idx:], label=odbname)
plt.legend(loc='best')
plt.grid()
plt.show()