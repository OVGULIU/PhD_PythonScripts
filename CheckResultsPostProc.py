# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 10:23:25 2018

@author: cerecam
"""
import numpy as np
import matplotlib.pyplot as plt


def getresults(name, total_int_file, influx_file, outflux_file):
    filename = '/home/cerecam/Desktop/Check_results'+name+'.inp'
    fread = open(filename, 'r')
    lines = fread.readlines()
    fread.close()
    for x in range(0, len(lines), 7):
        total_int_file.append(float(lines[x+3].split(':')[1]))
        influx_file.append(float(lines[x+5].split(':')[1]))
        outflux_file.append(float(lines[x+6].split(':')[1]))
    return total_int_file, influx_file, outflux_file


total_int = []
influx = []
outflux = []

# Get data from Check_results'jobname'.inp files
#total_int,palpha,outflux = getresults('Voxel_newFlux', total_int, palpha, outflux)
total_int, influx, outflux = getresults('Influx_k-5', total_int, influx, outflux)
#total_int,palpha,outflux = getresults('Delete_cont',total_int,palpha,outflux)

# Calcuate increment that teh concentration limit was first reached
#limit = [outflux.index(y) for y in outflux if y < 589][0]

# Normalize values for visualisation for trend
total_int_norm = [i/max(total_int, key=abs) for i in total_int]
influx_norm = [i/max(influx, key=abs) for i in influx]
outflux_norm = [i/max(outflux, key=abs) for i in outflux]
time = np.linspace(0, len(total_int), len(total_int))

# Lines fo best fit
line_influx = np.poly1d(np.polyfit(time, influx_norm, 4))
line_total_int = np.poly1d(np.polyfit(time, total_int_norm, 3))

#Plot figures
plt.figure(figsize=(17, 10))
plt.plot(time, total_int_norm, 'r',
         time, influx_norm, 'b',
         time, outflux_norm, 'g')
#         time, line_influx(time), 'b--',
#         time, line_total_int(time), 'r--')
# plt.plot([limit]*2,[min(min(total_int_norm),min(influx_norm),min(outflux_norm))-0.1,1.1],'k')
plt.plot([time[0], time[-1]], [1.0, 1.0], 'k')
plt.ylim(top=1.05)
plt.legend(('dc/dt', 'influx', 'outflux'), loc=4)
plt.show()
