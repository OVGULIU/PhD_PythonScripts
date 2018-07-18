# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 10:23:25 2018

@author: cerecam
"""
import numpy as np
import matplotlib.pyplot as plt


def getresults(name, total_int_file, palpha_file, flux_ele_file):
    filename = '/home/cerecam/Desktop/Check_results'+name+'.inp'
    fread = open(filename, 'r')
    lines = fread.readlines()
    fread.close()
    for x in range(0, len(lines), 4):
        total_int_file.append(float(lines[x+1].split(':')[1]))
        palpha_file.append(float(lines[x+2].split('  ')[1]))
        flux_ele_file.append(float(lines[x+3].split(':')[1]))
    return total_int_file, palpha_file, flux_ele_file


total_int = []
palpha = []
flux_ele = []

# Get data from Check_results'jobname'.inp files
#total_int,palpha,flux_ele = getresults('Voxel_newFlux', total_int, palpha, flux_ele)
total_int, palpha, flux_ele = getresults('Simulation_Length', total_int, palpha, flux_ele)
#total_int,palpha,flux_ele = getresults('Delete_cont',total_int,palpha,flux_ele)

# Calcuate increment that teh concentration limit was first reached
#limit = [flux_ele.index(y) for y in flux_ele if y < 589][0]

# Normalize values for visualisation for trend
total_int_norm = [i/max(total_int, key=abs) for i in total_int]
palpha_norm = [i/max(palpha, key=abs) for i in palpha]
flux_ele_norm = [i/max(flux_ele, key=abs) for i in flux_ele]
time = np.linspace(0, len(total_int), len(total_int))

# Lines fo best fit
line_palpha = np.poly1d(np.polyfit(time, palpha_norm, 4))
line_total_int = np.poly1d(np.polyfit(time, total_int_norm, 3))

#Plot figures
plt.figure(figsize=(17, 10))
plt.plot(time, total_int_norm, 'r',
         time, palpha_norm, 'b',
         time, flux_ele_norm, 'g',
         time, line_palpha(time), 'b--',
         time, line_total_int(time), 'r--')
# plt.plot([limit]*2,[min(min(total_int_norm),min(palpha_norm),min(flux_ele_norm))-0.1,1.1],'k')
plt.plot([time[0], time[-1]], [1.0, 1.0], 'k')
plt.ylim(top=1.05)
plt.legend(('dc/dt', 'palpha', '# flux elements'), loc=4)
plt.show()
