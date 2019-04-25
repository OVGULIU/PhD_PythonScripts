"""
Script to extract displacement and reaction force data from a tensile test with the aim of creating a load displacement curve

Inputs (variables to define):
    1. cwd
    2. odbname (no ext)
    3. ULnode
    4. UHnode

Output:
    None (file that contains  RF, UL and UH for every time step up until fracture)

"""
import sys
from odbAccess import openOdb
cwd = sys.argv[-1]
odbname = sys.argv[-2]
outputFname = sys.argv[-3]
UHnode = int(sys.argv[-4])
ULnode = int(sys.argv[-5])

odbname = odbname + '.odb'

odb = openOdb(cwd + odbname)
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
all_frames = steps.frames
last_frame = all_frames[-1]
assem = odb.rootAssembly
histData = list(steps.historyRegions.items())
histData = [(int(x[0].split('.')[-1]), x[1]) for x in histData[1:]]
histData.sort(key=lambda x: x[0])
RF = [0.0]*len(histData[1][1].historyOutputs[histData[1][1].historyOutputs.keys()[0]].data)
UL = []
UH = []
for i in histData:
    hKeys = i[1].historyOutputs.keys()
    time = [t[0] for t in i[1].historyOutputs[hKeys[0]].data]
    if 'RF2' in hKeys:
        for c,k in enumerate(i[1].historyOutputs['RF2'].data):
            RF[c] = RF[c] + k[-1]
    if i[0] == ULnode:
        for c,k in enumerate(i[1].historyOutputs['U2'].data):
            UL.append(k[-1])
    if i[0] == UHnode:
        for c,k in enumerate(i[1].historyOutputs['U2'].data):
            UH.append(k[-1])


RFplot = RF
ULplot = UL
UHplot = UH

with open(cwd + outputFname, 'w') as fOut:
    for i in range(len(RFplot)):
        fOut.write(', \t'.join([str(RFplot[i]),str(ULplot[i]),str(UHplot[i]), str(UHplot[i]-ULplot[i])])+ '\n')

odb.close()