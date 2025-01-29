#!/bin/bash
era=$1 # 2022 or 2023
WP=$2 # {WPvsJet}_{WPvsMu}_{WPvsE}, e.g. Tight_Tight_Tight
folder=/afs/cern.ch/work/r/rasp/HighPT/${era}/datacards
pwd
cd ${folder}

#combineCards.py ${folder}/munu_${era}.txt ${folder}/taunu_${WP}_trig.txt ${folder}/taunu_${WP}_nottrig.txt > ${folder}/tauTrigger_${WP}.txt
combineCards.py ${folder}/taunu_${WP}_trig.txt ${folder}/taunu_${WP}_notrig.txt > ${folder}/tauTrigger_${WP}.txt

datacards=tauTrigger_${WP}
combineTool.py -M T2W -o "${datacards}.root" -i ${datacards}.txt -m 200

#echo '-----'
#combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r --saveFitResult -d ${datacards}.root -n ".tauTrig.singles" --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --saveWorkspace 
#mv fitDiagnosticsTest.root tauTrigger_${WP}_fit.root

#echo "-----"
#combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r --saveFitResult -d higgsCombine.tauTrig.singles.MultiDimFit.mH200.root -n ".tauTrig.singles.postfit" --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --snapshotName MultiDimFit --saveWorkspace

#combine -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd ADDNLL_RECURSIVE=0 --X-rtd FITTER_NEW_CROSSING_ALGO --robustFit 1 --rMin=0 --rMax=3 -m 200 -d higgsCombine.tauTrig.singles.postfit.MultiDimFit.mH200.root --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy=0 -v 5 --snapshotName MultiDimFit --freezeNuisanceGroups sysUnc
#mv fitDiagnosticsTest.root tauTrigger_${WP}_${era}_fitStat.root

combine -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd ADDNLL_RECURSIVE=0 --X-rtd FITTER_NEW_CROSSING_ALGO --robustFit 1 --rMin=0.5 --rMax=1.5 -m 200 -d ${datacards}.root --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy=0 -v 5 
mv fitDiagnosticsTest.root tauTrigger_${WP}_fit.root

cd -
