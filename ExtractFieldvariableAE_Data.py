"""
abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PyhtonScripts/ExtractFieldvariableAE_Data.py -- cwd+odbname fieldoutput_key
"""


import numpy as np
import csv,math
import sys,os
from odbAccess import openOdb

FO_key = sys.argv[-1]
odbfile = sys.argv[-2]
if odbfile[-4:] != '.odb':
    odbfile = odbfile + '.odb'
# currentwd = '/home/cerecam/Desktop/Npg_Comp_Model_58_42/58_42/58_42'
# outputwd = currentwd
# Jobname = 'NPG_58_42'
# #filename = sys.argv[-1]
# if Jobname[0]!='/':
#     Jobname = '/'+Jobname
# odbfile = Jobname
FO_Array = {}
# odbname = str(currentwd)+str(odbfile)+'.odb'
print >> sys.__stdout__, odbfile, FO_key
odb = openOdb(odbfile)
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
frame_val = steps.frames[-1]
myinstance = odb.rootAssembly.instances[odb.rootAssembly.instances.keys()[0]]
FO = frame_val.fieldOutputs[str(FO_key)]
#print >> sys.__stdout__, str(CONCEN.values[1])
for val in FO.values:
    FO_Array[str(val.nodeLabel)] = val.dataDouble
odb.close()

##print >> sys.__stdout__, str()
outputname = odbfile[:-4]
np.savetxt((outputname + '_' + FO_key + '.csv'), np.array(FO_Array), delimiter=",")
    
