#!/bin/bash
ulimit -s unlimited
era=2023
WPvsJet=Medium
WPvsMu=Tight
WPvsE=Tight
folder=/afs/cern.ch/work/r/rasp/HighPT_${era}/datacards
name=${WPvsJet}_${WPvsMu}_${WPvsE}
folder=/afs/cern.ch/work/r/rasp/HighPT_${era}/datacards
cd ${folder}
combineTool.py -m 125 -M MultiDimFit -P r --setParameterRanges r=0.5,1.5 --floatOtherPOIs 1 --points 51 --robustFit 1 -d tauID_${name}.root --algo grid --alignEdges 1 --cminDefaultMinimizerStrategy=0 -n _${name}
cd -
