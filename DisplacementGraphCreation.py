"""
File to extract datat from csv file and plot data w.r.t time to find when data stabilizes
Data csv file created from script DataExtractionP2.py
"""

# import python libraries
import sys, csv
import matplotlib.pyplot as plt
import numpy as np


def extractCSVData(cwd, fileName):
    with open(cwd + fileName, 'r') as fname:
        dataFile = list(csv.reader(fname))
    frametime = [float(x) for x in dataFile[0][1:]]
    dispX_G = [float(x) for x in dataFile[1][1:]]
    dispX_P = [float(x) for x in dataFile[2][1:]]
    dispY_G = [float(x) for x in dataFile[3][1:]]
    dispY_P = [float(x) for x in dataFile[4][1:]]
    dispZ_G = [float(x) for x in dataFile[5][1:]]
    dispZ_P = [float(x) for x in dataFile[6][1:]]
    S_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[7][1:]]
    S_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[8][1:]]
    E_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[9][1:]]
    E_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[10][1:]]
    return frametime, dispX_G, dispX_P, dispY_G, dispY_P, dispZ_G, dispZ_P, S_G, S_P, E_G, E_P


fileName = 'Disp_Values.csv'

cwd = '/home/cerecam/Desktop/2M_96x96x96/2M_96x96x96_42PER/'
[time_42, x_g_42, x_p_42, y_g_42, y_p_42, z_g_42, z_p_42, s_g_42, s_p_42, e_g_42, e_p_42] = extractCSVData(cwd,
                                                                                                           fileName)

cwd = '/home/cerecam/Desktop/2M_96x96x96/2M_96x96x96_58PER/'
[time_58, x_g_58, x_p_58, y_g_58, y_p_58, z_g_58, z_p_58, s_g_58, s_p_58, e_g_58, e_p_58] = extractCSVData(cwd,
                                                                                                           fileName)

# fig = plt.figure()
# plt.plot(time_42, z_g_42, linestyle= '--', label = 'Gold displacment: 42 %')
# plt.plot(time_42, z_p_42, linestyle= '--', label = 'Polymer displacment: 42 %')
# plt.plot(time_58, z_g_58, label = 'Gold displacment: 58 %')
# plt.plot(time_58, z_p_58, label = 'Polymer displacment: 58 %')
# plt.title('Z-displacement of Z1 face')
# plt.legend(loc='best')
# plt.show()
# vol_s_g_42 = [_[:3] for _ in s_g_42]
# trace42gS = []
# trace42pS = []
# for i in s_g_42:
#     trace42gS.append(np.sum([float(_) for _ in i[:3]]) / 3.0)
# for i in s_p_42:
#     trace42pS.append(np.sum([float(_) for _ in i[:3]]) / 3.0)
#
# trace42gE = []
# trace42pE = []
# for i in e_g_42:
#     trace42gE.append((np.sum([float(_) for _ in i[:3]]) / 3.0)*100)
# for i in e_p_42:
#     trace42pE.append((np.sum([float(_) for _ in i[:3]]) / 3.0)*100)
#
# trace58gS = []
# trace58pS = []
# for i in s_g_58:
#     trace58gS.append(np.sum([float(_) for _ in i[:3]]) / 3.0)
# for i in s_p_58:
#     trace58pS.append(np.sum([float(_) for _ in i[:3]]) / 3.0)
#
# trace58gE = []
# trace58pE = []
# for i in e_g_58:
#     trace58gE.append((np.sum([float(_) for _ in i[:3]]) / 3.0)*100)
# for i in e_p_58:
#     trace58pE.append((np.sum([float(_) for _ in i[:3]]) / 3.0)*100)
#
# # fig = plt.figure()
# # # plt.plot(time_42, trace42gS, linestyle= '--', label = 'Gold: 42 %')
# # plt.plot(time_42, trace42pS, label='42 % gold vol frac (less gold)', linestyle='--')
# # plt.plot(time_58, trace58pS, label='58 % gold vol frac (more gold)')
# # plt.title('Dilatational stress of polymer over time')
# # plt.legend(loc='best')
# # # plt.show()
# #
# #
# # fig = plt.figure()
# # plt.plot(time_42, trace42gS, linestyle='--', label='42 % gold vol frac (less gold)')
# # # fig = plt.figure()
# # plt.plot(time_58, trace58gS, label='58 % gold vol frac (more gold)')
# # # plt.plot(time_42, trace42pE, label = 'Polymer: 42 %')
# # plt.title('Dilatational stress of gold over time')
# # plt.legend(loc='best')
# # plt.show()
#
# fig = plt.figure()
# # plt.plot(time_42, trace42gS, linestyle= '--', label = 'Gold: 42 %')
# plt.plot(time_42, trace42pE, label='42 % gold vol frac (less gold)', linestyle='--')
# plt.plot(time_58, trace58pE, label='58 % gold vol frac (more gold)')
# plt.title('Percentage volume change of polymer over time')
# plt.legend(loc='best')
# # plt.show()
#
#
# fig = plt.figure()
# plt.plot(time_42, trace42gE, linestyle='--', label='42 % gold vol frac (less gold)')
# # fig = plt.figure()
# plt.plot(time_58, trace58gE, label='58 % gold vol frac (more gold)')
# # plt.plot(time_42, trace42pE, label = 'Polymer: 42 %')
# plt.title('Percentage volume change of gold over time')
# plt.legend(loc='best')
#
colours = ['b', 'g', 'r','y', 'y', 'y']
# #
#
fig = plt.figure()
for i in range(6):
    plt.plot(time_42, [float(_[i]) for _ in e_p_42], label='42 % gold vol frac E$_{' + str(i + 1) + str(i + 1) + '}$',
             linestyle='--', color=colours[i])
# fig = plt.figure()
for i in range(6):
    plt.plot(time_58, [float(_[i]) for _ in e_p_58], label='58 % gold vol frac E$_{' + str(i + 1) + str(i + 1) + '}$',
             color=colours[i])
plt.title('Average strain development in polymer')
plt.legend(loc='best')

fig = plt.figure()
for i in range(6):
    plt.plot(time_42, [float(_[i]) for _ in s_p_42], label='42 % gold vol frac S$_{' + str(i + 1) + str(i + 1) + '}$',
             linestyle='--', color=colours[i])
# fig = plt.figure()
for i in range(6):
    plt.plot(time_58, [float(_[i]) for _ in s_p_58], label='58 % gold vol frac S$_{' + str(i + 1) + str(i + 1) + '}$',
             color=colours[i])
plt.title('Average stress development in polymer')
plt.legend(loc='best')

fig = plt.figure()
for i in range(6):
    plt.plot(time_42, [float(_[i]) for _ in e_g_42], label='42 % gold vol frac E$_{' + str(i + 1) + str(i + 1) + '}$',
             linestyle='--', color=colours[i])
# fig = plt.figure()
for i in range(6):
    plt.plot(time_58, [float(_[i]) for _ in e_g_58], label='58 % gold vol frac E$_{' + str(i + 1) + str(i + 1) + '}$',
             color=colours[i])
plt.title('Average strain development in gold')
plt.legend(loc='best')

fig = plt.figure()
for i in range(6):
    plt.plot(time_42, [float(_[i]) for _ in s_g_42], label='42 % gold vol frac S$_{' + str(i + 1) + '}$',
             linestyle='--', color=colours[i])
# fig = plt.figure()
for i in range(6):
    plt.plot(time_58, [float(_[i]) for _ in s_g_58], label='58 % gold vol frac S$_{' + str(i + 1) + '}$',
             color=colours[i])
plt.title('Average stress development in gold')
plt.legend(loc='best')
#
#
# # p_42 = np.poly1d(np.polyfit(time_42,z_p_42,6))
# # xp_42 = np.linspace(time_42[0],time_42[-1],len(time_42))
# #
# # p_58 = np.poly1d(np.polyfit(time_58,z_p_58,6))
# # xp_58 = np.linspace(time_58[0],time_58[-1],len(time_58))
# #
# fig = plt.figure()
# plt.plot(time_42, z_p_42, '-',color='b',  label='42 % gold vol frac')
# # plt.plot(xp_42, p_42(xp_42), '-',color='b',  label='42 % gold vol frac')
# plt.plot(time_58, z_p_58,color='r',  label='58 % gold vol frac')
# # plt.plot(xp_58, p_58(xp_58), '-',color='r',  label='58 % gold vol frac')
# plt.ylim(0.0)
# plt.xlim(0.0)
# plt.title('Z - displacement of Z1 face of polymer')
# plt.legend(loc='best')
# plt.show()
#
# p_42 = np.poly1d(np.polyfit(time_42,z_g_42,3))
# xp_42 = np.linspace(time_42[0],time_42[-1],len(time_42))
#
# p_58 = np.poly1d(np.polyfit(time_58,z_g_58,3))
# xp_58 = np.linspace(time_58[0],time_58[-1],len(time_58))
#
# fig = plt.figure()
# plt.plot(time_42, z_g_42, '-',color='b',  label='42 % gold vol frac')
# # plt.plot(xp_42, p_42(xp_42), '-',color='b',  label='42 % gold vol frac')
# plt.plot(time_58, z_g_58,color='r',  label='58 % gold vol frac')
# # plt.plot(xp_58, p_58(xp_58), '-',color='r',  label='58 % gold vol frac')
# plt.ylim(0.0)
# plt.xlim(0.0)
# plt.title('Z - displacement on Z1 face of gold')
# plt.legend(loc='best')



plt.show()
