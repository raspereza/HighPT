#!/bin/bash

n=$#
if [[ $n -ne 5 ]]; then
    echo usage : RunFitTrigger.bash [ERA] [WPvsJet] [WPvsMu] [WPvsE] [TRG_OPT]
    echo ERA = [2024, 2025]
    echo WPvsJet = [Loose, Medium, Tight, VTight, VVTight]
    echo WPvsMu = [VLoose, Tight]
    echo WPvsE = [VVLoose, Tight]
    echo TRG_OPTION = [pnet, deeptau, comb]
    exit
fi


era=${1}
WP=${2}_${3}_${4} # {WPvsJet}_{WPvsMu}_{WPvsE}, e.g. Tight_Tight_Tight
opt=${5} # pnet, deeptau or comb
folder=/afs/cern.ch/work/r/rasp/HighPT/${era}/datacards
pwd
cd ${folder}

#combineCards.py ${folder}/munu_${era}.txt ${folder}/taunu_${WP}_trig.txt ${folder}/taunu_${WP}_nottrig.txt > ${folder}/tauTrigger_${WP}.txt
combineCards.py ${folder}/taunu_${WP}_trig.txt ${folder}/taunu_${WP}_${opt}_notrig.txt > ${folder}/tauTrigger_${WP}_${opt}.txt

datacards=tauTrigger_${WP}_${opt}
combineTool.py -M T2W -o "${datacards}.root" -i ${datacards}.txt -m 200

#echo '-----'
#combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r --saveFitResult -d ${datacards}.root -n ".tauTrig.singles" --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --saveWorkspace 
#mv fitDiagnosticsTest.root tauTrigger_${WP}_fit.root

#echo "-----"
#combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r --saveFitResult -d higgsCombine.tauTrig.singles.MultiDimFit.mH200.root -n ".tauTrig.singles.postfit" --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --snapshotName MultiDimFit --saveWorkspace

#combine -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd ADDNLL_RECURSIVE=0 --X-rtd FITTER_NEW_CROSSING_ALGO --robustFit 1 --rMin=0 --rMax=3 -m 200 -d higgsCombine.tauTrig.singles.postfit.MultiDimFit.mH200.root --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy=0 -v 5 --snapshotName MultiDimFit --freezeNuisanceGroups sysUnc
#mv fitDiagnosticsTest.root tauTrigger_${WP}_${era}_fitStat.root

combine -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --robustHesse 1 --rMin=0.5 --rMax=1.5 -m 200 -d ${datacards}.root --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy 0 -v 5 
mv fitDiagnosticsTest.root tauTrigger_${WP}_${opt}_fit.root

combine -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --robustFit 1 --rMin=0.5 --rMax=1.5 -m 200 -d ${datacards}.root --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy 1 -v 5 
mv fitDiagnosticsTest.root tauTrigger_${WP}_${opt}_robustfit.root

cd -
