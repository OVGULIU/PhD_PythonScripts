"""
Post processing of CT_Specimens for various volume fractions and various voxel thicknesses
"""

from odbAccess import openOdb
import numpy as np
import csv, math, sys
from abaqusConstants import *
from math import pi

def totalDamageEnd():
	metalFrac = '30'
	#material = 'Composite'
	material = 'Pure_Npg'
	voxels = '20'
	resultsFile = open('/home/cerecam/Desktop/Crack_Models/' + 'Results2203_' + material + '.txt', 'w')
	#for voxels in ['5','10','15','20','30','40']:
	## Code to get total number of damaged elemtns at end fo simulation 
	for voxels in ['10','20','30','40']:
	#for voxels in ['10']:
		totalEleDamaged_metal = []
		totalEleDamaged_polymer = []
		#for metalFrac in ['20', '30', '40', '50', '60', '70', '80']:
		for metalFrac in ['40', '50', '60', '70', '80']:
			cwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/Results/' + material + '/'
			if material == 'Compsite':
				odbname = 'RVE_' + voxels + 'Vox_' + metalFrac + 'PER_1_Final.odb'
			elif material == 'Pure_Npg':
				odbname = 'NPG_' + metalFrac + 'PER_' + voxels + 'Vox_Final.odb'
			try:
				print >> sys.__stdout__, ("\n")
				print >> sys.__stdout__, str("Processing results for " + odbname)
				odb = openOdb(cwd + odbname)
				assem = odb.rootAssembly
				myInstance = assem.instances['CT-MODEL']
				stepKey = odb.steps.keys()
				steps = odb.steps[stepKey[-1]]
				all_frames = steps.frames
				last_frame = all_frames[-1]
				if material == 'Composite':
					polymerEle = myInstance.elementSets['POLYMER'].elements
				metalEle = myInstance.elementSets['METAL'].elements
				
				if material == 'Composite':
					polymerElset = [i.label for i in polymerEle]
				else:
					polymerElset = []
				metalElset = [i.label for i in metalEle]

				#polymerNset = []
				#for i in polymerEle:
					#polymerNset += list(i.connectivity)
				#polymerNset = list(set(polymerNset))

				#metalNset = []
				#for i in metalEle:
					#metalNset += list(i.connectivity)
				#metalNset = list(set(metalNset))

				#for frame in all_frames:
				frame = last_frame
				status = frame.fieldOutputs['STATUS']

				status_Dict = {}

				for i in status.values:
					status_Dict[i.elementLabel] = i.data
				#print >> sys.__stdout__, ('** Status variable extraction complete')		

				metalStatus_Dict = {}
				damagedEle_metal = 0
				for i in metalElset:
					metalStatus_Dict[i] = status_Dict[i]
					if status_Dict[i] == 0.0:
						damagedEle_metal += 1
				print >> sys.__stdout__, ("\n")
				totalEleDamaged_metal.append((int(metalFrac),int(voxels),damagedEle_metal,float(damagedEle_metal)/float(len(metalElset))*100.0,
				float(damagedEle_metal)/float(len(metalElset + polymerElset))*100.0))
				
				print >> sys.__stdout__, ("Percentage of damaged and removed metal elements: " + str(float(damagedEle_metal)/float(len(metalElset))*100.0) + " %")	
				print >> sys.__stdout__, ("Percentage of damaged and removed metal elements from total elements: " + str(float(damagedEle_metal)/float(len(metalElset + polymerElset))*100.0) + " %")	
				
				if material == 'Composite':
					polymerStatus_Dict = {}
					damagedEle_polymer = 0
					for i in polymerElset:
						polymerStatus_Dict[i] = status_Dict[i]
						if status_Dict[i] == 0.0:
							damagedEle_polymer += 1
					totalEleDamaged_polymer.append((int(metalFrac),int(voxels),damagedEle_polymer,float(damagedEle_polymer)/float(len(polymerElset))*100.0,
					float(damagedEle_polymer)/float(len(polymerElset + metalElset))*100.0))
					
					print >> sys.__stdout__, ("Percentage of damaged and removed polymer elements: " + str(float(damagedEle_polymer)/float(len(polymerElset))*100.0) + " %")
					print >> sys.__stdout__, ("Percentage of damaged and removed polymer elements from total elements: " + str(float(damagedEle_polymer)/float(len(polymerElset + metalElset))*100.0) + " %")

				#metal_damage = frame.fieldOutputs['SDV2']
				#SDV2_dict = {}
				#for i in metal_damage.values:
					#SDV2_dict[i.elementLabel] = i.data

				#polymer_damage = frame.fieldOutputs['SDV8']
				#SDV8_dict = {}
				#for i in polymer_damage.values:
					#SDV8_dict[i.elementLabel] = i.data

				#metalDamage_Dict = {}
				#for i in metalElset:
					#metalDamage_Dict[i] = SDV2_dict[i]
					
				#print >> sys.__stdout__, ('** metal damage variable extraction complete')	
				##print >> sys.__stdout__, (str(len(metalDamage_Dict)))

				#polymerDamage_Dict = {}
				#for i in polymerElset:
					#polymerDamage_Dict[i] = SDV8_dict[i]
						
				#print >> sys.__stdout__, ('** Polymer damage variable extraction complete')	
				##print >> sys.__stdout__, (str(len(polymerDamage_Dict)))
					
				odb.close()
				
			except:
				print >> sys.__stdout__, (cwd + odbname + " does not exist")
		#print >> sys.__stdout__, (str( totalEleDamaged_metal))
		#print >> sys.__stdout__, (str( totalEleDamaged_polymer))
		resultsFile.write(', '.join([str(i) for i in totalEleDamaged_metal]) + '\n')
		if material == 'Composite':
			resultsFile.write(', '.join([str(i) for i in totalEleDamaged_polymer]) + '\n')

	resultsFile.close()

#totalDamageEnd()

def DamageOverTime():
	### Code to calulate how the number of damaged elemnts changes over time
	resultsFile = open('/home/cerecam/Desktop/Crack_Models/' + 'Results2203_allFrames.txt', 'w')
	material = 'Composite'
	for voxels in ['5','10','15','20','30','40']:
		#for voxels in ['10']:
		totalEleDamaged_metal = []
		totalEleDamaged_polymer = []
		#for metalFrac in ['20', '30', '40', '50', '60', '70', '80']:
		for metalFrac in ['40']:
			cwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/Results/' + material + '/'
			if material == 'Composite':
				odbname = 'RVE_' + voxels + 'Vox_' + metalFrac + 'PER_1_Final.odb'
			elif material == 'Pure_Npg':
				odbname = 'NPG_' + metalFrac + 'PER_' + voxels + 'Vox_Final.odb'
			try:
				print >> sys.__stdout__, ("\n")
				print >> sys.__stdout__, str("Processing results for " + odbname)
				odb = openOdb(cwd + odbname)
				assem = odb.rootAssembly
				myInstance = assem.instances['CT-MODEL']
				stepKey = odb.steps.keys()
				steps = odb.steps[stepKey[-1]]
				all_frames = steps.frames
				last_frame = all_frames[-1]
				if material == 'Composite':
					polymerEle = myInstance.elementSets['POLYMER'].elements
				metalEle = myInstance.elementSets['METAL'].elements
				
				if material == 'Composite':
					polymerElset = [i.label for i in polymerEle]
				else:
					polymerElset = []
				metalElset = [i.label for i in metalEle]

				for frame in all_frames:
					print >> sys.__stdout__, ("Frame time: " + str(frame.frameValue))				
					status = frame.fieldOutputs['STATUS']

					status_Dict = {}

					for i in status.values:
						status_Dict[i.elementLabel] = i.data		

					metalStatus_Dict = {}
					damagedEle_metal = 0
					for i in metalElset:
						metalStatus_Dict[i] = status_Dict[i]
						if status_Dict[i] == 0.0:
							damagedEle_metal += 1
					print >> sys.__stdout__, ("\n")
					totalEleDamaged_metal.append((int(frame.frameValue), int(metalFrac),int(voxels),damagedEle_metal,float(damagedEle_metal)/float(len(metalElset))*100.0,
					float(damagedEle_metal)/float(len(metalElset + polymerElset))*100.0))
					
					print >> sys.__stdout__, ("Percentage of damaged and removed metal elements: " + str(float(damagedEle_metal)/float(len(metalElset))*100.0) + " %")	
					print >> sys.__stdout__, ("Percentage of damaged and removed metal elements from total elements: " + str(float(damagedEle_metal)/float(len(metalElset + polymerElset))*100.0) + " %")	
					
					if material == 'Composite':
						polymerStatus_Dict = {}
						damagedEle_polymer = 0
						for i in polymerElset:
							polymerStatus_Dict[i] = status_Dict[i]
							if status_Dict[i] == 0.0:
								damagedEle_polymer += 1
						totalEleDamaged_polymer.append((int(frame.frameValue), int(metalFrac),int(voxels),damagedEle_polymer,float(damagedEle_polymer)/float(len(polymerElset))*100.0,
						float(damagedEle_polymer)/float(len(polymerElset + metalElset))*100.0))
						
						print >> sys.__stdout__, ("Percentage of damaged and removed polymer elements: " + str(float(damagedEle_polymer)/float(len(polymerElset))*100.0) + " %")
						print >> sys.__stdout__, ("Percentage of damaged and removed polymer elements from total elements: " + str(float(damagedEle_polymer)/float(len(polymerElset + metalElset))*100.0) + " %")
						
				resultsFile.write(', '.join([str(i) for i in totalEleDamaged_metal]) + '\n')
				if material == 'Composite':
					resultsFile.write(', '.join([str(i) for i in totalEleDamaged_polymer]) + '\n')
						
					
					
			except:
				print >> sys.__stdout__, (cwd + odbname + " does not exist")
					
	resultsFile.close()
	odb.close()

#DamageOverTime()

### Code to give crack location in xy plane for first frame when damage occurs
def initialCrackLocation():
	resultsFile = open('/home/cerecam/Desktop/Crack_Models/' + 'Results2203_initialLocation_metal.txt', 'w')
	material = 'Composite'
	for voxels in ['40']:
	#for voxels in ['5']:
		totalEleDamaged_metal = []
		totalEleDamaged_polymer = []
		for metalFrac in ['20', '30', '40', '50', '60', '70', '80']:
		#for metalFrac in ['40']:
			cwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/Results/' + material + '/'
			if material == 'Composite':
				odbname = 'RVE_' + voxels + 'Vox_' + metalFrac + 'PER_1_Final.odb'
			elif material == 'Pure_Npg':
				odbname = 'NPG_' + metalFrac + 'PER_' + voxels + 'Vox_Final.odb'
			#try:
			print >> sys.__stdout__, ("\n")
			print >> sys.__stdout__, str("Processing results for " + odbname)
			odb = openOdb(cwd + odbname)
			assem = odb.rootAssembly
			myInstance = assem.instances['CT-MODEL']
			stepKey = odb.steps.keys()
			steps = odb.steps[stepKey[-1]]
			all_frames = steps.frames
			last_frame = all_frames[-1]
			nodeDict = {}
			for node in myInstance.nodes:
				nodeDict[node.label] = node.coordinates
		
			metalEle = myInstance.elementSets['METAL'].elements
			polymerElset = []
			if material == 'Composite':
				polymerEle = myInstance.elementSets['POLYMER'].elements
				polymerElsetICA = {}
				for i in polymerEle:
					polymerElset.append(i.label)
					polymerElsetICA[i.label] = i.connectivity
					
			
			metalElset = []
			metalElsetICA= {}
			for i in metalEle:
				metalElset.append(i.label)
				metalElsetICA[i.label] = i.connectivity

			for frame in all_frames:
				print >> sys.__stdout__, ("Frame time: " + str(frame.frameValue))				
				status = frame.fieldOutputs['STATUS']

				status_Dict = {}
				for i in status.values:
					status_Dict[i.elementLabel] = i.data		
				
				damagedEle_metal = 0	
				if any(k==1.0 for k in status_Dict.values()):
					metalStatus_Dict = {}
					for i in metalElset:
						metalStatus_Dict[i] = status_Dict[i]
						if status_Dict[i] == 0.0:
							damagedEle_metal += 1
							locationx = sum([nodeDict[k][0] for k in metalElsetICA[i]])/len(metalElsetICA[i])
							locationy = sum([nodeDict[k][1] for k in metalElsetICA[i]])/len(metalElsetICA[i])
							print >> sys.__stdout__, ("Failure in metal")
							print >> sys.__stdout__, ("X: " + str(locationx) + "; Y: " +  str(locationy))
							resultsFile.write(', '.join([str(j) for j in [frame.frameValue,locationx, locationy, 0]]) + '\n')
							
					
					#damagedEle_polymer = 0
					#if material == 'Composite':
						#polymerStatus_Dict = {}
						#for i in polymerElset:
							#polymerStatus_Dict[i] = status_Dict[i]
							#if status_Dict[i] == 0.0:
								#damagedEle_polymer += 1
								#locationx = sum([nodeDict[k][0] for k in polymerElsetICA[i]])/len(polymerElsetICA[i])
								#locationy = sum([nodeDict[k][1] for k in polymerElsetICA[i]])/len(polymerElsetICA[i])
								#print >> sys.__stdout__, ("Failure in polymer")
								#print >> sys.__stdout__, ("X: " + str(locationx) + "; Y: " +  str(locationy))
								#resultsFile.write(', '.join([str(j) for j in [frame.frameValue, locationx, locationy, 1]]) + '\n')
						
					#if (damagedEle_metal>0 or damagedEle_polymer>0):					
						#break
									
					if (damagedEle_metal>0):					
						break
				
			#except:
				#print >> sys.__stdout__, (cwd + odbname + " does not exist")
					
	resultsFile.close()
	odb.close()

initialCrackLocation()


def crackPropagation():
	resultsFile = open('/home/cerecam/Desktop/Crack_Models/' + 'Results2203_locations.txt', 'w')
	material = 'Composite'
	for voxels in ['40']:
		#for voxels in ['10']:
		totalEleDamaged_metal = []
		totalEleDamaged_polymer = []
		for metalFrac in ['20', '30', '40', '50', '60', '70', '80']:
		#for metalFrac in ['30']:
			cwd = '/home/cerecam/Desktop/Crack_Models/' + metalFrac + 'PER/1/Results/' + material + '/'
			if material == 'Composite':
				odbname = 'RVE_' + voxels + 'Vox_' + metalFrac + 'PER_1_Final.odb'
			elif material == 'Pure_Npg':
				odbname = 'NPG_' + metalFrac + 'PER_' + voxels + 'Vox_Final.odb'
			try:
				print >> sys.__stdout__, ("\n")
				print >> sys.__stdout__, str("Processing results for " + odbname)
				odb = openOdb(cwd + odbname)
				assem = odb.rootAssembly
				myInstance = assem.instances['CT-MODEL']
				stepKey = odb.steps.keys()
				steps = odb.steps[stepKey[-1]]
				all_frames = steps.frames
				last_frame = all_frames[-25]
				nodeDict = {}
				for node in myInstance.nodes:
					nodeDict[node.label] = node.coordinates
				
				if material == 'Composite':
					polymerEle = myInstance.elementSets['POLYMER'].elements
				metalEle = myInstance.elementSets['METAL'].elements
				
				if material == 'Composite':
					polymerElset = []
					polymerElsetICA = {}
					for i in polymerEle:
						polymerElset.append(i.label)
						polymerElsetICA[i.label] = i.connectivity
				else:
					polymerElset = []
				
				metalElset = []
				metalElsetICA= {}
				for i in metalEle:
					metalElset.append(i.label)
					metalElsetICA[i.label] = i.connectivity

				frame = last_frame
				#print >> sys.__stdout__, ("Frame time: " + str(frame.frameValue))				
				status = frame.fieldOutputs['STATUS']

				status_Dict = {}

				for i in status.values:
					status_Dict[i.elementLabel] = i.data		

				metalStatus_Dict = {}
				damagedEle_metal = 0
				damageMLocal = []
				for i in metalElset:
					metalStatus_Dict[i] = status_Dict[i]
					if status_Dict[i] == 0.0:
						locationx = sum([nodeDict[k][0] for k in metalElsetICA[i]])/len(metalElsetICA[i])
						locationy = sum([nodeDict[k][1] for k in metalElsetICA[i]])/len(metalElsetICA[i])
						#print >> sys.__stdout__, ("Failure in metal")
						#print >> sys.__stdout__, ("X: " + str(locationx) + "; Y: " +  str(locationy))
						damagedEle_metal += 1
						damageMLocal.append([locationx,locationy])
				
				print >> sys.__stdout__, (str(damagedEle_metal) + " damaged metal elements found \n")
				#totalEleDamaged_metal.append((int(frame.frameValue), int(metalFrac),int(voxels),damagedEle_metal,float(damagedEle_metal)/float(len(metalElset))*100.0,
				#float(damagedEle_metal)/float(len(metalElset + polymerElset))*100.0))
				
				#print >> sys.__stdout__, ("Percentage of damaged and removed metal elements: " + str(float(damagedEle_metal)/float(len(metalElset))*100.0) + " %")	
				#print >> sys.__stdout__, ("Percentage of damaged and removed metal elements from total elements: " + str(float(damagedEle_metal)/float(len(metalElset + polymerElset))*100.0) + " %")	
				damagedEle_polymer = 0
				if material == 'Composite':
					polymerStatus_Dict = {}
					damagedEle_polymer = 0
					damagePLocal = []
					for i in polymerElset:
						polymerStatus_Dict[i] = status_Dict[i]
						if status_Dict[i] == 0.0:
							damagedEle_polymer += 1
							locationx = sum([nodeDict[k][0] for k in polymerElsetICA[i]])/len(polymerElsetICA[i])
							locationy = sum([nodeDict[k][1] for k in polymerElsetICA[i]])/len(polymerElsetICA[i])
							damagePLocal.append([locationx,locationy])
							#print >> sys.__stdout__, ("Failure in polymer")
							#print >> sys.__stdout__, ("X: " + str(locationx) + "; Y: " +  str(locationy))
				print >> sys.__stdout__, (str(damagedEle_polymer) + " damaged polymer elements found \n")
					
				resultsFile.write(', '.join([str(j) for j in damagePLocal]) + '\n')	
				resultsFile.write(', '.join([str(j) for j in damageMLocal]) + '\n')	
			except:
				print >> sys.__stdout__, (cwd + odbname + " does not exist")
					
	resultsFile.close()
	odb.close()

#crackPropagation()
