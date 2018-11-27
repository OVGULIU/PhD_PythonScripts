"""
File to extract datat from csv file and plot data w.r.t time to find when data stabilizes
Data csv file created from script DataExtractionP2.py
"""

# import python libraries
import sys, csv
import matplotlib.pyplot as plt
import numpy as np
#from scipy.signal import savgol_filter


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


fileName = 'Disp_Values_21_Nov.csv'

#cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/'
#[time_25, x_g_25, x_p_25, y_g_25, y_p_25, z_g_25, z_p_25, s_g_25, s_p_25, e_g_25, e_p_25] = extractCSVData(cwd,
                                                                                                            #fileName)

cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_34PER/'
[time_34, x_g_34, x_p_34, y_g_34, y_p_34, z_g_34, z_p_34, s_g_34, s_p_34, e_g_34, e_p_34] = extractCSVData(cwd,
                                                                                                           fileName)

cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER/HPC_42PER/'
[time_42, x_g_42, x_p_42, y_g_42, y_p_42, z_g_42, z_p_42, s_g_42, s_p_42, e_g_42, e_p_42] = extractCSVData(cwd,
                                                                                                            fileName)

# cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_50PER/HPC_50PER/'
# [time_50, x_g_50, x_p_50, y_g_50, y_p_50, z_g_50, z_p_50, s_g_50, s_p_50, e_g_50, e_p_50] = extractCSVData(cwd,
#                                                                                                            fileName)
# time_25 = [i / time_25[-1] for i in time_25]
# time_34 = [i / time_34[-1] for i in time_34]
# time_42 = [i / time_42[-1] for i in time_42]
# time_50 = [i / time_50[-1] for i in time_50]

'''
trace42gS = []
trace42pS = []
for i in s_g_42:
    trace42gS.append(np.sum([float(_) for _ in i[:3]]) / 3.0)
for i in s_p_42:
    trace42pS.append(np.sum([float(_) for _ in i[:3]]) / 3.0)

trace42gE = []
trace42pE = []
for i in e_g_42:
    trace42gE.append((np.sum([float(_) for _ in i[:3]]) / 3.0))
for i in e_p_42:
    trace42pE.append((np.sum([float(_) for _ in i[:3]]) / 3.0))

trace58gS = []
trace58pS = []
for i in s_g_58:
    trace58gS.append(np.sum([float(_) for _ in i[:3]]) / 3.0)
for i in s_p_58:
    trace58pS.append(np.sum([float(_) for _ in i[:3]]) / 3.0)

trace58gE = []
trace58pE = []
for i in e_g_58:
    trace58gE.append((np.sum([float(_) for _ in i[:3]]) / 3.0))
for i in e_p_58:
    trace58pE.append((np.sum([float(_) for _ in i[:3]]) / 3.0))
for p in [5,-40,-30,-25,-20,-15,-10,-1]:
    trace42E = trace42gE[p] + trace42pE[p]
    trace58E = trace58gE[p] + trace58pE[p]
    trace42S = trace42gS[p] + trace42pS[p]
    trace58S = trace58gS[p] + trace58pS[p]


    S42 = np.array([float(i) for i in s_p_42[-1]]) + np.array([float(i) for i in s_g_42[-1]])
    S58 = np.array([float(i) for i in s_p_58[-1]]) + np.array([float(i) for i in s_g_58[-1]])
    E42 = np.array([float(i) for i in e_p_42[-1]]) + np.array([float(i) for i in e_g_42[-1]])
    E58 = np.array([float(i) for i in e_p_58[-1]]) + np.array([float(i) for i in e_g_58[-1]])

    S42 = [[S42[0],S42[3],S42[4]],[S42[3],S42[1],S42[5]],[S42[4],S42[5],S42[2]]]
    S58 = [[S58[0],S58[3],S58[4]],[S58[3],S58[1],S58[5]],[S58[4],S58[5],S58[2]]]
    E42 = [[E42[0],E42[3],E42[4]],[E42[3],E42[1],E42[5]],[E42[4],E42[5],E42[2]]]
    E58 = [[E58[0],E58[3],E58[4]],[E58[3],E58[1],E58[5]],[E58[4],E58[5],E58[2]]]

    devS42 = np.matrix(S42) - (trace42S*np.eye(3))
    devS58 = np.matrix(S58) - (trace58S*np.eye(3))
    devE42 = np.matrix(E42) - (trace42E*np.eye(3))
    devE58 = np.matrix(E58) - (trace58E*np.eye(3))

    kappaEff_42 = 1.0/3.0 * trace42S/trace42E
    kappaEff_58 = 1.0/3.0 * trace58S/trace58E
    muEff42 = 0.5*np.sqrt((np.tensordot(devS42,devS42,axes=2))/(np.tensordot(devE42,devE42,axes=2)))
    muEff58 = 0.5*np.sqrt((np.tensordot(devS58,devS58,axes=2))/(np.tensordot(devE58,devE58,axes=2)))

    EM42 = (9.0*(kappaEff_42*muEff42)/((3.0*kappaEff_42)+muEff42))
    EM58 = (9.0*(kappaEff_58*muEff58)/((3.0*kappaEff_58)+muEff58))

    # print(muEff42,muEff58)
    # print(kappaEff_42,kappaEff_58)
    print(EM42,EM58)
'''
# #
# fig = plt.figure()
# # plt.plot(time_42, trace42gS, linestyle= '--', label = 'Gold: 42 %')
# plt.plot(time_42, trace42pS, label='42 % gold vol frac (less gold)', linestyle='--')
# plt.plot(time_58, trace58pS, label='58 % gold vol frac (more gold)')
# plt.title('Dilatational stress of polymer over time')
# plt.legend(loc='best')
# # plt.show()
#
#
# fig = plt.figure()
# plt.plot(time_42, trace42gS, linestyle='--', label='42 % gold vol frac (less gold)')
# # fig = plt.figure()
# plt.plot(time_58, trace58gS, label='58 % gold vol frac (more gold)')
# # plt.plot(time_42, trace42pE, label = 'Polymer: 42 %')
# plt.title('Dilatational stress of gold over time')
# plt.legend(loc='best')
# plt.show()
# maxTraceP = max([max(trace58pE),max(trace42pE)])
# trace42pE = [i/maxTraceP for i in trace42pE]
# trace58pE = [i/maxTraceP for i in trace58pE]
# fig = plt.figure()
# plt.plot(time_42, trace42gS, linestyle= '--', label = 'Gold: 42 %')
# plt.plot(time_42, trace42pE, label='42 % gold vol frac', linestyle='--')
# plt.plot(time_58, trace58pE, label='58 % gold vol frac')
# plt.title('Volume change of polymer over time')
# plt.ylim(0.0)
# plt.xlim(0.0)
# plt.xlabel('time')
# plt.ylabel('normalized volume change')
# plt.legend(loc='best')
# # plt.show()
#
# maxTraceG = max([max(trace58gE),max(trace42gE)])
# trace42gE = [i/maxTraceG for i in trace42gE]
# trace58gE = [i/maxTraceG for i in trace58gE]
# fig = plt.figure()
# plt.plot(time_42, trace42gE, linestyle='--', label='42 % gold vol frac')
# # fig = plt.figure()
# plt.plot(time_58, trace58gE, label='58 % gold vol frac')
# # plt.plot(time_42, trace42pE, label = 'Polymer: 42 %')
# plt.title('Volume change of gold over time')
# plt.ylim(0.0)
# plt.xlim(0.0)
# plt.xlabel('time')
# plt.ylabel('normalized volume change')
# plt.legend(loc='best')

# fig = plt.figure()
# plt.plot(time_42, trace42gE, color = 'y',linestyle='--', label='42 % gold vol frac (less gold)')
# # fig = plt.figure()
# plt.plot(time_58, trace58gE, color = 'y',label='58 % gold vol frac (more gold)')
# plt.plot(time_42, trace42pE, color = 'b', label='42 % gold vol frac (less gold)', linestyle='--')
# plt.plot(time_58, trace58pE, color = 'b',label='58 % gold vol frac (more gold)')
# # plt.plot(time_42, trace42pE, label = 'Polymer: 42 %')
# plt.title('Volume change of gold over time')
# plt.legend(loc='best')
# #
colours = ['b', 'b', 'r', 'y', 'y', 'y']
lineType = ['--', '-', '--']
# # #
# #
# fig = plt.figure()
# for i in range(1,3):
#     plt.plot(time_42, [float(_[i]) for _ in e_p_42], label='42 % gold vol frac E$_{' + str(i + 1) + str(i + 1) + '}$',
#              linestyle='--', color=colours[i])
# # fig = plt.figure()
# for i in range(1,3):
#     plt.plot(time_58, [float(_[i]) for _ in e_p_58], label='58 % gold vol frac E$_{' + str(i + 1) + str(i + 1) + '}$',
#              color=colours[i])
# plt.title('Average strain development in polymer')
# plt.legend(loc='best')
legendLabels = ['34 % gold vol frac S$_{\parallel}$', '34 % gold vol frac S$_{\perp}$',
                '42 % gold vol frac S$_{\parallel}$', '42 % gold vol frac S$_{\perp}$']
# fig = plt.figure()
# for i in range(1,3):
#     plt.plot(time_42, [float(_[i]) for _ in e_g_42], label='42 % gold vol frac E$_{' + str(i + 1) + str(i + 1) + '}$',
#              linestyle='--', color=colours[i])
# # fig = plt.figure()
# for i in range(1,3):
#     plt.plot(time_58, [float(_[i]) for _ in e_g_58], label='58 % gold vol frac E$_{' + str(i + 1) + str(i + 1) + '}$',
#              color=colours[i])
# plt.title('Average strain development in gold')
# plt.legend(loc='best')

maxy = []
fig = plt.figure()
#for i in range(1, 3):
    #plt.plot(time_25, [-1*float(_[i]) for _ in s_g_25],
             #linestyle=lineType[i], color='b')
    #maxy.append(max([float(_[i]) for _ in s_g_25]))
for i in range(1, 3):
    plt.plot(time_34, [float(_[i]) for _ in s_g_34],
    linestyle = lineType[i], color = 'r')
    maxy.append(max([float(_[i]) for _ in s_g_34]))
for i in range(1, 3):
	plt.plot(time_42, [float(_[i]) for _ in s_g_42],
	linestyle = lineType[i], color = 'g')
	maxy.append(max([float(_[i]) for _ in s_g_42]))
# for i in range(1, 3):
#     plt.plot(time_50, [float(_[i]) for _ in s_g_50],
#     linestyle = lineType[i], color = 'y')
#     maxy.append(max([float(_[i]) for _ in s_g_50]))
# plt.ylim(0, max(maxy))
plt.title('Average stress development in gold')
plt.xlabel('time/time$_{end}$')
plt.ylabel('stress [MPa]')
plt.legend(legendLabels, loc='best')
    #
    #

fig = plt.figure()
#for i in range(1, 3):
    #plt.plot(time_25, [-1*float(_[i]) for _ in s_p_25],
             #linestyle=lineType[i], color='b')
    #maxy.append(max([float(_[i]) for _ in s_p_25]))
for i in range(1, 3):
    plt.plot(time_34, [float(_[i]) for _ in s_p_34],
    linestyle = lineType[i], color = 'r')
    maxy.append(max([float(_[i]) for _ in s_p_34]))
for i in range(1, 3):
	plt.plot(time_42, [float(_[i]) for _ in s_p_42],
	linestyle = lineType[i], color = 'g')
	maxy.append(max([float(_[i]) for _ in s_p_42]))
# for i in range(1, 3):
#     plt.plot(time_50, [float(_[i]) for _ in s_p_50],
#     linestyle = lineType[i], color = 'y')
#     maxy.append(max([float(_[i]) for _ in s_p_50]))
# plt.ylim(0, max(maxy))
plt.title('Average stress development in polymer')
plt.xlabel('time/time$_{end}$')
plt.ylabel('stress [MPa]')
plt.legend(legendLabels, loc='best')
# p_42 = np.poly1d(np.polyfit(time_42,z_p_42,6))
# xp_42 = np.linspace(time_42[0],time_42[-1],len(time_42))
#
# p_58 = np.poly1d(np.polyfit(time_58,z_p_58,6))
# xp_58 = np.linspace(time_58[0],time_58[-1],len(time_58))
#
#z_p_max = max([max(z_p_25), max(z_p_34), max(z_p_50)])
#z_g_max = max([max(z_g_25), max(z_g_34), max(z_g_50)])
#z_p_max = max([max(z_p_50)])
#z_g_max = max([max(z_g_50)])
#maxy = max([z_p_max, z_g_max])
# z_p_42 = [i/z_p_max for i in z_p_42]
# z_g_42 = [i/z_g_max for i in z_g_42]
# z_p_58 = [i/z_p_max for i in z_p_58]
# z_g_58 = [i/z_g_max for i in z_g_58]
# colour = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
# colorC = 0
fig = plt.figure()
# yhat = savgol_filter(z_p_42,23,2)
# plt.plot(time_42, yhat, '-',color='b',  label='42 % gold vol frac')
# plt.plot(xp_42, p_42(xp_42), '-',color='b',  label='42 % gold vol frac')
# for i in [11,13,15,17]:
# yhat = savgol_filter(z_p_58,17,2)
# plt.plot(time_58, yhat,'-',color='r',  label='58 % gold vol frac')
    # colorC += 1
#plt.plot(time_25, z_p_25, '-',color='b',  label='25 %')
plt.plot(time_34, z_p_34, '-',color='r',  label='34 %')
plt.plot(time_42, z_p_42, '-',color='g',  label='42 %')
# plt.plot(time_50, z_p_50, '-',color='y',  label='50 %')

# plt.plot(xp_58, p_58(xp_58), '-',color='r',  label='58 % gold vol frac')
# plt.ylim(0.0, maxy)
plt.xlim(0.0)
plt.xlabel('time/time$_{end}$')
plt.ylabel('displacement [nm]')
plt.title('Average displacement of polymer on influx face')
plt.legend(loc='best')
# plt.show()

# p_42 = np.poly1d(np.polyfit(time_42,z_g_42,3))
# xp_42 = np.linspace(time_42[0],time_42[-1],len(time_42))
#
# p_58 = np.poly1d(np.polyfit(time_58,z_g_58,3))
# xp_58 = np.linspace(time_58[0],time_58[-1],len(time_58))
#
# colour = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
# colorC = 0
fig = plt.figure()
# yhat = savgol_filter(z_g_42,23,2)
# plt.plot(time_42, yhat, '-',color='b',  label='42 % gold vol frac')
    # plt.plot(time_42, yhat, '-',color=colour[colorC],  label=str(i))
    # colorC +=1
# yhat = savgol_filter(z_g_58,17,2)
# plt.plot(time_58, yhat,'-',color='r',  label='58 % gold vol frac')
# plt.plot(time_58, z_g_58,color='r',  label='58 % gold vol frac')
#plt.plot(time_25, z_g_25, '-',color='b',  label='25 %')
plt.plot(time_34, z_g_34, '-',color='r',  label='34 %')
plt.plot(time_42, z_g_42, '-',color='g',  label='42 %')
# plt.plot(time_50, z_g_50, '-',color='y',  label='50 %')

# plt.ylim(0.0,maxy)
plt.xlim(0.0)
plt.xlabel('time/time$_{end}$')
plt.ylabel('displacement [nm]')
plt.title('Average displacement of gold on influx face')
plt.legend(loc='best')



plt.show()
# '''
