import numpy as np
import csv,sys
import matplotlib.path as mpltPath
"""
# Required files:
1) RVE_full_nodes: Nodes from geometry with cut out section for RVE
2) RVE_nodes_old.inp: Nodes of RVE geometry with original node numbering from CT speciment geometry 
3) RVE_elements_old.inp: Element ICA of RVE geometry with original node numbers
3) RVE_Cracktip.inp: List of elements within crack tip
4) RVE_Plane_Nodes.inp: List of nodes and co-ordinates of metal-polymer RVE calculated from file Create_RVE_2D_Plane.py (starting at 1)
5) RVE_Plane_Elements.inp: Elements and ICA of metal-polymer RVE calculated from file Create_RVE_2D_Plane.py
"""
metalFrac = '60'
cwd ='/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/'
RVE_name = 'RVE_2D_'+ metalFrac + 'PER_'
bash_script = open(cwd + 'python_abaqus_scrtipt.sh','w')
for RVE_number in ['1','2','3','4','5','6']:
# for RVE_number in ['1G']:
    RVE_name = 'RVE_2D_'+ metalFrac + 'PER_' + RVE_number
    print(RVE_name)
    # Input files, from User
    No_RVE_nodes = 'No_RVE_nodes.inp'
    RVE_nodes_old = 'noMat_RVE_nodes.inp'
    RVE_elements_old = 'noMat_RVE_elements.inp'
    RVE_Cracktip = 'RVE_Cracktip.inp'
    RVE_Plane_Nodes = RVE_name + '_Nodes.inp'
    RVE_Plane_Elements = RVE_name + '_Elements.inp'
    mat_set_full_RVE = 'Elsets.inp'
    RVE_boundary = 'No_RVE_boundary.inp'

    # Output files
    New_RVE_elements = 'RVE_elements_'+ RVE_name + '.inp'
    Material_Sets = 'Material_Elsets_'+ RVE_name + '.inp'
    RVE_nodes_output = 'RVE_nodes_'+ RVE_name + '.inp'


    output_EleSet = 'RVE_eleset.inp'
    RVE_size = round(4.48*1.5,3)
    # RVE_Ele = sorted(RVE_Ele, key=lambda x: (x[1][1]))

    #
    #
    def translate_nodes(x_value, y_value, orig_file, new_file):
        """
        Read in nodes and coordinates for RVE in full model, change coordes to start at 0.0, 0.0
        x_value     : translation in x-direction
        y_value     : translation in y-direction
        orig_file   : Filename on original nodal data
        new_file    : New filename to which translated nodal data will be written
        """
        global cwd
        RVE_nodes_trans = open(cwd + new_file,'w')
        with open(cwd + orig_file, 'r') as allNodeFile:
            RVE_nodes_trans.write(allNodeFile.readline())
            for line in allNodeFile:
                dataline = [int(line.split(',')[0])] + [float(i.strip(',')) for i in line.split()[1:]]
                dataline[1] = round(dataline[1]-x_value,8)
                dataline[2] = round(dataline[2]-y_value,8)
                RVE_nodes_trans.write(', \t'.join([str(p) for p in dataline])+'\n')
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
            newline[1:] = [round(i* enlargement,5) for i in newline[1:]]
            fwrite.write(str(newline).strip(']').strip('[') + '\n')

        fread.close()
        fwrite.close()
    # translate_nodes(-1.08749986, -18.132, No_RVE_nodes, 'translated' + No_RVE_nodes)
    # enlargeNodes(1.0,RVE_nodes_old, 'enlarged_'+RVE_nodes_old)
    # enlargeNodes(1.5*4.48, 'Nodes.inp', 'Large_3D_Nodes_all.inp')
    #

    # Read in material sets limits
    with open(cwd + mat_set_full_RVE, 'r') as mat_sets:
        matElsets_lines = mat_sets.readlines()
    # matElsets_lines.pop(-1)
    elsets = {}
    for line in matElsets_lines:
        if line == '\n':
            break
        elif line[0] == '*':
            firstline = line.split(',')
            elsets[firstline[1].split('=')[- 1].strip().lower()] = []
        elif firstline[-1].strip().lower() =='generate':
            splitline = line.strip().split(',')
            elsets[firstline[1].split('=')[- 1].strip().lower()] = list(range(int(splitline[0]), int(splitline[1])+1, int(splitline[2])))
        else:
            splitline = line.strip().split(',')
            elsets[firstline[1].split('=')[- 1].strip().lower()].extend(int(x) for x in splitline[:-1])

    for key, item in elsets.items():
        item.sort()
    metalMin = min(elsets['metal'])
    metalMax = max(elsets['metal'])
    polyMin = min(elsets['polymer'])
    polyMax =  max(elsets['polymer'])

    # Read in boundary nodes from noRVE_model
    boundary_Nodes = []
    with open(cwd+RVE_boundary, 'r') as boundary_Nodes_fread:
        for line in boundary_Nodes_fread:
            if line == '\n':
                break
            elif line[0] == '*':
                firstline = line.split(',')
            elif firstline[-1].strip().lower() =='generate':
                splitline = line.strip().split(',')
                boundary_Nodes = list(range(int(splitline[0]), int(splitline[1])+1, int(splitline[2])))
            else:
                splitline = line.strip().split(',')
                boundary_Nodes.extend(int(x) for x in splitline)

    # Create a dictionary out of the boundary nodes, key = co-ordinates, value=nodal number
    RVE_full_Node = {}
    boundary_NoRVE = []
    boundaryDict = {}
    with open(cwd + No_RVE_nodes, 'r') as node_coords_NoRVE:
        firstline = node_coords_NoRVE.readline()
        for line in node_coords_NoRVE:
            newline = line.split(',')
            dataline = [int(newline[0])] + [round(float(i),5) for i in newline[1:]]
            if dataline[0] in boundary_Nodes:
                boundaryDict[tuple(dataline[1:])] = dataline[0]
                boundary_NoRVE.append(dataline[0])

    # Read in nodes and coordinates for noMat RVE geometry and remove repeated nodes
    RVE_nodes_new = open(cwd + RVE_nodes_output,'w')
    boundary_swaps = {}
    with open(cwd + RVE_nodes_old, 'r') as RVENodeFile:
        RVENodeList = RVENodeFile.readlines()

    RVE_boundaryDict = {}
    for entry in RVENodeList[1:]:
        dataline = [int(entry.split(',')[0].strip())] + [float(i.strip(',')) for i in entry.split()[1:]]
        # RVE_full_Node[dataline[0]] = dataline[1:]
        dataline[0] = dataline[0] + 100000
        # dataline[1:] = [round(i,6) for i in dataline[1:]]
        # RVE_full_Node[dataline[0]] = dataline[1:]
        # if dataline[1] >= 0 and dataline[1] <= RVE_size and dataline[2] >= 0.0 and dataline[2] <= RVE_size:
        if tuple([dataline[1],dataline[2]]) in boundaryDict.keys():
            RVE_boundaryDict[dataline[0]] = boundaryDict[tuple([dataline[1],dataline[2]])]   # Saves node number pairing between RVE and no_RVE model
            RVE_full_Node[boundaryDict[tuple([dataline[1],dataline[2]])]] = dataline[1:]
            # boundary_swaps[dataline[0]] = boundaryDict[tuple([dataline[1],dataline[2]])]
        else:
            RVE_full_Node[dataline[0]] = dataline[1:]
            RVE_nodes_new.write(', \t'.join([str(p) for p in dataline])+'\n') # Writes nodal data for nodes within RVE

    RVE_nodes_new.close()

    # Replaces node numbering on boundary of RVE geometry with node numbers in full model
    replaced = 0
    RVE_element_new = open(cwd + New_RVE_elements, 'w')
    gold_Elements = []
    polymer_Elements = []
    RVE_elset = []
    with open(cwd + RVE_elements_old, 'r') as RVE_ele_file:
        for line in RVE_ele_file:
            dataline = [int(i.strip(','))+100000 for i in line.split()]
            # dataline[0] = dataline[0] + 100000
            for count,nodeNum in enumerate(dataline[1:]):
                # dataline[count + 1] = nodeNum + 100000
                if (nodeNum) in RVE_boundaryDict:
                    dataline[count+1] = RVE_boundaryDict[nodeNum]
                    replaced += 1
            RVE_element_new.write(', \t'.join([str(p) for p in dataline]) + '\n')
            RVE_elset.append(dataline[0])
    RVE_element_new.close()

    # Read in elements within curved section of crack tip elset
    with open(cwd+RVE_Cracktip, 'r') as RVE_full_CT_File:
        firstLine = RVE_full_CT_File.readline().split(',')
        if firstLine[-1].strip().lower() =='generate':
            dataLine = RVE_full_CT_File.readline().split(',')
            CT_elsetValues = list(range(int(dataLine[0])+100000,int(dataLine[1])+100001,int(dataLine[2])))
        else:
            CT_elsetValues = []
            for line in RVE_full_CT_File:
                CT_elsetValues.extend(int(x)+100000 for x in line.strip().split(','))

    # Read in elements and node connectivity for the elements within RVE section of full model
    with open(cwd + New_RVE_elements, 'r') as allEleFile:
        allEleList = allEleFile.readlines()

    RVE_Full_Ele = {}
    RVE_CT_Ele = {}
    maxX_ct = -100000
    minX_ct = 100000
    maxY_ct = -100000
    minY_ct = 100000
    for entry in allEleList:
        dataline = [int(i.strip()) for i in entry.split(',')]
        centroidx = round(sum([RVE_full_Node[n][0] for n in dataline[1:]])/len(dataline[1:]),5)
        centroidy = round(sum([RVE_full_Node[n][1] for n in dataline[1:]])/len(dataline[1:]),5)
        RVE_Full_Ele[centroidx, centroidy] = tuple(dataline)
    for entry in CT_elsetValues:
        dataline = [int(i.strip()) for i in allEleList[entry-100001].split(',')]
        centroidx = round(sum([RVE_full_Node[n][0] for n in dataline[1:]])/len(dataline[1:]),5)
        centroidy = round(sum([RVE_full_Node[n][1] for n in dataline[1:]])/len(dataline[1:]),5)
        RVE_CT_Ele[centroidx, centroidy] = tuple(dataline)
        for x_value in [RVE_full_Node[n][0] for n in dataline[1:]]:
            if x_value<minX_ct:
                minX_ct = x_value
            if x_value>maxX_ct:
                maxX_ct = x_value
        for y_value in [RVE_full_Node[n][1] for n in dataline[1:]]:
            if y_value<minY_ct:
                minY_ct = y_value
            if y_value>maxY_ct:
                maxY_ct = y_value
    print('Dimensions of crack tip: ' + str(minX_ct) + ', ' + str(maxX_ct) + ' ; ' + str(minY_ct) + ', ' + str(maxY_ct))
    polygon_CrackTip = [[minX_ct,minY_ct], [minX_ct,maxY_ct] ,[maxX_ct,maxY_ct], [maxX_ct,minY_ct]]
    path = mpltPath.Path(polygon_CrackTip)

    # Read in nodal co-ordinates from metal-polymer RVE planar section
    RVE_Node = {}
    with open(cwd + RVE_Plane_Nodes, 'r') as RVENodeFile:
        RVENodeList = RVENodeFile.readlines()
    for entry in RVENodeList[1:]:
        dataline = [int(entry.split(',')[0].strip())] + [float(i.strip(',')) for i in entry.split()[1:]]
        dataline[0] = dataline[0]
        dataline[1] = round(dataline[1],5)
        dataline[2] = round(dataline[2],5)
        RVE_Node[dataline[0]] = dataline[1:]

    # Read in elements, node connectivity and calulate centroidal value from metal-polymer RVE planar section
    gold_list = []
    poly_list = []
    non_ele = 0
    with open(cwd + RVE_Plane_Elements, 'r') as allEleFile:
        allEleList = allEleFile.readlines()

    RVE_Ele = {}
    crackTip_RVE = []
    CT_count = 0
    for entry in allEleList:
        dataline = [int(i.strip()) for i in entry.split(',')]
        centroidx = sum([round(RVE_Node[n][0],5) for n in dataline[1:]])/len(dataline[1:])
        centroidy = sum([round(RVE_Node[n][1],5) for n in dataline[1:]])/len(dataline[1:])
        if path.contains_point([centroidx,centroidy]):
            print(dataline[0])
            crackTip_RVE = crackTip_RVE + [dataline[0]]
            new_polygon =  [list(RVE_Node[n]) for n in dataline[1:]]
            newpath = mpltPath.Path(new_polygon)
            for i in RVE_CT_Ele.keys(): # Assigning material within the crack tip
                if newpath.contains_point(list(i)):
                    if dataline[0] >= metalMin and dataline[0] <= metalMax :
                        gold_list = gold_list + [RVE_CT_Ele[i][0]]  # This is a gold material element
                    else:
                        poly_list = poly_list + [RVE_CT_Ele[i][0]]  # This is a polymer material element
                    CT_count += 1
                    material = 'True' if gold_material else 'False'
                    print('CrackTip element: ' + str(RVE_CT_Ele[i][0]) + ' gold? : ' + material)
        else: # Assigning material elsewhere (not crack tip)
            if dataline[0] >= metalMin and dataline[0] <= metalMax :
                gold_material = 1 # This is a gold material element
            else:
                gold_material = 0 # This is a polymer material element

        centroidx = round(sum([round(RVE_Node[n][0],5) for n in dataline[1:]])/len(dataline[1:]),5)
        centroidy = round(sum([round(RVE_Node[n][1],5) for n in dataline[1:]])/len(dataline[1:]),5)
        RVE_Ele[centroidx,centroidy] = tuple([dataline[0]] + dataline[1:] + [gold_material])

    # Comparing metal-polymer RVE and RVE gemoetry model for material assignment
    count = 0
    notCount = 0
    g_count = 0
    p_count = 0
    newlist_Set = []
    crackTip  = []
    for key in RVE_Ele.keys():
        if key in RVE_Full_Ele:
            newlist_Set = newlist_Set + [RVE_Full_Ele[key][0]]
            if RVE_Ele[key][-1] == 1:
                gold_list = gold_list + [RVE_Full_Ele[key][0]]
                g_count += 1
            else:
                poly_list = poly_list + [RVE_Full_Ele[key][0]]
                p_count += 1
            count += 1
        else:
            notCount += 1

    print("volume fraction of gold is ~ " + str(g_count/(p_count + g_count)))

    # Creation of elsets for each material type
    with open(cwd + Material_Sets,'w') as outputICA:
        # outputICA.write('*Elset, elset=RVE_MaterialSet, instance=crack_model \n')
        outputICA.write('*Elset, elset=RVE_MaterialSet \n')
        for i in range(0,len(newlist_Set)+1,10):
            outputICA.write(str(newlist_Set[i:i+10]).strip('[').strip(']') + '\n')
        # outputICA.write('*Elset, elset=RVE_Gold, instance=crack_model \n')
        outputICA.write('*Elset, elset=RVE_Metal \n')
        for i in range(0, len(gold_list) + 1, 10):
            outputICA.write(str(gold_list[i:i + 10]).strip('[').strip(']') + '\n')
        # outputICA.write('*Elset, elset=RVE_Polymer, instance=crack_model \n')
        outputICA.write('*Elset, elset=RVE_Polymer \n')
        for i in range(0, len(poly_list) + 1, 10):
            outputICA.write(str(poly_list[i:i + 10]).strip('[').strip(']') + '\n')

    fwrite = open(cwd + RVE_name + "_Full.inp",'w')
    with open(cwd + "2D_CT_Specimen_INCLUDES.inp",'r') as fread:
        for line in fread:
            if line.strip()[:-11] == '*INCLUDE, INPUT=RVE_nodes_RVE_2D_':
                fwrite.write('*INCLUDE, INPUT=RVE_nodes_RVE_2D_' + metalFrac + 'PER_' + RVE_number + '.inp \n')
            elif line.strip()[:-11] == '*INCLUDE, INPUT=RVE_elements_RVE_2D_':
                fwrite.write('*INCLUDE, INPUT=RVE_elements_RVE_2D_' + metalFrac + 'PER_' + RVE_number + '.inp \n')
            elif line.strip()[:-11] == '*INCLUDE, INPUT=Material_Elsets_RVE_2D_':
                fwrite.write('*INCLUDE, INPUT=Material_Elsets_RVE_2D_' + metalFrac + 'PER_' + RVE_number + '.inp \n')
            else:
                fwrite.write(line)

    fwrite.close()
    bash_script.write("abaqus interactive datacheck ask_delete=NO double=both output_precision=full user=VUMAT_COMBINED_POLYMER_STEEL.f job=" + RVE_name + "_Full" + "\n")
bash_script.close()
