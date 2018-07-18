"""
Creates csv and inp files which list the elements that lie on the boundaries of the RVE
"""
import numpy as np


def readinp(filename, startline):
	"""
	Reads file and converts line to list and places inlist of list
	:param filename: filename to read from
	:param startline: whther to start from line 1 or 0.
	:return: list of list of each line of filename
	"""
	output_list = []
	readfile = open(filename, 'r')
	if startline:
		readfile.readline()
	for line in readfile:
		newarray = [float(x) for x in line.split(',')]
		output_list.append(newarray)
	readfile.close()
	return output_list


def writeinp(lst, output_name, set_name, eset=0, nset=0, create_csv=0):
	"""
	Writes .inp file given list of nodes or elements
	:param lst: list of elements of nodes
	:param output_name: file to write to
	:param set_name: name of el/nset
	:param eset: state if elset (default = 0)
	:param nset: state if nset (default = 0)
	:param create_csv: 1 = create a csv fiel from lst otherwise not
	only eset or nset, if both ==1 returns error
	:return: None
	"""
	if ((eset == 1) and (nset == 1)) or not((eset == 1) or (nset == 1)):
		print("Error list given as both nset or elset, only one to be given at a time")
	elif int(eset) == 1:
		firstline = "*elset, elset={}, instance=RVE \n".format(set_name)
	elif int(nset) == 1:
		firstline = "*nset, nset={}, instance=RVE \n".format(set_name)
	inpfile_write = open(output_name+'.inp', 'w')
	inpfile_write.write(firstline)
	for i in range(0, len(lst), 10):
		inpfile_write.write(''.join(str(lst[i:i + 10])).strip('[').strip(']') + '\n')
	if create_csv:
		arry = np.array([len(lst)] + lst)
		np.savetxt(output_name+'.csv', arry, delimiter=",", fmt='%i')
	inpfile_write.close()


cwd = '/home/etg/Desktop'
nodefile = 'Nodes.inp'
#elementfile = 'Elements_All.inp'
gold_element = range(1, 1213242+1)
poly_element = range(1213243, 2097152+1)
if cwd[-1] != '/':
	cwd = cwd + '/'
if nodefile[0] == '/':
	nodefile = nodefile[1:]
# if elementfile[0] == '/':
#     elementfile = elementfile[1:]

nodelist = readinp(cwd + nodefile, 1)
#elelist = readinp(cwd + elementfile, 0)
gold_elelist = readinp(cwd  + 'GoldElements.inp',0)

x0_val = min(nodelist, key=lambda z: z[-3])[-3]
x1_val = max(nodelist, key=lambda z: z[-3])[-3]
y0_val = min(nodelist, key=lambda z: z[-2])[-2]
y1_val = max(nodelist, key=lambda z: z[-2])[-2]
z0_val = min(nodelist, key=lambda z: z[-1])[-1]
z1_val = max(nodelist, key=lambda z: z[-1])[-1]

x0, x1 = [], []
y0, y1 = [], []
z0, z1 = [], []

for nodes in nodelist:
	if x0_val == nodes[1]:
		x0.append(int(nodes[0]))
	if x1_val == nodes[1]:
		x1.append(int(nodes[0]))
	if y0_val == nodes[2]:
		y0.append(int(nodes[0]))
	if y1_val == nodes[2]:
		y1.append(int(nodes[0]))
	if z0_val == nodes[3]:
		z0.append(int(nodes[0]))
	if z1_val == nodes[3]:
		z1.append(int(nodes[0]))

#writeinp(x0, cwd + 'NodeFiles/x0_all', 'x0', nset=1, create_csv=0)
#writeinp(x1, cwd + 'NodeFiles/x1_all', 'x1', nset=1, create_csv=0)
#writeinp(y0, cwd + 'NodeFiles/y0_all', 'y0', nset=1, create_csv=0)
#writeinp(y1, cwd + 'NodeFiles/y1_all', 'y1', nset=1, create_csv=0)
#writeinp(z0, cwd + 'NodeFiles/z0_all', 'z0', nset=1, create_csv=0)
#writeinp(z1, cwd + 'NodeFiles/z1_all', 'z1', nset=1, create_csv=0)

x_ele_int  = []
y_ele_int  = []
z_ele_int = []
X_dict = {}
Y_dict = {}
Z_dict = {}

# x0_gold, x0_poly = [], []
# x1_gold, x1_poly = [], []
# y0_gold, y0_poly = [], []
# y1_gold, y1_poly = [], []
# z0_gold, z0_poly = [], []
# z1_gold, z1_poly = [], []

# element_dist = abs((x1_val-x0_val)/128.0)
# xmin, ymin, zmin = [x+element_dist for x in [x0_val, y0_val, z0_val]]
# xmax, ymax, zmax = [x-element_dist for x in [x1_val, y1_val, z1_val]]


for increment in range(0, 32):  # type: int
    xmin = 0.0 + (increment*(30.0/32))
    xmax = xmin + (30.0/32.0)
    ymin, zmin = xmin, xmin
    ymax, zmax = xmax, xmax
    x_ele_int = []
    y_ele_int = []
    z_ele_int = []
    for element in gold_elelist:
        nodes_coord = [nodelist[int(_)-1][1:] for _ in element[1:]]
        x_cent, y_cent, z_cent = [_/len(element[1:]) for _ in (np.sum(np.array(nodes_coord), axis=0))]
        centroid = [x_cent, y_cent, z_cent]
        if all([x > centroid[i] for i, x in enumerate([xmin, ymin, zmin])]) and all([x < centroid[i] for i, x in enumerate([xmax, ymax, zmax])]):
            pass
        else:
            if xmax >= x_cent >= xmin:
                x_ele_int.append(int(element[0]))
            if ymax >= y_cent >= ymin:
                y_ele_int.append(int(element[0]))
            if zmax >= z_cent >= zmin:
                z_ele_int.append(int(element[0]))
    X_dict['X' + str(increment)] = x_ele_int
    Y_dict['Y' + str(increment)] = y_ele_int
    Z_dict['Z' + str(increment)] = z_ele_int
    print('X' + str(increment),len(x_ele_int))
    print('Y' + str(increment),len(y_ele_int))
    print('Z' + str(increment),len(z_ele_int))
	
#x0_ele.sort()
#x1_ele.sort()
#y0_ele.sort()
#y1_ele.sort()
#z0_ele.sort()
#z1_ele.sort()


#x0_gold = list(x0_ele[:(x0_ele.index(min(poly_element)))])
#y0_gold = list(y0_ele[:(y0_ele.index(min(poly_element)))])
#z0_gold = list(z0_ele[:(z0_ele.index(min(poly_element)))])
#x1_gold = list(x1_ele[:(x1_ele.index(min(poly_element)))])
#y1_gold = list(y1_ele[:(y1_ele.index(min(poly_element)))])
#z1_gold = list(z1_ele[:(z1_ele.index(min(poly_element)))])

#x0_poly = list(x0_ele[(x0_ele.index(min(poly_element))):])
#y0_poly = list(y0_ele[(y0_ele.index(min(poly_element))):])
#z0_poly = list(z0_ele[(z0_ele.index(min(poly_element))):])
#x1_poly = list(x1_ele[(x1_ele.index(min(poly_element)))+1:])
#y1_poly = list(y1_ele[(y1_ele.index(min(poly_element)))+1:])
#z1_poly = list(z1_ele[(z1_ele.index(min(poly_element)))+1:])

#writeinp(x0_ele, cwd + 'NodeFiles/X0_ele', 'X0_ele', eset=1, create_csv=0)
#writeinp(x1_ele, cwd + 'NodeFiles/X1_ele', 'X1_ele', eset=1, create_csv=0)
#writeinp(y0_ele, cwd + 'NodeFiles/Y0_ele', 'Y0_ele', eset=1, create_csv=0)
#writeinp(y1_ele, cwd + 'NodeFiles/Y1_ele', 'Y1_ele', eset=1, create_csv=0)
#writeinp(z0_ele, cwd + 'NodeFiles/Z0_ele', 'Z0_ele', eset=1, create_csv=0)
#writeinp(z1_ele, cwd + 'NodeFiles/Z1_ele', 'Z1_ele', eset=1, create_csv=0)

#writeinp(x0_poly, cwd + 'NodeFiles/X0_poly', 'X0_poly', eset=1, create_csv=1)
#writeinp(x1_poly, cwd + 'NodeFiles/X1_poly', 'X1_poly', eset=1, create_csv=1)
#writeinp(y0_poly, cwd + 'NodeFiles/Y0_poly', 'Y0_poly', eset=1, create_csv=1)
#writeinp(y1_poly, cwd + 'NodeFiles/Y1_poly', 'Y1_poly', eset=1, create_csv=1)
#writeinp(z0_poly, cwd + 'NodeFiles/Z0_poly', 'Z0_poly', eset=1, create_csv=1)
#writeinp(z1_poly, cwd + 'NodeFiles/Z1_poly', 'Z1_poly', eset=1, create_csv=1)

#writeinp(x0_gold, cwd + 'NodeFiles/X0_GOLD', 'X0_GOLD', eset=1, create_csv=1)
#writeinp(x1_gold, cwd + 'NodeFiles/X1_GOLD', 'X1_GOLD', eset=1, create_csv=1)
#writeinp(y0_gold, cwd + 'NodeFiles/Y0_GOLD', 'Y0_GOLD', eset=1, create_csv=1)
#writeinp(y1_gold, cwd + 'NodeFiles/Y1_GOLD', 'Y1_GOLD', eset=1, create_csv=1)
#writeinp(z0_gold, cwd + 'NodeFiles/Z0_GOLD', 'Z0_GOLD', eset=1, create_csv=1)
#writeinp(z1_gold, cwd + 'NodeFiles/Z1_GOLD', 'Z1_GOLD', eset=1, create_csv=1)
