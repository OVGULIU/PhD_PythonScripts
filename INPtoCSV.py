import numpy as np

cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER'
InpName = 'Elsets'
filename =  cwd + '/' + InpName+'.inp'
elements = []
switch=0
Readf = open(filename,'r')
lines = Readf.readlines()
Readf.close()
split_line_name = lines[0].split(',')
elset = split_line_name[1].split('=')[1]
entries_per_line = 16
if split_line_name[-1].strip()=='generate':
    generate=True
else:
    generate=False
elements = []
dummyElements = []
Writef = open(cwd + '/FullList'+InpName + '.inp','w')
for line in lines[1:]:
    if line[0] =='*':        
        np.savetxt(cwd+ '/'+elset +'.csv',np.array([len(elements)]+elements), delimiter=",",fmt='%i')
#        print('csv file '+elset+' is written in '+cwd+ '/'+elset +'.csv')
#         dummyElements.sort()
        Writef.write(' /) \n')
        Writef.write('*' + split_line_name[1].split('=')[-1] + ' = (/ ')
        if generate:
            dummyElementsGen = list(range(dummyElements[0],dummyElements[-1]+1,1))
            for x in range(0, len(dummyElementsGen), entries_per_line):
                Writef.write(str(dummyElementsGen[x:x + entries_per_line]).strip('[').strip(']') + ', & \n')
        else:
            for x in range(0,len(dummyElements),entries_per_line):
                Writef.write(str(dummyElements[x:x+entries_per_line]).strip('[').strip(']')+', & \n')
        print(len(elements),elset)
        split_line_name = line.split(',')
        elset = split_line_name[1].split('=')[1].strip()
        if split_line_name[-1].strip()=='generate':
            generate=True
        else:
            generate=False                
        elements = []
        dummyElements = []
    elif line.strip() != '':
        split_line = line.strip().split(',')
        if generate:  
            elements = list(range(int(split_line[0]),int(split_line[1])+1,int(split_line[2])))
#            if elset[3:].upper() == 'GOLD':                
#                dummyElements = range(int(split_line[0]),int(split_line[1]),int(split_line[2]))
#            else:
            dummyElements = list(range(int(split_line[0]),int(split_line[1])+1,int(split_line[2])))
        else:
            # values = map(int, line.strip().split(','))
#            if elset[3:].upper() == 'GOLD':
#                dummyvalues =map(int, line.strip().split(','))
#            else:
#             dummyvalues =[int(x) +500000 for x in line.strip().split(',') if x]
            elements.extend(int(x) for x in line.strip().split(',') if x)
            dummyElements.extend(int(x) for x in line.strip().split(',') if x)
    elif line == lines[-1]:
        np.savetxt(cwd+ '/'+elset +'.csv',np.array([len(elements)]+elements).astype(int), delimiter=",",fmt='%i')
#        print('csv file '+elset+' is written in '+cwd+ '/'+elset +'.csv')
        Writef.write(' /)')
        Writef.write('*' + split_line_name[1].split('=')[-1] + ' = (/ ')
        for x in range(0,len(dummyElements),entries_per_line):
            Writef.write(str(dummyElements[x:x+entries_per_line]).strip('[').strip(']')+', & \n')
        
        print(len(elements),elset)
Writef.close()

#with open(filename,'r') as readf:
#    for line in readf:
#        if line.strip()=='':
#            pass
#        elif line[0] == '*':
#            newarray = line.split(',')
#            Elementname=newarray[1].split('=')[1]
#            if newarray[-1].lower().strip()=='generate':
#                generate=1
#            else:
#                generate=0
#            if switch:
#                for x,y in enumerate(elements):
#                    elements[x] = y
#                elements = [len(elements)]+ elements
#                np.savetxt(cwd+ '/'+Elementname +'.csv',np.array(elements).astype(int), delimiter=",",fmt='%i')    
#                print('csv file '+Elementname+' is written in '+cwd+ '/'+Elementname +'.csv')
#                elements=[]
#            switch=1
#        else:
#            if generate:
#                start= int(line.split(',')[0])
#                stop = int(line.split(',')[1])
#                step = int(line.split(',')[2])
#                elements= range(start,stop+1,step)
#            else:
#                elements.extend(map(int,line.split(',')))

#cwd = '/home/cerecam/Desktop/GP_BoundaryConditionTests/InputFiles'
#Readf = open(cwd + '/ElementSets.inp','r')
#Writef = open(cwd + '/DummyElementSets.inp','w')
##import numpy as np
#
#dummyEle = []
#
#switch=0
#for line in Readf:
#    if line.strip()=='':
#            pass
#    elif line[0] == '*' or line.strip()=='':
#        elsetname = line.split(',')
#        if elsetname[-1].lower().strip()=='generate':
#            generate=1
#        else:
#            generate=0
#        if switch:
#            if generate:
#                pass
#            else:    
#                print(len(dummyEle),elsetname)
#                Writef.write(','.join(elsetname))                
#                for x in range(0,len(dummyEle),10):
#                    Writef.write(str(dummyEle[x:x+10]).strip('[').strip(']')+'\n')
#        dummyEle = []
#        switch = 1
#    else:        
#        newarray = []
#        newarray = [(entry+500000) for entry in map(int,line.split(','))]
#        if generate:
#            Writef.write(','.join(elsetname))
#            Writef.write(str(newarray[0])+', '+str(newarray[1])+', ' +str(newarray[2]-500000)+'\n')    
#        else:
#            dummyEle.extend(newarray)
#
#Readf.close()
##Writef = open(cwd + '/DummyElementSets.inp','w')
##dummyEle.sort()
##for x in range(0,len(dummyEle),10):
##    Writef.write(str(dummyEle[x:x+10]))
#
#Writef.close()
