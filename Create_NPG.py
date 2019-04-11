"""" Remove polymer elements and nodes from 3D RVE model """

import time

metalFrac = '40'
voxels = '40'
# cwd ='/home/cerecam/2M_128x128x128_full/2D_Planes/Npg_Composite/25Voxels_Thick/'
template_INP = "3D_CT_Model_INCLUDES.inp"  # found in mainwd
for voxels in ['40']:
    for metalFrac in ['20']:
        RVE_number = '1'
        print('Processing RVE_number: ' + RVE_number + ', Voxels: ' + voxels + ', Metal fraction: ' + metalFrac)
        print(' ...')

        cwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/' + voxels + 'Voxels/'
        mainwd = '/home/cerecam/Desktop/Crack_Models/' + voxels + 'Voxels/'
        start = time.time()
        # material = 'polymer'
        material = 'metal'
        # Read in all nodes and elements from RVE section
        outputwd = cwd + 'Pure_Npg/'
        RVE_nodes = 'newNodes' + RVE_number + '.inp'
        RVE_Elements = 'newICA_Elements' + RVE_number + '.inp'
        Material_Sets = '3D_Material_Assignment_' + RVE_number + '.inp'
        Boundary_nsets = 'CT_Specimen_noRVE_' + voxels + '_Boundary.inp'
        BoundaryNodes = 'Boundary_nodes.inp'
        elsets = {}
        with open(cwd + Material_Sets) as elsets_file:
            elsets_lines = elsets_file.readlines()
        # elsets_lines.pop(-1)
        with open(cwd + Boundary_nsets) as boundaryElsetFile:
            elsets_lines.extend(boundaryElsetFile.readlines())

        for line in elsets_lines:
            if line == '\n':
                break
            elif line[0] == '*':
                firstline = line.split(',')
                elsets[firstline[1].split('=')[- 1].strip().lower()] = []
            elif firstline[-1].strip().lower() == 'generate':
                splitline = line.strip().split(',')
                elsets[firstline[1].split('=')[- 1].strip().lower()] = range(int(splitline[0]), int(splitline[1]) + 1,
                                                                             int(splitline[2]))
            else:
                splitline = line.strip().split(',')
                elsets[firstline[1].split('=')[- 1].strip().lower()].extend(int(x) for x in splitline)

        for key, item in elsets.items():
            item.sort()



        with open(outputwd + material + '_Elset_' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp',
                  'w') as metal_elset:
            metal_elset.write('*Elset, elset=' + material + ' \n')
            for i in range(0, len(elsets[material]) + 1, 10):
                metal_elset.write(str(elsets[material][i:i + 10]).strip('[').strip(']') + '\n')
            metal_elset.write('*Elset, elset=RVE \n')
            for i in range(0, len(elsets[material]) + 1, 10):
                metal_elset.write(str(elsets[material][i:i + 10]).strip('[').strip(']') + '\n')

        RVE_elements_dict = {}
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
                    dataline = [int(i) for i in line.split(',')]
                    RVE_elements_dict[dataline[0]] = dataline

        Npg_file = open(outputwd + 'Pure_Npg_ICA' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp', 'w')
        for i in elsets[material]:
            line = RVE_elements_dict[i]
            Npg_file.write(', \t'.join([str(p) for p in line]) + '\n')
            metal_nodes.extend(line[1:])
            # dataline = [int(i) for i in line.split(',')]
            # if dataline[0] in elsets[material]:
            #     Npg_file.write(line)
            #     metal_nodes.extend(dataline[1:])
            # else:
            #     polymer_nodes.extend(dataline[1:])
        #
        polymer_nodes = list(set(polymer_nodes))
        metal_nodes = list(set(metal_nodes))
        metal_nodes.sort()
        polymer_nodes.sort()
        Npg_file.close()
        #
        t2 = time.time() - start
        # print('Time to write new element file')
        # print(t2) #####
        RVE_nodes_dict = {}
        Npg_Node_file = open(
            outputwd + 'Pure_Npg_nodes_' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp', 'w')  #####
        with open(cwd + RVE_nodes, 'r') as RVE_Nodes_file:
            # Nodes = RVE_Nodes_file.readlines()
            for line in RVE_Nodes_file:
                if line[0] == '*':
                    pass
                elif line == '\n':
                    break
                else:
                    RVE_nodes_dict[int(line.split(',')[0])] = line


        npg_nodes = metal_nodes + boundaryNodes
        for i in npg_nodes:
            if i in RVE_nodes_dict.keys():
                dataline = RVE_nodes_dict[i]
                Npg_Node_file.write(dataline)

                # # dataline = [int(line.split(',')[0])] + [float(i) for i in line.split(',')[1:]]
                # if (int(line.split(',')[0]) in metal_nodes) or (int(line.split(',')[0]) in elsets['rve_boundary']):
                #     Npg_Node_file.write(line)
        t3 = time.time() - t2
        # print('Time to write new node file')
        # print(t2) #####

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
                    fwrite.write(
                        '*INCLUDE, INPUT=Pure_Npg_nodes_' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp \n')
                elif line.strip()[:-5] == '*INCLUDE, INPUT=newICA_Elements':
                    fwrite.write(
                        '*INCLUDE, INPUT=Pure_Npg_ICA' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp \n')
                elif line.strip()[:-5] == '*INCLUDE, INPUT=3D_Material_Assignment_':
                    fwrite.write(
                        '*INCLUDE, INPUT=metal_Elset_' + voxels + 'Voxels_' + metalFrac + 'PER_' + RVE_number + '.inp \n')
                else:
                    fwrite.write(line)

        fwrite.close()
        print('CT-Specimen ' + voxels + ' voxels thick with inserted RVE ' + RVE_number + ' COMPLETE')
