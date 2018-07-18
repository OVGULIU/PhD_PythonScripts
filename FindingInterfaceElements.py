# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 08:02:54 2018

@author: cerecam
"""
from collections import defaultdict

cwd = '/home/cerecam/Desktop/Voxel_models/2M_32x32x32/'

NodeElementsG = defaultdict(list)
NodeElementsU = defaultdict(list)
NodeElements= defaultdict(list)
Ele_ConDict = {}
InterfaceNode =[]
InterfaceEle =[]
InterfaceSurf =[]

# Reading in gold elements and nodes connected
readf = open(cwd+"GoldElements.inp",'r')
for line in readf:
    newarray = map(int,line.split(','))
    for i in newarray[1:]:
        NodeElementsG[i].append(newarray[0])
        NodeElements[i].append(newarray[0])
        Ele_ConDict[newarray[0]] = newarray[1:]
readf.close()    
   
# Reading in user elements and nodes connected
readf = open(cwd+"UserElements.inp",'r')
for line in readf:
    newarray = map(int,line.split(','))
    for i in newarray[1:]:
        NodeElementsU[i].append(newarray[0])
        NodeElements[i].append(newarray[0])
        Ele_ConDict[newarray[0]] = newarray[1:]
readf.close()

##Calculating the nodes that lie on the interface of thegold an dpolymer
NonInterface1 = set(NodeElementsU.keys())-set(NodeElementsG.keys())
NonInterface2 = set(NodeElementsG.keys())-set(NodeElementsU.keys())
InterfaceNode = sorted(list(set(NodeElements.keys())-set(NonInterface1)-set(NonInterface2)))
#
##writef= open(cwd+"InterfaceNodes.inp",'w')
##for i in range(0,len(InterfaceNode),10):
##    writef.write(str(InterfaceNode[i:i+10]).strip(']').strip('[')+'\n')
##writef.close()
#
# Calculating the elements associated with interface nodes
for i in InterfaceNode:
    InterfaceEle.extend(NodeElements[i])
InterfaceEle = list(set(InterfaceEle))

#writef= open(cwd+"InterfaceElements.inp",'w')
#for i in range(0,len(InterfaceEle),10):
#    writef.write(str(InterfaceEle[i:i+10]).strip(']').strip('[')+'\n')
#writef.close()

Faces = {}
for i in InterfaceEle:
#    EleFaces = [sorted([Ele_ConDict[i][0],Ele_ConDict[i][1],Ele_ConDict[i][2],Ele_ConDict[i][3]]),
#                sorted([Ele_ConDict[i][4],Ele_ConDict[i][5],Ele_ConDict[i][6],Ele_ConDict[i][7]]),
#                sorted([Ele_ConDict[i][6],Ele_ConDict[i][2],Ele_ConDict[i][3],Ele_ConDict[i][7]]),
#                sorted([Ele_ConDict[i][5],Ele_ConDict[i][1],Ele_ConDict[i][0],Ele_ConDict[i][4]]),
#                sorted([Ele_ConDict[i][5],Ele_ConDict[i][1],Ele_ConDict[i][2],Ele_ConDict[i][6]]),
#                sorted([Ele_ConDict[i][4],Ele_ConDict[i][0],Ele_ConDict[i][3],Ele_ConDict[i][7]])]
    ElementCheck = list(set(Ele_ConDict[i])-set(InterfaceNode))
    if len(ElementCheck)<5:
        InterfaceSurf.append(i)
        Faces[i] = [set(Ele_ConDict[i])-(set(Ele_ConDict[i])-set(InterfaceNode))]
InterfaceSurf = list(set(InterfaceSurf))

#writef= open(cwd+"InterfaceEleSurfaces.inp",'w')
#for i in range(0,len(InterfaceSurf),10):
#    writef.write(str(InterfaceSurf[i:i+10]).strip(']').strip('[')+'\n')
#writef.close()

readf = open(cwd+"InterfaceEleSurfaces.inp",'r')
for line in readf:
    newarray = map(int,line.split(','))
    InterfaceSurf.extend(newarray)
readf.close()

count=0
for i,val in Faces.items():
    EleFaces = [sorted([Ele_ConDict[i][0],Ele_ConDict[i][1],Ele_ConDict[i][2],Ele_ConDict[i][3]]),
                sorted([Ele_ConDict[i][4],Ele_ConDict[i][5],Ele_ConDict[i][6],Ele_ConDict[i][7]]),
                sorted([Ele_ConDict[i][6],Ele_ConDict[i][2],Ele_ConDict[i][3],Ele_ConDict[i][7]]),
                sorted([Ele_ConDict[i][5],Ele_ConDict[i][1],Ele_ConDict[i][0],Ele_ConDict[i][4]]),
                sorted([Ele_ConDict[i][5],Ele_ConDict[i][1],Ele_ConDict[i][2],Ele_ConDict[i][6]]),
                sorted([Ele_ConDict[i][4],Ele_ConDict[i][0],Ele_ConDict[i][3],Ele_ConDict[i][7]])]
    for j in EleFaces:
        if sorted(list(val)) ==sorted(list(j)):
            count+=1



