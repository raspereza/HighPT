#!/bin/bash
era=$1
WPvsJet=$2
WPvsMu=$3
WPvsE=$4
wps=${WPvsJet}_${WPvsMu}_${WPvsE}

# Need to be changed ->
folder=/afs/cern.ch/work/r/rasp/HighPT/${era}/datacards_comb_${wps}
cd ${folder}
name=tauID_pttau_comb_${wps}

# running impacts for low pt anf high pt bins
combineTool.py -M Impacts -d ${name}.root --robustFit 1 --redefineSignalPOIs r --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1 --doInitialFit -m 200
combineTool.py -M Impacts -d ${name}.root --robustFit 1 --redefineSignalPOIs r --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1  --doFits -m 200
combineTool.py -M Impacts -d ${name}.root -o impacts_${name}_incl.json -m 200
plotImpacts.py -i impacts_${name}_incl.json -o impacts_${name}_incl

cd -

