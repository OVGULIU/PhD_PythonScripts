currentwd='/home/cerecam/Desktop/MesoporousSilica/Short/Coupled_Flux'
#echo ""
echo "	Extracting concentrations from AE"
#echo ""
abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PythonScripts/ExtractFieldvariableAE_2_AS.py -- $currentwd 'Short_coupled_NoElecFlux'
#echo ""
echo "------------------------------- DONE -------------------------------" 
echo "	Running AS"
#echo ""
cd $currentwd
abaqus job=Short_Standard User=/home/cerecam/Desktop/GIT/Abaqus_Subroutines/U1T4_robin.f double=both output_precision=full ask_delete=NO interactive
cp Short_Standard.odb Short_Standard_tmp.odb
#cd
#echo ""
echo "------------------------------- DONE -------------------------------" 
#echo ""
echo "		Extracting elec potentials from AS"
#echo ""
abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PythonScripts/ExtractFieldvariableCSV.py  -- $currentwd
#echo ""
echo "------------------------------- DONE -------------------------------" 
# sleep 5s
