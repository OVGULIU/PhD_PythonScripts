import numpy as np
cwd = '/home/cerecam/Desktop/Crack_Models/30PER/1/'
with open(cwd  + 'MetalNodes.inp') as dataFile:
    dataFile.readline()
    metalNodesData = dataFile.readlines()
metalNodes= []
for i in metalNodesData:
    metalNodes.extend([int(k) for k in i.split(',')])

with open(cwd + 'Boundary_nodes.inp') as boundaryNsetFile:
    boundaryNode_data = boundaryNsetFile.readlines()

boundaryNodes = []
boundaryNsets = {}
for line in boundaryNode_data:
    if line == '\n':
        break
    elif line[0] == '*':
        firstline = line.split(',')
        boundaryNsets[firstline[1].split('=')[- 1].strip().lower()] = []
    elif firstline[-1].strip().lower() == 'generate':
        splitline = line.strip().split(',')
        boundaryNodes.extend(range(int(splitline[0]), int(splitline[1]) + 1, int(splitline[2])))
        boundaryNsets[firstline[1].split('=')[- 1].strip().lower()] = list(range(int(splitline[0]), int(splitline[1]) + 1,
                                                                             int(splitline[2])))
    else:
        splitline = line.strip().split(',')
        boundaryNodes.extend(int(x) for x in splitline)
        boundaryNsets[firstline[1].split('=')[- 1].strip().lower()].extend(int(x) for x in splitline)

boundaryNodes = list(set(boundaryNodes))
for key, item in boundaryNsets.items():
    item.sort()

newNodeFilename = 'Pure_MetalNodes_withBoundary.inp'
newNodeFile = open(cwd + newNodeFilename, 'w')
newNodeFile.write('*Node \n')
with open(cwd+'Nodes.inp','r') as allNodesFile:
    allNodeList = allNodesFile.readlines()

RVE_nodes = sorted(list(set(metalNodes+boundaryNodes)))
for entry in RVE_nodes:
    dataLine = [int(allNodeList[entry].split(',')[0])] + [float(i.strip()) for i in
                                                                        allNodeList[entry].split(',')[1:]]
    newNodeFile.write(str(dataLine).strip('[').strip(']') + '\n')

newNodeFile.close()

with open(cwd + 'NsetsNodes.inp', 'w') as nsetFiles:
    for i in boundaryNodes:
        nsetFiles.write('*Nset, nset=RVE_'+ str(i) + ', instance=RVE \n')
        nsetFiles.write(str(i) + '\n')

equationsFile = open(cwd + 'PBC_Equations4.inp', 'w')
for i in boundaryNsets['x0_nodes']:
    for dof in [', 1, ',', 2, ',', 3, ']:
        equationsFile.write('*Equation \n')
        equationsFile.write('3\n')
        equationsFile.write('RVE_'+ str(i) + dof + '1\n')
        equationsFile.write('RVE_'+ str(i+16512) + dof + '-1\n')
        equationsFile.write('RefNode_X0' + dof + '-1\n')
for i in boundaryNsets['y0_nodes']:
    for dof in [', 1, ',', 2, ',', 3, ']:
        equationsFile.write('*Equation \n')
        equationsFile.write('3\n')
        equationsFile.write('RVE_'+ str(i) + dof + '1\n')
        equationsFile.write('RVE_'+ str(i+128) + dof + '-1\n')
        equationsFile.write('RefNode_Y0' + dof + '-1\n')
for i in boundaryNsets['z0_nodes']:
    for dof in [', 1, ',', 2, ',', 3, ']:
        equationsFile.write('*Equation \n')
        equationsFile.write('3\n')
        equationsFile.write('RVE_'+ str(i) + dof + '1\n')
        equationsFile.write('RVE_'+ str(i+2130048) + dof + '-1\n')
        equationsFile.write('RefNode_Z0' + dof + '-1\n')
"""
for key in ['x1z0','y1z0']:
    for i in boundaryNsets[key]:
        for dof in [', 1, ',', 2, ',', 3, ']:
            equationsFile.write('*Equation \n')
            equationsFile.write('3\n')
            equationsFile.write('RVE_'+ str(i) + dof + '1\n')
            equationsFile.write('RVE_'+ str(i+2130048) + dof + '-1\n')
            equationsFile.write('RefNode_Z0' + dof + '-1\n')
for key in ['x0z1','y0z1']:
    for i in boundaryNsets[key]:
        for dof in [', 1, ',', 2, ',', 3, ']:
            equationsFile.write('*Equation \n')
            equationsFile.write('3\n')
            equationsFile.write('RVE_'+ str(i) + dof + '1\n')
            equationsFile.write('RVE_'+ str(i-2130048) + dof + '-1\n')
            equationsFile.write('RefNode_Z0' + dof + '-1\n')
for key in ['y1z1','x1y1']:
    for i in boundaryNsets[key]:
        for dof in [', 1, ',', 2, ',', 3, ']:
            equationsFile.write('*Equation \n')
            equationsFile.write('3\n')
            equationsFile.write('RVE_'+ str(i) + dof + '1\n')
            equationsFile.write('RVE_'+ str(i-128) + dof + '-1\n')
            equationsFile.write('RefNode_Y0' + dof + '-1\n')
for key in ['x0y1']:
    for i in boundaryNsets[key]:
        for dof in [', 1, ',', 2, ',', 3, ']:
            equationsFile.write('*Equation \n')
            equationsFile.write('3\n')
            equationsFile.write('RVE_'+ str(i) + dof + '1\n')
            equationsFile.write('RVE_'+ str(i+16512) + dof + '-1\n')
            equationsFile.write('RefNode_X0' + dof + '-1\n')
for key in ['x1z1','x1y0']:
    for i in boundaryNsets[key]:
        for dof in [', 1, ',', 2, ',', 3, ']:
            equationsFile.write('*Equation \n')
            equationsFile.write('3\n')
            equationsFile.write('RVE_'+ str(i) + dof + '1\n')
            equationsFile.write('RVE_'+ str(i-16512) + dof + '-1\n')
            equationsFile.write('RefNode_X0' + dof + '-1\n')

for dof in [', 1, ',', 2, ',', 3, ']:
    equationsFile.write('*Equation \n')
    equationsFile.write('3\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x0y0z0'][0]) + dof + '1\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x1y0z0'][0]) + dof + '-1\n')
    equationsFile.write('RefNode_Y0' + dof + '-1\n')
for dof in [', 1, ',', 2, ',', 3, ']:
    equationsFile.write('*Equation \n')
    equationsFile.write('3\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x0y0z0'][0]) + dof + '1\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x1y1z0'][0]) + dof + '-1\n')
    equationsFile.write('RefNode_Z0' + dof + '-1\n')
for dof in [', 1, ',', 2, ',', 3, ']:
    equationsFile.write('*Equation \n')
    equationsFile.write('4\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x0y0z0'][0]) + dof + '1\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x1y0z0'][0]) + dof + '-1\n')
    equationsFile.write('RefNode_X0' + dof + '-1\n')
    equationsFile.write('RefNode_Y0' + dof + '-1\n')
for dof in [', 1, ',', 2, ',', 3, ']:
    equationsFile.write('*Equation \n')
    equationsFile.write('4\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x0y1z0'][0]) + dof + '1\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x0y0z0'][0]) + dof + '-1\n')
    equationsFile.write('RefNode_X0' + dof + '-1\n')
    equationsFile.write('RefNode_Z0' + dof + '-1\n')
for dof in [', 1, ',', 2, ',', 3, ']:
    equationsFile.write('*Equation \n')
    equationsFile.write('4\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x0y0z0'][0]) + dof + '1\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x0y0z1'][0]) + dof + '-1\n')
    equationsFile.write('RefNode_Y0' + dof + '-1\n')
    equationsFile.write('RefNode_Z0' + dof + '-1\n')
for dof in [', 1, ',', 2, ',', 3, ']:
    equationsFile.write('*Equation \n')
    equationsFile.write('5\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x0y0z0'][0]) + dof + '1\n')
    equationsFile.write('RVE_'+ str(boundaryNsets['x0y1z0'][0]) + dof + '-1\n')
    equationsFile.write('RefNode_X0' + dof + '-1\n')
    equationsFile.write('RefNode_Y0' + dof + '-1\n')
    equationsFile.write('RefNode_Z0' + dof + '-1\n')
"""
equationsFile.close()
import turtle as ttl
# import matplotlib.pyplot as plt
#
# with open('/home/cerecam/Desktop/Crack_Models/' + 'Results2203_locations.txt', 'r') as resultsFile:
#     results = resultsFile.readlines()
# volFrac = ['20', '30', '40', '50', '60', '70', '80']
# for x in range(0,len(results),2):
#
#     polymer_locations = [[float(i.split(',')[0]),float(i.split(',')[1])] for i in results[x].strip(']\n').strip('[').split('], [')]
#     polymer_locx = [i[0] for i in polymer_locations]
#     polymer_locy = [i[1] for i in polymer_locations]
#
#     metal_locations = [[float(i.split(',')[0]),float(i.split(',')[1])] for i in results[x+1].strip(']\n').strip('[').split('], [')]
#     metal_locx = [i[0] for i in metal_locations]
#     metal_locy = [i[1] for i in metal_locations]

    #
    # damageMetal = results[0].strip('(').strip(')\n').split('), (')
    # damageMetalData = []
    # for i in damageMetal:
    # 	formattedData = [float(i) for i in i.split(',')]
    # 	damageMetalData.append(formattedData)
    # frameValue = [i[0] for i in damageMetalData]
    #
    # metal = [i[3] for i in damageMetalData]
    # percentageMetal = [i[4] for i in damageMetalData]
    # percentageMetalTotal = [i[5] for i in damageMetalData]
    #
    # damagePolymer = results[1].strip('(').strip(')\n').split('), (')
    # damagePolymerData = []
    # for i in damagePolymer:
    # 	formattedData = [float(i) for i in i.split(',')]
    # 	damagePolymerData.append(formattedData)
    #
    # polymer = [i[3] for i in damagePolymerData]
    # percentagePolymer = [i[4] for i in damagePolymerData]
    # percentagePolymerTotal = [i[5] for i in damagePolymerData]
    # RVE_x = [0.0,6.72,6.72,5.0925,5.0925,6.72, 6.72,0.0,0.0]
    # RVE_y = [0.0,0.0,3.255,3.255,3.465,3.465,6.72,6.72,0.0]
    # plt.figure(int(x/2)+1)
    # plt.scatter(polymer_locx, polymer_locy, c='k')
    # plt.figure(int(x/2)+1)
    # plt.scatter(metal_locx, metal_locy, c='b')
    # plt.figure(int(x/2)+1)
    # plt.plot(RVE_x,RVE_y, color='k')
    # plt.xlim(-1.0, 7.0)
    # plt.ylim(-1.0, 7.0)
    # plt.title("Volume Fraction: " + str(volFrac[int((x/2))]))
    # plt.plot(frameValue, metal, label='Metal')
    # plt.plot(frameValue, polymer, label='Polymer')
    #
    # plt.legend()
    # plt.show()
    
#plt.figure(1)
#plt.figure(2)
#for count, voxels in enumerate(['10','20','30','40']):
## for count, voxels in enumerate(['5','10','15','20','30','40']):
## for count, voxels in enumerate(['10']):
    #position = (count)
    ## position = 2*(count)
    #print(position)
    #damageMetal = results[position].strip('(').strip(')\n').split('), (')
    #damageMetalData = []
    #for i in damageMetal:
        #formattedData = [float(i) for i in i.split(',')]
        #damageMetalData.append(formattedData)
    #metalFracMetal = [i[0] for i in damageMetalData]

    ## damagePolymer = results[position + 1].strip('(').strip(')\n').split('), (')
    ## damagePolymerData = []
    ## for i in damagePolymer:
    ##     formattedData = [float(i) for i in i.split(',')]
    ##     damagePolymerData.append(formattedData)
    ## metalFracPolymer = [i[0] for i in damagePolymerData]

    #percentageMetal = [i[3] for i in damageMetalData]
    #percentageMetalTotal = [i[4] for i in damageMetalData]
    ## percentagePolymer = [i[3] for i in damagePolymerData]
    ## percentagePolymerTotal = [i[4] for i in damagePolymerData]

    #plt.figure(1)
    #plt.plot(metalFracMetal, percentageMetal, label='Metal: ' + voxels + ' Voxels thick')
    ## plt.plot(metalFracPolymer, percentagePolymer, label='Polymer: ' + voxels + ' Voxels thick')
    #plt.figure(2)
    #plt.plot(metalFracMetal, percentageMetalTotal, label='Metal : ' + voxels + ' Voxels thick')
    ## plt.plot(metalFracPolymer, percentagePolymerTotal, label='Polymer : ' + voxels + ' Voxels thick')

#plt.figure(1)
#plt.title('Percentage of elements per each constituent total')
#plt.legend(loc = 'best')
#plt.figure(2)
#plt.title('Percentage of elements per total elements')
#plt.legend(loc = 'best')

#plt.show()
