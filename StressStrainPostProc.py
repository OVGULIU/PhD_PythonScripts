"""
File to process the homogeneized stress and strain values for an RVE simulated in Abaqus/Explicit for every frame
"""

import numpy as np
import time
import os
import sys
from odbAccess import openOdb

def logtotrueStrain(vector):
    import math
    l_l0 = [math.e**value for value in vector]
    true_E = [1.0-(1.0/x) for x in l_l0]
    return true_E

def logtoEngStrain(vector):
    import math
    l_l0 = [math.e**value for value in vector]
    eng_E = [x-1.0 for x in l_l0]
    return eng_E

cwd = '/home/cerecam/Desktop/Crack_Models/'
odbname = 'Tension_test_2.odb'
outputFile = 'test_results.txt'

odb = openOdb(cwd + odbname)
assem = odb.rootAssembly
myInstance = assem.instances['RVE']
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
all_frames = steps.frames
last_frame = all_frames[-1]

resultsFile = open(cwd+outputFile, 'w')
for frame in [last_frame]:
    print >> sys.__stdout__, ("Processing frame: " + str(frame.frameValue))

    trace_e_list = []
    e_dev = []
    trace_s_list = []
    s_dev = []

    stress = frame.fieldOutputs['S']
    strain = frame.fieldOutputs['LE']

    s_sum = np.array([0.0]*len(stress.values[0].data))
    e_sum = np.array([0.0]*len(strain.values[0].data))

    t1 = time.time()
    for x in range(len(stress.values)):
        s_data = np.array(stress.values[x].data)
        s_sum += s_data
        t2 = time.time()
        e_data = np.array(logtoEngStrain(strain.values[x].data))
        e_sum += e_data
        t3 = time .time()
        if frame.frameValue == last_frame.frameValue:
            x_tensor = np.array([[s_data[0], s_data[3], s_data[5]],
                                 [s_data[3], s_data[1], s_data[4]],
                                 [s_data[5], s_data[4], s_data[2]]])
            trace_s = np.tensordot(x_tensor, np.eye(3))/3.0
            s_dev.append(x_tensor-trace_s*np.eye(3))
            trace_s_list.append(trace_s)
            t4 = time .time()

            y_tensor = np.array([[e_data[0], e_data[3], e_data[5]],
                                 [e_data[3], e_data[1], e_data[4]],
                                 [e_data[5], e_data[4], e_data[2]]])
            trace_e = np.tensordot(y_tensor, np.eye(3))
            e_dev.append(y_tensor-trace_e*np.eye(3))
            trace_e_list.append(trace_e)
            t5 = time.time()

    print >> sys.__stdout__, ("s_data extraction complete: " + str(t1-t2))
    print >> sys.__stdout__, ("e_data extraction complete: " + str(t2-t3))
    print >> sys.__stdout__, ("s_data homogenization variables complete: " + str(t3-t4))
    print >> sys.__stdout__, ("e_data homogenization variables complete: " + str(t4-t5))
    homog_stress = s_sum/(len(stress.values))
    homog_strain = e_sum/(len(strain.values))

    resultsFile.write("Frame ID: " + str(frame.frameValue) + '\n')
    resultsFile.write("Stress: " + str(list(homog_stress)).strip('[').strip(']') + '\n')
    resultsFile.write("Strain: " + str(list(homog_strain)).strip('[').strip(']') + '\n')
    print >> sys.__stdout__, ("Frame ID: " + str(frame.frameValue))
    print >> sys.__stdout__, ("Stress: " + str(list(homog_stress)))
    print >> sys.__stdout__, ("Strain: " + str(list(homog_strain)))
    print >> sys.__stdout__, ("Results file written")
    if frame.frameValue == last_frame.frameValue:
        s_dev_sum = np.sum(np.array(s_dev),0)
        e_dev_sum = np.sum(np.array(e_dev),0)
        trace_s_sum = np.sum(trace_s_list)
        trace_e_sum = np.sum(trace_e_list)

        mu = 0.5*np.sqrt(np.tensordot(s_dev_sum, s_dev_sum)/np.tensordot(e_dev_sum,e_dev_sum))
        kappa = (1.0/3.0)*(trace_s_sum/trace_e_sum)
        em = (9.0*kappa*mu)/(3.0*kappa + mu)
        poisson = (3.0*kappa-2.0*mu)/(6.0*kappa + 2.0*mu)
        resultsFile.write("Youngs mod, poissons ratio, bulk (kappa), shear (mu) modulus: " +
                      str(em) + ', ' + str(poisson) + ', ' + str(kappa) + ', ' + str(mu) + '\n')
        print >> sys.__stdout__, ("Homogenization variable written")
    print >> sys.__stdout__, ("COMPLETED frame: " + str(frame.frameValue))
odb.close()
resultsFile.close()