'''
Data analysis of ligaments stress ditribution

===================================================================================
Check and change teh following variables:
	ligamentname
	Norm["ligamentname"]
	origin
	point1
	point2

crl+shift+v into terminal
abaqus viewer noGUI=/home/cerecam/Dropbox/Masters/PythonCodes/DefModePostProcess.py
===================================================================================
'''

def mag(x):
    """
    Function returnign the magnitude of a vector
    :param x: vector
    :return: magnitude of vector
    """
    return math.sqrt(sum(i ** 2 for i in x))


def dot_product(x, y):
    """
    Calculated the scalar product of two vectors
    :param x: vector
    :param y: vector
    :return: dot product
    """
    return np.dot(x, y)


def norm(x):
    """
    magnitude of Scalar product of vectors
    :param x:
    :return:
    """
    return math.sqrt(dot_product(x, x))


def normalize(x):
    return [x[i] / norm(x) for i in range(len(x))]


def writeFile(Data, filename, FirstLine, cwd):
    with open(cwd + odbname + '_' + ligamentname + filename + '.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(FirstLine)
        for key, value in Data.items():
            writer.writerow([key, value])


def BM(Q):
    """
    Calculated maximum bedning moment of a ligament
    :param Q:
    :return: Value of bendign moment (BendingMomnet) at multiple rotated values (RotatedVal)
    """
    BendingMoment = {}
    RotatedVal = {}
    BM_3D = [0, 0]
    for key, value in normals.items():
        Val = np.dot(Q, np.array(COORD_e[int(key) - 1]))
        RotatedVal[key] = Val[0:2]
        RotCentroid = np.dot(Q, np.array(Centroid))
        RotCentroid = RotCentroid[0:2]
        ##            abqPrint(RotCentroid)
        ##            abqPrint(RotatedVal)
        BendingMoment[key] = (normalstress[key] * Area[key] * (RotatedVal[key] - RotCentroid))
        BM_3D = BM_3D + (normalstress[key] * Area[key] * (RotatedVal[key] - RotCentroid))
    return BendingMoment, RotatedVal, BM_3D


def abaqusopen(filename):
    """
    open and retrive data from odb file
    :param filename:
    :return:
    """
    from odbAccess import openOdb
    odbname = filename + '.odb'
    odb = openOdb(odbname)
    assem = odb.rootAssembly
    stepKey = odb.steps.keys()
    steps = odb.steps[stepKey[-1]]
    frames = steps.frames[-1]
    FieldOut = frames.fieldOutputs

    return odb, assem, stepKey, steps, frames, FieldOut


from odbAccess import openOdb
import numpy as np
import csv, math, sys
from abaqusConstants import *
from math import pi

global normals
global Area
global normalvec
global normalstress
global shearstress
global FO
global angle
global ligamentname
global centroid
global odbname

# surfaces = {'F1': [1, 2, 3], 'F2': [1, 2, 4], 'F3': [2, 3, 4], 'F4': [1, 3, 4]}
surfaces = {'F1' : [1, 2, 3, 4], 'F2':[5, 6, 7, 8], 'F3' : [1, 8, 8, 4], 'F4' : [6, 2, 3, 7],
          'F5': [4, 8, 7, 3], 'F6' : [1, 5, 6, 2]}
axis = {'0': 'X', '1': 'Y', '2': 'Z'}

cwd = '/home/cerecam/Desktop/GP_BoundaryConditionTests/'
odbname = 'Test1_NoUEL'

ligvals = open(cwd + '/LigVals.txt', 'r')  # File containing Ligament name, origin, 2 points to define co-ord system and the face orientated
results = open(cwd + odbname + '.txt', 'w')
# File giving lig name, bendign moment at max angle, torque, normal stress, shear stress and area of ligament.
ligfile = ligvals.read()
ligfile = ligfile.split('\n')

for ligamentnumber in range(1):
    Norm = {}
    Coordnode = {}
    normals = {}
    Area = {}
    Centroid = []
    Rotation = {}
    Ligament_elements = []
    stresstens = {}
    tractionvec = {}

    ligamentname = 'Ligament' + str(ligamentnumber)
    for value in range(0, len(ligfile), 6):
        if ligfile[value].upper() == ligamentname.upper():
            print >> sys.__stdout__, (str(ligfile[value].upper()))
            origin = int(ligfile[value + 1][7:].strip())
            point1 = int(ligfile[value + 2][7:].strip())
            point2 = int(ligfile[value + 3][7:].strip())
            myface = str(ligfile[value+4][7:].strip())
            print >> sys.__stdout__, (str((origin, point1, point2, myface)))

    Norm[ligamentname] = [0, 0, 1]
    [ODB, assembly, Keys_steps, steps, frames, FO] = abaqusopen(cwd + odbname)
    myinstance = assembly.instances[assembly.instances.keys()[-1]]
    # Setting up no coord system and getting Transformed data (Sress, strain and Coords)
    NODEorigin = tuple(assembly.instances[assembly.instances.keys()[-1]].nodes[origin - 1].coordinates)
    NODEpoint1 = tuple(assembly.instances[assembly.instances.keys()[-1]].nodes[point1 - 1].coordinates)
    NODEpoint2 = tuple(assembly.instances[assembly.instances.keys()[-1]].nodes[point2 - 1].coordinates)
    NEWCSYS = ODB.rootAssembly.DatumCsysByThreePoints(name='NEW', coordSysType=CARTESIAN, origin=NODEorigin,
                                                      point1=NODEpoint1, point2=NODEpoint2)
    frame_val = ODB.steps[Keys_steps[-1]].frames[-1]
    FO_E = frame_val.fieldOutputs['E'].getTransformedField(NEWCSYS)
    E = [E_val.data for E_val in FO_E.values]
    FO_S = frame_val.fieldOutputs['S'].getTransformedField(NEWCSYS)
    S = [S_val.data for S_val in FO_S.values]
    FO_COORD = frame_val.fieldOutputs['Centroid'].getTransformedField(NEWCSYS)
    COORD_e = [COORD_val.data for COORD_val in FO_COORD.values]
    COORD_n = []
    for nodes in myinstance.nodes:
        if int(nodes.label) < 999990:
            intnode = [nodes.coordinates[0], nodes.coordinates[1],
                       nodes.coordinates[2]]  # Tuple of node data (node no., node x-coord, y-coord, z-coord)
            COORD_n.append(intnode)
            del intnode

    # with open(cwd + '/' + ligamentname.upper() + 'faces' + '.csv',
    #           'rb') as csv_file:
    #     readertwo = csv.reader(csv_file)
    #     myface = dict(readertwo)
    Ligament_elements = []
    Lig_ele_nodes = {}
    with open(cwd + '/' + ligamentname + '.inp', 'rb') as lig_file:
        lig_file.readline()
        lig_file.readline()
        for line in lig_file:
            Ligament_elements.append(line.split()[1])
            Lig_ele_nodes[line.split()[1]] = line.split()[3:]

    X = [COORD_e[int(i) - 1][0] for i in Ligament_elements]
    X = np.sort(X)
    Y = [COORD_e[int(i) - 1][1] for i in Ligament_elements]
    Y = np.sort(Y)
    Z = [COORD_e[int(i) - 1][2] for i in Ligament_elements]
    Z = np.sort(Z)

    Xmin = X[0]
    Xmax = X[-1]
    Ymin = Y[0]
    Ymax = Y[-1]
    Zmin = Z[0]
    Zmax = Z[-1]

    Centroid.append(Xmin + ((Xmax - Xmin) / 2))
    Centroid.append(Ymin + ((Ymax - Ymin) / 2))
    Centroid.append(Zmin + ((Zmax - Zmin) / 2))

    # Get elements on cross section of interest from save file (ligamentname+'faces.csv')
    normals2 = {}
    Area2 = {}
    for i in Ligament_elements:
        # Gets the connected nodes associated with required elements specified by the file ("ligamentname"+faces.csv)
        ConnectedNodes = Lig_ele_nodes[i]
        Ele_node_coords = []
        Ele_coords = []
        # Gets the co-ordinates of each node within those elements specified by the file ("ligamentname"+faces.csv)
        [Ele_node_coords.append(COORD_n[int(p) - 1]) for p in ConnectedNodes]
        eleNormal = {}
        FaceArea = {}
        # print >> sys.__stdout__, (str(Ele_node_coords[1]))
        # Calculation of normals of all surfaces
        value = surfaces[myface]
        surfacevec = []
        surfacevec.append(list(np.array(Ele_node_coords[value[0] - 1]) - np.array(Ele_node_coords[value[1] - 1])))
        surfacevec.append(list(np.array(Ele_node_coords[value[0] - 1]) - np.array(Ele_node_coords[value[2] - 1])))
        normaldir = np.cross(surfacevec[0], surfacevec[1])
        number = Norm[ligamentname].index(1)
        if float(normaldir[number]) < 0:
            normaldir = [float(x) * -1 for x in normaldir]
        normalmag = np.array(norm(normaldir))
        normals[i] = np.array([float(m) / normalmag for m in normaldir])
        Area[i] = normalmag / 2

    for key, value in normals.items():
        S_ele = S[int(key) - 1]
        stresstens[key] = np.array(
            [[S_ele[0], S_ele[3], S_ele[4]], [S_ele[3], S_ele[1], S_ele[5]], [S_ele[4], S_ele[5], S_ele[2]]])
        tractionvec[key] = np.dot(stresstens[key], normals[key]).T

    normalstress = {}
    N = Norm[ligamentname]
    for key, value in tractionvec.items():
        normalstress[key] = np.dot(value, N).T

    BM_Rot = {}
    maxBM = {}
    for angledeg in range(0, 180, 30):
        angle = angledeg * (pi / 180)
        if Norm[ligamentname][0] == 1:
            Q = [[1, 0, 0], [0, math.cos(angle), math.sin(angle)], [0, -math.sin(angle), math.cos(angle)]]
        if Norm[ligamentname][1] == 1:
            Q = [[math.cos(angle), 0, -math.sin(angle)], [0, 1, 0], [math.sin(angle), 0, math.cos(angle)]]
        if Norm[ligamentname][2] == 1:
            Q = [[math.cos(angle), math.sin(angle), 0], [-math.sin(angle), math.cos(angle), 0], [0, 0, 1]]
        _, _, BM_3D = BM(Q)
        BM_Rot[str(angle)] = BM_3D
        maxBM[str(angle)] = [np.amax(abs(BM_3D)), np.argmax(abs(BM_3D))]

    AngleBM = max(maxBM, key=lambda i: maxBM[i])
    angle = float(AngleBM)

    if Norm[ligamentname][0] == 1:
        Q = [[1, 0, 0], [0, math.cos(angle), math.sin(angle)], [0, -math.sin(angle), math.cos(angle)]]

    if Norm[ligamentname][1] == 1:
        Q = [[math.cos(angle), 0, -math.sin(angle)], [0, 1, 0], [math.sin(angle), 0, math.cos(angle)]]

    if Norm[ligamentname][2] == 1:
        Q = [[math.cos(angle), math.sin(angle), 0], [-math.sin(angle), math.cos(angle), 0], [0, 0, 1]]

    BMmatrix, Val, _ = BM(Q)

    Bmaxis = [values[maxBM[AngleBM][1]] for values in BMmatrix.values()]

    with open(cwd + odbname + '_' + ligamentname + 'Bending' + axis[
        str(maxBM[AngleBM][1])] + '.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([BM_3D[maxBM[AngleBM][1]], angle])
        for x, key in enumerate(BMmatrix):
            writer.writerow([key, Bmaxis[x], normalstress[key], Val[key][0], Val[key][1]])

    print >> sys.__stdout__, (str('\n'))
    print >> sys.__stdout__, (str( 'Bending Moment: ' + str(BM_3D[maxBM[AngleBM][1]]) + ' at angle: ' + str(float(AngleBM) * 180 / pi)))

    shearvec = {}
    for key, value in tractionvec.items():
        d = np.dot(value, N) / norm(N)
        p = np.array(d) * np.array(normalize(N))
        ShearMag = np.array(norm(value - p))
        shearvec[key] = np.array([i / ShearMag for i in (value - p)])

    Torque = {}
    PerpenVec = {}
    PXint = {}
    A = {}
    for key, value in normals.items():
        Val = np.array(COORD_e[int(key) - 1])
        PerpenPoint = Val + (np.dot((Centroid - Val), shearvec[key])) * shearvec[key]
        Vector = PerpenPoint - Centroid
        VecMag = np.array(norm(Vector))
        PerpenVec[key] = [i / VecMag for i in Vector]
        A[key] = PerpenPoint + 1000 * shearvec[key]
        PAint = (A[key] - Centroid)
        PAmag = np.array(norm(PAint))
        PA = np.array([(A[key][i] - Centroid[i]) / PAmag for i in range(len(A[key]))])
        PXint[key] = PerpenPoint - Centroid
        PXmag = np.array(norm(PXint[key]))
        PX = np.array([PXint[key][i] / PXmag for i in range(len(A[key]))])
        angle = np.cross(PA, PX)
        number = Norm[ligamentname].index(1)
        if angle[number] > 0:
            sign = 1
        else:
            sign = -1
        Rotation[key] = sign

    # Calculates Shear stress
    shearstress = {}
    for key, value in tractionvec.items():
        shearstress[key] = np.dot(value, shearvec[key]).T
        if Rotation[key] < 0:
            shearstress[key] = shearstress[key] * -1

    # Torque
    Torque = 0
    for key, value in shearstress.items():
        Torque = Torque + (value * Area[key] * np.array(norm(PXint[key])))
    print >> sys.__stdout__, (str('Torque ' + str(Torque)))

    # Shear Stress
    Shear = 0
    for key, value in shearstress.items():
        Shear = Shear + value * Area[key]
    print >> sys.__stdout__, (str('Shear ' + str(Shear)))

    # Normal Stress
    NormalS = 0
    for key, value in normalstress.items():
        NormalS = NormalS + value * Area[key]
    print >> sys.__stdout__, (str('Normal stress ' + str(NormalS)))

    # Normal Stress
    AreaTot = 0
    for key, value in Area.items():
        AreaTot = AreaTot + value

    writeFile(shearstress, 'ShearStress', [Shear], cwd)
    writeFile(normalstress, 'NormalStress', [NormalS], cwd)
    writeFile(shearvec, 'shearvec', [Torque], cwd)
    writeFile(tractionvec, 'trac', [], cwd)
    ##    writeFile(Area,'Areas',[AreaTot])
    print >> sys.__stdout__, (str('\n'))

    results.write(ligamentname + '\n')
    results.write(
        'Bending Moment: ' + str(BM_3D[maxBM[AngleBM][1]]) + ' at angle: ' + str(float(AngleBM) * 180 / pi) + '\n')
    results.write('Torque ' + str(Torque) + '\n')
    results.write('Normal stress ' + str(NormalS) + '\n')
    results.write('Shear ' + str(Shear) + '\n')
    results.write('Area ' + str(AreaTot) + '\n')
    results.write('\n')
