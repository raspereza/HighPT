#!/bin/bash
era=2023
WPvsJet=Medium
WPvsMu=Tight
WPvsE=Tight
folder=/afs/cern.ch/work/r/rasp/HighPT_${era}/datacards
name=${WPvsJet}_${WPvsMu}_${WPvsE}

cd ${folder}

combineCards.py munu_${era}.txt taunu_${name}_${era}.txt > tauID_${name}.txt 

combineTool.py -M T2W -o tauID_${name}.root -i tauID_${name}.txt

combineTool.py -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd ADDNLL_RECURSIVE=0 --X-rtd FITTER_NEW_CROSSING_ALGO --robustFit 1 --rMin 0 --rMax 3 -m 200 -d tauID_${name}.root --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy 1 

mv fitDiagnostics.Test.root tauID_${name}_fit.root

combineTool.py -M Impacts -d tauID_${name}.root --robustFit 1 --cminDefaultMinimizerTolerance 0.01 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 --doInitialFit -m 200
combineTool.py -M Impacts -d tauID_${name}.root --robustFit 1 --cminDefaultMinimizerTolerance 0.01 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 --doFits -m 200 
#--job-mode condor --sub-opts='+JobFlavour = "workday"' --merge 2 -m 200
combineTool.py -M Impacts -d tauID_${name}.root -o impacts_${name}.json -m 200
plotImpacts.py -i impacts_${name}.json -o impacts_${name}
cd -
