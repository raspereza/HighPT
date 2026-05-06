#!/bin/bash
era=$1
WPvsJet=$2
WPvsMu=$3
WPvsE=$4
poi=$5
wps=${WPvsJet}_${WPvsMu}_${WPvsE}

n=$#
if [[ $n -ne 5 ]]; then
    echo usage : RunImpactsMultiDim.bash [ERA] [WPvsJet] [WPvsMu] [WPvsE] [POI]
    echo ERA = [2024, 2025]
    echo WPvsJet = [Loose, Medium, Tight, VTight, VVTight]
    echo WPvsMu = [VLoose, Tight]
    echo WPvsE = [VVLoose, Tight]
    echo POI = [r_lowpt, r_mediumpt, r_highpt]
    exit
fi

folder=/afs/cern.ch/work/r/rasp/HighPT/${era}/datacards_comb_${wps}
cd ${folder}
rm higgsCombine*
name=tauID_pttau_comb_${wps}_ptbinned

# running impacts 
combineTool.py -M Impacts -d ${name}.root --robustFit 1 --redefineSignalPOIs ${poi} --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1 --doInitialFit -m 200
combineTool.py -M Impacts -d ${name}.root --robustFit 1 --redefineSignalPOIs ${poi} --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1  --doFits -m 200
combineTool.py -M Impacts -d ${name}.root --redefineSignalPOIs ${poi} -o impacts_${name}_${poi}.json -m 200
plotImpacts.py -i impacts_${name}_${poi}.json -o impacts_${name}_${poi}

cd -

