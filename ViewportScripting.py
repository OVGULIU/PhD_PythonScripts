"""
Script to read in Odb and open Abaqus CAE with the required:
displaygroups/viewport options.
Can also print files directly from script
"""

#open modulus, create viewport and open odb
from abaqus import *
from abaqusConstants import *
import displayGroupOdbToolset as dgo
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=268.952117919922,
height=154.15299987793)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
import sys
sys.path.append('/home/etg/PycharmProjects/PhD_PythonScripts')

from BoundaryElementDetect import ElementSlices

X,Y,Z = BoundaryElementDetect.ElementSlices()

executeOnCaeStartup()
o1 = session.openOdb(name='/home/cerecam/Desktop/GP_BoundaryConditionTests/Flux2_NoUEL.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
### CREATE OUTPUT ###

### Various primary variable selection to display current primary = default which is U ###
#session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        #variableLabel='Co', outputPosition=NODAL, )
#session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
	#variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(
	#INVARIANT, 'Mises'), )
#session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
	#variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(
	#COMPONENT, 'E11'), )
	
### Superimpose plot creation and preferences ##
#session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
	#UNDEFORMED, CONTOURS_ON_DEF, ))
#session.viewports['Viewport: 1'].odbDisplay.superimposeOptions.setValues(
	#renderStyle=FILLED, visibleEdges=FREE)

## Viewport visualization preferences
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=OFF,
	state=OFF, annotations=OFF, compass=OFF)	# Remove unnecessary viewport annotations
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triadColor='#000000', 
	triadPosition=(6, 8), legendTextColor='#000000', legendBox=OFF)	#Change triad and legend colours to black
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triadPosition=(5, 5))	# MOve triad to bottom left corner
session.viewports['Viewport: 1'].view.setValues(session.views['Right'])	# Set view to the RHS view

session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
        visibleEdges=FREE, deformationScaling=UNIFORM, uniformScaleFactor=2.0)
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
        contourStyle=CONTINUOUS)
        
### Creating Display Objects ###

#leaf = dgo.LeafFromElementSets(elementSets=('I_Cube.Polymer', )) # Leaf object from element sets
leaf_X0P = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',('1:625+1')),)) # Leaf object from element labels
leaf_X0G = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',('19017:19415+1')),)) # Leaf object from element labels

session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf_X0P)	# Create displaygourp from leafTest object
dg_X0P = session.viewports['Viewport: 1'].odbDisplay.displayGroup
dg_X0P = session.DisplayGroup(name='X0_poly', objectToCopy=dg_X0P)

session.viewports['Viewport: 1'].odbDisplay.displayGroup.add(leaf=leaf_X0G)	# Create displaygourp from leafTest object
dg_X0 = session.viewports['Viewport: 1'].odbDisplay.displayGroup
dg_X0 = session.DisplayGroup(name='X0_all', objectToCopy=dg_X0)

session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf_X0G)	# Create displaygourp from leafTest object
dg_X0G = session.viewports['Viewport: 1'].odbDisplay.displayGroup
dg_X0G = session.DisplayGroup(name='X0_gold', objectToCopy=dg_X0G)

leafTest = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',('11400:12424')),)) # Leaf object from element labels
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leafTest)	# Create displaygourp from leafTest object
dg2 = session.viewports['Viewport: 1'].odbDisplay.displayGroup
dg2 = session.DisplayGroup(name='TestDispGroup2', objectToCopy=dg2)

### Printing to file options ###
session.printOptions.setValues(vpDecorations=OFF, reduceColors=False)
session.pngOptions.setValues(imageSize=(1432,676))

#### Display display group in viewport ###
#session.viewports['Viewport: 1'].odbDisplay.setValues(visibleDisplayGroups=(dg_X0G, ))
#session.viewports['Viewport: 1'].odbDisplay.displayGroupInstances['X0_gold'].setValues(
	#lockOptions=OFF)
	
#### Printing to file ###
#session.printToFile(
        #fileName='/home/cerecam/Desktop/GP_BoundaryConditionTests/X0_Gold.png', 
        #format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
        
#session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        #variableLabel='Co', outputPosition=NODAL, )
#### Display display group in viewport ###
#session.viewports['Viewport: 1'].odbDisplay.setValues(visibleDisplayGroups=(dg_X0, ))
#session.viewports['Viewport: 1'].odbDisplay.displayGroupInstances['X0_all'].setValues(
	#lockOptions=OFF)
	
#### Printing to file ###
#session.printToFile(
        #fileName='/home/cerecam/Desktop/GP_BoundaryConditionTests/X0_All.png', 
        #format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))


