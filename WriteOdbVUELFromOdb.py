# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 12:04:48 2018

abaqus python /home/cerecam/Desktop/GIT/PhD_PythonScripts/WriteOdbVUELFromOdb.py

This script creates a 3D odb for a model that contains user defined elements.
It creates the following field outputs:
    - Displacement (U1,U2.U3, Magnitude) [NODAL]
    - Strain (E11,E22,E33,E12,E23,E13, Mises, Max/Mid and Min Principal ) [GAUSS POINT]
    - Stress (S11,S22,S33,S12,S23,S13, Mises, Max/Mid and Min Principal ) [GAUSS POINT]
    - Concentration (Co) [NODAL]
    - Electric Potential [GAUSS POINT]

Inputs to consider/change:
    - materialNames (list of strings of material names)
    - MatE (list of floats of Young's modulus of materials in materialNames)
    - Matmu (list of floats of Poisson's ratio of materials in materialNames)
    - cwd (current working directory i.e. where old odb and relevant .inp files are found and where new odb will be saved)
    - OldOdbName (odb of user definied elements)
    - ElementFiles (list of strings of location [cwd + filename] of input files containing each material elements nodal connectivity)
    - odbpath (path to and odb name of new odb to be created)
    - numIntervals (number of intervals that a display/frame must be created min=1 [one at beginning and on at analysisTime])
    
@author: cerecam_E Griffiths

* Note to print use:
# print >> sys.__stdout__, str()
"""
##
# import abaqus libraries


from odbAccess import *
from odbMaterial import *
from odbSection import *
from abaqusConstants import *
import numpy as np

# import python libraries
import sys, time, csv, os

def StressStrain(Ele_Con, Node_Vals, ElementType):
    if ElementType.strip() == 'C3D4':  # Tetrahedral element with one integration point
        GpCord = [[0.25, 0.25, 0.25]]

        dNdX1 = [[0.0] * int(ElementType[-1])] * len(GpCord)
        dNdX2 = [[0.0] * int(ElementType[-1])] * len(GpCord)
        dNdX3 = [[0.0] * int(ElementType[-1])] * len(GpCord)
        pNN = [[0.0] * int(ElementType[-1])] * len(GpCord)

        dNdXi1 = [-1.0, 1.0, 0.0, 0.0]
        dNdXi2 = [-1.0, 0.0, 1.0, 0.0]
        dNdXi3 = [-1.0, 0.0, 0.0, 1.0]

        for ip in range(len(GpCord)):
            xi1 = GpCord[ip][0]
            xi2 = GpCord[ip][1]
            xi3 = GpCord[ip][2]

            X1, X2, X3 = [], [], []
            for node in Ele_Con:
                X1.append(Node_Vals[str(node)][0])
                X2.append(Node_Vals[str(node)][1])
                X3.append(Node_Vals[str(node)][2])

            dX1dxi1 = np.dot(X1, dNdXi1)
            dX1dxi2 = np.dot(X1, dNdXi2)
            dX1dxi3 = np.dot(X1, dNdXi3)

            dX2dxi1 = np.dot(X2, dNdXi1)
            dX2dxi2 = np.dot(X2, dNdXi2)
            dX2dxi3 = np.dot(X2, dNdXi3)

            dX3dxi1 = np.dot(X3, dNdXi1)
            dX3dxi2 = np.dot(X3, dNdXi2)
            dX3dxi3 = np.dot(X3, dNdXi3)

            detJ = dX1dxi1 * dX2dxi2 * dX3dxi3 + dX2dxi1 * dX3dxi2 * dX1dxi3 + \
                   dX3dxi1 * dX1dxi2 * dX2dxi3 - dX1dxi3 * dX2dxi2 * dX3dxi1 - \
                   dX2dxi3 * dX3dxi2 * dX1dxi1 - dX3dxi3 * dX1dxi2 * dX2dxi1

            for nn in range(4):
                dNdX1[ip][nn] = 1.0 / detJ * ((dX2dxi2 * dX3dxi3 - dX3dxi2 * dX2dxi3) * dNdXi1[nn] +
                                              (dX3dxi1 * dX2dxi3 - dX2dxi1 * dX3dxi3) * dNdXi2[nn] +
                                              (dX2dxi1 * dX3dxi2 - dX3dxi1 * dX2dxi2) * dNdXi3[nn])
                dNdX2[ip][nn] = 1.0 / detJ * ((dX3dxi2 * dX1dxi3 - dX1dxi2 * dX3dxi3) * dNdXi1[nn] +
                                              (dX1dxi1 * dX3dxi3 - dX3dxi1 * dX1dxi3) * dNdXi2[nn] +
                                              (dX3dxi1 * dX1dxi2 - dX1dxi1 * dX3dxi2) * dNdXi3[nn])
                dNdX3[ip][nn] = 1.0 / detJ * ((dX1dxi2 * dX2dxi3 - dX2dxi2 * dX1dxi3) * dNdXi1[nn] +
                                              (dX2dxi1 * dX1dxi3 - dX1dxi1 * dX2dxi3) * dNdXi2[nn] +
                                              (dX1dxi1 * dX2dxi2 - dX2dxi1 * dX1dxi2) * dNdXi3[nn])

            pNN[ip] = [1.0 - xi1 - xi2 - xi3, xi1, xi2, xi3]

    elif ElementType.strip() == 'C3D8R':
        # Brick element with one integration point
        GpCord = [[0.0, 0.0, 0.0]]

        # Brick element with eight integration points
        # alpha =  np.sqrt(1.0/3.0)
        # GpCord = [[-alpha, -alpha, -alpha],
        #           [alpha, -alpha, -alpha],
        #           [alpha, alpha, -alpha],
        #           [alpha, alpha, alpha],
        #           [-alpha, alpha, alpha],
        #           [-alpha, -alpha, alpha],
        #           [-alpha, alpha, -alpha],
        #           [alpha, -alpha, alpha]]

        dNdX1 = [[0.0] * int(ElementType[-2])] * len(GpCord)
        dNdX2 = [[0.0] * int(ElementType[-2])] * len(GpCord)
        dNdX3 = [[0.0] * int(ElementType[-2])] * len(GpCord)
        pNN = [[0.0] * int(ElementType[-2])] * len(GpCord)

        for ip in range(len(GpCord)):
            xi1 = GpCord[ip][0]
            xi2 = GpCord[ip][1]
            xi3 = GpCord[ip][2]

            dNdXi1 = [-1.0 / 8.0 * (1 - xi2) * (1 - xi3), 1.0 / 8.0 * (1 - xi2) * (1 - xi3),
                      1.0 / 8.0 * (1 + xi2) * (1 - xi3), -1.0 / 8.0 * (1 + xi2) * (1 - xi3),
                      -1.0 / 8.0 * (1 - xi2) * (1 + xi3), 1.0 / 8.0 * (1 - xi2) * (1 + xi3),
                      1.0 / 8.0 * (1 + xi2) * (1 + xi3), -1.0 / 8.0 * (1 + xi2) * (1 + xi3)]

            dNdXi2 = [-1.0 / 8.0 * (1 - xi1) * (1 - xi3), -1.0 / 8.0 * (1 + xi1) * (1 - xi3),
                      1.0 / 8.0 * (1 + xi1) * (1 - xi3), 1.0 / 8.0 * (1 - xi1) * (1 - xi3),
                      -1.0 / 8.0 * (1 - xi1) * (1 + xi3), -1.0 / 8.0 * (1 + xi1) * (1 + xi3),
                      1.0 / 8.0 * (1 + xi1) * (1 + xi3), 1.0 / 8.0 * (1 - xi1) * (1 + xi3)]

            dNdXi3 = [-1.0 / 8.0 * (1 - xi1) * (1 - xi2), -1.0 / 8.0 * (1 + xi1) * (1 - xi2),
                      -1.0 / 8.0 * (1 + xi1) * (1 + xi2), -1.0 / 8.0 * (1 - xi1) * (1 + xi2),
                      1.0 / 8.0 * (1 - xi1) * (1 - xi2), 1.0 / 8.0 * (1 + xi1) * (1 - xi2),
                      1.0 / 8.0 * (1 + xi1) * (1 + xi2), 1.0 / 8.0 * (1 - xi1) * (1 + xi2)]

            X1, X2, X3 = [], [], []
            for node in Ele_Con:
                X1.append(Node_Vals[str(node)][0])
                X2.append(Node_Vals[str(node)][1])
                X3.append(Node_Vals[str(node)][2])

            dX1dxi1 = np.dot(X1, dNdXi1)
            dX1dxi2 = np.dot(X1, dNdXi2)
            dX1dxi3 = np.dot(X1, dNdXi3)

            dX2dxi1 = np.dot(X2, dNdXi1)
            dX2dxi2 = np.dot(X2, dNdXi2)
            dX2dxi3 = np.dot(X2, dNdXi3)

            dX3dxi1 = np.dot(X3, dNdXi1)
            dX3dxi2 = np.dot(X3, dNdXi2)
            dX3dxi3 = np.dot(X3, dNdXi3)

            J = np.array([[dX1dxi1, dX2dxi1, dX3dxi1],
                          [dX1dxi2, dX2dxi2, dX3dxi2],
                          [dX1dxi3, dX2dxi3, dX3dxi3]])
            detJ = np.linalg.det(J)

            for nn in range(8):
                dNdX1[ip][nn] = 1.0 / detJ * ((dX2dxi2 * dX3dxi3 - dX3dxi2 * dX2dxi3) * dNdXi1[nn] +
                                              (dX3dxi1 * dX2dxi3 - dX2dxi1 * dX3dxi3) * dNdXi2[nn] +
                                              (dX2dxi1 * dX3dxi2 - dX3dxi1 * dX2dxi2) * dNdXi3[nn])
                dNdX2[ip][nn] = 1.0 / detJ * ((dX3dxi2 * dX1dxi3 - dX1dxi2 * dX3dxi3) * dNdXi1[nn] +
                                              (dX1dxi1 * dX3dxi3 - dX3dxi1 * dX1dxi3) * dNdXi2[nn] +
                                              (dX3dxi1 * dX1dxi2 - dX1dxi1 * dX3dxi2) * dNdXi3[nn])
                dNdX3[ip][nn] = 1.0 / detJ * ((dX1dxi2 * dX2dxi3 - dX2dxi2 * dX1dxi3) * dNdXi1[nn] +
                                              (dX2dxi1 * dX1dxi3 - dX1dxi1 * dX2dxi3) * dNdXi2[nn] +
                                              (dX1dxi1 * dX2dxi2 - dX2dxi1 * dX1dxi2) * dNdXi3[nn])

            pNN[ip] = [1.0/8.0*(1-xi1)*(1-xi2)*(1-xi3), 1.0/8.0*(1+xi1)*(1-xi2)*(1-xi3),
                       1.0/8.0*(1+xi1)*(1+xi2)*(1-xi3), 1.0/8.0*(1-xi1)*(1+xi2)*(1-xi3),
                       1.0/8.0*(1-xi1)*(1-xi2)*(1+xi3), 1.0/8.0*(1+xi1)*(1-xi2)*(1+xi3),
                       1.0/8.0*(1+xi1)*(1+xi2)*(1+xi3), 1.0/8.0*(1-xi1)*(1+xi2)*(1+xi3)]

    return dNdX1, dNdX2, dNdX3, pNN
#
#########################################################
# Opening old odb file (pure VUEL file) to get nodal data:
#########################################################
#
materialNames = ["Polymer", "Gold"]
MatE = [1.951, 77.71]
Matmu = [0.3, 0.44]

# File names and locations for old odb
cwd = '/home/cerecam/Desktop/GP_BoundaryConditionTests/'
OldOdbNameNoext = 'Influx_full_exag25_kg50_doubleRho'
OldOdbName = OldOdbNameNoext + '.odb'
ElementFiles = [cwd + 'InputFiles/UserElements.inp',
                cwd + 'InputFiles/GoldElements.inp']  # Files with element connectivity description
Eletype = 'C3D8R'

# Accessing necessary objects in old odb                
oldOdb = openOdb(cwd + OldOdbName)
assembly = oldOdb.rootAssembly
instance = assembly.instances
I_final_Keys = instance.keys()[0]
myinstance = assembly.instances[instance.keys()[0]]
steps = oldOdb.steps[oldOdb.steps.keys()[-1]]
lastframe = steps.frames[-1]
analysisTime = steps.frames[-1].frameValue
FieldOutputs = lastframe.fieldOutputs

# node data read from old odb file
nodeData = []
nodeDict = {}
for nodes in myinstance.nodes:
	if int(nodes.label)<999990:
		intnode = (nodes.label, nodes.coordinates[0], nodes.coordinates[1],
				   nodes.coordinates[2])  # Tuple of node data (node no., node x-coord, y-coord, z-coord)
		nodeDict[str(nodes.label)] = (nodes.coordinates[0], nodes.coordinates[1], nodes.coordinates[2])
		nodeData.append(intnode)
		del intnode

# Creates an ODB
odbpath = cwd + OldOdbNameNoext + '_NoUEL.odb'
odb = Odb(name='WriteOdbTest', analysisTitle="ODB created by python script",
          description="Odb for showing VUEL data from a previous odb with no visualization elements",
          path=odbpath)

for num, mat in enumerate(materialNames):
    # Creates materials
    Material = odb.Material(name=mat)
    Material.Elastic(table=((MatE[num], Matmu[num]),))
    # polymerMaterial.Density(table=(  (1.47E-6),0))

    # Create sections
    section1 = odb.HomogeneousSolidSection(name=mat,
                                           material=mat)

# MODEL data, creation of part from node data
part1 = odb.Part(name='Part-1', embeddedSpace=THREE_D, type=DEFORMABLE_BODY)
part1.addNodes(nodeData=tuple(nodeData), nodeSetName='All_NODES')  # add nodes to part

# Element connectivity data read from .inp file (cannot use old odb as connectivity of user elements (RNODE3) not given)
EleList = []
EleListG = []
Ele_Con_Dict = {}
for num, Fname in enumerate(ElementFiles):
    elementData1 = []
    Efile = open(Fname)
    for line in Efile:
        if line[0] == '*':  # remove first line if element def present (i.e *element,type=...)
            pass
        else:
            newarray = map(int, line.split(','))  # Read first line and convert string to a list of integers
            elementData1.append(tuple(newarray))
            Ele_Con_Dict[newarray[0]] = [newarray[1:], num]
            EleList.append(newarray[0])
            if num==1:
				EleListG.append(newarray[0])
            del newarray
    elementData1 = tuple(elementData1)
    Efile.close()
    part1.addElements(elementData=elementData1, type=Eletype, elementSetName=materialNames[num])  # add elements to part
EleList = sorted(EleList)  # List of elements in ascending order
EleListG = sorted(EleListG)

for num, mat in enumerate(materialNames):
    # Creates materials
    Material = odb.Material(name=mat)
    Material.Elastic(table=((MatE[num], Matmu[num]),))
    # polymerMaterial.Density(table=(  (1.47E-6),0))

    # Create sections
    section1 = odb.HomogeneousSolidSection(name=mat,
                                           material=mat)

# Instance the part
instance1 = odb.rootAssembly.Instance(name='I_Cube', object=part1)

# Creating step and frame:

step1 = odb.Step(name='Step-1',
                 description='First step with displacement applied',
                 domain=TIME, timePeriod=1.0)

numIntervals = 50.0
frequency = analysisTime / numIntervals
FrameTime = 0.0

DispDataDict = {}
DispNodesDict = {}
TempDataDict = {}
TempNodesDict = {}
FieldValueDataDict = {}
FieldValueEleDict = {}
Efinal, S_totfinal = {}, {}
S_mechfinal, S_chemfinal, S_elecfinal = {}, {}, {}
count = 0

# Read electric potential values from inp file
# ElecFile = cwd + 'InputFiles/ElecPotentialsInitial.inp'
# ElecF = open(ElecFile, 'r')
# ElecData = [0] * len(nodeData)
# for line in ElecF:
#     newarray = map(str, line.split(','))
#     ElecData[int(newarray[0][-(len(newarray[0]) - len(OldOdbNameNoext) - 3):])] = float(newarray[1])

## FIELD DATA:
# Field data extraction from .odb file
# Data must be written as a tuple (tuple of data), if SCALAR tuple of data written as (scalar,);
#                                                  else if VECTOR (data1,data2,data3);
#                                                  else if TENSOR ((11,22,33,12,13,23),(...))
for MultiFrame in steps.frames:  # Loop over every frame captured in odb
    # for MultiFrame in [steps.frames[-1]]:
    # FrameTime= round(MultiFrame.frameValue,2)
    print >> sys.__stdout__, str(int(round(MultiFrame.frameValue)))
    print >> sys.__stdout__, str(FrameTime)
    print >> sys.__stdout__, str(int(round(MultiFrame.frameValue)) == FrameTime)
    if int(round(MultiFrame.frameValue)) == FrameTime:

        #########################################################################################
        # OLD ODB DATA EXTRACTION AND MANIPULATIONS
        #########################################################################################

        # Displacement data at nodes:
        Dispfield = MultiFrame.fieldOutputs['U']  # Extract disp field output object from old Odb
        DispData = []
        DispNodes = []
        for val in Dispfield.values:
            if int(val.nodeLabel) > len(nodeData):
                    pass
            else:
                DispNodes.append(val.nodeLabel) # Node label list
                DispData.append(tuple(val.dataDouble)) # Data at node
        #Add values to dictionary element with key = frameValue
        DispDataDict[int(round(MultiFrame.frameValue))] = tuple(DispData)
        DispNodesDict[int(round(MultiFrame.frameValue))] = tuple(DispNodes)

       # Temperature data at nodes:
        Tempfield = MultiFrame.fieldOutputs['NT11']    # Extract Temperature fieldOutput object from old Odb
        TempData = []
        TempNodes = []
        for val in Tempfield.values:
            if int(val.nodeLabel) > len(nodeData):
                    pass
            else:
                TempNodes.append(val.nodeLabel)  # Node label list
                TempData.append(tuple([val.dataDouble, ]))  # Data at node
        TempDataDict[int(round(MultiFrame.frameValue))] = tuple(TempData)
        TempNodesDict[int(round(MultiFrame.frameValue))] = tuple(TempNodes)

        Ee, Ss, Ee_principal, Ss_principal, V_mises = [], [], [], [], []
        Ss_mech, Ss_chem, Ss_elec, Ss_tot, EleListG = [], [], [], [], []
        ##################### Material Parameters #############################

        e_r = 1.0E3
        e_zero = 8.854E-3
        F = 9.6485337E+01
        Z = -1.0
        k = 5.0E+01
        csat = 1.3E-4

        #######################################################################

        for Ele_Label in EleList:

            Mat = Ele_Con_Dict[Ele_Label][1]  # Material of specified element
            Ele_con = Ele_Con_Dict[Ele_Label][0]  # Nodal connectivity of current element

            ## Elastic material parameters
            Gmod = 0.5 * MatE[Mat] / (1.0 + Matmu[Mat])
            lam = (MatE[Mat] * Matmu[Mat]) / ((1.0 + Matmu[Mat]) * (1.0 - 2.0 * Matmu[Mat]))

            Node_Vals = {}
            # Elec_Ele_Data = {}
            for i in Ele_con:  # Creates dictionary (key = node label) of nodal coordinates (X,Y,Z) for element in question (Ele_Con[0])
                Node_Vals[str(i)] = nodeDict[str(i)]
            #     Elec_Ele_Data[int(i)] = ElecData[int(i)]

            dNdX1, dNdX2, dNdX3, pNN = StressStrain(Ele_con, Node_Vals,
                                                    Eletype)  # Function defining shape functions and there derivatives
            H = [[0.0, 0.0, 0.0]*len(dNdX1)]
            # Conc_gp = [0.0]*len(dNdX1)
            # ElecField = np.array([0.0, 0.0, 0.0])
            Tarray = []
            for x, y in enumerate(Ele_con):
                for ip in range(len(dNdX1)):
                    Uarray = DispData[int(y) - 1]
                    H[ip] = H[ip] + np.outer(Uarray, np.array([dNdX1[ip][x], dNdX2[ip][x], dNdX3[ip][x]]))  # Grad(U)
                    if materialNames[Mat].lower() == 'polymer':
                        Tarray.append(float(TempDataDict[int(round(MultiFrame.frameValue))][int(y) - 1][0]))
                        # ElecField_int = [dNdX * Elec_Ele_Data[y] for dNdX in [dNdX1[ip][x], dNdX2[ip][x], dNdX3[ip][x]]]
                        # ElecField = ElecField - np.array(ElecField_int)

                    else:
                        Tarray.append(csat)

            Conc_gp = np.dot(np.array(pNN[0]), np.array(Tarray))

            # ElecDisp = np.array(e_zero * e_r * ElecField)
            Qf = F * (Z * Conc_gp + csat)
            if mat=='Gold':
				EleListG.append(Ele_Label)
				E = 0.5 * (np.transpose(H[0]) + H[0])  # Strain calculation at Gauss point
				#            if Ele_Label == 11150:
				#                print >> sys.__stdout__, str(E)

				S_mech = 2.0 * Gmod * E + lam * np.trace(E) * np.eye(3)  # Mecahnical stress calculation at Gauss point
				#S_chem = -((k * Qf) / Z) * np.eye(3)  # Chemical Stress calculation at Gauss point

				# S_elec = (1.0 / (e_zero * e_r)) * (
				#         (np.outer(ElecDisp, ElecDisp)) - 0.5 * (np.dot(ElecDisp, ElecDisp)) * np.eye(3))
				#            S_elec = np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
				# S_total = S_mech + S_chem + S_elec
				S_total = S_mech 
				Ee.append(tuple(E.flatten()[[0, 4, 8, 1, 2,
											 5]]))  # create vector format of strain data ('E11','E22','E33','E12','E13','E23')
				Ss_mech.append(tuple(S_mech.flatten()[[0, 4, 8, 1, 2,
													   5]]))  # create vector format of strain data ('S11','S22','S33','S12','S13','S23')
				#Ss_chem.append(tuple(S_chem.flatten()[[0, 4, 8, 1, 2, 5]]))
				# Ss_elec.append(tuple(S_elec.flatten()[[0, 4, 8, 1, 2, 5]]))
				Ss_tot.append(tuple(S_total.flatten()[[0, 4, 8, 1, 2, 5]]))
            # Store data for frame in question
        Efinal[int(round(MultiFrame.frameValue))] = tuple(Ee)
        #        print >> sys.__stdout__, str(Efinal)
        S_mechfinal[int(round(MultiFrame.frameValue))] = tuple(Ss_mech)
        #S_chemfinal[int(round(MultiFrame.frameValue))] = tuple(Ss_chem)
        # S_elecfinal[round(MultiFrame.frameValue, 3)] = tuple(Ss_elec)
        S_totfinal[int(round(MultiFrame.frameValue))] = tuple(Ss_tot)

        #########################################################################################
        # NEW ODB FIELD DATA CREATION
        #########################################################################################
        count += 1
        # Creation of displacement, cocentration, stress and strain field at n=numIntervals frames
        frame = step1.Frame(incrementNumber=count,
                            frameValue=FrameTime,
                            description='Results at time :\t ' + str(FrameTime) + 's')  # Creation of new frame
        # Add fieldoutput object to new odb
        newField = frame.FieldOutput(name='U',
                                     description='Displacement',
                                     type=VECTOR,
                                     validInvariants = (MAGNITUDE,))  # Creation of new field output object called 'U'

        # Add data to fieldoutput object
        newField.addData(position=NODAL,
                         instance=instance1,
                         labels=DispNodesDict[round(FrameTime, 3)],
                         data=DispDataDict[round(FrameTime, 3)])
        step1.setDefaultField(newField)

        # Add fieldoutput object to new odb
        newField2 = frame.FieldOutput(name='Co',
                                      description='Concentration',
                                      type=SCALAR)  # Creation of new field otput object called 'CONCENTRATION'
        # Add data to fieldoutput object
        newField2.addData(position=NODAL,
                          instance=instance1,
                          labels=TempNodesDict[round(FrameTime, 3)],
                          data=TempDataDict[round(FrameTime, 3)])
        # Add fieldoutput object to new odb
        newField3 = frame.FieldOutput(name='E',
                                      description='Small strain at gauss points',
                                      type=TENSOR_3D_FULL,
                                      componentLabels=('E11', 'E22', 'E33', 'E12', 'E13', 'E23'),
                                      validInvariants=(MISES, MAX_PRINCIPAL, MID_PRINCIPAL,
                                                       MIN_PRINCIPAL))  # Creation of new field otput object called 'STRAIN'

        # Add strain field
        newField3.addData(position=INTEGRATION_POINT,
                          instance=instance1,
                          labels=tuple(EleListG),
                          data=Efinal[round(FrameTime, 3)])

        # Add fieldoutput object to new odb
        newField4 = frame.FieldOutput(name='S',
                                      description='Total stress at gauss points',
                                      type=TENSOR_3D_FULL,
                                      componentLabels=('S11', 'S22', 'S33', 'S12', 'S13', 'S23'),
                                      validInvariants=(MISES, MAX_PRINCIPAL, MID_PRINCIPAL,
                                                       MIN_PRINCIPAL))  # Creation of new field otput object called 'STRESS'
        # Add Total stress field
        newField4.addData(position=INTEGRATION_POINT,
                          instance=instance1,
                          labels=tuple(EleListG),
                          data=S_totfinal[round(FrameTime, 3)])

        # Add data to fieldoutput object
        newField5 = frame.FieldOutput(name='S_m',
                                      description='Mechanical stress at gauss points',
                                      type=TENSOR_3D_FULL,
                                      componentLabels=('Sm11', 'Sm22', 'Sm33', 'Sm12', 'Sm13', 'Sm23'),
                                      validInvariants=(MISES, MAX_PRINCIPAL, MID_PRINCIPAL,
                                                       MIN_PRINCIPAL))  # Creation of new field otput object called 'STRESS'
        # Add mechanical stress field
        newField5.addData(position=INTEGRATION_POINT,
                          instance=instance1,
                          labels=tuple(EleListG),
                          data=S_mechfinal[round(FrameTime, 3)])

        ## Add data to fieldoutput object
        #newField6 = frame.FieldOutput(name='S_c',
                                      #description='Chemical stress at gauss points',
                                      #type=TENSOR_3D_FULL,
                                      #componentLabels=('Sc11', 'Sc22', 'Sc33', 'Sc12', 'Sc13', 'Sc23'),
                                      #validInvariants=(MISES, MAX_PRINCIPAL, MID_PRINCIPAL,
                                                       #MIN_PRINCIPAL))  # Creation of new field otput object called 'STRESS'
        ## Add chemical stress field
        #newField6.addData(position=INTEGRATION_POINT,
                          #instance=instance1,
                          #labels=tuple(EleList),
                          #data=S_chemfinal[round(FrameTime, 3)])

        # # Add data to fieldoutput object
        # newField7 = frame.FieldOutput(name='S_e',
        #                               description='Electrical stress at gauss points',
        #                               type=TENSOR_3D_FULL,
        #                               componentLabels=('Se11', 'Se22', 'Se33', 'Se12', 'Se13', 'Se23'),
        #                               validInvariants=(MISES, MAX_PRINCIPAL, MID_PRINCIPAL,
        #                                                MIN_PRINCIPAL))  # Creation of new field otput object called 'STRESS'

        # # Add electrical stress field
        # newField7.addData(position=INTEGRATION_POINT,
        #                   instance=instance1,
        #                   labels=tuple(EleList),
        #                   data=S_elecfinal[round(FrameTime, 3)])
        #

        #        # Add fieldoutput object to new odb
        #        newField8 = frame.FieldOutput(name='EP',
        #                                     description='Electric potential',
        #                                     type=SCALAR)
        #        # Add data to fieldoutput object
        #        newField8.addData(position=INTEGRATION_POINT,
        #                          instance=instance1,
        #                          labels=FieldValueEleDict[round(FrameTime,3)],
        #                          data=FieldValueDataDict[round(FrameTime,3)])

        step1.setDefaultField(newField)
        print >> sys.__stdout__, (
                'Displacement, temperature, electric potential, stress and strain  tensors created at ' + str(FrameTime) + 's')

        FrameTime += frequency
print >> sys.__stdout__, ('New odb: ' + odbpath)

oldOdb.close()
odb.save()
odb.close()
