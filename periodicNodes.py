# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 09:48:58 2017

@author: cerecam

abaqus viewer noGui=/home/cerecam/Desktop/periodicNodes.py
"""

def writefile(filename, values,nset):
    F = open(filename,'w+')
    F.write('*Nset, nset='+str(nset)+', instance=i_cube\n')
    count = 1
    for val in values:   
        if count%14 == 0:
            F.write(str(val[0])+'\n')
            count +=1
        else:
            F.write(str(val[0])+', ')   
            count  += 1
            
    F.close()
#    print >> sys.__stdout__, (str(filename)+' has been written with '+ str(len(values)))
 

import numpy as np
import csv,math
import sys,os
from odbAccess import openOdb

Dimensions = [(-20,20),(-20,20),(0,40)]

currentwd = '/home/cerecam/Desktop/MesoporousSilica/Long'
outputwd = currentwd
odbfile = '/Long' 
odbname = str(currentwd)+str(odbfile)+'.odb'
odb = openOdb(odbname)
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
frame_val = steps.frames[-1]
myinstance = odb.rootAssembly.instances[odb.rootAssembly.instances.keys()[0]]

RightInt,LeftInt, Right, Left, Top, Bottom, Front, Back = [], [], [], [], [], [], [], []

RI_T_F, LI_T_F, RI_Bot_F, LI_Bot_F = [],[],[],[]
RI_T_B, LI_T_B, RI_Bot_B, LI_Bot_B = [],[],[],[]
RI_F, RI_Bot, RI_T, RI_B = [],[],[],[]
LI_F, LI_Bot, LI_T, LI_B = [],[],[],[]
T_F, T_B, Bot_F, Bot_B = [],[],[],[]

PolymerNodeArray= []
for ele in myinstance.elementSets['DUMMY'].elements:
         PolymerNodeArray.extend(list(ele.connectivity))
         for nodes in ele.connectivity:
             if myinstance.nodes[int(nodes)-1].coordinates[2]==
PolymerNodeArray= sorted(list(set(PolymerNodeArray)))
print >> sys.__stdout__, ('Number of polymer nodes: '+str(len(PolymerNodeArray)))
SilicaNodeArray = []
for ele in myinstance.elementSets['SILIZIUM'].elements:
    SilicaNodeArray.extend(list(ele.connectivity))
SilicaNodeArray = sorted(list(set(SilicaNodeArray)))
print >> sys.__stdout__, ('Number of silica nodes: '+str(len(SilicaNodeArray)))

filename = currentwd+'/nodeSets/PolymerNodeSet.inp'
F = open(filename,'w+')
F.write('*Nset, nset='+str('PolymerNodes')+', instance=i_cube\n')
count = 1
for val in PolymerNodeArray:   
    if count%14 == 0:
        F.write(str(val)+'\n')
        count +=1
    else:
        F.write(str(val)+', ')   
        count  += 1
F.close()

filename = currentwd+'/nodeSets/SilicaNodeSet.inp'
F = open(filename,'w+')
F.write('*Nset, nset='+str('SillicaNodes')+', instance=i_cube\n')
count = 1
for val in SilicaNodeArray:   
    if count%14 == 0:
        F.write(str(val)+'\n')
        count +=1
    else:
        F.write(str(val)+', ')   
        count  += 1
F.close()

nodeArray = myinstance.nodes
for count,val in enumerate(myinstance.nodes):
    RI, LI, R, L, T, Bot, F, B =0,0,0,0,0,0,0,0

    if val.coordinates[0] == 30.0:
        Right.append((val.label,val.coordinates))
        
    if val.coordinates[0] == -30.0:
        Left.append((val.label,val.coordinates))
        
    if (val.coordinates[0] >= Dimensions[0][0]) & (val.coordinates[0] <= Dimensions[0][1]):
        if val.coordinates[1] == Dimensions[1][1]:
            T=1
        if val.coordinates[1] == Dimensions[1][0]:
            Bot=1
        if val.coordinates[2] == Dimensions[2][1]:
            F=1 
        if val.coordinates[2] == Dimensions[2][0]:
            B=1
        if val.coordinates[0] == Dimensions[0][1]:
            RI =1
            if T ==1:                
                if (F == 1):
                    RI_T_F.append((val.label,val.coordinates))
                elif (B == 1):
                    RI_T_B.append((val.label,val.coordinates))
                else:
                    RI_T.append((val.label,val.coordinates))
                    
            elif Bot ==1:
                if (F == 1):
                    RI_Bot_F.append((val.label,val.coordinates))
                elif (B == 1):
                    RI_Bot_B.append((val.label,val.coordinates))
                else:
                    RI_Bot.append((val.label,val.coordinates))
                
            elif F ==1:
                RI_F.append((val.label,val.coordinates))
                
            elif B ==1:
                RI_B.append((val.label,val.coordinates))
                
            else:
                RightInt.append((val.label,val.coordinates))
                
        if val.coordinates[0] == Dimensions[0][0]:
            LI =1
            if T ==1:                
                if (F == 1):
                    LI_T_F.append((val.label,val.coordinates))
                elif (B == 1):
                    LI_T_B.append((val.label,val.coordinates))
                else:
                    LI_T.append((val.label,val.coordinates))
                    
            elif Bot ==1:
                if (F == 1):
                    LI_Bot_F.append((val.label,val.coordinates))
                elif (B == 1):
                    LI_Bot_B.append((val.label,val.coordinates))
                else:
                    LI_Bot.append((val.label,val.coordinates))
                
            elif (F ==1):
                LI_F.append((val.label,val.coordinates))
                
            elif B ==1:
                LI_B.append((val.label,val.coordinates))
                
            else:
                LeftInt.append((val.label,val.coordinates))
        if (T==1) and (LI == 0) and (F == 0) and (B == 0) and (RI ==0):
            Top.append((val.label,val.coordinates))
        if (Bot==1) and (LI == 0) and (F == 0) and (B == 0) and (RI ==0):
            Bottom.append((val.label,val.coordinates))
        if T ==1 and (F==1) and (LI==0) and (RI ==0):
            T_F.append((val.label,val.coordinates))
        if Bot ==1 and (F==1) and (LI==0) and (RI ==0):
            Bot_F.append((val.label,val.coordinates))
        if (F==1) and (LI == 0) and (T == 0) and (Bot == 0) and (RI ==0):
            Front.append((val.label,val.coordinates))
        if T ==1 and (B==1) and (LI==0) and (RI ==0):
            T_B.append((val.label,val.coordinates))
        if Bot ==1 and (B==1) and (LI==0) and (RI ==0):
            Bot_B.append((val.label,val.coordinates))
        if (B==1) and (LI == 0) and (T == 0) and (Bot == 0) and (RI ==0):
            Back.append((val.label,val.coordinates))
#        if str(val.label) == '4432':
#            print >> sys.__stdout__, (str(RI)+str(LI)+str(Bot)+str(T)+str(F)+str(B)+str(L)+str(R))
#RightInt = sorted(RightInt, key=lambda x: x[1][1])
#LeftInt = sorted(LeftInt, key=lambda x: x[1][1])
#Top = sorted(Top, key=lambda x: x[1][1])
#Bottom = sorted(Bottom, key=lambda x: x[1][1])
#Back = sorted(Back, key=lambda x: x[1][1])
#Front = sorted(Front, key=lambda x: x[1][1])
#RI_T = sorted(RI_T, key=lambda x: x[1][1])
#RI_Bot = sorted(RI_Bot, key=lambda x: x[1][1])
#RI_F = sorted(RI_F, key=lambda x: x[1][1])
#RI_B = sorted(RI_B, key=lambda x: x[1][1])
#RI_T_F = sorted(RI_T_F, key=lambda x: x[1][1])
#RI_T_B = sorted(RI_T_B, key=lambda x: x[1][1])
#RI_Bot_F = sorted(RI_Bot_F, key=lambda x: x[1][1])
#RI_Bot_B = sorted(RI_Bot_B, key=lambda x: x[1][1])
#LI_T = sorted(LI_T, key=lambda x: x[1][1])
#LI_Bot = sorted(LI_Bot, key=lambda x: x[1][1])
#LI_F = sorted(LI_F, key=lambda x: x[1][1])
#LI_B = sorted(LI_B, key=lambda x: x[1][1])
#LI_T_F = sorted(LI_T_F, key=lambda x: x[1][1])
#LI_T_B = sorted(LI_T_B, key=lambda x: x[1][1])
#LI_Bot_F = sorted(LI_Bot_F, key=lambda x: x[1][1])
#LI_Bot_B = sorted(LI_Bot_B, key=lambda x: x[1][1])
#T_F = sorted(T_F, key=lambda x: x[1][1])
#T_B = sorted(T_B, key=lambda x: x[1][1])
#Bot_F = sorted(Bot_F, key=lambda x: x[1][1])
#Bot_B = sorted(Bot_B, key=lambda x: x[1][1])
#               
#nodeSets = {'RightInterface':RightInt,'LeftInterface':LeftInt,'Top_sqr':Top,'Bottom_sqr':Bottom,'Back_sqr':Back,'Front_sqr':Front,
#            'RI_T':RI_T,'RI_Bot':RI_Bot,'RI_F':RI_F,'RI_B':RI_B,'RI_T_F':RI_T_F,'RI_T_B':RI_T_B,'RI_Bot_F':RI_Bot_F,'RI_Bot_B':RI_Bot_B,
#            'LI_T':LI_T,'LI_Bot':LI_Bot,'LI_F':LI_F,'LI_B':LI_B,'LI_T_F':LI_T_F,'LI_T_B':LI_T_B,'LI_Bot_F':LI_Bot_F,'LI_Bot_B':LI_Bot_B,
#            'T_F' : T_F, 'T_B': T_B, 'Bot_F': Bot_F, 'Bot_B':Bot_B}
#for key,value in nodeSets.items():
#    filename = '/home/cerecam/Desktop/'+'nodeSets/'+str(key)+'.inp'
#    writefile(filename, value, key)
#  

  
#Partners = [('Top_sqr','Bottom_sqr'),('Back_sqr','Front_sqr')] 
#PartnersX = [('RightInterface','LeftInterface'),('RI_T','LI_T'),('RI_Bot','LI_Bot'),('RI_F','LI_F'),('RI_B','LI_B'),('RI_T_F','LI_T_F'),('RI_T_B','LI_T_B'),('RI_Bot_F','LI_Bot_F'),('RI_Bot_B','LI_Bot_B')]  
#PX = []    
#for PartnerNodes in [('RightInterface','LeftInterface')]:
#    start_at = -1
#    locs = []
#    for i in nodeSets[str(PartnerNodes[0])]:
#        while True:
#            try:
#                loc= nodeSets[str(PartnerNodes[0])].index(i[1][1],start_at+1)
#            except ValueError:
#                break
#            else:
#                locs.append(loc)
#                start_at = loc                   
#                   
#print >> sys.__stdout__, (str(loc)) 
# 
#PartnersY = [('RI_T','RI_Bot'),('RI_T_F','RI_Bot_F'),('RI_Bot_B','RI_T_B'),('LI_T','LI_Bot'),('LI_T_F','LI_Bot_F'),('LI_Bot_B','LI_T_B')('T_F', 'Bot_B')]  
#PartnersZ = [('RI_F','RI_B'),('RI_T_F','RI_T_B'),('RI_Bot_F','RI_Bot_B'),('LI_F','LI_B'),('LI_T_F','LI_T_B'),('LI_Bot_F','LI_Bot_B'),('T_F', 'T_B'), ('Bot_F', 'Bot_B')]  
#print >> sys.__stdout__, str(RightInt.values().__getitem__(1)[1])
#sorted(D.items(), key=lambda x:L.index(x[0])
#print >> sys.__stdout__, ('RI_F: ' + str(sorted(RI_F, key=RI_F.get[1]))) #1 Sorted values by item in values
#print >> sys.__stdout__, ('RI_F: ' + str(LI_F)) # Sorted values by item in values
#print >> sys.__stdout__, (' ') # Sorted values by item in values
#print >> sys.__stdout__, ('RI_F: ' + str(sorted(LI_F, key=lambda x: x[1][1]))) # Sorted values by item in values




