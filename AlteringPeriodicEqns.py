# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 14:27:37 2018

@author: cerecam

Changing periodic equation to remove equatiosn related to Z_REF_PNT
(only perioidic on faces perpendicular to transport axis)
"""
ExtraZ = [34849, 34882, 34915, 34948, 34981, 35014, 35047, 35080, 35113, 35146,
          35179, 35212, 35245, 35278, 35311, 35344, 35377, 35410, 35443, 35476,
          35509, 35542, 35575, 35608, 35641, 35674, 35707, 35740, 35773, 35806,
          35839, 35872, 35905, 35941, 34850, 34851, 34852, 34853, 34854, 34855, 34856, 34857, 34858, 34859,
          34860, 34861, 34862, 34863, 34864, 34865, 34866, 34867, 34868, 34869,
          34870, 34871, 34872, 34873, 34874, 34875, 34876, 34877, 34878, 34879,
          34880]
EdgeZ = list(set(
             [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
              30, 31, 32, 33,  # X0Z0
              1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073,
              1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089,  # X1Z0
              33, 66, 99, 132, 165, 198, 231, 264, 297, 330, 363, 396, 429, 462, 495, 528, 561, 594, 627, 660, 693, 726,
              759, 792, 825, 858, 891, 924, 957, 990, 1023, 1056, 1089,  # Y1Z0
              1, 34, 67, 100, 133, 166, 199, 232, 265, 298, 331, 364, 397, 430, 463, 496, 529, 562, 595, 628, 661, 694,
              727, 760, 793, 826, 859, 892, 925, 958, 991, 1024, 1057,  # Y0Z0
              34849, 34850, 34851, 34852, 34853, 34854, 34855, 34856, 34857, 34858, 34859, 34860, 34861, 34862, 34863,
              34864, 34865, 34866, 34867, 34868, 34869, 34870, 34871, 34872, 34873, 34874, 34875, 34876, 34877, 34878,
              34879, 34880, 34881,  # X0Z1
              35905, 35906, 35907, 35908, 35909, 35910, 35911, 35912, 35913, 35914, 35915, 35916, 35917, 35918, 35919,
              35920, 35921, 35922, 35923, 35924, 35925, 35926, 35927, 35928, 35929, 35930, 35931, 35932, 35933, 35934,
              35935, 35936, 35937,  # X1Z1
              34849, 34882, 34915, 34948, 34981, 35014, 35047, 35080, 35113, 35146, 35179, 35212, 35245, 35278, 35311,
              35344, 35377, 35410, 35443, 35476, 35509, 35542, 35575, 35608, 35641, 35674, 35707, 35740, 35773, 35806,
              35839, 35872, 35905,  # Y0Z1
              34881, 34914, 34947, 34980, 35013, 35046, 35079, 35112, 35145, 35178, 35211, 35244, 35277, 35310, 35343,
              35376, 35409, 35442, 35475, 35508, 35541, 35574, 35607, 35640, 35673, 35706, 35739, 35772, 35805, 35838,
              35871, 35904, 35937  # Y1Z1
              ]))
EZcheck = []
cwd1 = '/home/cerecam/Desktop/Voxel_models/2M_32x32x32'
cwd2 = '/home/cerecam/Desktop/GP_BoundaryConditionTests/NodeSets'
# cwd = '/home/cerecam/Desktop/MesoporousSilica/Short'
with open(cwd1 + '/PBC_Equations.inp', 'r') as readf:
    line = readf.read()
line = line.split('*Equation\n')
del line[0]
print(len(line))
count = 0
for ind, val in enumerate(line):
    newarray = val.strip().split('\n')
    line[ind] = newarray
xref = []
yref = []
zref = []
xyref = []
xzref = []
yzref = []
xyzref = []
PeriodicN = []
for x in line:
    if x[0] == '3':
        if x[3][0] == 'X':
            xref.append(x)
        if x[3][0] == 'Y':
            yref.append(x)
        if x[3][0] == 'Z':
            zref.append(x)
    elif x[0] == '4':
        if x[3][0] == 'X' and x[4][0] == 'Y':
            xyref.append(x)
        if x[3][0] == 'X' and x[4][0] == 'Z':
            xzref.append(x)
        if x[3][0] == 'Y' and x[4][0] == 'Z':
            yzref.append(x)
    elif x[0] == '5':
        xyzref.append(x)
    else:
        print('ERROR')
        print(line)
check = []
for x in xref:
    check.append(x)
    PeriodicN.append(int(x[1].split(',')[0].split('_')[-1]))
    PeriodicN.append(int(x[2].split(',')[0].split('_')[-1]))
for x in yref:
    check.append(x)
    PeriodicN.append(int(x[1].split(',')[0].split('_')[-1]))
    PeriodicN.append(int(x[2].split(',')[0].split('_')[-1]))
for x in zref:
    if any([y == int(x[1].split(',')[0].split('_')[-1]) for y in ExtraZ]):
        check.append(x)
        PeriodicN.append(int(x[1].split(',')[0].split('_')[-1]))
for x in xyref:
    check.append(x)
    PeriodicN.append(int(x[1].split(',')[0].split('_')[-1]))
    PeriodicN.append(int(x[2].split(',')[0].split('_')[-1]))
for x in xzref:
    check.append(x)
    PeriodicN.append(int(x[1].split(',')[0].split('_')[-1]))
    PeriodicN.append(int(x[2].split(',')[0].split('_')[-1]))
for x in yzref:
    check.append(x)
    PeriodicN.append(int(x[1].split(',')[0].split('_')[-1]))
    PeriodicN.append(int(x[2].split(',')[0].split('_')[-1]))
for x in xyzref:
    check.append(x)
    PeriodicN.append(int(x[1].split(',')[0].split('_')[-1]))
    PeriodicN.append(int(x[2].split(',')[0].split('_')[-1]))

PeriodicN = list(set(PeriodicN))

with open(cwd2 + '/PBC_Equations_noZEdge.inp', 'w') as writef:
    for s in check:
        if all([z != int(s[1].split('_')[-1].split(',')[0]) for z in EdgeZ]) or all(
                [p != int(s[2].split('_')[-1].split(',')[0]) for p in EdgeZ]):
            EZcheck.append(s[1].split('_')[-1].split(',')[0])
            #            print(s)
            writef.write('*Equation\n')
            for y in s:
                writef.write(y + '\n')
        else:
            pass
            #            print(s)
            #            if s[1].split(',')[1]=='1' or s[1].split(',')[1]=='2':
            #                print('yes')
            # writef.write('*Equation\n')
            # for y in s:
            #     writef.write(y + '\n')

with open(cwd2 + '/PeriodicNodes2.inp', 'w') as writef:
    writef.write('*Nset,nset=PeriodicNodes2,instance=RVE \n')
    for x in range(0, len(PeriodicN), 10):
        writef.write(''.join(str(PeriodicN[x:x + 10])).strip('[').strip(']') + '\n')
