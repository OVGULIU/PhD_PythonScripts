"""
Python script to create and print images using displaygroups created by ViewportScripting.py file
"""

from abaqus import *
from abaqusConstants import *
import displayGroupOdbToolset as dgo
from caeModules import *
from driverUtils import executeOnCaeStartup
import csv

def GoldPrint(DispGroupName):	
	session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
		variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(
		INVARIANT, 'Mises'), )
	session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
	        renderStyle=SHADED, visibleEdges=FREE, deformationScaling=UNIFORM, uniformScaleFactor=3.5)
	session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
        contourStyle=CONTINUOUS)
	session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
		UNDEFORMED, CONTOURS_ON_DEF, ))
	session.viewports['Viewport: 1'].odbDisplay.superimposeOptions.setValues(
		renderStyle=WIREFRAME, visibleEdges=FREE, edgeColorWireHide='#000000', 
        edgeLineThickness=MEDIUM, colorCodeOverride=OFF)
	if DispGroupName[0].upper()=='X':
		session.viewports['Viewport: 1'].view.setValues(session.views['Right'])	# Set view to the RHS view
		session.viewports['Viewport: 1'].odbDisplay.superimposeOptions.setValues(
		deformedOffsetMode=NONUNIFORM, nonuniformOffset=(-2.0,0.0,0.0))
	elif DispGroupName[0].upper()=='Y':
		session.viewports['Viewport: 1'].view.setValues(session.views['Top'])	# Set view to the Top view
		session.viewports['Viewport: 1'].odbDisplay.superimposeOptions.setValues(
		deformedOffsetMode=NONUNIFORM, nonuniformOffset=(0.0,-2.0,0.0))
	elif DispGroupName[0].upper()=='Z':
		session.viewports['Viewport: 1'].view.setValues(session.views['Front'])	# Set view to the Front view
		session.viewports['Viewport: 1'].odbDisplay.superimposeOptions.setValues(
		deformedOffsetMode=NONUNIFORM, nonuniformOffset=(0.0,0.0,-2.0))
		
	return
	
def PolyPrint(DispGroupName):
	session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
		DEFORMED, CONTOURS_ON_DEF, ))
	session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
        renderStyle=FILLED, visibleEdges=NO EDGE)
    if DispGroupName[0].upper()=='X':
		session.viewports['Viewport: 1'].view.setValues(session.views['Right'])	# Set view to the RHS view
	elif DispGroupName[0].upper()=='Y':
		session.viewports['Viewport: 1'].view.setValues(session.views['Top'])	# Set view to the Top view
	elif DispGroupName[0].upper()=='Z':
		session.viewports['Viewport: 1'].view.setValues(session.views['Front'])	# Set view to the Front view
	return

session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=OFF,
	state=OFF, annotations=OFF, compass=OFF)	# Remove unnecessary viewport annotations
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triadColor='#000000', 
	triadPosition=(5, 5), legendTextColor='#000000', legendBox=OFF)	#Change triad and legend colours to black, MOve triad to bottom left corner

session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
        
InputDir  = '/home/cerecam/Desktop/GP_BoundaryConditionTests/InputFiles'
csvFile = open(InputDir + '/DictionaryKeys.csv', 'r')
Keys = []
reader = csv.reader(csvFile)
for row in reader:
    Keys.extend(row)
for DictKey in Keys()[0:3]:
	print(DictKey)
	if DictKey[-4:].lower() == 'gold':
		GoldPrint(DictKey)
	if DictKey[-4:].lower() == 'poly':
		PolyPrint(DictKey)
	#### Display display group in viewport ###
	session.viewports['Viewport: 1'].odbDisplay.setValues(visibleDisplayGroups=(dg, ))
	session.viewports['Viewport: 1'].odbDisplay.displayGroupInstances[DictKey].setValues(
		lockOptions=OFF)
		
	### Printing to file ###
	session.printToFile(
	        fileName='/home/cerecam/Desktop/GP_BoundaryConditionTests/' + DictKey + '.png', 
	        format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
	        
