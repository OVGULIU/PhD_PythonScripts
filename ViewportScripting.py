"""
Script to read in Odb and open Abaqus CAE with the required:
displaygroups/viewport options.
Can also print files directly from script??
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
executeOnCaeStartup()
o1 = session.openOdb(name='/home/cerecam/Desktop/GP_BoundaryConditionTests/Flux2_NoUEL.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
### CREATE OUTPUT ###
## Viewport visualization preferences
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=OFF,
	state=OFF, annotations=OFF, compass=OFF)	# Remove unnecessary viewport annotations
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triadColor='#000000', 
	triadPosition=(6, 8), legendTextColor='#000000', legendBox=OFF)	#Change triad and legend colours to black
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triadPosition=(5, 5))	# MOve triad to bottom left corner
session.viewports['Viewport: 1'].view.setValues(session.views['Right'])	# Set view to the RHS view

#Creating Display Object

leafTest = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',(1,'2',3,'4:1024')),)) # Leaf object from element labels
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leafTest)	# Create displaygourp from leafTest object
dg = session.viewports['Viewport: 1'].odbDisplay.displayGroup
dg = session.DisplayGroup(name='TestDispGroup', objectToCopy=dg)

leafTest = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',('11400:12424')),)) # Leaf object from element labels
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leafTest)	# Create displaygourp from leafTest object
dg2 = session.viewports['Viewport: 1'].odbDisplay.displayGroup
dg2 = session.DisplayGroup(name='TestDispGroup', objectToCopy=dg2)

session.viewports['Viewport: 1'].odbDisplay.setValues(visibleDisplayGroups=(dg, ))
session.viewports['Viewport: 1'].odbDisplay.displayGroupInstances['TestDispGroup'].setValues(
	lockOptions=OFF)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
        visibleEdges=FREE, deformationScaling=UNIFORM, uniformScaleFactor=2.0)
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
        contourStyle=CONTINUOUS)
    

# Printing to file
session.printOptions.setValues(vpDecorations=OFF, reduceColors=False)
session.pngOptions.setValues(imageSize=(1432,676))
session.printToFile(
        fileName='/home/cerecam/Desktop/GP_BoundaryConditionTests/Test.png', 
        format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))


