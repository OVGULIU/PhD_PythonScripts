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
InterfaceNode =[]

readf = open(cwd+"GoldElements.inp",'r')
for line in readf:
    newarray = map(int,line.split(','))
    for i in newarray[1:]:
        NodeElementsG[i].append(newarray[0])
        NodeElements[i].append(newarray[0])
readf.close()       
readf = open(cwd+"UserElements.inp",'r')
for line in readf:
    newarray = map(int,line.split(','))
    for i in newarray[1:]:
        NodeElementsU[i].append(newarray[0])
        NodeElements[i].append(newarray[0])
readf.close()
NonInterface1 = set(NodeElementsU.keys())-set(NodeElementsG.keys())
NonInterface2 = set(NodeElementsG.keys())-set(NodeElementsU.keys())
InterfaceNode = sorted(list(set(NodeElements.keys())-set(NonInterface1)-set(NonInterface2)))

writef= open(cwd+"InterfaceNodes.inp",'w')
for i in range(0,len(InterfaceNode),10):
    writef.write(str(InterfaceNode[i:i+10]).strip(']').strip('[')+'\n')
writef.close()
