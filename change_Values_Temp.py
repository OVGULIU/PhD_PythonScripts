# new_file = open('/home/cerecam/Desktop/Crack_Models/20PER/1/changed_RVE_2D_20PER_1G_Elements.inp' , 'w')
# with open('/home/cerecam/Desktop/Crack_Models/20PER/1/RVE_2D_20PER_1G_Elements.inp' , 'r') as old_file:
#     for entry in old_file:
#         dataline = [int(i.strip()) for i in entry.split(',')]
#         dataline[1:] = [x-16641 for x in dataline[1:]]
#         new_file.write(', \t'.join([str(p) for p in dataline]) + '\n')
# new_file.close()

RVE_nodes_old = 'Nodes.inp'
cwd = '/home/cerecam/Desktop/Crack_Models/40PER/1/'
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
enlargeNodes(6.72/2.4,RVE_nodes_old, 'scaled_'+RVE_nodes_old)