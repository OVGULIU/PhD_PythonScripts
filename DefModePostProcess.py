'''
Data analysis of ligaments stress ditribution

===================================================================================
abaqus viewer noGUI=/home/cerecam/Dropbox/Masters/PythonCodes/DefModePostProcess.py
===================================================================================
'''

def mag(x): 
    return math.sqrt(sum(i**2 for i in x))

def dot_product(x, y):
    return np.dot(x,y)

def norm(x):
    return math.sqrt(dot_product(x, x))

def normalize(x):
    return [x[i] / norm(x) for i in range(len(x))]

def writeFile(Data,filename,FirstLine):
    with open('/home/cerecam/Documents/NpgRVE/Results/'+odbname[0:3]+'_'+odbname[-1]+'_'+ligamentname+filename+'.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(FirstLine)
        for key, value in Data.items():
                writer.writerow([key, value])

def BM(Q):
    BendingMoment = {}
    RotatedVal = {}
    BM_3D = [0,0]
    for key,value in normals.items():
            Val = np.dot(Q,np.array(COORD_e[int(key)-1]))
            RotatedVal[key] = Val[0:2]
            RotCentroid = np.dot(Q,np.array(Centroid))
            RotCentroid = RotCentroid[0:2]
##            abqPrint(RotCentroid)
##            abqPrint(RotatedVal)
            BendingMoment[key] = (normalvec[key]*Area[key]*(RotatedVal[key]-RotCentroid))
            BM_3D = BM_3D + (normalvec[key]*Area[key]*(RotatedVal[key]-RotCentroid))       
    return BendingMoment,RotatedVal,BM_3D



from odbAccess import openOdb
from open import abaqusopen
import numpy as np
from log import abqPrint
import csv,math
from abaqusConstants import *
from math import pi

global normals
global Area
global normalvec
global shearstress
global FO
global angle
global ligamentname
global centroid
global odbname

surfaces = {'F1': [1,2,3],'F2': [1,2,4],'F3': [2,3,4],'F4': [1,3,4]}
axis = {'0':'X','1':'Y','2':'Z'}

odbname = 'PBCCompositeZ'
instancename = 'RVE'
ligvals = open('/home/cerecam/Dropbox/Masters/PythonCodes/LigamentLocals.txt','r')
results = open('/home/cerecam/Dropbox/Masters/Results/LigamentResults'+odbname[0:3]+'_'+odbname[-1]+'.txt','w')
ligfile = ligvals.read()
ligfile = ligfile.split('\n')

for ligamentnumber in range(1,11):
    Norm = {}
    Coordnode = {}
    normals = {}
    Area = {}
    Centroid = []
    Rotation = {}
    Ligament_elements = []
    stresstens = {}
    tractionvec = {}

    ligamentname = 'Ligament'+str(ligamentnumber)
    Norm[ligamentname] = [0,0,1]
    #Get abaqus objects
    
    #-------------------------------------------------------------------------------------------------------------
    # EXTRACTION OF DATA FROM ABAQUS
    #-------------------------------------------------------------------------------------------------------------
    [ods,steps,frames,FO] = abaqusopen(odbname)
    myinstance = ods.rootAssembly.instances[instancename]

    #Reading in file/data containing 3 points to use to craete a co-ord system that is ~lying on the cross section of given ligament.
    for value in range(0,len(ligfile),5):
        if ligfile[value].upper() == ligamentname.upper():
            abqPrint(ligfile[value].upper() )
            origin = int(ligfile[value+1][7:].strip())
            point1 = int(ligfile[value+2][7:].strip())
            point2 = int(ligfile[value+3][7:].strip())

    #Setting up new coord system and getting Transformed data (Sress, strain and Coords)
    NODEorigin=tuple(ods.rootAssembly.instances[instancename].nodes[origin-1].coordinates)
    NODEpoint1=tuple(ods.rootAssembly.instances[instancename].nodes[point1-1].coordinates)
    NODEpoint2=tuple(ods.rootAssembly.instances[instancename].nodes[point2-1].coordinates)
    NEWCSYS = ods.rootAssembly.DatumCsysByThreePoints(name = 'NEW', coordSysType = CARTESIAN,origin = NODEorigin,point1=NODEpoint1,point2=NODEpoint2) #New co-ord system
    frame_val = ods.steps['QUASI_STATIC_LOADING'].frames[-1]
    # Field values (stress,strain,co-ordinates) re: new co-ord system
    FO_E = frame_val.fieldOutputs['E'].getTransformedField(NEWCSYS)
    E = [ E_val.data for E_val in FO_E.values]
    FO_S = frame_val.fieldOutputs['S'].getTransformedField(NEWCSYS)
    S = [ S_val.data for S_val in FO_S.values]
    FO_COORD = frame_val.fieldOutputs['COORD'].getTransformedField(NEWCSYS)
    COORD = [ COORD_val.data for COORD_val in FO_COORD.values]
    COORD_e = COORD[0:437913] #Co-ordinates of the centroid of all the elements
    COORD_n = COORD[437916:] # Co-ordinates of each node point in the mesh

    #Reading in file containing list of elements and the faces corresponding to the selected ligament cross section
    with open('/home/cerecam/Documents/NpgRVE/Results'+'/'+ligamentname.upper()+'faces'+'.csv', 'rb') as csv_file:
        readertwo = csv.reader(csv_file)
        myface = dict(readertwo)
        
    for key,value in myface.items():
        Ligament_elements.append(key)
        
    X = [COORD_e[int(i)-1][0] for i in Ligament_elements]
    X = np.sort(X)
    Y = [COORD_e[int(i)-1][1] for i in Ligament_elements]
    Y = np.sort(Y)
    Z = [COORD_e[int(i)-1][2] for i in Ligament_elements]
    Z = np.sort(Z)

    Xmin = X[0]
    Xmax = X[-1]
    Ymin = Y[0]
    Ymax = Y[-1]
    Zmin = Z[0]
    Zmax = Z[-1]

    #Calculating centroid of ligamnet cross section
    Centroid.append(Xmin+ ((Xmax-Xmin)/2))
    Centroid.append(Ymin +((Ymax-Ymin)/2))
    Centroid.append(Zmin +((Zmax-Zmin)/2))

    # Get elements on cross section of interest from save file (ligamentname+'faces.csv')
    normals2 = {}
    Area2 = {}
    for i in Ligament_elements:
        #Gets the connected nodes associated with required elements specified by the file ("ligamentname"+faces.csv)
        ConnectedNodes = myinstance.elements[int(i)-1]
        Ele_node_coords = []
        Ele_coords = []
        # Gets the co-ordinates of each node within those elements specified by the file ("ligamentname"+faces.csv)
        [Ele_node_coords.append(COORD_n[int(p)-1]) for p in ConnectedNodes.connectivity]
        eleNormal = {}
        FaceArea = {}
        # Calculation of normals and area of all surfaces
        for key,value in surfaces.items():
            if key == myface[i]:
                surfacevec = []
                surfacevec.append(Ele_node_coords[value[0]-1]-Ele_node_coords[value[1]-1]) #Vector1 in-plane
                surfacevec.append(Ele_node_coords[value[0]-1]-Ele_node_coords[value[2]-1]) #Vector2 in-plane
                normaldir = np.cross(surfacevec[0],surfacevec[1])   #Vector perpendicular too both vec1 and vec2 (i.e normal to plane)
                number = Norm[ligamentname].index(1)
                if float(normaldir[number]) <0: #Ensures all normals are outward pointing
                    normaldir = [float(x)*-1 for x in normaldir]
                normalmag = np.array(norm(normaldir))
                normals[i]= np.array([float(m)/normalmag for m in normaldir])   #Calculation of unit normal
                Area[i]= normalmag/2
                
    #----------------------------------- TRACTION VECTOR [MPa] --------------------------------------------------
    #Calculation of traction vector at each element centroid
    for key, value in normals.items():
        S_ele = S[int(key)-1]
        stresstens[key] = np.array([[S_ele[0],S_ele[3],S_ele[4]],[S_ele[3],S_ele[1],S_ele[5]],[S_ele[4],S_ele[5],S_ele[2]]])
        tractionvec[key] = np.dot(stresstens[key],normals[key]).T

    #----------------------------------- NORMAL VECTOR TO PLANE [MPa] -------------------------------------------
    #Calculation of normal vector magnitude
    normalvec = {}
    N = Norm[ligamentname]
    for key, value in tractionvec.items():
        normalvec[key] = np.dot(value,N).T
    
    #----------------------------------- UNIT SHEAR VECTOR ON PLANE [MPa]-------------------------------------------
    # Calculation of shear stress vector (direction)
    unitshearvec = {}
    for key,value in tractionvec.items():
        d = np.dot(value,N)/norm(N)
        p = np.array(d)*np.array(normalize(N))
        ShearMag = np.array(norm(value-p))
        unitshearvec[key] = np.array([i/ShearMag for i in (value-p)])

    #----------------------------------- SHEAR VECTOR ON PLANE [MPa]-------------------------------------------
    # Calculates Shear vector
    shearstress = {}
    for key, value in tractionvec.items():
            shearstress[key] = np.dot(value,unitshearvec[key]).T
            if Rotation[key]<0:
                shearstress[key] = shearstress[key]*-1
        
    #--------------------------CALCULATE BENDING MOMENT-------------------------------------------------------
    #First testing at various angles to get maximum
    BM_Rot = {}
    maxBM = {}
    for angledeg in range(0,180,30):
        angle= angledeg*(pi/180)
        Q = [[math.cos(angle), math.sin(angle),0],[-math.sin(angle), math.cos(angle),0],[0, 0, 1]]
        _,_,BM_3D = BM(Q)
        BM_Rot[str(angle)] = BM_3D
        maxBM[str(angle)] = [np.amax(abs(BM_3D)),np.argmax(abs(BM_3D))]

    AngleBM = max(maxBM, key=lambda i:maxBM[i]) #Calculation at what angle gave the maximum bending moment
    angle= float(AngleBM)
    Q = [[math.cos(angle), math.sin(angle),0],[-math.sin(angle), math.cos(angle),0],[0, 0, 1]]
            
    BMmatrix,Val,_ = BM(Q)  #Calculation of max BM

    Bmaxis = [values[maxBM[AngleBM][1]] for values in BMmatrix.values()]

    with open('/home/cerecam/Documents/NpgRVE/Results/BendingResults/'+ligamentname+'Bending'+axis[str(maxBM[AngleBM][1])]+odbname[0:3]+'_'+odbname[-1]+ '.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([BM_3D[maxBM[AngleBM][1]],angle])
        for x,key in enumerate(BMmatrix):
            writer.writerow([key,Bmaxis[x],normalvec[key] ,Val[key][0],Val[key][1]])
            
    abqPrint('Bending Moment: ' + str(BM_3D[maxBM[AngleBM][1]]) + ' at angle: '+ str(float(AngleBM)*180/pi))        


    # --------------------------------------CACLUATION OF TORQUE ---------------------------------------------
    # Shear vector X perpendicular vector from centroid to shear vector
    Torque = {}
    PerpenVec = {}
    PXint = {}
    A = {}
    for key,value in normals.items():
        #Calculations to calculate magnitude and direction of vector perpendicular to shear vector from the centroid of the ligament
        Val= np.array(COORD_e[int(key)-1])
        PerpenPoint = Val +(np.dot((Centroid-Val),unitshearvec[key]))*unitshearvec[key]
        Vector = PerpenPoint-Centroid
        VecMag = np.array(norm(Vector))
        PerpenVec[key] = [i/VecMag for i in Vector]
        A[key] = PerpenPoint+1000*unitshearvec[key]
        PAint = (A[key]-Centroid)
        PAmag = np.array(norm(PAint))
        PA = np.array([(A[key][i]-Centroid[i])/PAmag for i in range(len(A[key]))])
        PXint[key] = PerpenPoint-Centroid
        PXmag = np.array(norm(PXint[key]))
        PX = np.array([PXint[key][i]/PXmag for i in range(len(A[key]))])
        angle = np.cross(PA,PX)
        number = Norm[ligamentname].index(1)
        if angle[number] >0:
                sign = 1
        else:
                sign =-1
        Rotation[key] = sign

    #---------------------CALCULATOIN OF TOTAL: BENDING MOMENT, TORQUE, NORMAL FORCE, SHEAR FORCE ----------------------
    # Torque
    Torque = 0
    for key,value in shearstress.items():
            Torque = Torque+(value*Area[key]*np.array(norm(PXint[key])))
    abqPrint('Torque '+str(Torque))

    
    # Shear Stress
    Shear= 0
    for key,value in shearstress.items():
        ShearForce = ShearForce+value*Area[key]
    abqPrint('Shear '+ str(ShearForce))

    # Normal Stress
    NormalForce= 0
    for key,value in normalvec.items():
        NormalForce = NormalForce+value*Area[key]
    abqPrint('Normal stress '+ str(NormalForce))

    # Tot Area of cross section
    AreaTot= 0
    for key,value in Area.items():
        AreaTot = AreaTot+value

    #------------------------------------- WRITE RESULTS TO FILES -----------------------------------------------------
    #Write results to files as specified by string     
    writeFile(shearstress,'ShearStress',[ShearForce])
    writeFile(normalvec,'NormalVector',[NormalForce])
    writeFile(unitshearvec,'ShearVector',[Torque])
    writeFile(tractionvec,'TractionVector',[])
##    writeFile(Area,'Areas',[AreaTot])
    abqPrint('\n')

    #Write results to general ligament data file (all summarized data of all ligaments)
    results.write(ligamentname+'\n')
    results.write('Bending Moment: ' + str(BM_3D[maxBM[AngleBM][1]]) + ' at angle: '+ str(float(AngleBM)*180/pi)+'\n')
    results.write('Torque '+str(Torque)+'\n')
    results.write('Normal stress '+ str(NormalForce)+'\n')
    results.write('Shear '+ str(ShearForce)+'\n')
    results.write('Area '+ str(AreaTot)+'\n')
    results.write('\n')
