"""
Script to change list fo all elements in fiel into separate elements list for each material
"""
cwd = '/home/cerecam/Desktop/MesoporousSilica/Short/ShortExperimental'
filename = cwd+'/UserElementsSets.inp'
fread = open(filename,'r')
UserElements = []
for line in fread:
	if line[0]=='*':
		pass
	else:
		UserElements.extend(map(int,line.split(',')))
print(len(UserElements))
fread.close()

SiliconElements = range(1,39184+1)
filename = cwd+'/SiliconElementsSets.inp'
fread = open(filename,'r')
fread.readline()
fread.readline()
for line in fread:
	if line[0]=='*':
		pass
	else:
		SiliconElements.extend(map(int,line.split(',')))
SiliconElements= list(set(SiliconElements))
print(len(SiliconElements))
fread.close()

filename = cwd+'/Elements.inp'
fread = open(filename,'r')
Elements = []
UserElementsCon = []
SiliconElementsCon = []
for line in fread:
	if line[0]=='*':
		pass
	else:
		Elements.append(map(int,line.split(',')))
fread.close()
print(len(UserElements)+len(SiliconElements))
print(Elements[10])
print(Elements[1000])
print(Elements[33250])
		
for i in UserElements:
	UserElementsCon.append(Elements[i-1])
		
for i in SiliconElements:
	SiliconElementsCon.append(Elements[i-1])
	
filename = cwd + '/UserElements.inp'	
with open( filename,'w') as  fwrite:
	for i in UserElementsCon:
		fwrite.write(str(i).strip('[').strip(']') + '\n')
		
		
filename = cwd + '/SiliconElements.inp'	
with open(filename,'w') as  fwrite:
	for i in SiliconElementsCon:
		fwrite.write(str(i).strip('[').strip(']') + '\n')		

