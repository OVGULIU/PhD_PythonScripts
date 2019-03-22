"""
Post processing of CT_Specimens for various volume fractions and various voxel thicknesses
"""

from odbAccess import openOdb
import numpy as np
import csv, math, sys
from abaqusConstants import *
from math import pi

metalFrac = '40'
material = 'Composite'
voxels = '20'
cwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/Results/' + material + '/'
odbname = 'RVE_' + voxels + 'Vox_' + metalFrac + 'PER_1_Final.odb'

odb = openOdb(cwd + odbname)
assem = odb.rootAssembly
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
all_frames = steps.frames
FieldOut = frames.fieldOutputs

