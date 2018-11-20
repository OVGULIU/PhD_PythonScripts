"""
Created 19 October 2018

abaqus viewer noGUI=/home/cerecam/Desktop/GIT/PhD_PythonScripts/DataExtractionP2.py

File to extract data to be processed for results for paper on metal-polymer composites (P2)

Data to be extracted:
    - U3 displacement on the Z1 face for each constituent individually
    - Stress and strain data for each material type
"""

#import abaqus libraries
from odbAccess import *
from odbMaterial import *
from odbSection import *
from abaqusConstants import *

# import python libraries
import sys, time, csv, os, datetime
import numpy as np

Z1_Poly_file = 'Z1_POLY.csv'
Z1_Gold_file = 'Z1_Gold.csv'
GoldEle_file = 'GoldElements.csv'
PolyEle_file = 'PolymerElements.csv'
fOut = 'Disp_Values_20Nov'

# cwd = '/home/cerecam/Desktop/2M_96x96x96/2M_96x96x96_42PER/'
# cwd = '/home/cerecam/Desktop/2M_96x96x96/Old_NoUEL_odb/'
# odblist = ['S11300_0pnt25_NoUEL.odb']
# odblist = ['S1300_0pnt25_NoUEL2.odb', 'S2600_0pnt25_NoUEL.odb', 'S3300_0pnt25_NoUEL2.odb', 'S4150_0pnt25_NoUEL.odb']
# odblist = ['S1300_0pnt25_NoUEL2.odb', 'S2600_0pnt25_NoUEL.odb', 'S3300_0pnt25_NoUEL2.odb', 'S4150_0pnt25_NoUEL.odb',
#            'S5150_0pnt25_NoUEL.odb', 'S6150_0pnt25_NoUEL.odb', 'S7150_0pnt25_NoUEL.odb', 'S8150_0pnt25_NoUEL.odb',
#            'S9150_0pnt25_NoUEL.odb', 'S10150_0pnt25_NoUEL.odb', 'S11300_0pnt25_NoUEL.odb']
# odblist = ['S11300_0pnt25_NoUEL.odb']
# cwd = '/home/cerecam/Desktop/2M_96x96x96/2M_96x96x96_58PER/'
# odblist = ['S7_G58_5_NoUEL.odb']
# # odblist = ['S1_G58_NoUEL3.odb', 'S2_G58_NoUEL.odb']
# odblist = ['S1_G58_NoUEL3.odb', 'S2_G58_NoUEL.odb', 'S3_G58_NoUEL5.odb', 'S4_G58_NoUEL2.odb','S5_G58_8_NoUEL3.odb','S6_G58_20_NoUEL.odb','S7_G58_5_NoUEL.odb']

cwdDictionary = {}
cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/'] = ['S1_NoUEL.odb', 'S2_25PER_NoUEL.odb',
                                                                                 'S3_25PER_NoUEL.odb', 'S4_25PER_NoUEL.odb']

cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_34PER/'] = ['S1_34PER_NoUEL.odb', 'S2_34PER_NoUEL.odb',
                                                                                 'S3_34PER_NoUEL.odb', 'S4_34PER_NoUEL.odb']

cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER/'] = ['S1_42PER_NoUEL.odb', 'S2_42PER_NoUEL.odb',
                                                                                 'S3_42PER_NoUEL.odb']

cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_50PER/'] = ['S1_50PER_NoUEL.odb', 'S2_50PER_NoUEL.odb',
                                                                                 'S3_50PER_NoUEL.odb', 'S4_50PER_NoUEL.odb',
                                                                                 'S5_50PER_NoUEL.odb', 'S6_50PER_NoUEL.odb',
                                                                                 'S7_50PER_NoUEL.odb']

for cwd,odblist in cwdDictionary.items():
    with open(cwd + Z1_Gold_file, 'r') as fname:
        Z1_G = list(csv.reader(fname, delimiter=","))
    Z1_G = Z1_G[1:]

    with open(cwd + Z1_Poly_file, 'r') as fname:
        Z1_P = list(csv.reader(fname, delimiter=","))
    Z1_P = Z1_P[1:]

    with open(cwd + GoldEle_file, 'r') as fname:
        G_ele = list(csv.reader(fname, delimiter=","))

    with open(cwd + PolyEle_file, 'r') as fname:
        P_ele = list(csv.reader(fname, delimiter=","))

    numberElements = (len(G_ele) + len(P_ele))
    lastFrameValue = 0
    all_meandispP = []
    all_meandispG = []
    sav_gold = []
    eav_gold = []
    sav_poly = []
    eav_poly = []

    for odbName in odblist:
        print >> sys.__stdout__, 'Extracting data from : ' + str(odbName) + ' into ' + fOut
        odb = openOdb(cwd + odbName)
        # assembly = odb.rootAssembly
        # instance = assembly.instances
        # I_final_Keys = instance.keys()[-1]
        # myinstance = assembly.instances[instance.keys()[-1]]
        stepKeys = odb.steps.keys()
        allSteps = odb.steps
        lastStep = odb.steps[stepKeys[-1]]
        allFrames = lastStep.frames
        analysisTime = lastStep.frames[-1].frameValue
        for frame in allFrames:
            # extraction of displacement data
            disp = frame.fieldOutputs['U']
            disp_array = sorted([(dispVal.nodeLabel, dispVal.data) for dispVal in disp.values])
            dispListG = []
            for i in Z1_G:
                dispListG.append(disp_array[int(i[0]) - 1][1])

            dispListP = []
            for i in Z1_P:
                dispListP.append(disp_array[int(i[0]) - 1][1])

            meandispG = np.mean(np.array(dispListG), 0)
            meandispP = np.mean(np.array(dispListP), 0)



            all_meandispG.append((lastFrameValue + frame.frameValue, meandispG))
            all_meandispP.append((lastFrameValue + frame.frameValue, meandispP))

            print >> sys.__stdout__, 'frame ' + str(lastFrameValue + frame.frameValue) + ' complete'
            print >> sys.__stdout__, 'Average displacement of Polymer nodes: \t' + str(meandispP)
            print >> sys.__stdout__, 'Average displacement of Gold nodes: \t' + str(meandispG)

            # Extraction of volume averaged stress data
            stress = frame.fieldOutputs['S']
            stress_array = sorted([(stressVal.elementLabel,stressVal.data) for stressVal in stress.values])

            strain = frame.fieldOutputs['E']
            strain_array = sorted([(strainVal.elementLabel,strainVal.data) for strainVal in strain.values])

            stressListG = []
            strainListG = []
            for i in G_ele:
                stressListG.append(stress_array[int(i[0]) - 1][1])
                strainListG.append(strain_array[int(i[0]) - 1][1])

            stressListP = []
            strainListP = []
            for i in P_ele:
                stressListP.append(stress_array[int(i[0]) - 1][1])
                strainListP.append(strain_array[int(i[0]) - 1][1])

            Sav_G = np.sum(stressListG,0) / len(G_ele)
            Eav_G = np.sum(strainListG,0) / len(G_ele)
            Sav_P = np.sum(stressListP,0) / len(P_ele)
            Eav_P = np.sum(strainListP,0) / len(P_ele)

            sav_gold.append((lastFrameValue + frame.frameValue, Sav_G))
            eav_gold.append((lastFrameValue + frame.frameValue, Eav_G))
            sav_poly.append((lastFrameValue + frame.frameValue, Sav_P))
            eav_poly.append((lastFrameValue + frame.frameValue, Eav_P))


        lastFrameValue = lastFrameValue + frame.frameValue

    with open(cwd + fOut + '.csv', 'w') as fname:
        csvWriter = csv.writer(fname, delimiter=',')
        csvWriter.writerow(['Frame time: '] + [x[0] for x in all_meandispG])
        csvWriter.writerow(['X-Displacement gold: '] + [x[1][0] for x in all_meandispG])
        csvWriter.writerow(['X-Displacement polymer: '] + [x[1][0] for x in all_meandispP])
        csvWriter.writerow(['Y-Displacement gold: '] + [x[1][1] for x in all_meandispG])
        csvWriter.writerow(['Y-Displacement polymer: '] + [x[1][1] for x in all_meandispP])
        csvWriter.writerow(['Z-Displacement gold: '] + [x[1][2] for x in all_meandispG])
        csvWriter.writerow(['Z-Displacement polymer: '] + [x[1][2] for x in all_meandispP])
        csvWriter.writerow(['S-Volume average gold: '] + [list(x[1]) for x in sav_gold])
        csvWriter.writerow(['S-Volume average polymer: '] + [list(x[1]) for x in sav_poly])
        csvWriter.writerow(['E-Volume average gold: '] + [list(x[1]) for x in eav_gold])
        csvWriter.writerow(['E-Volume average polymer: '] + [list(x[1]) for x in eav_poly])
