"""
Created 19 October 2018

abaqus viewer noGUI=/home/cerecam/Desktop/GIT/PhD_PythonScripts/DataExtractionP2.py

File to extract data to be processed for results for paper on metal-polymer composites (P2)

Data to be extracted:
    - U3 displacement on the Z1 face for each constituent individually
    - Stress and strain data for each material type
"""

# import abaqus libraries
from odbAccess import *
from odbMaterial import *
from odbSection import *
from abaqusConstants import *

# import python libraries
import sys, time, csv, os, datetime
import numpy as np

# Z1_Poly_file = 'Z1_POLY.csv'
# Z1_Gold_file = 'Z1_Gold.csv'
#
# Z09_Poly_file = 'Z0pnt9_POLY_nodes.csv'
# Z09_Gold_file = 'Z0pnt9_GOLD_nodes.csv'
# Z09_file = 'All_Z_90.csv'
# X09_Poly_file = 'X_Half_NSet_Poly_90.csv'
# X09_Gold_file = 'X_Half_NSet_Gold_90.csv'
# X09_file = 'X_Half_NSet_All_90.csv'
# Y09_Poly_file = 'Y_Half_NSet_Poly_90.csv'
# Y09_Gold_file = 'Y_Half_NSet_Gold_90.csv'
# Y09_file = 'Y_Half_NSet_All_90.csv'

# Z90_file = 'All_90.csv'
# Z75_file = 'All_75.csv'
# Z50_file = 'All_50.csv'
# Z25_file = 'All_25.csv'
# Z10_file = 'All_10.csv'
# 
# Z90_P_file = 'Poly_90.csv'
# Z75_P_file = 'Poly_75.csv'
# Z50_P_file = 'Poly_50.csv'

Z30_file = 'All_50.csv'
Z30G_file = 'Gold_50.csv'
Z30P_file = 'Poly_50.csv'

X30_file = 'All_X_50.csv'
X30G_file = 'Gold_X_50.csv'
X30P_file = 'Poly_X_50.csv'

Y30_file = 'All_Y_50.csv'
Y30G_file = 'Gold_Y_50.csv'
Y30P_file = 'Poly_Y_50.csv'
# Z085_Poly_file = 'Z0pnt85_POLY_nodes.csv'
# Z085_Gold_file = 'Z0pnt85_GOLD_nodes.csv'
# Z08_Poly_file = 'Z0pnt8_POLY_nodes.csv'
# Z08_Gold_file = 'Z0pnt8_GOLD_nodes.csv'

# GoldEle_file = 'GoldElements.csv'
# PolyEle_file = 'PolymerElements.csv'
# GoldEle_file = 'Gold_75.csv'
# PolyEle_file = 'Poly_75.csv'
# Gold90Ele_file = 'Gold_EleSet_90.csv'
# Poly90Ele_file = 'Poly_EleSet_90.csv'

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
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/HPC_25PER/'] = [
#                                                                                             'S1_25PER_new3_NoUEL.odb',
#                                                                                            'S2_25PER_new3_NoUEL.odb',
#                                                                                            'S3_25PER_new3_NoUEL.odb',
#                                                                                            'S4_25PER_new3_NoUEL.odb',
#                                                                                            'S5_25PER_new3_NoUEL.odb',
#                                                                                            'S6_25PER_new3_NoUEL.odb',
#                                                                                            'S7_25PER_new3_NoUEL.odb',
#                                                                                            'S8_25PER_new3_NoUEL.odb']
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_34PER/HPC_34PER/'] = [
#                                                                                             'S1_34PER_new2_NoUEL2.odb',
#                                                                                            'S2_34PER_new2_NoUEL.odb',
#                                                                                            'S3_34PER_new2_NoUEL3.odb',
#                                                                                            'S4_34PER_new2_NoUEL.odb',
#                                                                                            'S5_34PER_new2_NoUEL.odb',
#                                                                                            'S6_34PER_new2_NoUEL.odb',
#                                                                                            'S7_34PER_new2_NoUEL2.odb']
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER/HPC_42PER/'] = [
#                                                                                         'S1_42PER_new2_NoUEL3.odb',
#                                                                                            'S2_42PER_new3_NoUEL.odb',
#                                                                                            'S3_42PER_new3_NoUEL.odb',
#                                                                                            'S4_42PER_new3_NoUEL.odb',
#                                                                                            'S5_42PER_new3_NoUEL.odb',
#                                                                                            'S6_42PER_new3_NoUEL.odb']
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_50PER/HPC_50PER/'] = [
#                                                                                         'S1_50PER_new3_NoUEL2.odb',
#                                                                                            'S2_50PER_new3_NoUEL.odb',
#                                                                                            'S3_50PER_new3_NoUEL.odb',
#                                                                                            'S4_50PER_new3_NoUEL.odb',
#                                                                                            'S5_50PER_new3_NoUEL.odb',
#                                                                                            'S6_50PER_new3_NoUEL.odb']
# #
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/NewDensitySims/'] = ['S1_25PER_2.odb','S2_25PER_2.odb','S3_25PER_2.odb','S4_25PER_2.odb','S5_25PER_2.odb','S6_25PER_2.odb']
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_34PER/NewDensitySims/'] = ['S1_34PER.odb', 'S2_34PER.odb', 'S3_34PER.odb', 'S4_34PER.odb', 'S5_34PER.odb', 'S6_34PER.odb']
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER/NewDensitySims/'] = ['S1_42PER.odb','S2_42PER.odb','S3_42PER.odb','S4_42PER.odb','S5_42PER.odb','S6_42PER.odb']
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_50PER/NewDensitySims/'] = ['S1_50PER.odb','S2_50PER.odb','S3_50PER.odb','S4_50PER.odb','S5_50PER.odb','S6_50PER.odb']
#
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/NewDensitySims/'] = ['S1_25PER_2_NoUEL.odb']
#
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/NewDensitySims/'] = ['S1_25PER_2_NoUEL.odb','S2_25PER_2_NoUEL.odb','S3_25PER_2_NoUEL.odb','S4_25PER_2_NoUEL.odb','S5_25PER_2_NoUEL.odb','S6_25PER_2_NoUEL.odb']
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_34PER/NewDensitySims/'] = ['S1_34PER_NoUEL.odb', 'S2_34PER_NoUEL.odb', 'S3_34PER_NoUEL.odb', 'S4_34PER_NoUEL.odb', 'S5_34PER_NoUEL.odb', 'S6_34PER_NoUEL.odb']
# cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER/NewDensitySims/'] = ['S1_42PER_NoUEL.odb','S2_42PER_NoUEL.odb','S3_42PER_NoUEL.odb','S4_42PER_NoUEL.odb','S5_42PER_NoUEL.odb','S6_42PER_NoUEL.odb']
cwdDictionary['/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_50PER/NewDensitySims/'] = ['S1_50PER_NoUEL.odb','S2_50PER_NoUEL.odb','S3_50PER_NoUEL.odb','S4_50PER_NoUEL.odb','S5_50PER_NoUEL.odb','S6_50PER_NoUEL.odb']

for cwd, odblist in cwdDictionary.items():
    fOut = 'Values_XYZdisp_50'

    # with open(cwd + Z09_Gold_file, 'r') as fname:
    #     Z09_G = list(csv.reader(fname, delimiter=","))
    # Z09_G = Z09_G[1:]

    # with open(cwd + Z09_Poly_file, 'r') as fname:
    #     Z09_P = list(csv.reader(fname, delimiter=","))
    # Z09_P = Z09_P[1:]

    # with open(cwd + Z09_file, 'r') as fname:
    #     Z09 = list(csv.reader(fname, delimiter=","))
    # Z09 = Z09[1:]

    # with open(cwd + X09_Gold_file, 'r') as fname:
    #     X09_G = list(csv.reader(fname, delimiter=","))
    # X09_G = X09_G[1:]

    # with open(cwd + X09_Poly_file, 'r') as fname:
    #     X09_P = list(csv.reader(fname, delimiter=","))
    # X09_P = X09_P[1:]

    # with open(cwd + X09_file, 'r') as fname:
    #     X09 = list(csv.reader(fname, delimiter=","))
    # X09 = X09[1:]

    # with open(cwd + Y09_Gold_file, 'r') as fname:
    #     Y09_G = list(csv.reader(fname, delimiter=","))
    # Y09_G = Y09_G[1:]

    # with open(cwd + Y09_Poly_file, 'r') as fname:
    #     Y09_P = list(csv.reader(fname, delimiter=","))
    # Y09_P = Y09_P[1:]

    # with open(cwd + Y09_file, 'r') as fname:
    #     Y09 = list(csv.reader(fname, delimiter=","))
    # Y09 = Y09[1:]

    # with open(cwd + Z085_Gold_file, 'r') as fname:
    #     Z085_G = list(csv.reader(fname, delimiter=","))
    # Z085_G = Z085_G[1:]

    # with open(cwd + Z085_Poly_file, 'r') as fname:
    #     Z085_P = list(csv.reader(fname, delimiter=","))
    # Z085_P = Z085_P[1:]
    # 
    # with open(cwd + Z08_Gold_file, 'r') as fname:
    #     Z08_G = list(csv.reader(fname, delimiter=","))
    # Z08_G = Z08_G[1:]
    # 
    # with open(cwd + Z08_Poly_file, 'r') as fname:
    #     Z08_P = list(csv.reader(fname, delimiter=","))
    # Z08_P = Z08_P[1:]

    # with open(cwd + Z1_Gold_file, 'r') as fname:
    #     Z1_G = list(csv.reader(fname, delimiter=","))
    # Z1_G = Z1_G[1:]

    # with open(cwd + Z90_file, 'r') as fname:
    #     Z_90 = list(csv.reader(fname, delimiter=","))
    # Z_90 = Z_90[1:]
    # 
    # with open(cwd + Z75_file, 'r') as fname:
    #     Z_75 = list(csv.reader(fname, delimiter=","))
    # Z_75 = Z_75[1:]
    # 
    # with open(cwd + Z50_file, 'r') as fname:
    #     Z_50 = list(csv.reader(fname, delimiter=","))
    # Z_50 = Z_50[1:]
    # 
    # with open(cwd + Z25_file, 'r') as fname:
    #     Z_25 = list(csv.reader(fname, delimiter=","))
    # Z_25 = Z_25[1:]
    # 
    # with open(cwd + Z10_file, 'r') as fname:
    #     Z_10 = list(csv.reader(fname, delimiter=","))
    # Z_10 = Z_10[1:]
    # 
    # with open(cwd + Z90_P_file, 'r') as fname:
    #     Z90_P = list(csv.reader(fname, delimiter=","))
    # Z90_P = Z90_P[1:]
    # 
    # with open(cwd + Z75_P_file, 'r') as fname:
    #     Z75_P = list(csv.reader(fname, delimiter=","))
    # Z75_P = Z75_P[1:]
    # 
    # with open(cwd + Z50_P_file, 'r') as fname:
    #     Z50_P = list(csv.reader(fname, delimiter=","))
    # Z50_P = Z50_P[1:]

    with open(cwd + Z30_file, 'r') as fname:
        Z30 = list(csv.reader(fname, delimiter=","))
    Z30 = Z30[1:]

    with open(cwd + Z30P_file, 'r') as fname:
        Z30_P = list(csv.reader(fname, delimiter=","))
    Z30_P = Z30_P[1:]

    with open(cwd + Z30G_file, 'r') as fname:
        Z30_G = list(csv.reader(fname, delimiter=","))
    Z30_G = Z30_G[1:]

    with open(cwd + X30_file, 'r') as fname:
        X30 = list(csv.reader(fname, delimiter=","))
    X30 = X30[1:]

    with open(cwd + X30P_file, 'r') as fname:
        X30_P = list(csv.reader(fname, delimiter=","))
    X30_P = X30_P[1:]

    with open(cwd + X30G_file, 'r') as fname:
        X30_G = list(csv.reader(fname, delimiter=","))
    X30_G = X30_G[1:]

    with open(cwd + Y30_file, 'r') as fname:
        Y30 = list(csv.reader(fname, delimiter=","))
    Y30 = Y30[1:]

    with open(cwd + Y30P_file, 'r') as fname:
        Y30_P = list(csv.reader(fname, delimiter=","))
    Y30_P = Y30_P[1:]

    with open(cwd + Y30G_file, 'r') as fname:
        Y30_G = list(csv.reader(fname, delimiter=","))
    Y30_G = Y30_G[1:]

    # with open(cwd + GoldEle_file, 'r') as fname:
    #     G_ele = list(csv.reader(fname, delimiter=","))
    # 
    # with open(cwd + PolyEle_file, 'r') as fname:
    #     P_ele = list(csv.reader(fname, delimiter=","))

    # with open(cwd + Gold90Ele_file, 'r') as fname:
    #     G_90ele = list(csv.reader(fname, delimiter=","))
    #
    # with open(cwd + Poly90Ele_file, 'r') as fname:
    #     P_90ele = list(csv.reader(fname, delimiter=","))
    #
    # numberElements09 = (len(G_90ele) + len(P_90ele))
    lastFrameValue = 0
    # all_meandispP09 = []
    # all_meandispG09 = []
    # all_meandispZ09 = []
    # all_meandispPX09 = []
    # all_meandispGX09 = []
    # all_meandispX09 = []
    # all_meandispPY09 = []
    # all_meandispGY09 = []
    # all_meandispY09 = []
    # 
    # 
    # all_meandisp90 = []
    # all_meandisp75 = []
    # all_meandisp50 = []
    # all_meandisp25 = []
    # all_meandisp10 = []
    # all_meanconc09 = [] 
    # all_meanconc90 = []
    # all_meanconc75 = []
    # all_meanconc50 = [] 

    all_meandispZ30 = []
    all_meandispZ30_P = []
    all_meandispZ30_G = []
    all_meandispX30 = []
    all_meandispX30_P = []
    all_meandispX30_G = []
    all_meandispY30 = []
    all_meandispY30_P = []
    all_meandispY30_G = []
    all_meanconc30 = []
    # all_meandispP085 = []
    # all_meandispG085 = []
    # all_meanconc085 = []
    # all_meandispP08 = []
    # all_meandispG08 = []
    # all_meanconc08 = []
    # sav_gold = []
    # eav_gold = []
    # sav_poly = []
    # eav_poly = []
    # sav_gold90 = []
    # eav_gold90 = []
    # sav_poly90 = []
    # eav_poly90 = []
    FrameValue = []

    for odbName in odblist:
        print >> sys.__stdout__, 'Extracting data from : ' + str(odbName) + ' into ' + fOut
        # odb = openOdb(cwd + 'NoUEL_ODBs/' + odbName)
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
            # disp_array = sorted([(dispVal.nodeLabel, dispVal.data) for dispVal in disp.values])

            # dispListG09 = []
            # for i in Z09_G:
            #     dispListG09.append(disp_array[int(i[0]) - 1][1])
            #
            # dispListP09 = []
            # for i in Z09_P:
            #     dispListP09.append(disp_array[int(i[0]) - 1][1])

            # dispListZ09 = []
            # for i in Z09:
            #     dispListZ09.append(disp_array[int(i[0]) - 1][1])

            # dispListGX09 = []
            # for i in X09_G:
            #     dispListGX09.append(disp_array[int(i[0]) - 1][1])
            #
            # dispListPX09 = []
            # for i in X09_P:
            #     dispListPX09.append(disp_array[int(i[0]) - 1][1])

            # dispListX09 = []
            # for i in X09:
            #     dispListX09.append(disp_array[int(i[0]) - 1][1])

            # dispListGY09 = []
            # for i in Y09_G:
            #     dispListGY09.append(disp_array[int(i[0]) - 1][1])
            #
            # dispListPY09 = []
            # for i in Y09_P:
            #     dispListPY09.append(disp_array[int(i[0]) - 1][1])

            # dispListY09 = []
            # for i in Y09:
                # dispListY09.append(disp_array[int(i[0]) - 1][1])

            # meandispG09 = np.mean(np.array(dispListG09), 0)
            # meandispP09 = np.mean(np.array(dispListP09), 0)
            # meandispZ09 = np.mean(np.array(dispListZ09), 0)
            # meandispGX09 = np.mean(np.array(dispListGX09), 0)
            # meandispPX09 = np.mean(np.array(dispListPX09), 0)
            # meandispX09 = np.mean(np.array(dispListX09), 0)
            # meandispGY09 = np.mean(np.array(dispListGY09), 0)
            # meandispPY09 = np.mean(np.array(dispListPY09), 0)
            # meandispY09 = np.mean(np.array(dispListY09), 0)

            # all_meandispG09.append((lastFrameValue + frame.frameValue, meandispG09))
            # all_meandispP09.append((lastFrameValue + frame.frameValue, meandispP09))
            # all_meandispZ09.append((lastFrameValue + frame.frameValue, meandispZ09))
            # all_meandispGX09.append((lastFrameValue + frame.frameValue, meandispGX09))
            # all_meandispPX09.append((lastFrameValue + frame.frameValue, meandispPX09))
            # all_meandispX09.append((lastFrameValue + frame.frameValue, meandispX09))
            # all_meandispGY09.append((lastFrameValue + frame.frameValue, meandispGY09))
            # all_meandispPY09.append((lastFrameValue + frame.frameValue, meandispPY09))
            # all_meandispY09.append((lastFrameValue + frame.frameValue, meandispY09))

            # dispListZ30 = []
            # for i in Z30:
            #     dispListZ30.append(disp_array[int(i[0]) - 1][1])
            #
            #
            # meandispZ30= np.mean(np.array(dispListZ30), 0)
            #
            # all_meandispZ30.append((lastFrameValue + frame.frameValue, meandispZ30))
            #
            # dispListZ30_P = []
            # for i in Z30_P:
            #     dispListZ30_P.append(disp_array[int(i[0]) - 1][1])
            #
            #
            # meandispZ30_P= np.mean(np.array(dispListZ30_P), 0)
            #
            # all_meandispZ30_P.append((lastFrameValue + frame.frameValue, meandispZ30_P))
            #
            # dispListZ30_G = []
            # for i in Z30_G:
            #     dispListZ30_G.append(disp_array[int(i[0]) - 1][1])
            #
            #
            # meandispZ30_G= np.mean(np.array(dispListZ30_G), 0)
            #
            # all_meandispZ30_G.append((lastFrameValue + frame.frameValue, meandispZ30_G))
            #
            # dispListX30 = []
            # for i in X30:
            #     dispListX30.append(disp_array[int(i[0]) - 1][1])
            #
            #
            # meandispX30= np.mean(np.array(dispListX30), 0)
            #
            # all_meandispX30.append((lastFrameValue + frame.frameValue, meandispX30))
            #
            # dispListX30_P = []
            # for i in X30_P:
            #     dispListX30_P.append(disp_array[int(i[0]) - 1][1])
            #
            #
            # meandispX30_P= np.mean(np.array(dispListX30_P), 0)
            #
            # all_meandispX30_P.append((lastFrameValue + frame.frameValue, meandispX30_P))
            #
            # dispListX30_G = []
            # for i in X30_G:
            #     dispListX30_G.append(disp_array[int(i[0]) - 1][1])
            #
            #
            # meandispX30_G= np.mean(np.array(dispListX30_G), 0)
            #
            # all_meandispX30_G.append((lastFrameValue + frame.frameValue, meandispX30_G))
            #
            # dispListY30 = []
            # for i in Y30:
            #     dispListY30.append(disp_array[int(i[0]) - 1][1])
            #
            #
            # meandispY30= np.mean(np.array(dispListY30), 0)
            #
            # all_meandispY30.append((lastFrameValue + frame.frameValue, meandispY30))
            #
            # dispListY30_P = []
            # for i in Y30_P:
            #     dispListY30_P.append(disp_array[int(i[0]) - 1][1])
            #
            #
            # meandispY30_P= np.mean(np.array(dispListY30_P), 0)
            #
            # all_meandispY30_P.append((lastFrameValue + frame.frameValue, meandispY30_P))
            #
            # dispListY30_G = []
            # for i in Y30_G:
            #     dispListY30_G.append(disp_array[int(i[0]) - 1][1])
            #
            #
            # meandispY30_G= np.mean(np.array(dispListY30_G), 0)
            #
            # all_meandispY30_G.append((lastFrameValue + frame.frameValue, meandispY30_G))

            # dispList90 = []
            # for i in Z_90:
            #     dispList90.append(disp_array[int(i[0]) - 1][1])
            # 
            # 
            # meandisp90= np.mean(np.array(dispList90), 0)
            # 
            # all_meandisp90.append((lastFrameValue + frame.frameValue, meandisp90))
            # 
            # dispList75 = []
            # for i in Z_75:
            #     dispList75.append(disp_array[int(i[0]) - 1][1])
            # 
            # 
            # meandisp75= np.mean(np.array(dispList75), 0)
            # 
            # all_meandisp75.append((lastFrameValue + frame.frameValue, meandisp75))
            # 
            # dispList50 = []
            # for i in Z_50:
            #     dispList50.append(disp_array[int(i[0]) - 1][1])
            # 
            # 
            # meandisp50= np.mean(np.array(dispList50), 0)
            # 
            # all_meandisp50.append((lastFrameValue + frame.frameValue, meandisp50))
            # 
            # dispList25 = []
            # for i in Z_25:
            #     dispList25.append(disp_array[int(i[0]) - 1][1])
            # 
            # 
            # meandisp25= np.mean(np.array(dispList25), 0)
            # 
            # all_meandisp25.append((lastFrameValue + frame.frameValue, meandisp25))
            # 
            # dispList10 = []
            # for i in Z_10:
            #     dispList10.append(disp_array[int(i[0]) - 1][1])
            # 
            # 
            # meandisp10= np.mean(np.array(dispList10), 0)
            # 
            # all_meandisp10.append((lastFrameValue + frame.frameValue, meandisp10))

            # dispListG08 = []
            # for i in Z08_G:
            #     dispListG08.append(disp_array[int(i[0]) - 1][1])
            #
            # dispListP08 = []
            # for i in Z08_P:
            #     dispListP08.append(disp_array[int(i[0]) - 1][1])
            #
            # meandispG08 = np.mean(np.array(dispListG08), 0)
            # meandispP08 = np.mean(np.array(dispListP08), 0)
            #
            # all_meandispG08.append((lastFrameValue + frame.frameValue, meandispG08))
            # all_meandispP08.append((lastFrameValue + frame.frameValue, meandispP08))

            # extraction of concentration data
            conc = frame.fieldOutputs['C']
            # conc = frame.fieldOutputs['NT11']
            conc_array = sorted([(concVal.nodeLabel, concVal.data) for concVal in conc.values])
            #
            # concList09 = []
            # for i in Z09_P:
            #     concList09.append(conc_array[int(i[0]) - 1][1])
            #
            # meanconc09 = np.mean(np.array(concList09), 0)
            #
            # all_meanconc09.append((lastFrameValue + frame.frameValue, meanconc09))
            
            concList30 = []
            for i in Z30_P:
                concList30.append(conc_array[int(i[0]) - 1][1])

            meanconc30 = np.mean(np.array(concList30), 0)

            all_meanconc30.append((lastFrameValue + frame.frameValue, meanconc30))
            
            # concList75 = []
            # for i in Z75_P:
            #     concList75.append(conc_array[int(i[0]) - 1][1])
            # 
            # meanconc75 = np.mean(np.array(concList75), 0)
            # 
            # all_meanconc75.append((lastFrameValue + frame.frameValue, meanconc75))
            # 
            # concList50 = []
            # for i in Z50_P:
            #     concList50.append(conc_array[int(i[0]) - 1][1])
            # 
            # meanconc50 = np.mean(np.array(concList50), 0)
            # 
            # all_meanconc50.append((lastFrameValue + frame.frameValue, meanconc50))

            # concList08 = []
            # for i in Z08_P:
            #     concList08.append(conc_array[int(i[0]) - 1][1])
            #
            # meanconc08 = np.mean(np.array(concList08), 0)
            #
            # all_meanconc08.append((lastFrameValue + frame.frameValue, meanconc08))
            #
            print >> sys.__stdout__, 'frame ' + str(lastFrameValue + frame.frameValue) + ' complete'
            FrameValue.append(lastFrameValue + frame.frameValue)
            # print >> sys.__stdout__, 'Average displacement of Polymer nodes (X-DIRECTION, half RVE): \t' + str(meandispPX09[0])
            # print >> sys.__stdout__, 'Average displacement of Gold nodes (X-DIRECTION, half RVE): \t' + str(meandispGX09[0])
            # print >> sys.__stdout__, 'Average displacement of Polymer nodes (Y-DIRECTION, half RVE): \t' + str(meandispPY09[1])
            # print >> sys.__stdout__, 'Average displacement of Gold nodes (Y-DIRECTION, half RVE): \t' + str(meandispGY09[1])
            # print >> sys.__stdout__, 'Average displacement of Polymer nodes (Z-DIRECTION): \t' + str(meandispP09[2])
            # print >> sys.__stdout__, 'Average displacement of Gold nodes (Z-DIRECTION): \t' + str(meandispG09[2])
            # print >> sys.__stdout__, 'Average Concentration: \t' + str(meanconc09)

            # Extraction of volume averaged stress data
            # stress = frame.fieldOutputs['S']
            # stress_array = sorted([(stressVal.elementLabel, stressVal.data) for stressVal in stress.values])
            # 
            # strain = frame.fieldOutputs['E']
            # strain_array = sorted([(strainVal.elementLabel, strainVal.data) for strainVal in strain.values])
            # 
            # stressListG = []
            # strainListG = []
            # for i in G_ele:
            #     stressListG.append(stress_array[int(i[0]) - 1][1])
            #     strainListG.append(strain_array[int(i[0]) - 1][1])
            # 
            # stressListP = []
            # strainListP = []
            # for i in P_ele:
            #     stressListP.append(stress_array[int(i[0]) - 1][1])
            #     strainListP.append(strain_array[int(i[0]) - 1][1])
            # 
            # Sav_G = np.sum(stressListG, 0) / len(G_ele)
            # Eav_G = np.sum(strainListG, 0) / len(G_ele)
            # Sav_P = np.sum(stressListP, 0) / len(P_ele)
            # Eav_P = np.sum(strainListP, 0) / len(P_ele)
            # 
            # sav_gold.append((lastFrameValue + frame.frameValue, Sav_G))
            # eav_gold.append((lastFrameValue + frame.frameValue, Eav_G))
            # sav_poly.append((lastFrameValue + frame.frameValue, Sav_P))
            # eav_poly.append((lastFrameValue + frame.frameValue, Eav_P))

            # # Extraction of volume averaged stress data
            # stress = frame.fieldOutputs['S']
            # stress_array = sorted([(stressVal.elementLabel, stressVal.data) for stressVal in stress.values])
            #
            # strain = frame.fieldOutputs['E']
            # strain_array = sorted([(strainVal.elementLabel, strainVal.data) for strainVal in strain.values])
            #
            # stressListG = []
            # strainListG = []
            # for i in G_90ele:
            #     stressListG.append(stress_array[int(i[0]) - 1][1])
            #     strainListG.append(strain_array[int(i[0]) - 1][1])
            #
            # stressListP = []
            # strainListP = []
            # for i in P_90ele:
            #     stressListP.append(stress_array[int(i[0]) - 1][1])
            #     strainListP.append(strain_array[int(i[0]) - 1][1])
            #
            # Sav_G = np.sum(stressListG, 0) / len(G_90ele)
            # Eav_G = np.sum(strainListG, 0) / len(G_90ele)
            # Sav_P = np.sum(stressListP, 0) / len(P_90ele)
            # Eav_P = np.sum(strainListP, 0) / len(P_90ele)
            #
            # sav_gold90.append((lastFrameValue + frame.frameValue, Sav_G))
            # eav_gold90.append((lastFrameValue + frame.frameValue, Eav_G))
            # sav_poly90.append((lastFrameValue + frame.frameValue, Sav_P))
            # eav_poly90.append((lastFrameValue + frame.frameValue, Eav_P))

        lastFrameValue = lastFrameValue + frame.frameValue
        odb.close()

    with open(cwd + fOut + '.csv', 'w') as fname:
        csvWriter = csv.writer(fname, delimiter=',')
        csvWriter.writerow(['Frame time: '] + [_ for _ in FrameValue])
        # csvWriter.writerow(['X-Displacement gold 90%: '] + [x[1][0] for x in all_meandispGX09])
        # csvWriter.writerow(['X-Displacement polymer 90%: '] + [x[1][0] for x in all_meandispPX09])
        # csvWriter.writerow(['X-Displacement all 90%: '] + [x[1][0] for x in all_meandispX09])
        # csvWriter.writerow(['Y-Displacement gold 90%: '] + [x[1][1] for x in all_meandispGY09])
        # csvWriter.writerow(['Y-Displacement polymer 90%: '] + [x[1][1] for x in all_meandispPY09])
        # csvWriter.writerow(['Y-Displacement all 90%: '] + [x[1][1] for x in all_meandispY09])
        # csvWriter.writerow(['Z-Displacement gold 90%: '] + [x[1][2] for x in all_meandispG09])
        # csvWriter.writerow(['Z-Displacement polymer 90%: '] + [x[1][2] for x in all_meandispP09])
        # csvWriter.writerow(['Z-Displacement all 90%: '] + [x[1][2] for x in all_meandispZ09])
        # csvWriter.writerow(['S-Volume average gold: '] + [list(x[1]) for x in sav_gold])
        # csvWriter.writerow(['S-Volume average polymer: '] + [list(x[1]) for x in sav_poly])
        # csvWriter.writerow(['E-Volume average gold: '] + [list(x[1]) for x in eav_gold])
        # csvWriter.writerow(['E-Volume average polymer: '] + [list(x[1]) for x in eav_poly])
        # csvWriter.writerow(['S-Volume average gold (90 % RVE): '] + [list(x[1]) for x in sav_gold90])
        # csvWriter.writerow(['S-Volume average polymer (90 % RVE): '] + [list(x[1]) for x in sav_poly90])
        # csvWriter.writerow(['E-Volume average gold (90 % RVE): '] + [list(x[1]) for x in eav_gold90])
        # csvWriter.writerow(['E-Volume average polymer (90 % RVE): '] + [list(x[1]) for x in eav_poly90])
        # csvWriter.writerow(['Concentration polymer 90%: '] + [x[1] for x in all_meanconc09])

        # csvWriter.writerow(['X-Displacement gold 100% '] + [x[1][0] for x in all_meandispG085])
        # csvWriter.writerow(['X-Displacement polymer 100%: '] + [x[1][0] for x in all_meandispP085])
        # csvWriter.writerow(['Y-Displacement gold 100%: '] + [x[1][1] for x in all_meandispG085])
        # csvWriter.writerow(['Y-Displacement polymer 100%: '] + [x[1][1] for x in all_meandispP085])
        # csvWriter.writerow(['Z-Displacement gold 100%: '] + [x[1][2] for x in all_meandispG085])
        # csvWriter.writerow(['Z-Displacement polymer 100%: '] + [x[1][2] for x in all_meandispP085])
        # csvWriter.writerow(['Concentration polymer 100%: '] + [x[1] for x in all_meanconc085])
        # 
        # csvWriter.writerow(['Z-Displacement 90%: '] + [x[1][2] for x in all_meandisp90])
        # csvWriter.writerow(['Z-Displacement 75%: '] + [x[1][2] for x in all_meandisp75])
        # csvWriter.writerow(['Z-Displacement 50%: '] + [x[1][2] for x in all_meandisp50])
        # csvWriter.writerow(['Z-Displacement 25%: '] + [x[1][2] for x in all_meandisp25])
        # csvWriter.writerow(['Z-Displacement 10%: '] + [x[1][2] for x in all_meandisp10])
        # csvWriter.writerow(['Concentration 90%: '] + [x[1] for x in all_meanconc90])
        # csvWriter.writerow(['Concentration 75%: '] + [x[1] for x in all_meanconc75])
        # csvWriter.writerow(['Concentration 50%: '] + [x[1] for x in all_meanconc50])

        csvWriter.writerow(['X-Displacement 50%: '] + [x[1][0] for x in all_meandispX30])
        csvWriter.writerow(['X-Displacement Poly 50%: '] + [x[1][0] for x in all_meandispX30_P])
        csvWriter.writerow(['X-Displacement Gold 50%: '] + [x[1][0] for x in all_meandispX30_G])
        csvWriter.writerow(['Y-Displacement 50%: '] + [x[1][1] for x in all_meandispY30])
        csvWriter.writerow(['Y-Displacement Poly 50%: '] + [x[1][1] for x in all_meandispY30_P])
        csvWriter.writerow(['Y-Displacement Gold 50%: '] + [x[1][1] for x in all_meandispY30_G])
        csvWriter.writerow(['Z-Displacement 50%: '] + [x[1][2] for x in all_meandispZ30])
        csvWriter.writerow(['Z-Displacement Poly 50%: '] + [x[1][2] for x in all_meandispZ30_P])
        csvWriter.writerow(['Z-Displacement Gold 50%: '] + [x[1][2] for x in all_meandispZ30_G])
        csvWriter.writerow(['Concentration 50%: '] + [x[1] for x in all_meanconc30])
        # csvWriter.writerow(['S-Volume average gold 75%: '] + [list(x[1]) for x in sav_gold])
        # csvWriter.writerow(['S-Volume average polymer 75%: '] + [list(x[1]) for x in sav_poly])
        # csvWriter.writerow(['E-Volume average gold 75%: '] + [list(x[1]) for x in eav_gold])
        # csvWriter.writerow(['E-Volume average polymer 75%: '] + [list(x[1]) for x in eav_poly])
        # csvWriter.writerow(['Concentration polymer 80%: '] + [x[1] for x in all_meanconc08])

    print >> sys.__stdout__, '------ Data written to ' + cwd + fOut + '.csv' + ' ------'
