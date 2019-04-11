
allNodes = 'Nodes.inp'
allElements = 'Elements.inp'
metalFrac = '40'
mainwd = "/home/cerecam/Desktop/Crack_Models/" + metalFrac + "PER/1/"
enlargementFactor = 6.72
vol_fractions = []

with open(mainwd + 'MetalElements.inp', 'r') as metalread:
    data = metalread.readlines()
metalMax = int(data[-1].split(',')[0])
metalMin = int(data[0].split(',')[0])

with open(mainwd + 'PolymerElements.inp', 'r') as polymerread:
    data = polymerread.readlines()
polymerMax = int(data[-1].split(',')[0])
polymerMin = int(data[0].split(',')[0])

polyElements = range(polymerMin, polymerMax +1, 1)
metalElements = range(metalMin, metalMax + 1, 1)

def enlargeNodes(enlargement, old_nodes_file, new_nodes_file):
    global cwd
    print('Enlarging nodes by a factor of ' + str(enlargement))
    # cwd = '/home/cerecam/2M_128x128x128_full/2D_Planes/'
    fread = open(cwd + old_nodes_file, 'r')
    fwrite = open(cwd + new_nodes_file, 'w')
    line1 = fread.readline()
    fwrite.write(line1)
    for line in fread:
        newline = [float(x) for x in line.split(',')]
        newline[0] = int(newline[0])
        newline[1:] = [round(i * enlargement,8) for i in newline[1:]]
        fwrite.write(str(newline).strip(']').strip('[') + '\n')

    fread.close()
    fwrite.close()


# translate_nodes(8.76249981,   11.6400003, 0, 'CT_Specimen_3D_NoRVE_15_Nodes.inp', 'xxxCT_Specimen_3D_NoRVE_Nodes.inp')
# for RVE_number in ['1','2','3']:
bash_script = open(mainwd + "post_python_script.sh" , 'w')

# for RVE_data in [('5', '1'), ('10', '1'), ('15', '1'), ('20', '1'), ('30', '1'), ('40', '1'),
#                  ('5', '2'), ('10', '2'), ('15', '2'), ('20', '2'), ('30', '2'), ('40', '2'),
#                  ('5', '3'), ('10', '3'), ('15', '3'), ('20', '3'), ('30', '3'), ('40', '3')]:
for RVE_data in [('15', '2'), ('30', '3')]:
# for RVE_data in [('5', '1')]:
    RVE_number = RVE_data[1]
    voxels = RVE_data[0]

    cwd = "/home/cerecam/Desktop/Crack_Models/" + metalFrac + "PER/1/" + voxels + "Voxels/"

    print('Processing RVE ' + RVE_number + ', volume fraction: ' + metalFrac + ', voxel thickness: ' + voxels + ' ...')
    RVE_name = 'RVE_' + metalFrac + "PER_" + voxels + 'Voxels_' + RVE_number + '.inp'
    RVE_nset = 'RVE_' + metalFrac + "PER_" + voxels + 'Voxels_' + RVE_number + '_nset.inp'
    RVE_elset = 'RVE_' + metalFrac + "PER_" + voxels + 'Voxels_' + RVE_number + '_elset.inp'

    elset = []
    with open(cwd+RVE_elset, 'r') as rveElset:
        firstline = rveElset.readline()
        if firstline[-1].strip().lower() =='generate':
            line = rveElset.readline().split(',')
            elset = list(range(int(line[0]), int(line[1])+1, int(line[2])))
        else:
            for line in rveElset:
                dataLine = [int(x) for x in line.split(',')]
                elset.extend(dataLine)

    elset.sort()

    nset = []
    with open(cwd+RVE_nset, 'r') as rveNset:
        firstline = rveNset.readline().split(',')
        if firstline[-1].strip().lower() =='generate':
            line = rveNset.readline().split(',')
            nset = list(range(int(line[0]), int(line[1])+1, int(line[2])))
        else:
            for line in rveNset:
                dataLine = [int(x) for x in line.split(',')]
                nset.extend(dataLine)
    nset.sort()

    max_node_val = -5000000
    min_node_val = 5000000
    count = 0
    newNodeFile = open(cwd + '3D_RVE_Section_NodeCoords' + RVE_number + '.inp', 'w')
    newNodeFile.write('*Node \n')
    with open(mainwd+allNodes,'r') as allNodesFile:
        allNodeList = allNodesFile.readlines()
    min_NodeNum = int(allNodeList[sorted(nset)[0]].split(',')[0]) - 1
    for entry in nset:
        dataLine = [int(allNodeList[entry].split(',')[0]) - min_NodeNum] + [float(i.strip()) for i in
                                                                            allNodeList[entry].split(',')[1:]]
        if max(dataLine[1:3]) > max_node_val:
            max_node_val = max(dataLine[1:])
        if min(dataLine[1:3]) < min_node_val:
            min_node_val = min(dataLine[1:])
        newNodeFile.write(str(dataLine).strip('[').strip(']') + '\n')

    newNodeFile.close()

    metalElset = []
    polymerElset = []
    newElementFile = open(cwd+'3D_RVE_Section_ElementICA' + RVE_number + '.inp', 'w')
    # newElementFile.write('*Element, type=C3D8R \n')
    with open(mainwd+allElements,'r') as allElementFile:
        allEleList = allElementFile.readlines()
    for entry in elset:
        dataLine = [int(i.strip()) for i in allEleList[entry-1].split(',')]
        nodeNumbering = [i - min_NodeNum for i in dataLine[1:]]
        dataLine = [dataLine[0]] + nodeNumbering
        newElementFile.write(str(dataLine).strip('[').strip(']') + '\n')
        if dataLine[0] <= polyElements[-1] and dataLine[0] >= polyElements[0]:
            polymerElset.append(dataLine[0])
        else:
            metalElset.append(dataLine[0])
    newElementFile.close()

    with open(cwd + 'metal_Elset' + RVE_number + '.inp', 'w') as metalElsetfile:
        for i in range(0,len(metalElset)+1,10):
            metalElsetfile.write(str(metalElset[i:i+10]).strip('[').strip(']') + '\n')

    with open(cwd + 'polymer_Elset' + RVE_number + '.inp', 'w') as polymerElsetfile:
        for i in range(0,len(polymerElset)+1,10):
            polymerElsetfile.write(str(polymerElset[i:i+10]).strip('[').strip(']') + '\n')

    vol_fractions.append(str(len(metalElset) / ( float( len(metalElset) ) + float( len(polymerElset) ) ) ))

    enlargement = enlargementFactor / max_node_val

    enlargeNodes(enlargement , '3D_RVE_Section_NodeCoords' + RVE_number + '.inp', 'scaled_3D_RVE_Section_NodeCoords' + RVE_number + '.inp')

    bash_script.write("cp " + cwd + '3D_RVE_Section_NodeCoords' + RVE_number + '.inp ' + cwd + 'old_3D_RVE_Section_NodeCoords' + RVE_number + '.inp \n')
    bash_script.write("mv " + cwd + 'scaled_3D_RVE_Section_NodeCoords' + RVE_number + '.inp ' + cwd + '3D_RVE_Section_NodeCoords' + RVE_number + '.inp \n')
    print('RVE ' + RVE_number + ', volume fraction: ' + metalFrac + ', voxel thickness: ' + voxels + ' DONE')

print('sh ' + mainwd + "post_python_script.sh")
bash_script.write("echo \"" + ', \t'.join([str(p) for p in vol_fractions]) + '\"\n')
bash_script.close()