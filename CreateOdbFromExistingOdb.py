# import abaqus libraries
from odbAccess import *
from odbMaterial import *
from odbSection import *
from abaqusConstants import *
import numpy as np

# import python libraries
import sys,time,csv,os

# File names and locations for old odb
cwd = '/home/cerecam/Desktop/GP_BoundaryConditionTests/'
OldOdbNameNoext = 'Voxel_1A_cont'
OldOdbName = OldOdbNameNoext + '.odb'
                
# Accessing necessary objects in old odb                
oldOdb=openOdb(cwd+OldOdbName)
assembly = oldOdb.rootAssembly
instance= assembly.instances
myinstance = assembly.instances[instance.keys()[0]]
steps = oldOdb.steps[oldOdb.steps.keys()[-1]]
lastframe = steps.frames[-1]
analysisTime = steps.frames[-1].frameValue
FieldOutputs = lastframe.fieldOutputs

oldOdb.steps.keys()[0] = 'new'
print(oldOdb.steps.keys())
oldOdb.save()
oldOdb.close()

## Creates an ODB
#odbpath = cwd+'/Cube_PythonWritten.odb'
#odb = Odb(name='Model-1', analysisTitle = "ODB created by python script",
          #description = "using python scripting to create an odb for showing VUEL data from a previous odb with no visualization elements",
          #path = odbpath)
         
         
## Create Model object from existing output database
#newModel = mdb.ModelFromOdbFile(name='Newmodel', odbFileName='/home/cerecam/Desktop/GP_BoundaryConditionTests/Voxel_1A.odb')

## Creates materials
## Create sections

#mdb.models['Newmodel'].PartFromOdb(name='I_CUBE', odb='/home/cerecam/Desktop/GP_BoundaryConditionTests/Voxel_1A.odb')


