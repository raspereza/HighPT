#!/bin/bash
era=$1
WPvsJet=$2
WPvsMu=$3
WPvsE=$4
folder=/afs/cern.ch/work/r/rasp/HighPT/${era}/datacards
name=${WPvsJet}_${WPvsMu}_${WPvsE}

cd ${folder}
# combine W*->mu+v and W*->tau+v cards
combineCards.py munu_${era}.txt taunu_${name}_${era}.txt > tauID_${name}.txt 
# creating workspace
combineTool.py -M T2W -o tauID_${name}.root -i tauID_${name}.txt
# doing fit
combineTool.py -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --robustFit 1 --rMin 0 --rMax 3 -m 200 -d tauID_${name}.root --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1 -v 2
# renaming output
mv fitDiagnostics.Test.root tauID_${name}_fit.root
# running impacts
#combineTool.py -M Impacts -d tauID_${name}.root --robustFit 1 --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 --doInitialFit -m 200
#combineTool.py -M Impacts -d tauID_${name}.root --robustFit 1 --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 --doFits -m 200 
# plotting impacts
#combineTool.py -M Impacts -d tauID_${name}.root -o impacts_${name}.json -m 200
#plotImpacts.py -i impacts_${name}.json -o impacts_${name}
echo leaving folder ${folder}
cd -
