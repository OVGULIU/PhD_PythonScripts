"""
Created 29 June 2018

Function that draws mesh and deformed mesh given elemental connectiviity and nodal positions

abaqus viewer noGUI=/home/cerecam/Desktop/GIT/PhD_PythonScripts/MeshCreation.py
"""
import matplotlib.pyplot as plt
from odbAccess import *
from mpl_toolkits.mplot3d import axes3d


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


def mesh_maker(ica, position, plane):
    """
    Function to draw mesh of deformed and undeformed model
    :param ica: Interconnectivity array (list of list) giving element number and connected nodes, dim=0 = element number, dim=1 = nodes
    :param position_undef: nodal values of original position configuration
    :param position_def: nodal values of deformed configuration
    :param plane :: array definied which plane the slice is taken on [xy, yz, xz]
    :return: None
    """
    xy, yz, xz = plane
    if xy:
        node_set = [1, 2, 3, 4]
        line_data = [1, 1, 0]
    elif yz:
        node_set = [1, 4, 8, 5]
        line_data = [0, 1, 1]
    elif xz:
        node_set = [1, 5, 6, 2]
        line_data = [1, 0, 1]
    else:
        node_set = [0, 0, 0]
        line_data = [0, 0, 0]
    # ax = fig.add_subplot(111)
    for e in ica[1:]:
        x_line = []
        y_line = []
        z_line = []
        for n in node_set:
            x, y, z = position[int(e[n])]
            x_line.append(x)
            y_line.append(y)
            z_line.append(z)
        all_lines = [x_line, y_line, z_line]
        # print(all_lines)
        lines = []
        [lines.append(all_lines[count]+[all_lines[count][0]]) for count, i in enumerate(line_data) if i]
        # print(lines[0],lines[1])
        plt.plot(lines[0], lines[1],'b')



odbname = '/home/cerecam/Desktop/GP_BoundaryConditionTests/Voxel_stiff_both'
if odbname[-4:] != '.odb':
    odbname = odbname + '.odb'
odb = openOdb(odbname)
instances = odb.rootAssembly.instances[odb.rootAssembly.instances.keys()[-1]]
Deformed_nodes = odb.steps[odb.steps.keys()[-1]].frames[-1].fieldOutputs['U']
nodes_og = {}
nodes_def = {}
for n in instances.nodes:
    nodes_og[n.label] = n.coordinates

for n in Deformed_nodes.values:
    nodes_def[n.nodeLabel] = n.dataDouble

odb.close()

ele_connect = readinp('/home/cerecam/Desktop/GIT/PhD_PythonScripts/ElementsConTest.inp',0)
# nodes = readinp('/home/cerecam/Desktop/GP_BoundaryConditionTests/InputFiles/Nodes.inp', 1)

plt.figure()
mesh_maker(ele_connect, nodes_og, [0, 1, 0])
mesh_maker(ele_connect, nodes_def, [0, 1, 0])
plt.show()