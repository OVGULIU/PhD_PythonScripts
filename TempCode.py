"""
To create node list of only polymer nodes
"""
P_nodes = []
with open('/home/cerecam/Desktop/emma_models_NEW/2M_96x96x96_89_over_146/PolymerNodes.inp','r') as fread:
    for line in fread:
        newarray = map(int,line.split(','))
        P_nodes.extend(newarray)

All_Nodes = []
P_Node_Coord = []
with open('/home/cerecam/Desktop/emma_models_NEW/2M_96x96x96_89_over_146/Nodes.inp','r') as fread:
    fread.readline()
    count = 0
    for line in fread:
        if count==len(P_nodes):
            break
        newarray = [float(x) for x in line.split(',')]
        All_Nodes.append(newarray)
        if int(newarray[0])==P_nodes[count]:
            P_Node_Coord.append(str(int(newarray[0])) + ', \t ' +  str(newarray[1:]).strip('[').strip(']'))
            count+=1
with open('/home/cerecam/Desktop/emma_models_NEW/2M_96x96x96_89_over_146/P_Nodes.inp','w') as fwrite:
    fwrite.write('*Node \n')
    for P in P_Node_Coord:
        fwrite.write(P+ ' \n')