import sys, csv
import matplotlib.pyplot as plt

import numpy as np
from matplotlib.ticker import FormatStrFormatter

plt.rcParams['figure.dpi']=100
plt.rcParams['font.size']=12
plt.rcParams['legend.fontsize' ] = 'large'
plt.rcParams['figure.titlesize']= 'medium'
plt.rcParams['lines.linewidth']=1.75
plt.rcParams['grid.linestyle']='-'
plt.rcParams['grid.color']=(0.75,0.75,0.75)
plt.rcParams['axes.axisbelow']= True
# from scipy.signal import savgol_filter


def extractCSVData(cwd, fileName):
    with open(cwd + fileName, 'r') as fname:
        dataFile = list(csv.reader(fname))
    frametime = [float(x) for x in dataFile[0][1:]]
    # frametime=0
    E_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[1][1:]]
    E_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[2][1:]]
    E_T = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[3][1:]]
    # S_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[7][1:]]
    # S_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[8][1:]]
    # E_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[9][1:]]
    # E_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[10][1:]]
    # return frametime, dispX_G, dispX_P, dispY_G, dispY_P, dispZ_G, dispZ_P, S_G, S_P, E_G, E_P
    return frametime, E_G, E_P, E_T



lineType = [':', '--', '-']
fileName = 'Strain_Values.csv'
#
# # cwd = '/home/etg/Dropbox/UCT/PhD/Results/Paper2/25PER/'
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/HPC_25PER/'
[time_25, E_G_25, E_P_25, E_T_25] = extractCSVData(cwd,fileName)
timeEnd25 = time_25.index(1500.00) +1
time_25 = time_25[:timeEnd25]
E_G_25 = E_G_25[:timeEnd25]
E_P_25 = E_P_25[:timeEnd25]
E_T_25 = E_T_25[:timeEnd25]
#
# # fileName = 'Disp_Values_only_tmpS1_34.csv'
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_34PER/HPC_34PER/'
[time_34, E_G_34, E_P_34, E_T_34] = extractCSVData(cwd,fileName)
timeEnd34 = time_34.index(1500.00) +1
time_34 = time_34[:timeEnd34]
E_G_34 = E_G_34[:timeEnd34]
E_P_34 = E_P_34[:timeEnd34]
E_T_34 = E_T_34[:timeEnd34]
#
# # cwd = '/home/etg/Dropbox/UCT/PhD/Results/Paper2/25PER/'
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER/HPC_42PER/'
#
[time_42, E_G_42, E_P_42, E_T_42] = extractCSVData(cwd,fileName)
#
# # cwd = '/home/etg/Dropbox/UCT/PhD/Results/Paper2/25PER/'
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_50PER/HPC_50PER/'
[time_50, E_G_50, E_P_50, E_T_50] = extractCSVData(cwd,fileName)


# fig = plt.figure(1)
# ax = plt.gca()
# plt.plot(time_25,conc_25, 'b', label = '$\phi_G = 25 \% $')
# plt.plot(time_34,conc_34, 'r', label = '$\phi_G = 34 \% $')
# plt.plot(time_42,conc_42, 'g', label = '$\phi_G = 42 \% $')
# plt.plot(time_50,conc_50, 'm', label = '$\phi_G = 50 \% $')
#
# plt.xlabel('time [ns]')
# plt.ylabel('concentration [mol/nm$^3$]')
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
# ax.legend( frameon=False, loc = 'upper right', ncol=2)
# plt.grid(which='both')

fig = plt.figure(2)
ax2 = plt.gca()
plt.plot(time_25, [float(_[2]) for _ in E_T_25],
         linestyle=lineType[2], color='b', label= '25% E$_\parallel$')
plt.plot(time_34, [float(_[2]) for _ in E_T_34],
         linestyle=lineType[2], color='r', label= '34% E$_\parallel$')
plt.plot(time_42, [float(_[2]) for _ in E_T_42],
         linestyle=lineType[2], color='g', label= '42% E$_\parallel$')
plt.plot(time_50, [float(_[2]) for _ in E_T_50],
         linestyle=lineType[2], color='k', label= '50% S E$_\parallel$')
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.title('Average strain development on influx face (in flux direction)')
plt.xlabel('time [ns]')
# plt.xlabel('time/time$_{end}$')
plt.ylabel('strain nm/nm')
plt.grid()
ax2.legend( frameon=False, loc = 'upper right', ncol=2)

fig = plt.figure(3)
ax3 = plt.gca()
for i in range(0, 1):
    plt.plot(time_25, [float(_[i]) for _ in E_T_25],
             linestyle=lineType[i], color='b', label= '25% E$_\perp$')
for i in range(0, 1):
    plt.plot(time_34, [float(_[i]) for _ in E_T_34],
             linestyle=lineType[i], color='r', label= '34% E$_\perp$')
for i in range(0, 1):
    plt.plot(time_42, [float(_[i]) for _ in E_T_42],
             linestyle=lineType[i], color='g', label= '42% E$_\perp$')
for i in range(0, 1):
    plt.plot(time_50, [float(_[i]) for _ in E_T_50],
             linestyle=lineType[i], color='k', label= '50% E$_\perp$')
ax3.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.title('Average strain development on influx face (perpendicular to flux direction)')
# plt.title('Average strain development on influx face')
plt.xlabel('time [ns]')
# plt.xlabel('time/time$_{end}$')
plt.ylabel('strain nm/nm')
plt.grid()
ax3.legend( frameon=False, loc = 'upper right', ncol=2)
"""
fig = plt.figure(4)
ax4 = plt.gca()
plt.plot(time_25, [float(_[2]) for _ in E_P_25],
         linestyle=lineType[2], color='b', label= '25% E$_\parallel$')
plt.plot(time_34, [float(_[2]) for _ in E_P_34],
         linestyle=lineType[2], color='r', label= '34% E$_\parallel$')
plt.plot(time_42, [float(_[2]) for _ in E_P_42],
         linestyle=lineType[2], color='g', label= '42% E$_\parallel$')
plt.plot(time_50, [float(_[2]) for _ in E_P_50],
         linestyle=lineType[2], color='k', label= '50% S E$_\parallel$')
ax4.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.title('Average strain development on influx face: Polymer (in flux direction)')
plt.xlabel('time [ns]')

# plt.xlabel('time/time$_{end}$')
plt.ylabel('strain nm/nm')
plt.grid()
ax4.legend( frameon=False, loc = 'upper right', ncol=2)

fig = plt.figure(5)
ax5 = plt.gca()
for i in range(0, 1):
    plt.plot(time_25, [float(_[i]) for _ in E_P_25],
             linestyle=lineType[i], color='b', label= '25% S_' + str(i+1) + str(i+1))
for i in range(0, 1):
    plt.plot(time_34, [float(_[i]) for _ in E_P_34],
             linestyle=lineType[i], color='r', label= '34% S_' + str(i+1) + str(i+1))
for i in range(0, 1):
    plt.plot(time_42, [float(_[i]) for _ in E_P_42],
             linestyle=lineType[i], color='g', label= '42% S_' + str(i+1) + str(i+1))
for i in range(0, 1):
    plt.plot(time_50, [float(_[i]) for _ in E_P_50],
             linestyle=lineType[i], color='k', label= '50% S_' + str(i+1) + str(i+1))
ax5.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.title('Average strain development on influx face: Polymer (perpendicular to flux direction)')
plt.xlabel('time [ns]')
# plt.xlabel('time/time$_{end}$')
plt.ylabel('strain nm/nm')
plt.grid()
ax5.legend( frameon=False, loc = 'upper right', ncol=2)

fig = plt.figure(6)
ax6 = plt.gca()
plt.plot(time_25, [float(_[2]) for _ in E_G_25],
         linestyle=lineType[2], color='b', label= '25% E$_\parallel$')
plt.plot(time_34, [float(_[2]) for _ in E_G_34],
         linestyle=lineType[2], color='r', label= '34% E$_\parallel$')
plt.plot(time_42, [float(_[2]) for _ in E_G_42],
         linestyle=lineType[2], color='g', label= '42% E$_\parallel$')
plt.plot(time_50, [float(_[2]) for _ in E_G_50],
         linestyle=lineType[2], color='k', label= '50% S E$_\parallel$')
ax6.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.title('Average strain development on influx face: Gold (in flux direction)')
plt.xlabel('time [ns]')
# plt.xlabel('time/time$_{end}$')
plt.ylabel('strain nm/nm')
plt.grid()
ax6.legend( frameon=False, loc = 'upper right', ncol=2)

fig = plt.figure(7)
ax7 = plt.gca()
for i in range(0, 1):
    plt.plot(time_25, [float(_[i]) for _ in E_G_25],
             linestyle=lineType[i], color='b', label= '25% S_' + str(i+1) + str(i+1))
for i in range(0, 1):
    plt.plot(time_34, [float(_[i]) for _ in E_G_34],
             linestyle=lineType[i], color='r', label= '34% S_' + str(i+1) + str(i+1))
for i in range(0, 1):
    plt.plot(time_42, [float(_[i]) for _ in E_G_42],
             linestyle=lineType[i], color='g', label= '42% S_' + str(i+1) + str(i+1))
for i in range(0, 1):
    plt.plot(time_50, [float(_[i]) for _ in E_G_50],
             linestyle=lineType[i], color='k', label= '50% S_' + str(i+1) + str(i+1))
ax7.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.title('Average strain development on influx face: Gold (perpendicular to flux direction)')
plt.xlabel('time [ns]')
# plt.xlabel('time/time$_{end}$')
plt.ylabel('strain nm/nm')
plt.grid()
ax7.legend( frameon=False, loc = 'upper right', ncol=2)
"""
plt.show()