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
    Conc = [float(x) for x in dataFile[1][1:]]
    # S_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[7][1:]]
    # S_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[8][1:]]
    # E_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[9][1:]]
    # E_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[10][1:]]
    # return frametime, dispX_G, dispX_P, dispY_G, dispY_P, dispZ_G, dispZ_P, S_G, S_P, E_G, E_P
    return frametime, Conc



fileName = 'Conc_Values_full.csv'

# cwd = '/home/etg/Dropbox/UCT/PhD/Results/Paper2/25PER/'
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/HPC_25PER/'
[time_25, conc_25] = extractCSVData(cwd,fileName)
timeEnd25 = time_25.index(1500.00) +1
time_25 = time_25[:timeEnd25]
conc_25 = conc_25[:timeEnd25]
concMax_25 = max(conc_25)
conMax_25_index = conc_25.index(concMax_25)
timeMaxConc_25 = time_25[conMax_25_index]
print('25 %')
print('Max concentration is: {}, at time {} (increment: {})'.format(str(concMax_25),str(timeMaxConc_25), str(timeMaxConc_25/1.903E-01)))

# fileName = 'Disp_Values_only_tmpS1_34.csv'
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_34PER/HPC_34PER/'
[time_34, conc_34] = extractCSVData(cwd,fileName)
timeEnd34 = time_34.index(1500.00) +1
time_34 = time_34[:timeEnd34]
conc_34 = conc_34[:timeEnd34]
concMax_34 = max(conc_34)
conMax_34_index = conc_34.index(concMax_34)
timeMaxConc_34 = time_34[conMax_34_index]
print('34 %')
print('Max concentration is: {}, at time {} (increment: {})'.format(str(concMax_34),str(timeMaxConc_34), str(timeMaxConc_34/1.903E-01)))

# cwd = '/home/etg/Dropbox/UCT/PhD/Results/Paper2/25PER/'
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER/HPC_42PER/'

[time_42, conc_42] = extractCSVData(cwd,fileName)
concMax_42 = max(conc_42)
conMax_42_index = conc_42.index(concMax_42)
timeMaxConc_42 = time_42[conMax_42_index]
print('42 {}')
print('Max concentration is: {}, at time {} (increment: {})'.format(str(concMax_42),str(timeMaxConc_42), str(timeMaxConc_42/1.903E-01)))

# cwd = '/home/etg/Dropbox/UCT/PhD/Results/Paper2/25PER/'
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_50PER/HPC_50PER/'
[time_50, conc_50] = extractCSVData(cwd,fileName)
concMax_50 = max(conc_50)
conMax_50_index = conc_50.index(concMax_50)
timeMaxConc_50 = time_50[conMax_50_index]
print('50 {}')
print('Max concentration is: {}, at time {} (increment: {})'.format(str(concMax_50),str(timeMaxConc_50), str(timeMaxConc_50/1.903E-01)))

conc_25_molPm = [_*7148.0 for _ in conc_25]
conc_34_molPm = [_*6403.0 for _ in conc_34]
conc_42_molPm = [_*5748.0 for _ in conc_42]
conc_50_molPm = [_*5056.0 for _ in conc_50]

fig = plt.figure(1)
ax = plt.gca()
plt.plot(time_25,conc_25, 'b', label = '$\phi_G = 25 \% $')
plt.plot(time_34,conc_34, 'r', label = '$\phi_G = 34 \% $')
plt.plot(time_42,conc_42, 'g', label = '$\phi_G = 42 \% $')
plt.plot(time_50,conc_50, 'm', label = '$\phi_G = 50 \% $')

plt.xlabel('time [ns]')
plt.ylabel('concentration [mol/nm$^3$]')
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
ax.legend( frameon=False, loc = 'upper right', ncol=2)
plt.grid(which='both')

fig = plt.figure(2)
ax2 = plt.gca()
plt.plot(time_25,conc_25_molPm, 'b', label = '$\phi_G = 25 \% $')
plt.plot(time_34,conc_34_molPm, 'r', label = '$\phi_G = 34 \% $')
plt.plot(time_42,conc_42_molPm, 'g', label = '$\phi_G = 42 \% $')
plt.plot(time_50,conc_50_molPm, 'm', label = '$\phi_G = 50 \% $')

plt.xlabel('time [ns]')
plt.ylabel('concentration [mol/nm]')
ax2.legend( frameon=False, loc = 'upper right', ncol=2)
plt.grid(which='both')

plt.show()