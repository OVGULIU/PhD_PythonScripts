"""
Script to create a 2D section of an RVE from a 3D representatiev cube.
Given: Nset with all nodes on plane
Required: Element file with ICA
"""
import os
from subprocess import call
metalFrac = '60'

cwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/'

bash_script = open(cwd + "post_python_script.sh" , 'w')
vol_fractions = []

with open(cwd + 'MetalElements.inp', 'r') as metalread:
    data = metalread.readlines()
metalMax = int(data[-1].split(',')[0])
metalMin = int(data[0].split(',')[0])

with open(cwd + 'PolymerElements.inp', 'r') as polymerread:
    data = polymerread.readlines()
polymerMax = int(data[-1].split(',')[0])
polymerMin = int(data[0].split(',')[0])

polyElements = range(polymerMin, polymerMax +1, 1)
metalElements = range(metalMin, metalMax + 1, 1)

for RVE_number in ['1','2','3','4','5','6']:
# for RVE_number in ['1G']:
    RVE_name = 'RVE_2D_' + metalFrac + 'PER_' + RVE_number
    nsetFname = RVE_name + '.inp' # Nset of nodes within planar RVE section
    elsetFname = RVE_name + '_elset.inp' # Elset of nodes within planar RVE section
    allNodes = 'Nodes.inp' # All nodes within 3D RVE
    allElements = 'Elements.inp' # All elements within 3D RVE
    plane = [1,2] # Plane on which 2D slice sits: xy plane = [1,2], nodes = [5,6,7,8]; xz plane = [1,3]; yz plane = [2,3], nodes = [5,8,4,1]
    elementNodes = [5,6,7,8] # element node numbering order
    enlargementFactor = 6.72 # enlargement factor to apply to RVE


    #Output Filenames
    plane_ICA_file = RVE_name + '_Elements.inp'
    outpolyEle_file = RVE_name + '_PolyElements.inp'
    outmetalEle_file = RVE_name + '_MetalElements.inp'
    RVE_Nodes =  RVE_name + '_Nodes.inp'


    with open(cwd+nsetFname, 'r') as nsetFile:
        firstLine = nsetFile.readline().split(',')
        if firstLine[-1].strip().lower() =='generate':
            dataLine = nsetFile.readline().split(',')
            nsetValues = list(range(int(dataLine[0]),int(dataLine[1])+1,int(dataLine[2])))
        else:
            nsetValues = []
            for line in nsetFile:
                nsetValues.extend(int(x) for x in line.strip().split(','))
    print('Number of nodes on the plane (expect 33282): ' + str(len(nsetValues)))

    with open(cwd + elsetFname, 'r') as elsetFile:
        firstLine = elsetFile.readline().split(',')
        if firstLine[-1].strip().lower() == 'generate':
            dataLine = elsetFile.readline().split(',')
            elsetValues = list(range(int(dataLine[0]), int(dataLine[1]) + 1, int(dataLine[2])))
        else:
            elsetValues = []
            for line in elsetFile:
                elsetValues.extend(int(x) for x in line.strip().split(','))


    print('Number of elements on the plane (expect 16384): ' + str(len(elsetValues)))

    max_node_val = -5000000
    min_node_val = 5000000
    with open(cwd + allNodes, 'r') as allNodeFile:
        nodeDict = {}
        newPlanecoords_4nodes = []
        allNodeList = allNodeFile.readlines()
    min_NodeNum = int(allNodeList[sorted(nsetValues)[0]].split(',')[0])-1
    print('min_NodeNum: ' + str(min_NodeNum))
    for entry in nsetValues:
        dataLine = [int(allNodeList[entry].split(',')[0])-min_NodeNum] + [float(i.strip()) for i in [allNodeList[entry].split(',')[plane[0]],allNodeList[entry].split(',')[plane[1]]]]
        if max(dataLine[1:]) >max_node_val:
            max_node_val = max(dataLine[1:])
        if min(dataLine[1:]) < min_node_val:
            min_node_val = min(dataLine[1:])
        nodeDict[dataLine[0]]  = dataLine[1:]
        newPlanecoords_4nodes.append(dataLine)
    # print('RVE dimensions: min= '+ str(min_node_val) + '; max= ' + str(max_node_val))


    with open(cwd + allElements, 'r') as allEleFile:
        eleDict = {}
        newPlaneICA_4nodes = []
        polyEle = []
        metalEle = []
        allEleList = allEleFile.readlines()
    for entry in elsetValues:
        dataLine = [int(i.strip()) for i in allEleList[entry-1].split(',')]
        eleDict[dataLine[0]]  = dataLine[1:]
        nodeNumbering  = [i-min_NodeNum for i in [dataLine[elementNodes[0]], dataLine[elementNodes[1]], dataLine[elementNodes[2]], dataLine[elementNodes[3]]]]
        newPlaneICA_4nodes.append([dataLine[0]] + nodeNumbering)
        if dataLine[0]<=polyElements[-1] and dataLine[0]>=polyElements[0]:
            polyEle.extend([int(dataLine[0])])
        else:
            metalEle.extend([int(dataLine[0])])


    with open(cwd+RVE_Nodes,'w') as outputICA:
        outputICA.write('*Node\n')
        for i in newPlanecoords_4nodes:
            outputICA.write(str(i).strip('[').strip(']') + '\n')

    with open(cwd+plane_ICA_file,'w') as outputICA:
        for i in newPlaneICA_4nodes:
            outputICA.write(str(i).strip('[').strip(']') + '\n')

    with open(cwd+outpolyEle_file,'w') as outputICA:
        for i in range(0,len(polyEle)+1,10):
            outputICA.write(str(polyEle[i:i+10]).strip('[').strip(']') + '\n')

    with open(cwd+outmetalEle_file,'w') as outputICA:
        for i in range(0,len(metalEle)+1,10):
            outputICA.write(str(metalEle[i:i+10]).strip('[').strip(']') + '\n')


    # print('Number of elements on plane (expect 16384): ' + str(len(newPlaneICA_4nodes)))
    # print('Number of polymer elements on plane : ' + str(len(polyEle)))
    # print('Number of metal elements on plane : ' + str(len(metalEle)))
    # print('Volume Fraction of metal: ' + str(len(metalEle)/float(len(newPlaneICA_4nodes))))
    vol_fractions.append(str(len(metalEle)/float(len(newPlaneICA_4nodes))))

    enlargement = enlargementFactor/max_node_val
    # print('Enlarging nodes by a factor of ' + str(enlargement))
    # cwd = '/home/cerecam/2M_128x128x128_full/2D_Planes/'
    fread = open(cwd + RVE_Nodes, 'r')
    fwrite = open(cwd + "scaled_" + RVE_Nodes, 'w')
    line1 = fread.readline()
    fwrite.write(line1)
    for line in fread:
        newline = [float(x) for x in line.split(',')]
        newline[0] = int(newline[0])
        newline[1:] = [i * enlargement for i in newline[1:]]
        fwrite.write(str(newline).strip(']').strip('[') + '\n')

    fread.close()
    fwrite.close()

    bash_script.write("cp " + cwd + RVE_name + "_Nodes.inp " + cwd + "old_" + RVE_name + "_Nodes.inp \n")
    bash_script.write("cp " + cwd + "scaled_" + RVE_name + "_Nodes.inp " + cwd + RVE_name + "_Nodes.inp \n")
    print("Section " + str(RVE_number) + " done.")
# print(vol_fractions)
bash_script.write("echo \"" + ', \t'.join([str(p) for p in vol_fractions]) + '\"\n')
bash_script.close()