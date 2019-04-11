import numpy as np
import csv,sys
import matplotlib.path as mpltPath
"""
# Required files:
1) RVE_full_nodes: Nodes from geometry with cut out section for RVE
2) RVE_nodes_old.inp: Nodes of RVE geometry with original node numbering form CT specimen gemoetry 
3) RVE_elements_old.inp: Element ICA of RVE geometry with original node numbers
3) RVE_Cracktip.inp: List of elements within crack tip
4) RVE_Plane_Nodes.inp: List of nodes and co-ordinates of metal-polymer RVE calculated from file Create_RVE_2D_Plane.py (starting at 1)
5) RVE_Plane_Elements.inp: Elements and ICA of metal-polymer RVE calculated from file Create_RVE_2D_Plane.py
"""

def translate_nodes(x_value, y_value, z_value, orig_file, new_file):
    """
    Read in nodes and coordinates for RVE in full model, change coordes to start at 0.0, 0.0
    x_value     : translation in x-direction
    y_value     : translation in y-direction
    orig_file   : Filename on original nodal data
    new_file    : New filename to which translated nodal data will be written
    """
    global cwd
    RVE_nodes_trans = open(cwd + new_file, 'w')
    with open(cwd + orig_file, 'r') as allNodeFile:
        RVE_nodes_trans.write(allNodeFile.readline())
        for line in allNodeFile:
            dataline = [int(line.split(',')[0])] + [float(i.strip(',')) for i in line.split()[1:]]
            dataline[1] = round(dataline[1] - x_value, 6)
            dataline[2] = round(dataline[2] - y_value, 6)
            dataline[3] = round(dataline[3] - z_value, 6)
            RVE_nodes_trans.write(', \t'.join([str(p) for p in dataline]) + '\n')
    RVE_nodes_trans.close()

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


volFrac = '40'

# for RVE_Data in [(volFrac, '5', '1'), (volFrac, '10', '1'), (volFrac, '15', '1'), (volFrac, '20', '1'), (volFrac, '30', '1'), (volFrac, '40', '1'),
#                  (volFrac, '5', '2'), (volFrac, '10', '2'), (volFrac, '15', '2'), (volFrac, '20', '2'), (volFrac, '30', '2'), (volFrac, '40', '2'),
#                  (volFrac, '5', '3'), (volFrac, '10', '3'), (volFrac, '15', '3'), (volFrac, '20', '3'), (volFrac, '30', '3'), (volFrac, '40', '3')]: #tuple(metal volume fraction, thickness of model, RVE number)
for RVE_Data in [ (volFrac, '15', '2'), (volFrac, '30', '3')]: #tuple(metal volume fraction, thickness of model, RVE number)

    metalFrac = RVE_Data[0]
    voxels = RVE_Data[1]
    RVE_number = RVE_Data[2]

    voxelwd = '/home/cerecam/Desktop/Crack_Models/' + voxels + 'Voxels/'
    cwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/' + voxels + 'Voxels/'
# enlargeNodes(4.48*1.5, RVE_3D_Section_Nodes, 'enlarged' + RVE_3D_Section_Nodes)
# Input files, from User
# translate_nodes(8.76249981,   12.2650003, 0.0, 'CT_Specimen_noRVE_5_Nodes.inp', 'translated_CT_Specimen_noRVE_5_Nodes.inp')
# for RVE_number in ['1', '2', '3']:
# for RVE_number in ['1']:
    print('Processing files for ' + metalFrac + '% CT-Specimen for RVE ' + RVE_number + ' with ' + voxels + ' voxels ...')

    RVE_3D_Section_Nodes = '3D_RVE_Section_NodeCoords' + RVE_number + '.inp' # found in cwd
    RVE_3D_Section_Elements = '3D_RVE_Section_ElementICA' + RVE_number + '.inp' # foudn in cwd

    noMaterial_RVE_nodes = 'noMAT_RVE_Nodes.inp' # found in voxelwd
    noMaterial_RVE_elements = 'noMAT_RVE_Elements.inp' # found in voxelwd
    crackTip_File = 'crackTip_elset.inp' # found in voxelwd

    CT_Specimen_3D_NoRVE_Nodes = 'CT_Specimen_noRVE_' + voxels + '_Nodes.inp' # found in cwd
    CT_Specimen_3D_NoRVE_Boundary = 'CT_Specimen_noRVE_' + voxels + '_Boundary.inp' # found in cwd
    CT_Specimen_NoRVE_Elements = 'CT_Specimen_noRVE_' + voxels + '_Elements.inp' # found in cwd

    template_INP =  "3D_CT_Model_INCLUDES.inp" # found in voxelwd

    Material_Sets = '3D_Material_Assignment_' + RVE_number + '.inp'

    ##
    mainwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/'
    with open(mainwd + 'MetalElements.inp', 'r') as metalread:
        data = metalread.readlines()
    metalMax = int(data[-1].split(',')[0])
    metalMin = int(data[0].split(',')[0])

    with open(mainwd + 'PolymerElements.inp', 'r') as polymerread:
        data = polymerread.readlines()
    polymerMax = int(data[-1].split(',')[0])
    polymerMin = int(data[0].split(',')[0])

    polyElements = range(polymerMin, polymerMax + 1, 1)
    metalElements = range(metalMin, metalMax + 1, 1)

    #Read in nodal co-ordinates of RVE WITH material definitions and translate nodes if necessary
    Mat_nodes_dict = {}
    Mat_coords = [[], [], []]
    with open(cwd + RVE_3D_Section_Nodes, 'r') as Mat_RVE:
        for line in Mat_RVE:
            if line[0] == '*':
                pass
            else:
                newline = line.split(',')
                dataline = [int(newline[0])] + [round(float(i),5) for i in newline[1:]]
                Mat_nodes_dict[dataline[0]] = dataline[1:] # Dictionary where key = node number; value = co-ordinates x,y,x
                for i in range(1,4):
                    Mat_coords[i-1].append(dataline[i])
    if min(Mat_coords[0]) != 0.0 or min(Mat_coords[1]) != 0.0 or min(Mat_coords[2]) != 0.0:
        x_value = min(Mat_coords[0])
        y_value = min(Mat_coords[1])
        z_value = min(Mat_coords[2])
        translate_nodes(x_value, y_value, z_value, RVE_3D_Section_Nodes, 'translated' + RVE_3D_Section_Nodes)
        Mat_nodes_dict = {}
        with open(cwd + 'translated' + RVE_3D_Section_Nodes, 'r') as Mat_RVE:
            for line in Mat_RVE:
                if line[0] == '*':
                    pass
                else:
                    newline = line.split(',')
                    dataline = [int(newline[0])] + [float(i) for i in newline[1:]]
                    Mat_nodes_dict[dataline[0]] = dataline[1:]
    ##
    ##
    # Read in element connectivity of RVE WITH material definitions (no crack) and store with (centroid) as dictionary key and last entry is material description
    Mat_elements_dict = {}
    Mat_ICA_dict = {}
    p_count = 0
    g_count = 0
    o_element = 0
    with open(cwd + RVE_3D_Section_Elements, 'r') as Mat_RVE_ele:
        for line in Mat_RVE_ele:
            newline = [int(i) for i in line.split(',')]
            centroid = [0,0,0]
            for x in range(3):
                centroid[x] = round(sum([Mat_nodes_dict[i][x] for i in newline[1:]])/float(len(newline[1:])),5)
            if newline[0] >= metalMin and newline[0] <= metalMax:
                polymer = 0
                g_count += 1
            elif newline[0] >= polymerMin and newline[0] <= polymerMax:
                polymer = 1
                p_count += 1
            else:
                o_element += 1
            Mat_elements_dict[tuple(centroid)] = newline + [polymer] # Dictionary where key=centroid; value = [element number, ICA, material definition]
            Mat_ICA_dict[newline[0]] = newline[1:]
    # print(Mat_elements_dict[tuple([0.02625, 0.02625, 0.02625])])
    ##
    ##
    # Read in node numbers on the boundary of the RVE within the CT_Specimen from nset range
    boundaryNodes = []
    with open(cwd + CT_Specimen_3D_NoRVE_Boundary, 'r') as CT_Specimen_BNodes:
        CT_Specimen_BNodes.readline()
        for line in CT_Specimen_BNodes:
            boundaryNodes.extend([int(i) for i in line.split(',')])
    boundaryNodes.sort()
    ##
    ##
    # read in node co-ordinates of boundary nodes in CT_Specimen
    CT_nodes_dict = {}
    CT_nodes = []
    CT_coords = [[], [], []]
    with open(cwd + CT_Specimen_3D_NoRVE_Nodes, 'r') as CT_Nodes:
        for line in CT_Nodes:
            if line[0] == '*':
                pass
            else:
                newline = line.split(',')
                dataline = [int(newline[0])] + [round(float(i),5) for i in newline[1:]]
                if dataline[0] in boundaryNodes:
                    CT_nodes_dict[tuple(dataline[1:])] = dataline[0] # Dictionary where key = co-ordinates, value = node number
                    CT_nodes.append(dataline[0])
    ##
    ##
    # Read in nodal co-ordinates of plain RVE with no material definitions and translate nodes if necessary
    noMat_nodes_dict = {}
    CT_node_swaps = {}
    noMat_coords = [[], [], []]
    newNode = open(cwd + 'newNodes' + RVE_number + '.inp','w')
    newNode.write('*Node \n')
    with open(voxelwd + noMaterial_RVE_nodes, 'r') as noMat_RVE:
        for line in noMat_RVE:
            if line[0] == '*':
                pass
            else:
                newline = line.split(',')
                dataline = [int(newline[0])+5000000] + [round(float(i),5) for i in newline[1:]]
                if tuple(dataline[1:]) in CT_nodes_dict: # if the nodal co-ordinates of RVE match with those on the boundary then, replace with node number from CT_Specimen_NoRVE
                    CT_node_swaps[dataline[0]] = CT_nodes_dict[tuple(dataline[1:])] # CT_Swapped nodes saved in diction where key = RVE original node number, value = CT_Specimen node number
                    dataline[0] = CT_nodes_dict[tuple(dataline[1:])]
                else:
                    newNode.write(str(dataline).strip('[').strip(']') + '\n')
                noMat_nodes_dict[dataline[0]] = dataline[1:] # Dictionary where key = node number, value = nodal co-ordinates
                for i in range(1,4):
                    noMat_coords[i-1].append(dataline[i])
    # if min(noMat_coords[0]) != 0.0 or min(noMat_coords[1]) != 0.0 or min(noMat_coords[2]) != 0.0:
    #     x_value = min(noMat_coords[0])
    #     y_value = min(noMat_coords[1])
    #     z_value = min(noMat_coords[2])
    #     translate_nodes(x_value, y_value, z_value, noMaterial_RVE_nodes, 'translated' + noMaterial_RVE_nodes)
    #     noMat_nodes_dict = {}
    #     CT_node_swaps = {}
    #     with open(voxelwd + 'translated' + noMaterial_RVE_nodes, 'r') as noMat_RVE:
    #         noMat_RVE.readline()
    #         for line in noMat_RVE:
    #             if line[0] == '*':
    #                 pass
    #             else:
    #                 newline = line.split(',')
    #                 dataline = [int(newline[0])+5000000] + [round(float(i),5) for i in newline[1:]]
    #                 if tuple(dataline[1:]) in CT_nodes_dict:
    #                     dataline[0] = CT_nodes_dict[tuple(dataline[1:])]+5000000
    #                     CT_node_swaps[dataline[0]] = CT_nodes_dict[tuple(dataline[1:])]
    #                 noMat_nodes_dict[dataline[0]] = dataline[1:]
    # with open(cwd + 'crackTip_elset' + RVE_number + '.inp', 'r') as crackTip_elset_file:
    with open(voxelwd + crackTip_File, 'r') as crackTip_elset_file:
        firstline = crackTip_elset_file.readline().split(',')
        if firstline[-1].strip().lower() =='generate':
            line = crackTip_elset_file.readline().strip().split(',')
            crackTip_elements = list(range(int(line[0])+5000000, int(line[1])+5000000+1, int(line[2])))
        else:
            crackTip_elements = []
            for line in crackTip_elset_file:
                crackTip_elements.extend(int(x) for x in line.strip().split(','))

    newNode.close()
    ##
    ##
    # Read in element connectivity and store with (centroid) as dictionary key
    noMat_elements_dict = {}
    polymer_elements = []
    gold_elements = []
    other_elements = []
    polymer_elements2 = []
    gold_elements2 = []
    other_elements2 = []
    crackTip_Dict = {}
    cracktip_coords = [[], [], []]
    crack_element_Location = {}
    newICA_dict = {}
    crackTip_ICA = {}
    crackTip_centroids = {}
    newICA = open(cwd + 'newICA_Elements' + RVE_number + '.inp', 'w')
    with open(voxelwd + noMaterial_RVE_elements, 'r') as noMat_RVE_ele:
        for line in noMat_RVE_ele:
            if line[0] == '*':
                pass
            else:
                newline = [int(i) for i in line.split(',')]
                newline2 = [int(i) for i in line.split(',')]
                newline2[0] = newline2[0] + 5000000
                for count,x in enumerate(newline[1:]): #going through ICA to remove repeated nodes
                    if (x+5000000) in CT_node_swaps:
                        newline[count+1] = CT_node_swaps[x+5000000]
                        newline2[count+1] = CT_node_swaps[x+5000000]
                    else:
                        newline2[count + 1] = newline2[count + 1] + 5000000
                newICA.write(str(newline2).strip('[').strip(']') + '\n')
                newICA_dict[newline2[0]] = newline2[1:]
                centroid = [0,0,0]
                for x in range(3):
                    centroid[x] = round(sum([noMat_nodes_dict[i][x] for i in newline2[1:]])/float(len(newline[1:])),5)
                if tuple(centroid) in Mat_elements_dict.keys():
                    noMat_elements_dict[tuple(centroid)] = newline + [Mat_elements_dict[tuple(centroid)][-1]]
                    if Mat_elements_dict[tuple(centroid)][-1]:
                        polymer_elements.append(newline[0])
                        polymer_elements2.append(newline2[0])
                    else:
                        gold_elements.append(newline[0])
                        gold_elements2.append(newline2[0])
                else:
                    crackTip_ICA[newline2[0]] = newline2[1:]
                    crackTip_centroids[newline2[0]] = centroid
                if newline2[0] in crackTip_elements:
                    crackTip_RVE = newline2[1:-1]
                    z_position = min([noMat_nodes_dict[n][-1] for n in crackTip_RVE])
                    new_polygon = []
                    for n in crackTip_RVE:
                        if noMat_nodes_dict[n][-1] == z_position:
                            new_polygon.append(list(noMat_nodes_dict[n][0:2]))
                            crack_element_Location[newline2[0]] = [tuple(new_polygon) + tuple([z_position, centroid])]
                    for x in range(3):
                        cracktip_coords[x].extend(noMat_nodes_dict[i+5000000][x] for i in newline[1:])
                    noMat_elements_dict[tuple(centroid)] = newline + [99]
                    crackTip_Dict[newline[0]] = centroid
                    # other_elements.append(newline[0])
                    # other_elements2.append(newline2[0])
    newICA.close()
    print('Crack tip dimensions: \t x: ' + str(max(cracktip_coords[0])) + ' ' + str(min(cracktip_coords[0])) +
          '\n \t \t \t \t \t \t y: ' + str(max(cracktip_coords[1])) + ' '  + str(min(cracktip_coords[1])))
    polygon_CrackTip = [[min(cracktip_coords[0]),min(cracktip_coords[1])], [min(cracktip_coords[0]),max(cracktip_coords[1])] ,
                        [max(cracktip_coords[0]),max(cracktip_coords[1])], [max(cracktip_coords[0]),min(cracktip_coords[1])]]
    path = mpltPath.Path(polygon_CrackTip)

    count = 0
    cracktip_assignment = []
    crack_location_ele = []
    for key,values in Mat_elements_dict.items():
        if path.contains_point(key[0:-1]):
            # print(key)
            nodes = values[1:-1]
            # for count,n in enumerate(nodes):
            #     if n in CT_node_swaps:
            #         nodes[count] = CT_node_swaps[n]
            z_position = min([Mat_nodes_dict[n][-1] for n in nodes])
            z_centroid = round(sum([Mat_nodes_dict[n][-1] for n in nodes])/len(nodes),5)
            new_polygon = []
            for n in nodes:
                # if noMat_nodes_dict[n][-1] == z_position:
                new_polygon.append(list(Mat_nodes_dict[n][0:2]))
            # print(new_polygon)
            # new_path= mpltPath.Path([new_polygon[i] for i in [0,2,-1,4]] )
            new_path= mpltPath.Path([new_polygon[i] for i in [1,2, 3,4]] )
            for element in crackTip_elements:
                # crackTip_RVE = crackTip_ICA[element]
                centroid = crackTip_centroids[element]
                if centroid[-1]==z_centroid:
                    # if element == 662576:
                    #     print(centroid)
                    #     print([new_polygon[i] for i in [0,2,-1,4]])
                    #     print(new_path.contains_point(centroid[:-1]))
                    # print(centroid)
                    # print(new_path.contains_point(centroid[:-1]))
                    if new_path.contains_point(centroid[:-1]):
                        if values[-1] ==1:
                            polymer_elements2.append(element)
                        elif values[-1] == 0:
                            gold_elements2.append(element)
                        cracktip_assignment.append(element)
    other_elements2= list(set(crackTip_elements)-set(cracktip_assignment))
    total_RVE = polymer_elements2 + gold_elements2


    with open(cwd + Material_Sets,'w') as outputICA:
        # outputICA.write('*Elset, elset=RVE_Gold, instance=crack_model \n')
        outputICA.write('*Elset, elset=Metal \n')
        for i in range(0, len(gold_elements2) + 1, 10):
            outputICA.write(str(gold_elements2[i:i + 10]).strip('[').strip(']') + '\n')
        # outputICA.write('*Elset, elset=RVE_Polymer, instance=crack_model \n')
        outputICA.write('*Elset, elset=Polymer \n')
        for i in range(0, len(polymer_elements2) + 1, 10):
            outputICA.write(str(polymer_elements2[i:i + 10]).strip('[').strip(']') + '\n')
        outputICA.write('*Elset, elset=RVE \n')
        for i in range(0, len(total_RVE) +1, 10):
            outputICA.write(str(total_RVE[i:i + 10]).strip('[').strip(']') + '\n')
        if len(other_elements2)>0:
            outputICA.write('*Elset, elset=RVE_Other \n')
            print('**** ' + str(len(other_elements2)) + ' elements have missing property definitions')
            for i in range(0, len(other_elements2) + 1, 10):
                outputICA.write(str(other_elements2[i:i + 10]).strip('[').strip(']') + '\n')

    RVE_name = '3D_RVE_' + voxels + 'Voxels_' + metalFrac + 'PER_'+ RVE_number + '.inp'
    fwrite = open(cwd + RVE_name,'w')
    with open(voxelwd + template_INP,'r') as fread:
        for line in fread:
            if line.strip() == '*INCLUDE, INPUT=CT_Specimen_noRVE_5_Nodes.inp':
                fwrite.write('*INCLUDE, INPUT=CT_Specimen_noRVE_'+ voxels + '_Nodes.inp \n')
            elif line.strip() == '*INCLUDE, INPUT=CT_Specimen_noRVE_5_Elements.inp':
                fwrite.write('*INCLUDE, INPUT=CT_Specimen_noRVE_'+ voxels + '_Elements.inp \n')
            elif line.strip() == '*INCLUDE, INPUT=CT_Specimen_noRVE_5_Surfaces.inp':
                fwrite.write('*INCLUDE, INPUT=CT_Specimen_noRVE_'+ voxels + '_Surfaces.inp \n')
            elif line.strip()[:-5] == '*INCLUDE, INPUT=newNodes':
                fwrite.write('*INCLUDE, INPUT=newNodes' + RVE_number + '.inp \n')
            elif line.strip()[:-5] == '*INCLUDE, INPUT=newICA_Elements':
                fwrite.write('*INCLUDE, INPUT=newICA_Elements' + RVE_number + '.inp \n')
            elif line.strip()[:-5] == '*INCLUDE, INPUT=3D_Material_Assignment_':
                fwrite.write('*INCLUDE, INPUT=3D_Material_Assignment_' + RVE_number + '.inp \n')
            else:
                fwrite.write(line)

    fwrite.close()
    print(' ...')
    print('CT-Specimen ' + voxels + ' voxels thick with inserted RVE ' + RVE_number + ' COMPLETE')
    print('Volume fraction: ' + str(len(gold_elements2)/(len(gold_elements2)+len(polymer_elements2))) )
