"""
Script to read in Odb and open Abaqus CAE with the required:
displaygroups/viewport options.
Can also print files directly from script
"""
def ElementSlices(cwd):
    import numpy as np
    print("ElementSlices.py is running")
    def readinp(filename, startline):
        """
        Reads file and converts line to list and places inlist of list
        :param filename: filename to read from
        :param startline: whther to start from line 1 or 0.
        :return: list of list of each line of filename
        """
        output_list = []
        readfile = open(filename, 'r')
        if startline:
            readfile.readline()
        for line in readfile:
            newarray = [float(x) for x in line.split(',')]
            output_list.append(newarray)
        readfile.close()
        return output_list


    def writeinp(lst, output_name, set_name, eset=0, nset=0, create_csv=0):
        """
        Writes .inp file given list of nodes or elements
        :param lst: list of elements of nodes
        :param output_name: file to write to
        :param set_name: name of el/nset
        :param eset: state if elset (default = 0)
        :param nset: state if nset (default = 0)
        :param create_csv: 1 = create a csv fiel from lst otherwise not
        only eset or nset, if both ==1 returns error
        :return: None
        """
        if ((eset == 1) and (nset == 1)) or not((eset == 1) or (nset == 1)):
            print("Error list given as both nset or elset, only one to be given at a time")
        elif int(eset) == 1:
            firstline = "*elset, elset={}, instance=RVE \n".format(set_name)
        elif int(nset) == 1:
            firstline = "*nset, nset={}, instance=RVE \n".format(set_name)
        inpfile_write = open(output_name+'.inp', 'w')
        inpfile_write.write(firstline)
        for i in range(0, len(lst), 10):
            inpfile_write.write(''.join(str(lst[i:i + 10])).strip('[').strip(']') + '\n')
        if create_csv:
            arry = np.array([len(lst)] + lst)
            np.savetxt(output_name+'.csv', arry, delimiter=",", fmt='%i')
        inpfile_write.close()


    nodefile = 'Nodes.inp'
    #elementfile = 'Elements_All.inp'
    gold_element = range(1, 1213242+1)
    poly_element = range(1213243, 2097152+1)
    if cwd[-1] != '/':
        cwd = cwd + '/'
    if nodefile[0] == '/':
        nodefile = nodefile[1:]
    # if elementfile[0] == '/':
    #     elementfile = elementfile[1:]

    nodelist = readinp(cwd + nodefile, 1)
    #elelist = readinp(cwd + elementfile, 0)
    gold_elelist = readinp(cwd  + 'GoldElements.inp',0)

    x0_val = min(nodelist, key=lambda z: z[-3])[-3]
    x1_val = max(nodelist, key=lambda z: z[-3])[-3]
    y0_val = min(nodelist, key=lambda z: z[-2])[-2]
    y1_val = max(nodelist, key=lambda z: z[-2])[-2]
    z0_val = min(nodelist, key=lambda z: z[-1])[-1]
    z1_val = max(nodelist, key=lambda z: z[-1])[-1]

    x0, x1 = [], []
    y0, y1 = [], []
    z0, z1 = [], []

    for nodes in nodelist:
        if x0_val == nodes[1]:
            x0.append(int(nodes[0]))
        if x1_val == nodes[1]:
            x1.append(int(nodes[0]))
        if y0_val == nodes[2]:
            y0.append(int(nodes[0]))
        if y1_val == nodes[2]:
            y1.append(int(nodes[0]))
        if z0_val == nodes[3]:
            z0.append(int(nodes[0]))
        if z1_val == nodes[3]:
            z1.append(int(nodes[0]))

    #writeinp(x0, cwd + 'NodeFiles/x0_all', 'x0', nset=1, create_csv=0)
    #writeinp(x1, cwd + 'NodeFiles/x1_all', 'x1', nset=1, create_csv=0)
    #writeinp(y0, cwd + 'NodeFiles/y0_all', 'y0', nset=1, create_csv=0)
    #writeinp(y1, cwd + 'NodeFiles/y1_all', 'y1', nset=1, create_csv=0)
    #writeinp(z0, cwd + 'NodeFiles/z0_all', 'z0', nset=1, create_csv=0)
    #writeinp(z1, cwd + 'NodeFiles/z1_all', 'z1', nset=1, create_csv=0)

    x_ele_int  = []
    y_ele_int  = []
    z_ele_int = []
    X_dict = {}
    Y_dict = {}
    Z_dict = {}

    # x0_gold, x0_poly = [], []
    # x1_gold, x1_poly = [], []
    # y0_gold, y0_poly = [], []
    # y1_gold, y1_poly = [], []
    # z0_gold, z0_poly = [], []
    # z1_gold, z1_poly = [], []

    # element_dist = abs((x1_val-x0_val)/128.0)
    # xmin, ymin, zmin = [x+element_dist for x in [x0_val, y0_val, z0_val]]
    # xmax, ymax, zmax = [x-element_dist for x in [x1_val, y1_val, z1_val]]


    for increment in range(0, 32):  # type: int
        xmin = 0.0 + (increment*(30.0/32))
        xmax = xmin + (30.0/32.0)
        ymin, zmin = xmin, xmin
        ymax, zmax = xmax, xmax
        x_ele_int = []
        y_ele_int = []
        z_ele_int = []
        for element in gold_elelist:
            nodes_coord = [nodelist[int(_)-1][1:] for _ in element[1:]]
            x_cent, y_cent, z_cent = [_/len(element[1:]) for _ in (np.sum(np.array(nodes_coord), axis=0))]
            centroid = [x_cent, y_cent, z_cent]
            if all([x > centroid[i] for i, x in enumerate([xmin, ymin, zmin])]) and all([x < centroid[i] for i, x in enumerate([xmax, ymax, zmax])]):
                pass
            else:
                if xmax >= x_cent >= xmin:
                    x_ele_int.append(int(element[0]))
                if ymax >= y_cent >= ymin:
                    y_ele_int.append(int(element[0]))
                if zmax >= z_cent >= zmin:
                    z_ele_int.append(int(element[0]))
        X_dict['X' + str(increment)] = x_ele_int
        Y_dict['Y' + str(increment)] = y_ele_int
        Z_dict['Z' + str(increment)] = z_ele_int
        # print('X' + str(increment),len(x_ele_int))
        # print('Y' + str(increment),len(y_ele_int))
        # print('Z' + str(increment),len(z_ele_int))
    return X_dict, Y_dict, Z_dict

import displayGroupOdbToolset as dgo
# open modulus, create viewport and open odb
from abaqus import *
from abaqusConstants import *

session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=268.952117919922,
height=154.15299987793)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup

#from BoundaryElementDetect import ElementSlices
InputDir  = '/home/cerecam/Desktop/GP_BoundaryConditionTests/InputFiles'
X,Y,Z = ElementSlices(InputDir)
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

for DictKey in X.keys():
	elements = tuple([str(y) for y in X[DictKey]])
	leaf = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',elements),))
	session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)	# Create displaygourp from leafTest object
	dg = session.viewports['Viewport: 1'].odbDisplay.displayGroup
	dg = session.DisplayGroup(name=DictKey + '_poly', objectToCopy=dg)
##leaf = dgo.LeafFromElementSets(elementSets=('I_Cube.Polymer', )) # Leaf object from element sets
#leaf_X0P = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',('1:625+1')),)) # Leaf object from element labels
#leaf_X0G = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',('19017:19415+1')),)) # Leaf object from element labels

#session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf_X0P)	# Create displaygourp from leafTest object
#dg_X0P = session.viewports['Viewport: 1'].odbDisplay.displayGroup
#dg_X0P = session.DisplayGroup(name='X0_poly', objectToCopy=dg_X0P)

#session.viewports['Viewport: 1'].odbDisplay.displayGroup.add(leaf=leaf_X0G)	# Create displaygourp from leafTest object
#dg_X0 = session.viewports['Viewport: 1'].odbDisplay.displayGroup
#dg_X0 = session.DisplayGroup(name='X0_all', objectToCopy=dg_X0)

#session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf_X0G)	# Create displaygourp from leafTest object
#dg_X0G = session.viewports['Viewport: 1'].odbDisplay.displayGroup
#dg_X0G = session.DisplayGroup(name='X0_gold', objectToCopy=dg_X0G)

#leafTest = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',('11400:12424')),)) # Leaf object from element labels
#session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leafTest)	# Create displaygourp from leafTest object
#dg2 = session.viewports['Viewport: 1'].odbDisplay.displayGroup
#dg2 = session.DisplayGroup(name='TestDispGroup2', objectToCopy=dg2)

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


