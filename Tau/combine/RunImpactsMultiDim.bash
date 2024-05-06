#!/bin/bash
era=$1
WPvsJet=$2
WPvsMu=$3
WPvsE=$4
# name=${WPvsJet}_${WPvsMu}_${WPvsE}
# Need to be changed ->
name=comb_${WPvsJet}_${WPvsMu}_${WPvsE}
    
folder=/eos/user/j/jmalvaso/HighPt/${era}/datacards_${name}

cd ${folder}

for poi in r_lowpt r_highpt
do
    combineTool.py -M Impacts -d tauID_pttau_${name}_ptbinned.root --robustFit 1 --redefineSignalPOIs ${poi} --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 --doInitialFit -m 200
    combineTool.py -M Impacts -d tauID_pttau_${name}_ptbinned.root --robustFit 1 --redefineSignalPOIs ${poi} --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1  --doFits -m 200
    combineTool.py -M Impacts -d tauID_pttau_${name}_ptbinned.root -o impacts_${name}_${poi}.json -m 200
    plotImpacts.py -i impacts_${name}_${poi}.json -o impacts_${name}_${poi}
done

cd -
