"""
Script to read in Elements of large RVE and make a cut out form the middle of a smaller RVE
"""

def InteriorElements(cwd):
    import numpy as np
    print("InteriorElements.py is running")
    def readinp(filename, startline):
        """
        Reads file and converts line to list and places inlist of list
        :param filename: filename to read from
        :param startline: whther to start from line 1 or 0.
        :return: list of list of each line of filename
        """
        print('Reading input file: '+ filename)
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
    if cwd[-1] != '/':
        cwd = cwd + '/'
    if nodefile[0] == '/':
        nodefile = nodefile[1:]
    # if elementfile[0] == '/':
    #     elementfile = elementfile[1:]

    nodelist = readinp(cwd + nodefile, 1)
    #elelist = readinp(cwd + elementfile, 0)
    gold_elelist = readinp(cwd  + 'GoldElements.inp',0)
    Poly_elelist = readinp(cwd  + 'UserElements.inp',0)
    print('Number of gold elements of larger RVE: ' + str(len(gold_elelist)))
    print('Number of polymer elements of larger RVE: ' + str(len(Poly_elelist)))
    print('Total number of elements in larger RVE: ' + str(len(gold_elelist) + len(Poly_elelist)))
    print('Total number of nodes in larger RVE: ' + str(len(nodelist)))

    ele_g, ele_p  = [], []
    new_nodes = []

    L_size_voxel = 64.0
    S_size_voxel = 32.0
    Size_change = (1.0/L_size_voxel)*((L_size_voxel-S_size_voxel)/2.0)
    xmin, ymin, zmin = Size_change, Size_change,Size_change
    xmax, ymax,zmax = 1.0-Size_change, 1.0-Size_change, 1.0-Size_change
    for node in nodelist:
        nodes_coord = node[1:]
        if any( x > nodes_coord[i] for i, x in enumerate([xmin, ymin, zmin])) or any(x < nodes_coord[i] for i, x in enumerate([xmax, ymax, zmax])):
            pass
        else:
            new_nodes.append(node)

    for element in gold_elelist:
        nodes_coord = [nodelist[int(_)-1][1:] for _ in element[1:]]
        x_cent, y_cent, z_cent = [_/len(element[1:]) for _ in (np.sum(np.array(nodes_coord), axis=0))]
        centroid = [x_cent, y_cent, z_cent]
        if all([x <= centroid[i] for i, x in enumerate([xmin, ymin, zmin])]) and all([x >= centroid[i] for i, x in enumerate([xmax, ymax, zmax])]):
            pass
        else:
            formattedList = [int(member) for member in element]
            ele_g.append(formattedList)

    for element in Poly_elelist:
        nodes_coord = [nodelist[int(_)-1][1:] for _ in element[1:]]
        x_cent, y_cent, z_cent = [_/len(element[1:]) for _ in (np.sum(np.array(nodes_coord), axis=0))]
        centroid = [x_cent, y_cent, z_cent]
        if all([x <= centroid[i] for i, x in enumerate([xmin, ymin, zmin])]) and all([x >= centroid[i] for i, x in enumerate([xmax, ymax, zmax])]):
            pass
        else:
            formattedList = [int(member) for member in element]
            ele_p.append(formattedList)
    print('\n')
    print('Number of gold elements of smaller RVE: ' + str(len(ele_g)))
    print('Number of polymer elements of smaller RVE: ' + str(len(ele_p)))
    print('Total number of elements in smaller RVE: ' + str(len(ele_p) + len(ele_g)))
    print('Total number of nodes in smaller RVE: ' + str(len(new_nodes)))
    print('Expected number of elements: ' + "(" + str(int((L_size_voxel ** 3) - (S_size_voxel ** 3))) + ') ' + str((L_size_voxel ** 3) - (S_size_voxel ** 3) == (len(ele_p) + len(ele_g))))
    print('Expected number of nodes: ' + "(" + str(int(((S_size_voxel + 1) ** 3))) + ') ' + str((S_size_voxel + 1) ** 3 == (len(new_nodes))))
    return ele_g, ele_p,new_nodes

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
    
# open modulus, create viewport and open odb
# import numpy as np
# from abaqus import *
# from abaqusConstants import *
# import displayGroupOdbToolset as dgo
# from caeModules import *

#from BoundaryElementDetect import ElementSlices
InputDir  = '/home/etg/Desktop/2M_64x64x64'
Gold_new, Poly_new, new_nodelist = InteriorElements(InputDir)

with open(InputDir + '/GoldElements_s.inp', 'w') as writef:
    for i in Gold_new:
        writef.write(str(i).strip('[').strip(']') + '\n')

with open(InputDir + '/PolyElements_s.inp', 'w') as writef:
    for i in Poly_new:
        writef.write(str(i).strip('[').strip(']') + '\n')

with open(InputDir + '/Nodes_s.inp', 'w') as writef:
    for i in new_nodelist:
        writef.write(str(i).strip('[').strip(']') + '\n')
# Keys = X.keys() + Y.keys() + Z.keys()
# HalfDict = merge_two_dicts(X,Y)
# FullDict = merge_two_dicts(HalfDict, Z)
# executeOnCaeStartup()
# o1 = session.openOdb(name='/home/cerecam/Desktop/GP_BoundaryConditionTests/Flux2_NoUEL.odb')
# session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#
# ### Printing to file options ###
# session.printOptions.setValues(vpDecorations=OFF, reduceColors=False)
# session.pngOptions.setValues(imageSize=(1150,676))
# np.savetxt(InputDir+ '/DictionaryKeys.csv',np.array(Keys), delimiter=",",fmt='%s')
# ### CREATE OUTPUT ###
#
# session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
# session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=OFF,
# 	state=OFF, annotations=OFF, compass=OFF)	# Remove unnecessary viewport annotations
# session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triadColor='#000000',
# 	triadPosition=(5, 5), legendTextColor='#000000', legendBox=OFF)	#Change triad and legend colours to black, MOve triad to bottom left corner
#
# ### Creating Display Objects ###
#
# for DictKey in Keys:
# 	print(DictKey)
# 	elements = tuple([str(y) for y in FullDict[DictKey]])
# 	leaf = dgo.LeafFromModelElemLabels(elementLabels=(('I_Cube',elements),))
# 	session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)	# Create displaygourp from leafTest object
# 	dg = session.viewports['Viewport: 1'].odbDisplay.displayGroup
# 	dg = session.DisplayGroup(name=DictKey , objectToCopy=dg)
# execfile('/home/cerecam/Desktop/GIT/PhD_PythonScripts/ImageCreationandPrint.py')