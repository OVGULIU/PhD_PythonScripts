"""
Created on Mon Jun 18 11:50:52 2018
Script to run boundary conditiosn test cases (changing pkback and pkfront)

1) Write new props file 
3) Run new Abaqus simulation (wait till complete)

@author: cerecam
"""
    
import os
import time
import datetime

#PropsVals = [0, 0.1, 1, 100,-0.1, -1, -10, -100]
#FluxVals = [1.0E-5, 1.0E-4, 1.0E-3]
#PropsValsF = [-0.1,-0.25,-0.5]
#PropsValsB = [-0.1,-0.25,-0.5]

simulationtime = 100
PropsValsF = [-10.0]
# PropsValsB = [-10.0,-25.0]
FluxVals = ['1.0E-4']
InputFile = 'Voxel32_TEMPLATE.inp'
User = '/home/cerecam/Desktop/GIT/Abaqus_Subroutines/U3T8_Combined.f'

RunAbq = ('cd {} \nabaqus output_precision=FULL double=Both interactive ask_delete=NO ' 
          'input={} job={} user={}')
SuccessfulSims, UnsuccessfulSims = [], []
t0 = time.time()
newinp = []
prevline = ''
with open('/home/cerecam/Desktop/GP_BoundaryConditionTests/Voxel32_TEMPLATE.inp', 'r') as inpRead:
    for inpline in inpRead:
        if prevline == '*Dynamic Temperature-displacement, Explicit, ELEMENT BY ELEMENT\n':
            inpline = ' , {}\n'.format(simulationtime)
        elif inpline.split(',')[0] == '*Output':
            inpline = '*Output, field, time marks=NO, NUMBER INTERVAL={} \n'.format(int(simulationtime/2.5)
                                                                                    if int(simulationtime/2.5) < 50
                                                                                    else 50)
        newinp.append(inpline)
        prevline = inpline
with open('/home/cerecam/Desktop/GP_BoundaryConditionTests/Voxel32_TEMPLATE.inp', 'w') as inpWrite:
    for line in newinp:
        inpWrite.write(line)

# for valB in PropsValsB:
for valF in PropsValsF:
    for inFlux in FluxVals:
        cwd = '/home/cerecam/Desktop/GP_BoundaryConditionTests/'
        filename = cwd + 'InputFiles/Props1.inp'
        writef = open(filename, 'w')
        writef.write("1.951E+00, 0.3, 1.47E-02, 1.0E+03, 8.854E-03, 2.4331E+00, 9.6485337E+01, -1.0 \n")
        writef.write("5.0E+01, 1.0E-01, 0.0E-03, 0.0, 	0.0E-03,	{}, 	1, {} \n".format(inFlux, 1.0*valF))
        writef.write("{} \n".format(valF))
        writef.close()

        filename = cwd + 'InputFiles/Props2.inp'
        writef = open(filename, 'w')
        writef.write("77.71E+00, 0.44, 19.3E-02, {}, {},\n".format(-1.0*valF*2.0, valF*2.0))
        writef.close()

        Jobname = 'Voxel_stiff_both_negBack'
        start = time.time()
        os.system(f'rm {cwd+Jobname+".lck"}')
        result = os.system(RunAbq.format(cwd, InputFile, Jobname, User))
        LenSim = time.time() - start
        LenSim = str(datetime.timedelta(seconds=LenSim)).split(':')
        if result == 0:
            print('Simulation: {} COMPLETE'.format(Jobname))
            print('{} is complete in {} hours, {} minutes, {} seconds'.format(Jobname,
                                                                              LenSim[-3],
                                                                              LenSim[-2],
                                                                              LenSim[-1].strip('0')))
            SuccessfulSims.append(Jobname)
        else:
            UnsuccessfulSims.append(Jobname)
            print('Simulation: {} INCOMPLETE'.format(Jobname))
        print('_________________________________________________________________________')
print('{} successful simulations complete'.format(len(SuccessfulSims))) 
print('{} simulations were unsucessful'.format(len(UnsuccessfulSims)))
#print('Total time taken: {}'.format(time.time()-t0))
