#!/bin/bash
era=$1
WPvsJet=$2
WPvsMu=$3
WPvsE=$4
name=${WPvsJet}_${WPvsMu}_${WPvsE}

# Need to be changed ->
folder=/afs/cern.ch/work/r/rasp/HighPT/${era}/datacards
cd ${folder}

#combineCards.py munu_${era}.txt taunu_${name}_lowpt_${era}.txt taunu_${name}_highpt_${era}.txt > tauID_${name}_ptbinned.txt
#combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/*_highpt_${era}:r_highpt[1,0,2]"' --PO '"map=^.*/*_lowpt_${era}:r_lowpt[1,0,2]"' -o tauID_${name}_ptbinned.root -i tauID_${name}_ptbinned.txt 

# running impacts for low pt anf high pt bins
for poi in r_lowpt r_highpt
do
    combineTool.py -M Impacts -d tauID_${name}.root --robustFit 1 --redefineSignalPOIs ${poi} --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 --doInitialFit -m 200
    combineTool.py -M Impacts -d tauID_${name}.root --robustFit 1 --redefineSignalPOIs ${poi} --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1  --doFits -m 200
    combineTool.py -M Impacts -d tauID_${name}.root -o impacts_${name}_${poi}.json -m 200
    plotImpacts.py -i impacts_${name}.json -o impacts_${name}_${poi}
done

cd -
