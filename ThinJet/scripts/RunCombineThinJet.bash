#!/bin/bash
era=$1
WP=$2
dm=$3
folder=${CMSSW_BASE}/src/HighPT/ThinJet/output/datacards/
cd ${folder}
if ! test -f munu_${era}.txt; then
    echo file munu_${era}.txt does not exist. 
    exit
fi
if ! test -f taunu_${WP}_${dm}_${era}.txt; then
    echo file taunu_${WP}_${dm}_${era}.txt does not exist. 
    exit
fi
if ! test -f taunu_${WP}_${dm}_${era}.root; then
    echo file taunu_${WP}_${dm}_${era}.root does not exist. 
    exit
fi
combineCards.py munu_${era}.txt taunu_${WP}_${dm}_${era}.txt > tauID_${WP}_${dm}_${era}.txt
combine -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd ADDNLL_RECURSIVE=0 --X-rtd FITTER_NEW_CROSSING_ALGO --robustFit 1 --rMin=0 --rMax=3 -m 200 tauID_${WP}_${dm}_${era}.txt --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy=0 -v 3

mv fitDiagnosticsTest.root tauID_${WP}_${dm}_${era}_fit.root

cd -
