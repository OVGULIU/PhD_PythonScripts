"""
Create restart file where inpits:
sys.argv[-1] = length fo simulation
sys.argv[-2] = step number
"""
import sys


cwd = '/home/grfemm002/UCT_hpc/2M_96x96x96_89_over_146/'
cwd = '/home/cerecam/'
stepNo = sys.argv[-2]
len_sim = sys.argv[-1]
fwrite = open(cwd +'Voxel_96_89_over_146_restart.inp','w')
fwrite.write(""" *Heading
**
*Restart, Read, STEP={}
**
*Preprint, echo=NO, model=NO, history=NO, contact=NO
*step, name=restart, nlgeom=YES
*Dynamic Temperature-displacement, Explicit, element by element
, {}
*Bulk Viscosity

0.6,1.2
** =============================================================================
** PRE-DEFINED FIELDS
** =============
**
*FIELD, VARIABLE=1, INPUT=/home/cerecam/Desktop/GP_BoundaryConditionTests/InputFiles/ElecPotentials.inp
**
** OUTPUT REQUESTS
**FIELD OUTPUT
**
*Output, field, time marks=YES, NUMBER INTERVAL=10
*Element Output
 LE
*Node Output
 NT, U
***Element Output
** S, LE, EVOL, FV
***Node Output
** NT, U, V, A
**
*Output, history
*Energy Output 
ALLKE, ALLIE, ALLAE, ALLHF, ALLIHE, ALLSE
*Energy Output
ALLWK, ETOTAL
*End Step
""".format(stepNo,len_sim))
fwrite.close()
