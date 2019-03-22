"""" Remove polymer elements and nodes from 3D RVE model """

import time
metalFrac = '40'
voxels = '10'
# cwd ='/home/cerecam/2M_128x128x128_full/2D_Planes/Npg_Composite/25Voxels_Thick/'
cwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/' + voxels + 'Voxels/'
mainwd = '/home/cerecam/Desktop/Crack_Models/10Voxels/'
template_INP =  "3D_CT_Model_INCLUDES.inp" # found in mainwd
for RVE_number in ['1']:
    start = time.time()
    # material = 'polymer'
    material = 'metal'
    # Read in all nodes and elements from RVE section
    outputwd = cwd + 'Pure_Npg/'
    RVE_nodes = 'newNodes' + RVE_number + '.inp'
    RVE_Elements = 'newICA_Elements' + RVE_number + '.inp'
    Material_Sets = '3D_Material_Assignment_' + RVE_number + '.inp'
    Boundary_nsets = 'CT_Specimen_noRVE_' + voxels + '_Boundary.inp'
    elsets = {}
    with open(cwd + Material_Sets) as elsets_file:
        elsets_lines = elsets_file.readlines()
    elsets_lines.pop(-1)
    with open(cwd +Boundary_nsets) as boundaryElsetFile:
        elsets_lines.extend(boundaryElsetFile.readlines())

    for line in elsets_lines:
        if line == '\n':
            break
        elif line[0] == '*':
            firstline = line.split(',')
            elsets[firstline[1].split('=')[- 1].strip().lower()] = []
        elif firstline[-1].strip().lower() =='generate':
            splitline = line.strip().split(',')
            elsets[firstline[1].split('=')[- 1].strip().lower()] = range(int(splitline[0]), int(splitline[1])+1, int(splitline[2]))
        else:
            splitline = line.strip().split(',')
            elsets[firstline[1].split('=')[- 1].strip().lower()].extend(int(x) for x in splitline)

    for key,item in elsets.items():
        item.sort()

    # print(time.time() - start) #####

    with open(outputwd + material + '_Elset_'+ voxels + 'Voxels_' + metalFrac + 'PER_' + '_' +  RVE_number + '.inp','w') as metal_elset:
        metal_elset.write('*Elset, elset='+material+ ' \n')
        for i in range(0, len(elsets[material]) + 1, 10):
            metal_elset.write(str(elsets[material][i:i + 10]).strip('[').strip(']') + '\n')
        metal_elset.write('*Elset, elset=RVE \n')
        for i in range(0, len(elsets[material]) + 1, 10):
            metal_elset.write(str(elsets[material][i:i + 10]).strip('[').strip(']') + '\n')

    # print(time.time() - start) #####
    RVE_elements_dict = {}
    Npg_file = open(outputwd + 'Pure_Npg_ICA' + voxels + 'Voxels_' + metalFrac + 'PER_' +  RVE_number + '.inp', 'w')
    metal_nodes = []
    polymer_nodes = []
    with open(cwd + RVE_Elements, 'r') as RVE_elements_file:
        for line in RVE_elements_file:
            if line[0] == '*':
                print(line)
                pass
            elif line == '\n':
                break
            else:
                RVE_elements_dict[dataline[0]] = dataline
                dataline = [int(i) for i in line.split(',')]
                if dataline[0] in elsets[material]:
                    Npg_file.write(line)
                    metal_nodes.extend(dataline[1:])
                else:
                    polymer_nodes.extend(dataline[1:])
    #
    polymer_nodes = list(set(polymer_nodes))
    metal_nodes = list(set(metal_nodes))
    metal_nodes.sort()
    polymer_nodes.sort()
    Npg_file.close()
    #

    # print(time.time() - start) #####

    Npg_Node_file = open(outputwd + 'Pure_Npg_nodes_' + voxels + 'Voxels_' + metalFrac + 'PER_' +  RVE_number + '.inp','w') #####
    with open(cwd + RVE_nodes, 'r') as RVE_Nodes_file:
        # Nodes = RVE_Nodes_file.readlines()

        for line in RVE_Nodes_file:
            if line[0] == '*':
                pass
            elif line == '\n':
                break
            else:
                # dataline = [int(line.split(',')[0])] + [float(i) for i in line.split(',')[1:]]
                if (int(line.split(',')[0]) in metal_nodes) or (int(line.split(',')[0]) in elsets['rve_boundary']):
                    Npg_Node_file.write(line)

    print(time.time() - start) #####

    Npg_Node_file.close()
    RVE_name = '3D_NPG_' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp'
    fwrite = open(outputwd + RVE_name, 'w')
    with open(mainwd + template_INP, 'r') as fread:
        for line in fread:
            if line.strip() == '*INCLUDE, INPUT=CT_Specimen_noRVE_5_Nodes.inp':
                fwrite.write('*INCLUDE, INPUT=CT_Specimen_noRVE_' + voxels + '_Nodes.inp \n')
            elif line.strip() == '*INCLUDE, INPUT=CT_Specimen_noRVE_5_Elements.inp':
                fwrite.write('*INCLUDE, INPUT=CT_Specimen_noRVE_' + voxels + '_Elements.inp \n')
            elif line.strip() == '*INCLUDE, INPUT=CT_Specimen_noRVE_5_Surfaces.inp':
                fwrite.write('*INCLUDE, INPUT=CT_Specimen_noRVE_' + voxels + '_Surfaces.inp \n')
            elif line.strip()[:-5] == '*INCLUDE, INPUT=newNodes':
                fwrite.write('*INCLUDE, INPUT=Pure_Npg_nodes_' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp \n')
            elif line.strip()[:-5] == '*INCLUDE, INPUT=newICA_Elements':
                fwrite.write('*INCLUDE, INPUT=Pure_Npg_ICA' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp \n')
            elif line.strip()[:-5] == '*INCLUDE, INPUT=3D_Material_Assignment_':
                fwrite.write('*INCLUDE, INPUT=metal_Elset_' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp \n')
            else:
                fwrite.write(line)

    fwrite.close()
    print(' ...')
    print('CT-Specimen ' + voxels + ' voxels thick with inserted RVE ' + RVE_number + ' COMPLETE')
    print(time.time()-start)

