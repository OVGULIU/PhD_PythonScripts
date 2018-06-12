import numpy as np

cwd = '/home/cerecam/Desktop/GP_BoundaryConditionTests/InputFiles'
InpName = '/ElementSets'
filename =  cwd + InpName+'.inp'
elements = []
switch=0
with open(filename,'r') as readf:
    for line in readf:
        if line.strip()=='':
            pass
        elif line[0] == '*':
            newarray = line.split(',')
            Elementname=newarray[1].split('=')[1]
            if newarray[-1].lower().strip()=='generate':
                generate=1
            else:
                generate=0
            if switch:
                for x,y in enumerate(elements):
                    elements[x] = y
                np.savetxt(cwd+ '/'+Elementname +'.csv',np.array(elements).astype(int), delimiter=",",fmt='%i')    
                print('csv file '+Elementname+' is written in '+cwd+ '/'+Elementname +'.csv')
                elements=[]
            switch=1
        else:
            if generate:
                start= int(line.split(',')[0])
                stop = int(line.split(',')[1])
                step = int(line.split(',')[2])
                elements= range(start,stop+1,step)
            else:
                elements.extend(map(int,line.split(',')))

