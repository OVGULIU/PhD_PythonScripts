"""
File to extract datat from csv file and plot data w.r.t time to find when data stabilizes
Data csv file created from script DataExtractionP2.py
"""

# import python libraries
import sys, csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 12
plt.rcParams['legend.fontsize'] = 'large'
plt.rcParams['legend.loc'] = 'best'
plt.rcParams['figure.titlesize'] = 'medium'
plt.rcParams['lines.linewidth'] = 4
plt.rcParams['grid.linestyle'] = '-'
plt.rcParams['grid.color'] = (0.75, 0.75, 0.75)
plt.rcParams['axes.axisbelow'] = True


from scipy.signal import savgol_filter


def extractCSVData1(cwd, fileName):
    with open(cwd + fileName, 'r') as fname:
        dataFile = list(csv.reader(fname))

    # frametime = [float(x) for x in dataFile[0][1:]]
    # dispX = [float(x) for x in dataFile[1][1:]]
    # dispY = [float(x) for x in dataFile[2][1:]]
    # dispZ = [float(x) for x in dataFile[3][1:]]
    # dispZ = [i * -1.0 for i in dispZ]
    # return frametime, dispX, dispY, dispZ
    #
    # frametime = [float(x) for x in dataFile[0][1:]]
    # dispZ_90 = [float(x)*-1.0 for x in dataFile[1][1:]]
    # dispZ_75 = [float(x)*-1.0 for x in dataFile[2][1:]]
    # dispZ_50 = [float(x)*-1.0 for x in dataFile[3][1:]]
    # dispZ_25 = [float(x)*-1.0 for x in dataFile[4][1:]]
    # dispZ_10 = [float(x)*-1.0 for x in dataFile[5][1:]]
    # conc_90 = [float(x) for x in dataFile[6][1:]]
    # conc_75 = [float(x) for x in dataFile[7][1:]]
    # conc_50 = [float(x) for x in dataFile[8][1:]]
    # return frametime, dispZ_90, dispZ_75, dispZ_50, dispZ_25, dispZ_10, conc_90, conc_75, conc_50

    frametime = [float(x) for x in dataFile[0][1:]]
    dispX = [float(x) for x in dataFile[1][1:]]
    dispX_P = [float(x) for x in dataFile[2][1:]]
    dispX_G = [float(x) for x in dataFile[3][1:]]
    dispY = [float(x) for x in dataFile[4][1:]]
    dispY_P = [float(x) for x in dataFile[5][1:]]
    dispY_G = [float(x) for x in dataFile[6][1:]]
    dispZ = [float(x)*-1.0 for x in dataFile[7][1:]]
    dispZ_P = [float(x)*-1.0 for x in dataFile[8][1:]]
    dispZ_G = [float(x)*-1.0 for x in dataFile[9][1:]]
    Conc = [float(x) for x in dataFile[10][1:]]
    return frametime, dispX, dispX_G, dispX_P, dispY, dispY_G, dispY_P, dispZ, dispZ_G, dispZ_P, Conc
    #
    # frametime = [float(x) for x in dataFile[0][1:]]
    # S_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[1][1:]]
    # S_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[2][1:]]
    # E_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[3][1:]]
    # E_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[4][1:]]
    # return frametime, S_G, S_P, E_G, E_P


def extractCSVData2(cwd, fileName):
    with open(cwd + fileName, 'r') as fname:
        dataFile = list(csv.reader(fname))

    frametime = [float(x) for x in dataFile[0][1:]]
    # dispX = [float(x) for x in dataFile[1][1:]]
    # dispY = [float(x) for x in dataFile[2][1:]]
    # dispZ = [float(x) for x in dataFile[3][1:]]
    # dispZ = [i * -1.0 for i in dispZ]
    # return frametime, dispX, dispY, dispZ

    # frametime = [float(x) for x in dataFile[0][1:]]
    # dispX_G = [float(x) for x in dataFile[1][1:]]
    # dispX_P = [float(x) for x in dataFile[2][1:]]
    # dispY_G = [float(x) for x in dataFile[3][1:]]
    # dispY_P = [float(x) for x in dataFile[4][1:]]
    # dispZ_G = [float(x) for x in dataFile[5][1:]]
    # dispZ_P = [float(x) for x in dataFile[6][1:]]
    # Conc = [float(x) for x in dataFile[7][1:]]
    # dispZ_G = [i * -1.0 for i in dispZ_G]
    # dispZ_P = [i * -1.0 for i in dispZ_P]
    # return frametime, dispX_G, dispX_P, dispY_G, dispY_P, dispZ_G, dispZ_P, Conc
    #
    # frametime = [float(x) for x in dataFile[0][1:]]
    # S_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[1][1:]]
    # S_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[2][1:]]
    # E_G = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[3][1:]]
    # E_P = [x.split('"')[0].strip('[').strip(']').split(',') for x in dataFile[4][1:]]
    # return frametime, S_G, S_P, E_G, E_P


# fileName = 'Values_Stress_Strain.csv'
# fileName = 'Values_Stress_Strain_90.csv'
# fileName = 'Values_Stress_Strain.csv'
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/NewDensitySims/'
# fileName = 'Values_Full_Face_Disp.csv'
# [time_25, x_25, y_25, z_25] = extractCSVData1(cwd, fileName)
# fileName = 'XYZ_Values_Stress.csv'
# fileName = 'Values_Zdisp_Interval2.csv'
# [time_25, dispZ_90_25, dispZ_75_25, dispZ_50_25, dispZ_25_25, dispZ_10_25, conc_90_25, conc_75_25, conc_50_25] = extractCSVData1(cwd, fileName)
fileName = 'Values_XYZdisp_50.csv'
# fileName = 'Values_Stress_75.csv'
[time_25, x_25, x_g_25, x_p_25, y_25, y_g_25, y_p_25, z_25, z_g_25, z_p_25, Conc_25] = extractCSVData1(cwd, fileName)
# [time_25, s_p_25, s_g_25, e_p_25, e_g_25] = extractCSVData1(cwd, fileName)
# [time_25, s_g_25, s_p_25, e_g_25, e_p_25] = extractCSVData1(cwd, fileName)
# print(max(Conc_25))
#
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_34PER/NewDensitySims/'
# fileName = 'Values_Full_Face_Disp.csv'
# [time_34, x_34, y_34, z_34] = extractCSVData1(cwd, fileName)
# fileName = 'XYZ_Values_Stress.csv'
# [time_34, x_g_34, x_p_34, y_g_34, y_p_34, z_g_34, z_p_34, Conc_34] = extractCSVData2(cwd, fileName)
[time_34, x_34, x_g_34, x_p_34, y_34, y_g_34, y_p_34, z_34, z_g_34, z_p_34, Conc_34] = extractCSVData1(cwd, fileName)
# [time_34, s_g_34, s_p_34, e_g_34, e_p_34] = extractCSVData1(cwd, fileName)
#
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER/NewDensitySims/'
# fileName = 'Values_Full_Face_Disp.csv'
# [time_42, x_42, y_42, z_42] = extractCSVData1(cwd, fileName)
# fileName = 'XYZ_Values_Stress.csv'
# [time_42, x_g_42, x_p_42, y_g_42, y_p_42, z_g_42, z_p_42, Conc_42] = extractCSVData2(cwd, fileName)
# fileName = 'Values_Zdisp_Interval2.csv'
# [time_42, dispZ_90_42, dispZ_75_42, dispZ_50_42, dispZ_25_42, dispZ_10_42, conc_90_42, conc_75_42, conc_50_42] = extractCSVData1(cwd, fileName)
[time_42, x_42, x_g_42, x_p_42, y_42, y_g_42, y_p_42, z_42, z_g_42, z_p_42, Conc_42] = extractCSVData1(cwd, fileName)
# [time_42, s_g_42, s_p_42, e_g_42, e_p_42] = extractCSVData1(cwd, fileName)
#
cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_50PER/NewDensitySims/'
# fileName = 'Values_Full_Face_Disp.csv'
# [time_50, x_50, y_50, z_50] = extractCSVData1(cwd, fileName)
# fileName = 'XYZ_Values_Stress.csv'
# [time_50, x_g_50, x_p_50, y_g_50, y_p_50, z_g_50, z_p_50, Conc_50] = extractCSVData2(cwd,fileName)
[time_50, x_50, x_g_50, x_p_50, y_50, y_g_50, y_p_50, z_50, z_g_50, z_p_50, Conc_50] = extractCSVData1(cwd, fileName)
# [time_50, s_g_50, s_p_50, e_g_50, e_p_50] = extractCSVData1(cwd, fileName)
#
#
# time_25 = [i / time_25[-1] for i in time_25]
# time_34 = [i / time_34[-1] for i in time_34]
# time_42 = [i / time_42[-1] for i in time_42]
# time_50 = [i / time_50[-1] for i in time_50]
#

# s_25 = []
# for i in range(len(s_g_25)):
#     tmp_g = [float(_) for _ in s_g_25[i]]
#     # tmp_p = [float(_) for _ in s_p_25[i]]
#     # s_25.append(list(np.array(tmp_g) + np.array(tmp_p)))
#     s_25.append(list(np.array(tmp_g)))
# s_34 = []
# for i in range(len(s_g_34)):
#     tmp_g = [float(_) for _ in s_g_34[i]]
#     # tmp_p = [float(_) for _ in s_p_34[i]]
#     # s_34.append(list(np.array(tmp_g) + np.array(tmp_p)))
#     s_34.append(list(np.array(tmp_g)))
# s_42 = []
# for i in range(len(s_g_42)):
#     tmp_g = [float(_) for _ in s_g_42[i]]
#     # tmp_p = [float(_) for _ in s_p_42[i]]
#     # s_42.append(list(np.array(tmp_g) + np.array(tmp_p)))
#     s_42.append(list(np.array(tmp_g)))
# s_50 = []
# for i in range(len(s_g_50)):
#     tmp_g = [float(_) for _ in s_g_50[i]]
#     # tmp_p = [float(_) for _ in s_p_50[i]]
#     # s_50.append(list(np.array(tmp_g) + np.array(tmp_p)))
#     s_50.append(list(np.array(tmp_g)))
# #
# pop_values_25 = [300.0, 700.0, 1000.0, 1300.0, 1600.0]
# for k in pop_values_25:
#     time_25.remove(k)
#     s_25.pop(time_25.index(k))
#     s_g_25.pop(time_25.index(k))
#     s_p_25.pop(time_25.index(k))
#     # Conc_25.pop(time_25.index(k))
#
# pop_values_34 = [300.0, 600.0, 800.0, 1200.0, 1750.0]
# for k in pop_values_34:
#     time_34.remove(k)
#     s_34.pop(time_34.index(k))
#     s_g_34.pop(time_34.index(k))
#     s_p_34.pop(time_34.index(k))
#     # Conc_34.pop(time_34.index(k))
#
# pop_values_42 = [300.0, 600.0, 900.0, 1200.0, 1750.0]
# for k in pop_values_42:
#     time_42.remove(k)
#     s_42.pop(time_42.index(k))
#     s_g_42.pop(time_42.index(k))
#     s_p_42.pop(time_42.index(k))
#     # Conc_42.pop(time_42.index(k))
#
# pop_values_50 = [400.0, 700.0, 1000.0, 1300.0, 1600.0]
# for k in pop_values_50:
#     time_50.remove(k)
#     s_50.pop(time_50.index(k))
#     s_g_50.pop(time_50.index(k))
#     s_p_50.pop(time_50.index(k))
#     # Conc_50.pop(time_50.index(k))
#
# def smoothing(x,y):
#     # Smoothed moving average
#     w = 7
#     weights = np.repeat(1.0, w) / w
#     yMA = np.convolve(y, weights, 'valid')
#
#     #  Savitzky-Golay digital filter
#     points = 17
#     y_filtered = savgol_filter(yMA, points, 2)
#     x_filtered = x[2:-4]
#     return x_filtered, y_filtered
#
# s_y_25 = [_[1] * 1000.0 for _ in s_25]
# s_y_34 = [_[1] * 1000.0 for _ in s_34]
# s_y_42 = [_[1] * 1000.0 for _ in s_42]
# s_y_50 = [_[1] * 1000.0 for _ in s_50]
#
# s_x_25 = [_[2] * 1000.0 for _ in s_25]
# s_x_34 = [_[2] * 1000.0 for _ in s_34]
# s_x_42 = [_[2] * 1000.0 for _ in s_42]
# s_x_50 = [_[2] * 1000.0 for _ in s_50]
#
# s_yp_25 = [float(_[1]) * 1000.0 for _ in s_p_25]
# s_yp_34 = [float(_[1]) * 1000.0 for _ in s_p_34]
# s_yp_42 = [float(_[1]) * 1000.0 for _ in s_p_42]
# s_yp_50 = [float(_[1]) * 1000.0 for _ in s_p_50]
#
# s_yg_25 = [float(_[1]) * 1000.0 for _ in s_g_25]
# s_yg_34 = [float(_[1]) * 1000.0 for _ in s_g_34]
# s_yg_42 = [float(_[1]) * 1000.0 for _ in s_g_42]
# s_yg_50 = [float(_[1]) * 1000.0 for _ in s_g_50]
#
# x = time_25
# y = s_y_25
#
# fig = plt.figure()
# ax1 = plt.gca()
#
# time_filtered_25, x_filtered_25 = smoothing(time_25,s_y_25)
# # time_filtered_25, sz_filtered_25 = smoothing(time_25,s_x_25)
# # time_filtered_25, xp_filtered_25 = smoothing(time_25,s_yp_25)
# # time_filtered_25, xg_filtered_25 = smoothing(time_25,s_yg_25)
# end_index_25 = time_filtered_25.index(1750.0)+1
# plt.plot(time_filtered_25[:end_index_25],x_filtered_25[:end_index_25], '-', color = 'b', label='25 %')
# plt.plot(time_25[:3],s_y_25[:2] + [x_filtered_25[0]],'-',color = 'b')
# # plt.plot(time_filtered_25[:end_index_25],sz_filtered_25[:end_index_25], ':', color = 'b', label='parallel')
# # plt.plot(time_25[:3],s_x_25[:2] + [sz_filtered_25[0]],':',color = 'b')
# # plt.plot(time_filtered_25[:end_index_25],xp_filtered_25[:end_index_25], '-.', color = 'b', label='polymer')
# # plt.plot(time_25[:3],s_y_25[:2] + [xp_filtered_25[0]],'-.',color = 'b')
# # plt.plot(time_filtered_25[:end_index_25],xg_filtered_25[:end_index_25], '--', color = 'b', label='gold')
# # plt.plot(time_25[:3],s_y_25[:2] + [xg_filtered_25[0]],'--',color = 'b')
# # time_new_25 = time_25[2:-2], label='25 %'
# time_filtered_34, x_filtered_34 = smoothing(time_34,s_y_34)
# # time_filtered_34, sz_filtered_34 = smoothing(time_34,s_x_34)
# # time_filtered_34, xp_filtered_34 = smoothing(time_34,s_yp_34)
# # time_filtered_34, xg_filtered_34 = smoothing(time_34,s_yg_34)
# end_index_34 = time_filtered_34.index(1750.0)+1
# plt.plot(time_filtered_34[:end_index_34],x_filtered_34[:end_index_34], '-', color = 'r', label='34 %')
# plt.plot(time_34[:3],s_y_34[:2] + [x_filtered_34[0]],'-',color = 'r')
# # plt.plot(time_filtered_34[:end_index_34],sz_filtered_34[:end_index_34], ':', color = 'r')
# # plt.plot(time_34[:3],s_x_34[:2] + [x_filtered_34[0]],':',color = 'r')
# # plt.plot(time_filtered_34[:end_index_34],xp_filtered_34[:end_index_34], '-.', color = 'r')
# # plt.plot(time_34[:3],s_y_34[:2] + [xp_filtered_34[0]],'-.',color = 'r')
# # plt.plot(time_filtered_34[:end_index_34],xg_filtered_34[:end_index_34], '--', color = 'r')
# # plt.plot(time_34[:3],s_y_34[:2] + [xg_filtered_34[0]],'--',color = 'r')
# #
# time_filtered_42, x_filtered_42 = smoothing(time_42,s_y_42)
# # time_filtered_42, sz_filtered_42 = smoothing(time_42,s_x_42)
# # time_filtered_42, xp_filtered_42 = smoothing(time_42,s_yp_42)
# # time_filtered_42, xg_filtered_42 = smoothing(time_42,s_yg_42)
# end_index_42 = time_filtered_42.index(1750.0)+1
# plt.plot(time_filtered_42[:end_index_42],x_filtered_42[:end_index_42], '-', color = 'g', label='42 %')
# plt.plot([time_42[0],time_42[2]],s_y_42[:1] + [x_filtered_42[0]],'-',color = 'g')
# # plt.plot(time_filtered_42[:end_index_42],sz_filtered_42[:end_index_42], ':', color = 'g', label='42 %')
# # plt.plot([time_42[0],time_42[2]],s_x_42[:1] + [sz_filtered_42[0]],':',color = 'g')
# # plt.plot(time_filtered_42[:end_index_42],xp_filtered_42[:end_index_42], '-.', color = 'g')
# # plt.plot(time_42[:3],s_y_42[:2] + [xp_filtered_42[0]],'-.',color = 'g')
# # plt.plot(time_filtered_42[:end_index_42],xg_filtered_42[:end_index_42], '--', color = 'g')
# # plt.plot(time_42[:3],s_y_42[:2] + [xg_filtered_42[0]],'--',color = 'g')
# #
# time_filtered_50, x_filtered_50 = smoothing(time_50,s_y_50)
# # time_filtered_50, sz_filtered_50 = smoothing(time_50,s_x_50)
# # time_filtered_50, xp_filtered_50 = smoothing(time_50,s_yp_50)
# # time_filtered_50, xg_filtered_50 = smoothing(time_50,s_yg_50)
# end_index_50 = time_filtered_50.index(1750.0)+1
# plt.plot(time_filtered_50[:end_index_50],x_filtered_50[:end_index_50], '-', color = 'm', label='50 %')
# plt.plot([time_50[0],time_50[2]],s_y_50[:1] + [x_filtered_50[0]],'-',color = 'm')
# # plt.plot(time_filtered_50[:end_index_50],sz_filtered_50[:end_index_50], ':', color = 'm', label='50 %')
# # plt.plot([time_50[0],time_50[2]],s_x_50[:1] + [sz_filtered_50[0]],':',color = 'm')
# # plt.plot(time_filtered_50[:end_index_50],xp_filtered_50[:end_index_50], '-.', color = 'm')
# # plt.plot(time_50[:3],s_y_50[:2] + [xp_filtered_50[0]],'-.',color = 'm')
# # plt.plot(time_filtered_50[:end_index_50],xg_filtered_50[:end_index_50], '--', color = 'm')
# # plt.plot(time_50[:3],s_y_50[:2] + [xg_filtered_50[0]],'--',color = 'm')
# #
# # end_sx_25 = x_filtered_25[-1]
# # end_sy_25 = sz_filtered_25[-1]
# # #
# # end_sx_34 = x_filtered_34[-1]
# # end_sy_34 = sz_filtered_34[-1]
# # #
# # end_sx_42 = x_filtered_42[-1]
# # end_sy_42 = sz_filtered_42[-1]
# # #
# # end_sx_50 = x_filtered_50[-1]
# # end_sy_50 = sz_filtered_50[-1]
# # #
# # end_sxp_25 = xp_filtered_25[-1]
# # end_sxg_25 = xg_filtered_25[-1]
# # #
# # end_sxp_34 = xp_filtered_34[-1]
# # end_sxg_34 = xg_filtered_34[-1]
# # #
# # end_sxp_42 = xp_filtered_42[-1]
# # end_sxg_42 = xg_filtered_42[-1]
# # #
# # end_sxp_50 = xp_filtered_50[-1]
# # end_sxg_50 = xg_filtered_50[-1]
# # #
# # volFrac = [25,34,42,50]
# # #
# # print('S_xx')
# # print([end_sx_25, end_sx_34, end_sx_42, end_sx_50])
# # print('S_yy')
# # print([end_sy_25, end_sy_34, end_sy_42, end_sy_50])
# # plt.plot(volFrac,[end_sx_25, end_sx_34, end_sx_42, end_sx_50], '-', color = 'k', label = 'S$_{xx}$ - Parallel')
# # plt.plot(volFrac,[end_sy_25, end_sy_34, end_sy_42, end_sy_50], '-.', color = 'k', label = 'S$_{yy}$ - Perpendicular')
# # plt.plot(volFrac,[end_sxp_25, end_sxp_34, end_sxp_42, end_sxp_50], '-', color = 'k', label = 'S$_{xx}$ - polymer')
# # plt.plot(volFrac,[end_sxg_25, end_sxg_34, end_sxg_42, end_sxg_50], '-.', color = 'k', label = 'S$_{xx}$ - gold')
# ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# # #
# plt.xlim(left = 0.0, right=1750)
# plt.ylim(bottom = -30, top=5)
# # plt.xlabel('volume fraction [%]')
# # plt.ylabel('stress [MPa]')
# plt.xlabel('time [ns]')
# plt.ylabel('stress [MPa]')
# plt.xticks(list(range(0,1750+1,250)))
# # plt.title('Final stresses of the composite in both the parallel and perpendicular direction for each volume fraction')
# # plt.title('Normal stress of gold in the direction perpendicular to the ion flux within RVE')
# plt.legend()
# # fig.tight_layout()
# plt.grid()
#
#
# test = [_[1] * 1000.0 for _ in s_25]
# windowSize = [7]
#
# colours = ['b', 'y',  'k', 'g', 'm']
# for count, w in enumerate(windowSize):
#     weights = np.repeat(1.0, w) / w
#     yMA = np.convolve(test[10:], weights, 'valid')

    # lineType = [':', '--', '-']
    #
    # StressLabels = ['S$_{33}$', 'S$_{22}$', 'S$_{11}$']
    # stressIndices = [2, 1, 0]
    # stressIndices = [1, 0]
    # end = -1*(w-2)
    # plt.plot(time_25[:11] + [time_25[11]], test[:11] + [yMA[0]], label='Smoothed: ' + str(w), color = colours[count])
    # plt.plot(time_25[11:end], yMA, label='Smoothed: ' + str(w), color = colours[count])

# for i in stressIndices:
#     plt.plot(time_25, [_[i] * 1000.0 for _ in s_25],
#              linestyle=lineType[i], color='b')
# for i in stressIndices:
#     plt.plot(time_34, [_[i] * 1000.0 for _ in s_34],
#              linestyle=lineType[i], color='r')
# for i in stressIndices:
#     plt.plot(time_42, [_[i] * 1000.0 for _ in s_42],
#              linestyle=lineType[i], color='g')
# for i in stressIndices:
#     plt.plot(time_50, [_[i] * 1000.0 for _ in s_50],
#              linestyle=lineType[i], color='m')
# #
# plt.plot(time_25[0], [_[2] * 1000.0 for _ in s_25][0], linestyle=lineType[0], color='k', label='S$_{33}$')
# plt.plot(time_25[0], [_[1] * 1000.0 for _ in s_25][0], linestyle=lineType[1], color='k', label='S$_{22}$')
# # plt.plot(time_25[0], [_[0] * 1000.0 for _ in s_25][0], linestyle=lineType[2], color='k', label='S$_{11}$')
# plt.plot(time_25[0], [_[1] * 1000.0 for _ in s_25][0], linestyle='-', color='b', label='25%')
# plt.plot(time_34[0], [_[1] * 1000.0 for _ in s_34][0], linestyle='-', color='r', label='34%')
# plt.plot(time_42[0], [_[1] * 1000.0 for _ in s_42][0], linestyle='-', color='g', label='42%')
# plt.plot(time_50[0], [_[1] * 1000.0 for _ in s_50][0], linestyle='-', color='m', label='50%')
# ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# # #
# # # plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('stress [MPa]')
# plt.title('Average normal stresses perpendicular to ion flux direction development within RVE')
# plt.legend()
# fig.tight_layout()
# plt.grid()
#
# fig = plt.figure()
# ax1 = plt.gca()
# lineType = [[1, 0, 1, 0], [1, 1, 6, 1, 6, 6], [3, 1, 3, 10]]
# lineType = [':', '--', '-']
# StressLabels = ['S$_{23}$', 'S$_{13}$', 'S$_{12}$']
# stressIndices = [5, 4, 3]
# for i in stressIndices:
#     plt.plot(time_25, [_[i] * 1000.0 for _ in s_25],
#              linestyle=lineType[i - 3], color='b')
# for i in stressIndices:
#     plt.plot(time_34, [_[i] * 1000.0 for _ in s_34],
#              linestyle=lineType[i - 3], color='r')
# for i in stressIndices:
#     plt.plot(time_42, [_[i] * 1000.0 for _ in s_42],
#              linestyle=lineType[i - 3], color='g')
# for i in stressIndices:
#     plt.plot(time_50, [_[i] * 1000.0 for _ in s_50],
#              linestyle=lineType[i - 3], color='k')
#
# plt.plot(time_25[0], [_[i] * 1000.0 for _ in s_25][0], linestyle=lineType[2], color='k', label='S$_{12}$')
# plt.plot(time_25[0], [_[i] * 1000.0 for _ in s_25][0], linestyle=lineType[1], color='k', label='S$_{13}$')
# plt.plot(time_25[0], [_[i] * 1000.0 for _ in s_25][0], linestyle=lineType[0], color='k', label='S$_{23}$')
# plt.plot(time_25[0], [_[i] * 1000.0 for _ in s_25][0], linestyle='-', color='b', label='25%')
# plt.plot(time_34[0], [_[i] * 1000.0 for _ in s_34][0], linestyle='-', color='r', label='34%')
# plt.plot(time_42[0], [_[i] * 1000.0 for _ in s_42][0], linestyle='-', color='g', label='42%')
# plt.plot(time_50[0], [_[i] * 1000.0 for _ in s_50][0], linestyle='-', color='m', label='50%')
# ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# # plt.ylim(top=0.75)
# # plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('stress [MPa]')
# plt.title('Average shear stress development (both constituents) within RVE')
# # plt.title('Average stress development (both constituents) within RVE for 50 % gold volume fraction')
# plt.legend()
# fig.tight_layout()
# plt.grid()

# fig = plt.figure()
# ax1 = plt.gca()
# StressLabels = ['S$_{33}$', 'S$_{22}$', 'S$_{11}$']
# # stressIndices = [2, 1, 0]
# stressIndices = [1, 0]
# for i in stressIndices:
#     plt.plot(time_25, [float(_[i]) * 1000.0 for _ in s_g_25],
#              linestyle=lineType[i], color='b')
# for i in stressIndices:
#     plt.plot(time_34, [float(_[i]) * 1000.0 for _ in s_g_34],
#              linestyle=lineType[i], color='r')
# for i in stressIndices:
#     plt.plot(time_42, [float(_[i]) * 1000.0 for _ in s_g_42],
#              linestyle=lineType[i], color='g')
# for i in stressIndices:
#     plt.plot(time_50, [float(_[i]) * 1000.0 for _ in s_g_50],
#              linestyle=lineType[i], color='m')
#
# # plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_g_25][0], linestyle=lineType[2], color='k', label='S$_{11}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_g_25][0], linestyle=lineType[1], color='k', label='S$_{22}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_g_25][0], linestyle=lineType[0], color='k', label='S$_{33}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_g_25][0], linestyle='-', color='b', label='25%')
# plt.plot(time_34[0], [float(_[1]) * 1000.0 for _ in s_g_34][0], linestyle='-', color='r', label='34')
# plt.plot(time_42[0], [float(_[i]) * 1000.0 for _ in s_g_42][0], linestyle='-', color='g', label='42%')
# plt.plot(time_50[0], [float(_[i]) * 1000.0 for _ in s_g_50][0], linestyle='-', color='m', label='50%')
# ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# # plt.ylim(top=10.0, bottom=-80.0)
# # plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('stress [MPa]')
# # plt.title('Average normal stress development of gold within RVE')
# plt.title('Average normal stresses perpendicular to ion flux direction of gold phase development within RVE')
# plt.legend()
# # fig.tight_layout()
# plt.grid()

# fig = plt.figure()
# ax1 = plt.gca()
# StressLabels = ['S$_{23}$', 'S$_{13}$', 'S$_{12}$']
# stressIndices = [5, 4, 3]
# for i in stressIndices:
#     plt.plot(time_25, [float(_[i]) * 1000.0 for _ in s_g_25],
#              linestyle=lineType[i - 3], color='b')
# for i in stressIndices:
#     plt.plot(time_34, [float(_[i]) * 1000.0 for _ in s_g_34],
#              linestyle=lineType[i - 3], color='r')
# for i in stressIndices:
#     plt.plot(time_42, [float(_[i]) * 1000.0 for _ in s_g_42],
#              linestyle=lineType[i - 3], color='g')
# for i in stressIndices:
#     plt.plot(time_50, [float(_[i]) * 1000.0 for _ in s_g_50],
#              linestyle=lineType[i - 3], color='m')
# #
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_g_25][0], linestyle=lineType[2], color='k', label='S$_{12}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_g_25][0], linestyle=lineType[1], color='k', label='S$_{13}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_g_25][0], linestyle=lineType[0], color='k', label='S$_{23}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_g_25][0], linestyle='-', color='b', label='25%')
# plt.plot(time_34[0], [float(_[i]) * 1000.0 for _ in s_g_34][0], linestyle='-', color='r', label='34%')
# plt.plot(time_42[0], [float(_[i]) * 1000.0 for _ in s_g_42][0], linestyle='-', color='g', label='42%')
# plt.plot(time_50[0], [float(_[i]) * 1000.0 for _ in s_g_50][0], linestyle='-', color='m', label='50%')
# ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.ylim(top=3.0, bottom=-2)
# # plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('stress [MPa]')
# plt.title('Average shear stress development of gold within RVE')
# plt.legend()
# fig.tight_layout()
# plt.grid()

#
# fig = plt.figure()
# ax1 = plt.gca()
# StressLabels = ['S$_{33}$', 'S$_{22}$', 'S$_{11}$']
# stressIndices = [2, 1, 0]
# for i in stressIndices:
#     plt.plot(time_25, [float(_[i]) * 1000.0 for _ in s_p_25],
#              linestyle=lineType[i], color='b')
# for i in stressIndices:
#     plt.plot(time_34, [float(_[i]) * 1000.0 for _ in s_p_34],
#              linestyle=lineType[i], color='b')
# for i in stressIndices:
#     plt.plot(time_42, [float(_[i]) * 1000.0 for _ in s_p_42],
#              linestyle=lineType[i], color='g')
# for i in stressIndices:
#     plt.plot(time_50, [float(_[i]) * 1000.0 for _ in s_p_50],
#              linestyle=lineType[i], color='m')
#
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_p_25][0], linestyle=lineType[2], color='k', label='S$_{11}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_p_25][0], linestyle=lineType[1], color='k', label='S$_{22}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_p_25][0], linestyle=lineType[0], color='k', label='S$_{33}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_p_25][0], linestyle='-', color='b', label='25%')
# plt.plot(time_34[0], [float(_[1]) * 1000.0 for _ in s_p_34][0], linestyle='-', color='b', label='Polymer')
# plt.plot(time_42[0], [float(_[i]) * 1000.0 for _ in s_p_42][0], linestyle='-', color='g', label='42%')
# plt.plot(time_50[0], [float(_[i]) * 1000.0 for _ in s_p_50][0], linestyle='-', color='m', label='50%')
# ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.ylim(top=17.5, bottom = -15)
# # plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('stress [MPa]')
# plt.title('Average normal stress development of polymer within RVE')
# plt.legend()
# fig.tight_layout()
# plt.grid()

# fig = plt.figure()
# ax1 = plt.gca()
# StressLabels = ['S$_{23}$', 'S$_{13}$', 'S$_{12}$']
# stressIndices = [5, 4, 3]
# for i in stressIndices:
#     plt.plot(time_25, [float(_[i]) * 1000.0 for _ in s_p_25],
#              linestyle=lineType[i - 3], color='b')
# for i in stressIndices:
#     plt.plot(time_34, [float(_[i]) * 1000.0 for _ in s_p_34],
#              linestyle=lineType[i - 3], color='r')
# for i in stressIndices:
#     plt.plot(time_42, [float(_[i]) * 1000.0 for _ in s_p_42],
#              linestyle=lineType[i - 3], color='g')
# for i in stressIndices:
#     plt.plot(time_50, [float(_[i]) * 1000.0 for _ in s_p_50],
#              linestyle=lineType[i - 3], color='m')
#
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_p_25][0], linestyle=lineType[2], color='k', label='S$_{12}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_p_25][0], linestyle=lineType[1], color='k', label='S$_{13}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_p_25][0], linestyle=lineType[0], color='k', label='S$_{23}$')
# plt.plot(time_25[0], [float(_[i]) * 1000.0 for _ in s_p_25][0], linestyle='-', color='b', label='25%')
# plt.plot(time_34[0], [float(_[i]) * 1000.0 for _ in s_p_34][0], linestyle='-', color='r', label='34%')
# plt.plot(time_42[0], [float(_[i]) * 1000.0 for _ in s_p_42][0], linestyle='-', color='g', label='42%')
# plt.plot(time_50[0], [float(_[i]) * 1000.0 for _ in s_p_50][0], linestyle='-', color='m', label='50%')
# ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.ylim(top=20.0, bottom=-72.5)
# # plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('stress [MPa]')
# plt.title('Average normal stress development in each constituent and the  \n composite as a whole for 24% volume fraction')
# plt.legend()
# fig.tight_layout()
# plt.grid()
#

# fig = plt.figure(2)
# ax2 = plt.gca()
# time_25.index(1750.0)
# # z_g = [z_g_25[time_25.index(1750.0)], z_g_34[time_34.index(1750.0)], z_g_42[time_42.index(1750.0)], z_g_50[time_50.index(1750.0)]]
# # z_p = [z_p_25[time_25.index(1750.0)], z_p_34[time_34.index(1750.0)], z_p_42[time_42.index(1750.0)], z_p_50[time_50.index(1750.0)]]
# z = [z_25[time_25.index(1750.0)], z_34[time_34.index(1750.0)], z_42[time_42.index(1750.0)], z_50[time_50.index(1750.0)]]
# # y_g = [y_g_25[time_25.index(1750.0)], y_g_34[time_34.index(1750.0)], y_g_42[time_42.index(1750.0)], y_g_50[time_50.index(1750.0)]]
# # y_p = [y_p_25[time_25.index(1750.0)], y_p_34[time_34.index(1750.0)], y_p_42[time_42.index(1750.0)], y_p_50[time_50.index(1750.0)]]
# y = [y_25[time_25.index(1750.0)], y_34[time_34.index(1750.0)], y_42[time_42.index(1750.0)], y_50[time_50.index(1750.0)]]
# # log_y = [np.log(i) for i in y]
# # x_g = [x_g_25[time_25.index(1750.0)], x_g_34[time_34.index(1750.0)], x_g_42[time_42.index(1750.0)], x_g_50[time_50.index(1750.0)]]
# # x_p = [x_p_25[time_25.index(1750.0)], x_p_34[time_34.index(1750.0)], x_p_42[time_42.index(1750.0)], x_p_50[time_50.index(1750.0)]]
# x = [x_25[time_25.index(1750.0)], x_34[time_34.index(1750.0)], x_42[time_42.index(1750.0)], x_50[time_50.index(1750.0)]]
# # log_x = [np.log(i) for i in x]
# volFrac = [25,34,42,50]
# # log_volFrac = [np.log(i) for i in volFrac]
# for count,i in enumerate(volFrac):
#     print('Volume fraction: ' + str(i) + '; displacement: ' + str(x[count]))
# # plt.plot(volFrac,z_g, color = 'y',linestyle = '-')
# # plt.plot(volFrac,z_p, color = 'b',linestyle = '-')
# plt.plot(volFrac,z, color = 'k',linestyle = '-')
# # plt.plot(volFrac,y_g, color = 'y',linestyle = ':')
# # plt.plot(volFrac,y_p, color = 'b',linestyle = ':')
# # plt.plot(log_volFrac,log_y, color = 'k',linestyle = ':')
# # plt.loglog(volFrac,y, color = 'k',linestyle = ':')
# plt.plot(volFrac,y, color = 'k',linestyle = ':')
# # plt.plot(volFrac,x_g, color = 'y',linestyle = '-.')
# # plt.plot(volFrac,x_p, color = 'b',linestyle = '-.')
# # plt.plot(log_volFrac,log_x, color = 'k',linestyle = '-.')
# # plt.loglog(volFrac,x, color = 'k',linestyle = '-.')
# # plt.plot(volFrac,x, color = 'k',linestyle = '-.')
#
# plt.plot(volFrac[0],z[0], color = 'k',linestyle = '-',label = 'u$_{x}$ (parallel)')
# plt.plot(volFrac[0],y[0], color = 'k',linestyle = ':',label = 'u$_{y}$ (perpendicular)')
#
# # plt.plot(volFrac[0],x[0], color = 'k',linestyle = '-.',label = 'U$_z$')
#
# # [A,B] = np.polyfit(volFrac,np.log(x),1)
# # x_exp = np.arange(volFrac[0],volFrac[-1],1)
# # y_exp = [np.exp(B)*np.exp(A*_) for _ in x_exp]
# # print(' Equation disp = ' + str(round(np.exp(B),2)) + 'e$^' + str(round(np.exp(A),2)) + 'x$')
# # plt.plot(x_exp,y_exp,'r', label = ' Equation disp = ' + str(round(np.exp(B),2)) + 'e$^{' + str(round(np.exp(A),2)) + '\phi}$')
# # plt.plot(volFrac[0],x_g[0], color = 'y',linestyle = '-',label = 'Gold Constituent')
# # plt.plot(volFrac[0],x_p[0], color = 'b',linestyle = '-',label = 'Polymer Constituent')
# # plt.plot(volFrac[0],x_p[0], color = 'k',linestyle = '-',label = 'Composite')
# plt.xlim(left = 25.0, right = 50.0)
# plt.ylim(bottom=0.0, top = 1.8)
# plt.xlabel('volume fraction [%]')
# plt.ylabel('displacement [nm]')
# plt.title('Volume fraction vs average displacement at time = 1750.0 ')
# plt.legend()
# # fig.tight_layout()
# plt.grid()
#
#
# fig = plt.figure(2)
# ax2 = plt.gca()
#
# plt.plot(time_25, z_25, '-', color='b')
# plt.plot(time_34, z_34, '-', color='r')
# plt.plot(time_42, z_42, '-', color='g')
# plt.plot(time_50, z_50, '-', color='m')
# plt.plot(time_25[0], z_25[0], '-', color='k', label='U$_x$')
#
# plt.plot(time_25, y_25, ':', color='b')
# plt.plot(time_34, y_34, ':', color='r')
# plt.plot(time_42, y_42, ':', color='g')
# plt.plot(time_50, y_50, ':', color='m')
# plt.plot(time_25[0], y_25[0], ':', color='k', label='U$_y$')
#
# plt.plot(time_25, x_25, '--', color='b')
# plt.plot(time_34, x_34, '--', color='r')
# plt.plot(time_42, x_42, '--', color='g')
# plt.plot(time_50, x_50, '--', color='m')
# plt.plot(time_25[0], x_25[0], '--', color='k', label='U$_z$')
#
# plt.plot(time_25[0], z_25[0], '-', color='b', label='25 %')
# plt.plot(time_34[0], z_34[0], '-', color='r', label='34 %')
# plt.plot(time_42[0], z_42[0], '-', color='g', label='42 %')
# plt.plot(time_50[0], z_50[0], '-', color='m', label='50 %')
#
# ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('displacement [nm]')
# plt.title('Average displacement of face inside RVE')
# plt.legend()
# fig.tight_layout()
# plt.grid()
#
#
# fig = plt.figure(3)
# ax2 = plt.gca()
#
# fig, plt = plt.subplots()

# plt.plot(time_25, dispZ_10_25, '-', color='b', label='10 %')
# plt.plot(time_25, dispZ_25_25, '-', color='r', label='25 %')
# plt.plot(time_25, dispZ_50_25, '-', color='g', label='50 %')
# plt.plot(time_25, dispZ_75_25, '-', color='m', label='75 %')
# plt.plot(time_25, dispZ_90_25, '-', color='k', label='90 %')
# plt.plot(time_25[0], conc_90_25[0], '--', color='k', label='Concentration')

# plt.plot(time_42, dispZ_10_42, '-.', color='b', label='10 %')
# plt.plot(time_42, dispZ_25_42, '-.', color='r', label='25 %')
# plt.plot(time_42, dispZ_50_42, '-.', color='g', label='50 %')
# plt.plot(time_42, dispZ_75_42, '-.', color='m', label='75 %')
# plt.plot(time_42, dispZ_90_42, '-.', color='k', label='90 %')
# plt.plot(time_42[0], conc_90_42[0], ':', color='k', label='Concentration')
#
# plt.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.xlim(0.0)
# plt.set_xlabel('time [ns]')
# plt.set_ylabel('displacement [nm]', color='k')
# plt.title('Parallel displacement at various point along flow direction within the RVE')
# plt.legend()
# fig.tight_layout()
# plt.grid()
#
#
# ax9 = plt.twinx()
# fig, ax9 = plt.subplots()
# ax9.plot(time_25, conc_50_25, '--', color='g', label='50 %')
# ax9.plot(time_25, conc_75_25, '--', color='m', label='75 %')
# ax9.plot(time_25, conc_90_25, '--', color='k', label='90 %')
# fig, ax9 = plt.subplots()
# ax9.plot(time_42, conc_50_42, ':', color='g', label='50 %')
# ax9.plot(time_42, conc_75_42, ':', color='m', label='75 %')
# ax9.plot(time_42, conc_90_42, ':', color='k', label='90 %')
# ax9.tick_params('y', colors='b')
# ax9.set_xlabel('time [ns]')
# ax9.set_ylabel('concentration [mol/nm$^3$]', color='b')
# # ax9.ylim(bottom=0.0)
# ax9.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
# plt.title('Average concentration at various point along flow direction within the RVE')
# ax9.legend(loc='best')
# # # #
# plt.grid()
# # fig.tight_layout()
#
# fig = plt.figure()
# ax2 = plt.gca()
#
# plt.plot(time_25, conc_50, '-', color='g', label='50 %')
# plt.plot(time_25, conc_75, '-', color='m', label='75 %')
# plt.plot(time_25, conc_90, '-', color='k', label='90 %')
#
# ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
# plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('displacement [nm]')
# plt.title('Average concentration at various point along flow direction within the RVE')
# plt.legend()
# fig.tight_layout()
# plt.grid()
# z_p_max = max([max(z_p_25), max(z_p_34), max(z_p_42), max(z_p_50)])
# z_g_max = max([max(z_g_25), max(z_g_34), max(z_g_42), max(z_g_50)])
# maxy = max([z_p_max, z_g_max])
# maxy = maxy + 0.1*maxy
# z_p_min = min([min(z_p_25), min(z_p_34), min(z_p_42), min(z_p_50)])
# z_g_min = min([min(z_g_25), min(z_g_34), min(z_g_42), min(z_g_50)])
# miny = min([z_p_min, z_g_min])
# miny = miny + 0.1*miny
# print miny, maxy
# colorC = 0
# fig = plt.figure(2)
# ax2 = plt.gca()
#
# plt.plot(time_25, z_g_25, '--', color='b')
# plt.plot(time_34, z_g_34, '--', color='r')
# plt.plot(time_42, z_g_42, '--', color='g')
# plt.plot(time_50, z_g_50, '--', color='m')
# plt.plot(time_25, z_p_25, '-', color='b', label='25 %')
# plt.plot(time_34, z_p_34, '-', color='r', label='34 %')
# plt.plot(time_42, z_p_42, '-', color='g', label='42 %')
# plt.plot(time_50, z_p_50, '-', color='m', label='50 %')
#
#
# max_z_25 = max(z_p_25)
# max_z_34 = max(z_p_34)
# max_z_42 = max(z_p_42)
# max_z_50 = max(z_p_50)
# plt.plot([time_25[z_p_25.index(max_z_25)], time_34[z_p_34.index(max_z_34)],
# time_42[z_p_42.index(max_z_42)],time_50[z_p_50.index(max_z_50)]],
#      [max_z_25, max_z_34,max_z_42,max_z_50], color = 'k')
#
# plt.plot(time_25[0], z_p_25[0], '-', color = 'k', label = 'Polymer')
# plt.plot(time_25[0], z_p_25[0], '--', color = 'k', label = 'Gold')
#
# ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.ylim(top = maxy, bottom = miny)
# plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('displacement [nm]')
# plt.title('Average displacement in flow direction (u_x) of constituents of face inside RVE')
# plt.legend(loc='best')
# fig.tight_layout()
# plt.grid()
#
#
# fig = plt.figure(3)
# ax3 = plt.gca()
#
# plt.plot(time_25, z_g_25, '--', color='b')
# plt.plot(time_34, z_g_34, '--', color='r')
# plt.plot(time_42, z_g_42, '--', color='g')
# plt.plot(time_50, z_g_50, '--', color='m')
# plt.plot(time_25, z_p_25, '-', color='b', label='25 %')
# plt.plot(time_34, z_p_34, '-', color='r', label='34 %')
# plt.plot(time_42, z_p_42, '-', color='g', label='42 %')
# plt.plot(time_50, z_p_50, '-', color='m', label='50 %')
# #
# pp_g_25_mean = [(y_g_25[i] + x_g_25[i])/2.0 for i in range(len(y_g_25))]
# pp_p_25_mean = [(y_p_25[i] + x_p_25[i])/2.0 for i in range(len(y_p_25))]
# #
# pp_g_34_mean = [(y_g_34[i] + x_g_34[i])/2.0 for i in range(len(y_g_34))]
# pp_p_34_mean = [(y_p_34[i] + x_p_34[i])/2.0 for i in range(len(y_p_34))]
# #
# pp_g_42_mean = [(y_g_42[i] + x_g_42[i])/2.0 for i in range(len(y_g_42))]
# pp_p_42_mean = [(y_p_42[i] + x_p_42[i])/2.0 for i in range(len(y_p_42))]
# #
# pp_g_50_mean = [(y_g_50[i] + x_g_50[i])/2.0 for i in range(len(y_g_50))]
# pp_p_50_mean = [(y_p_50[i] + x_p_50[i])/2.0 for i in range(len(y_p_50))]
# #
# plt.plot(time_25, pp_g_25_mean, ':', color='b')
# plt.plot(time_34, pp_g_34_mean, ':', color='r')
# plt.plot(time_42, pp_g_42_mean, ':', color='g')
# plt.plot(time_50, pp_g_50_mean, ':', color='m')
# #
# plt.plot(time_25, pp_p_25_mean, '-.', color='b')
# plt.plot(time_34, pp_p_34_mean, '-.', color='r')
# plt.plot(time_42, pp_p_42_mean, '-.', color='g')
# plt.plot(time_50, pp_p_50_mean, '-.', color='m')
# #
# plt.plot(time_25[0], z_p_25[0], '-', color = 'k', label = 'Polymer')
# plt.plot(time_25[0], z_p_25[0], '--', color = 'k', label = 'Gold')
# plt.plot(time_25[0], z_p_25[0], ':', color = 'k', label = 'Perpendicular: Gold')
# plt.plot(time_25[0], z_p_25[0], '-.', color = 'k', label = 'Perpendicular: Polymer')
# #
# ax3.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# # plt.ylim(top = 0.75)
# plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('displacement [nm]')
# plt.title('Average displacement of constituents of face inside RVE')
# plt.legend(loc='best')
# fig.tight_layout()
# plt.grid()
#

# fig = plt.figure(4)
# ax4 = plt.gca()
#
# plt.plot(time_25, y_g_25, '--', color='b')
# plt.plot(time_34, y_g_34, '--', color='r')
# plt.plot(time_42, y_g_42, '--', color='g')
# plt.plot(time_50, y_g_50, '--', color='m')
#
# plt.plot(time_25, y_p_25, '--', color='b')
# plt.plot(time_34, y_p_34, '--', color='r')
# plt.plot(time_42, y_p_42, '--', color='g')
# plt.plot(time_50, y_p_50, '--', color='m')
#
# plt.plot(time_25, x_g_25, ':', color='b')
# plt.plot(time_34, x_g_34, ':', color='r')
# plt.plot(time_42, x_g_42, ':', color='g')
# plt.plot(time_50, x_g_50, ':', color='m')
#
# plt.plot(time_25, x_p_25, ':', color='b')
# plt.plot(time_34, x_p_34, ':', color='r')
# plt.plot(time_42, x_p_42, '-', color='g', label='42 %')
# plt.plot(time_42, x_p_42, ':', color='g')
# plt.plot(time_50, x_p_50, ':', color='m')
#
# plt.plot(time_25, z_g_25, '-', color='b')
# plt.plot(time_34, z_g_34, '-', color='r')
# plt.plot(time_42, z_g_42, '-', color='g')
# plt.plot(time_50, z_g_50, '-', color='m')
# #
# plt.plot(time_25, z_p_25, '-', color='b', label='25 %')
# plt.plot(time_34, z_p_34, '-', color='r', label='34 %')
# plt.plot(time_42, z_p_42, '-', color='g', label='42 %')
# plt.plot(time_42, z_p_42, '-', color='g', label='42 %')
# plt.plot(time_50, z_p_50, '-', color='m', label='50 %')
#
# plt.plot(time_25[0], x_p_25[0], '-', color = 'k', label = 'u_x')
# plt.plot(time_25[0], x_p_25[0], ':', color = 'k', label = 'u_y')
# plt.plot(time_25[0], x_p_25[0], '--', color = 'k', label = 'u_z')
# #
# plt.plot(time_42[0], x_p_42[0], '--', color = 'k', label = 'u_x')
# plt.plot(time_42[0], x_p_42[0], ':', color = 'k', label = 'u_y')
# plt.plot(time_42[0], x_p_42[0], '-', color = 'k', label = 'u_z')
#
# plt.plot(time_25[0], x_p_25[0], '--', color = 'k', label = 'u_y: Gold')
# plt.plot(time_25[0], x_p_25[0], '-.', color = 'k', label = 'u_y: Polymer')
# plt.plot(time_25[0], x_p_25[0], ':', color = 'k', label = 'u_x: Gold')
# plt.plot(time_25[0], x_p_25[0], '-', color = 'k', label = 'u_x: Polymer')
# ax4.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.ylim(top = 0.75)
# plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('displacement [nm]')
# plt.title('Average displacement of constituents of face (70%) within RVE for each volume fractions')
# plt.title('Average displacement perpendicular to the flow direction of constituents of face inside RVE')
# plt.legend(loc='best')
# fig.tight_layout()
# plt.grid()

#
#
# fig = plt.figure(5)
# ax5 = plt.gca()
# #
# plt.plot(time_25, x_g_25, ':', color='b')
# plt.plot(time_34, x_g_34, ':', color='r')
# plt.plot(time_42, x_g_42, ':', color='g')
# plt.plot(time_50, x_g_50, ':', color='m')
# #
# plt.plot(time_25, x_p_25, '-', color='b', label = '25 %')
# plt.plot(time_34, x_p_34, '-', color='r', label='34 %')
# plt.plot(time_42, x_p_42, '-', color='g', label='42 %')
# plt.plot(time_50, x_p_50, '-', color='m', label='50 %')
# #
# plt.plot(time_25[0], x_p_25[0], ':', color = 'k', label = 'Gold')
# plt.plot(time_25[0], x_p_25[0], '-', color = 'k', label = 'Polymer')
# ax5.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.ylim(top = 0.75)
# plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('displacement [nm]')
# plt.title('Average displacement perpendicular to the flow direction (u_z) of constituents of face inside RVE')
# plt.legend(loc='best')
# fig.tight_layout()
# plt.grid()
#
#
# fig = plt.figure(6)
# ax6 = plt.gca()
# # colorC += 1
# plt.plot(time_25, y_g_25, '--', color='b')
# plt.plot(time_34, y_g_34, '--', color='r')
# plt.plot(time_42, y_g_42, '--', color='g')
# plt.plot(time_50, y_g_50, '--', color='m')
# #
# plt.plot(time_25, y_p_25, '-', color='b', label = '25 %')
# plt.plot(time_34, y_p_34, '-', color='r', label = '34 %')
# plt.plot(time_42, y_p_42, '-', color='g', label = '42 %')
# plt.plot(time_50, y_p_50, '-', color='m', label = '50 %')
# plt.plot(time_25[0], y_p_25[0], '--', color = 'k', label = 'Gold')
# plt.plot(time_25[0], y_p_25[0], '-', color = 'k', label = 'Polymer')
# ax6.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.ylim(top = 0.75)
# plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('displacement [nm]')
# plt.title('Average displacement perpendicular to the flow direction (u_y) of constituents of face inside RVE')
# plt.legend(loc='best')
# fig.tight_layout()
# plt.grid()
#
#
# fig = plt.figure(7)
# ax7 = plt.gca()
# # colorC += 1
# plt.plot(time_25, Conc_25, '-', color='b', label = '25 %')
# plt.plot(time_34, Conc_34, '-', color='r', label = '34 %')
# plt.plot(time_42, Conc_42, '-', color='g', label = '42 %')
# plt.plot(time_50, Conc_50, '-', color='m', label = '50 %')
# ax7.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
# # plt.ylim(top = 0.75)
# plt.xlim(0.0)
# plt.xlabel('time [ns]')
# plt.ylabel('concentration [mol/nm$^3$]')
# plt.title('Average concentration of face inside RVE')
# plt.legend(loc='best')
# fig.tight_layout()
# plt.grid()
#
#

fig, ax8 = plt.subplots()

# test = x_34
# time = time_34
# windowSize = [9]
# fig = plt.figure()
# ax1 = plt.gca()
# plt.plot(time_25, test, label='Full results', color = 'r')
#
# plt.plot(time, test, ':', color='r', label='Full')
colours = ['k', 'b',  'k', 'g', 'm']
# for count, w in enumerate(windowSize):
#     weights = np.repeat(1.0, w) / w
#     yMA = np.convolve(test, weights, 'valid')

    # lineType = [':', '--', '-']
    #
    # StressLabels = ['S$_{33}$', 'S$_{22}$', 'S$_{11}$']
    # stressIndices = [2, 1, 0]
    # stressIndices = [1, 0]
    # end = -1*(w-2)
    # plt.plot(time[:2] + [time[2]], test[:2] + [yMA[0]], label='Smoothed: ' + str(w), color = colours[count])
    # plt.plot(time[2:end+1], yMA, label='Smoothed: ' + str(w), color = colours[count])

# plt.plot(time_25, x_25, '-', color='b')
# plt.plot(time_25, z_g_25, '--', color='b')
# plt.plot(time_34, x_34, '-', color='r')
# plt.plot(time_42, x_42, '-', color='g')
# plt.plot(time_42, z_g_42, '--', color='g')
# plt.plot(time_50, x_50, '--', color='m')
# plt.plot(time_50, x_g_50, '--', color='m')


pop_values_25 = [300.0, 700.0, 1000.0, 1300.0, 1600.0]
for k in pop_values_25:
    time_25.remove(k)
    x_25.pop(time_25.index(k))
    z_25.pop(time_25.index(k))
    Conc_25.pop(time_25.index(k))

pop_values_34 = [300.0, 600.0, 800.0, 1200.0, 1500.0]
for k in pop_values_34:
    time_34.remove(k)
    x_34.pop(time_34.index(k))
    z_34.pop(time_34.index(k))
    Conc_34.pop(time_34.index(k))

pop_values_42 = [300.0, 600.0, 900.0, 1200.0, 1500.0]
for k in pop_values_42:
    time_42.remove(k)
    x_42.pop(time_42.index(k))
    z_42.pop(time_42.index(k))
    Conc_42.pop(time_42.index(k))

pop_values_50 = [400.0, 700.0, 1000.0, 1300.0, 1600.0]
for k in pop_values_50:
    time_50.remove(k)
    x_50.pop(time_50.index(k))
    z_50.pop(time_50.index(k))
    Conc_50.pop(time_50.index(k))

def smoothing(x,y):
    # Smoothed moving average
    w = 7
    weights = np.repeat(1.0, w) / w
    yMA = np.convolve(y, weights, 'valid')

    #  Savitzky-Golay digital filter
    points = 17
    y_filtered = savgol_filter(yMA, points, 2)
    x_filtered = x[2:-4]
    return x_filtered, y_filtered

# plt.plot(time_25, x_25, '-', color='b', label='25 %')

time_filtered_25, x_filtered_25 = smoothing(time_25,x_25)
# time_filtered_25, z_filtered_25 = smoothing(time_25,z_25)
end_index_25 = time_filtered_25.index(1750.0)+1
ax8.plot(time_filtered_25[:end_index_25],x_filtered_25[:end_index_25], '-', color = 'b', label='25 %')
ax8.plot(time_25[:3],x_25[:2] + [x_filtered_25[0]],'-',color = 'b')
# plt.plot(time_filtered_25[:end_index_25],z_filtered_25[:end_index_25], ':', color = 'b', label='U_parallel')
# time_new_25 = time_25[2:-2], label='25 %'
time_filtered_34, x_filtered_34 = smoothing(time_34,x_34)
time_filtered_34, z_filtered_34 = smoothing(time_34,z_34)
end_index_34 = time_filtered_34.index(1750.0)+1
ax8.plot(time_filtered_34[:end_index_34],x_filtered_34[:end_index_34], '-', color = 'r', label='34 %')
ax8.plot(time_34[:3],x_34[:2] + [x_filtered_34[0]],'-',color = 'r')
# plt.plot(time_filtered_34[:end_index_34],z_filtered_34[:end_index_34], ':', color = 'r')
#
time_filtered_42, x_filtered_42 = smoothing(time_42,x_42)
time_filtered_42, z_filtered_42 = smoothing(time_42,z_42)
end_index_42 = time_filtered_42.index(1750.0)+1
ax8.plot(time_filtered_42[:end_index_42],x_filtered_42[:end_index_42], '-', color = 'g', label='42 %')
ax8.plot([time_42[0],time_42[2]],x_42[:1] + [x_filtered_42[0]],'-',color = 'g')
# plt.plot(time_filtered_42[:end_index_42],z_filtered_42[:end_index_42], ':', color = 'g')
#
time_filtered_50, x_filtered_50 = smoothing(time_50,x_50)
time_filtered_50, z_filtered_50 = smoothing(time_50,z_50)
end_index_50 = time_filtered_50.index(1750.0)+1
ax8.plot(time_filtered_50[:end_index_50],x_filtered_50[:end_index_50], '-', color = 'm', label='50 %')
ax8.plot([time_50[0],time_50[2]],x_50[:1] + [x_filtered_50[0]],'-',color = 'm')
# plt.plot(time_filtered_50[:end_index_50],z_filtered_50[:end_index_50], ':', color = 'm')

# volFrac = [25,34,42,50]
# x_max = [x_filtered_25[-1], x_filtered_34[-1], x_filtered_42[-1], x_filtered_50[-1]]
# z_max = [z_filtered_25[-1], z_filtered_34[-1], z_filtered_42[-1], z_filtered_50[-1]]
#
# plt.plot(volFrac, z_max, '-', color = 'k', label = 'u$_x$ (parallel)')
# plt.plot(volFrac, x_max , '--', color = 'k', label = 'u$_y$ (perpendicular)')
# plt.xlabel('gold volume fraction [%]')
# plt.ylabel('displacement [ns]')
# plt.xlim(left=25, right=50)
# plt.ylim(bottom=0.0, top=1.80)
# # ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.legend()
# plt.grid()
# max_x_25 = max(x_filtered_25[:time_filtered_25.index(300.0)])
# max_t_25 = time_filtered_25[list(x_filtered_25).index(max_x_25)]
# for count, i in enumerate(volFrac):
#     print('Volume fraction: ' + str(i))
#     print("Parallel: " + str(z_max[count]))
#     print("Perpendicular: " + str(x_max[count]))
# print()
#
# max_x_34 = max(x_filtered_34[:time_filtered_34.index(300.0)])
# max_t_34 = time_filtered_34[list(x_filtered_34).index(max_x_34)]
# print('34 %)')
# print(max_x_34, max_t_34)
# print()
#
# max_x_42 = max(x_filtered_42[:time_filtered_42.index(300.0)])
# max_t_42 = time_filtered_42[list(x_filtered_42).index(max_x_42)]
# print('42 %)')
# print(max_x_42, max_t_42)
# print()
#
# max_x_50 = max(x_filtered_50[:time_filtered_50.index(300.0)])
# max_t_50 = time_filtered_50[list(x_filtered_50).index(max_x_50)]
# print('50 %)')
# print(max_x_50, max_t_50)
# print()
# w = 3
# weights = np.repeat(1.0, w) / w
# yMA_25_2 = np.convolve(yMA_25, weights, 'valid')
# plt.plot(time_25[:2], yMA_25[:2] + [yMA_25_2[0]], color = 'r', label='25 %')
# plt.plot(time_new_25[1:-1], yMA_25_2, label='Smoothed: ' + str(w), color = 'r')
#
# plt.plot(time_34, x_34, '-', color='r', label='34 %')
# w = 7
# weights = np.repeat(1.0, w) / w
# yMA_34 = np.convolve(x_34, weights, 'valid')
# plt.plot(time_34[:2] + [time_34[2]], x_34[:2] + [yMA_34[0]], color = 'r', label='34 %')
# plt.plot(time_34[2:-4], yMA_34, label='Smoothed: ' + str(w), color = 'r')
#
# # plt.plot(time_42, x_42, '-', color='g', label='42 %')
# weights = np.repeat(1.0, w) / w
# yMA_42 = np.convolve(x_42, weights, 'valid')
# plt.plot(time_42[:2] + [time_42[2]], x_42[:2] + [yMA_42[0]], color = 'g', label='42 %')
# plt.plot(time_42[2:-4], yMA_42, label='Smoothed: ' + str(w), color = 'g')
#
# # plt.plot(time_50, x_50, '-', color='m', label='50 %')
# weights = np.repeat(1.0, w) / w
# yMA_50 = np.convolve(x_50, weights, 'valid')
# plt.plot(time_50[:2] + [time_50[2]], x_50[:2] + [yMA_50[0]], color = 'm', label='50 %')
# plt.plot(time_50[2:-4], yMA_50, label='Smoothed: ' + str(w), color = 'm')
#
plt.plot(time_25[0], x_25[0], '--', color='k', label='Concentration')
plt.plot(time_25[0], x_25[0], '-', color='k', label='Displacement')
# #
ax8.set_xlabel('time [ns]')
ax8.set_ylabel('displacement [nm]', color='k')
ax8.set_ylim(bottom=0.0, top=0.5)
ax8.set_xlim(left = 0.0)
start, end = ax8.get_ylim()
ax8.set_yticks(np.arange(start, end + (end-start)/5.0, (end-start)/5.0))
ax8.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.tick_params('y', colors='k')
# # plt.title('Average displacement parallel to the flow direction (u_x) of constituents of face inside RVE')
# # plt.title('Average displacement perpendicular to the flow direction (u_z) midway through RVE')
# plt.ylim(bottom=0.0)
# #
ax9 = plt.twinx()
ax9.plot(time_25[:time_25.index(1750.0)+1], Conc_25[:time_25.index(1750.0)+1], '--', color='b')
ax9.plot(time_34[:time_34.index(1750.0)+1], Conc_34[:time_34.index(1750.0)+1], '--', color='r')
ax9.plot(time_42[:time_42.index(1750.0)+1], Conc_42[:time_42.index(1750.0)+1], '--', color='g')
ax9.plot(time_50[:time_50.index(1750.0)+1], Conc_50[:time_50.index(1750.0)+1], '--', color='m')
ax9.set_ylabel('concentration [mol/nm$^3$]', color='k')
ax9.set_ylim(bottom=1.3E-04)
ax9.set_xlim(left = 0.0, right = 1750)
start, end = ax9.get_ylim()
ax9.set_yticks(np.arange(start, end + (end-start)/5.0, (end-start)/5.0))
ax9.set_xticks(np.arange(0, 1750+1, 250.0))
ax9.tick_params('y', colors='k')
ax9.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
ax8.legend()
#
# plt.grid()
ax9.grid()
ax8.grid()
# fig.tight_layout()
#
# """
plt.show()
