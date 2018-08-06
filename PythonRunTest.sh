currentwd='/home/cerecam/Desktop/GP_BoundaryConditionTests'
ExplicitSim='Full_coupled_2000'
StandardSim='Voxel32_Standard'
echo $ExplicitSim
echo $StandardSim
#echo ""
echo "	Extracting concentrations from ${currentwd}/$ExplicitSim"
#echo ""
abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PythonScripts/ExtractFieldvariableAE_2_AS.py -- $currentwd $ExplicitSim
#echo ""
echo "------------------------------- DONE -------------------------------" 
echo "	Running AS"
#echo ""
cd $currentwd
abaqus job=$StandardSim User=/home/cerecam/Desktop/GIT/Abaqus_Subroutines/U1T8.f double=both output_precision=full ask_delete=NO interactive
cp "${StandardSim}.odb" "${StandardSim}_tmp.odb"
#cd
#echo ""
echo "------------------------------- DONE -------------------------------" 
#echo ""
echo "		Extracting elec potentials from  ${currentwd}/$StandardSim"
#echo ""
abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PythonScripts/ExtractFieldvariableCSV.py  -- $currentwd $StandardSim
#echo ""
echo "------------------------------- DONE -------------------------------" 
# sleep 5s
