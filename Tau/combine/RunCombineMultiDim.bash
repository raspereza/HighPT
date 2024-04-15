#!/bin/bash
era=$1
WPvsJet=$2
WPvsMu=$3
WPvsE=$4
name=${WPvsJet}_${WPvsMu}_${WPvsE}
folder=/afs/cern.ch/work/r/rasp/HighPT/${era}/datacards
cd ${folder}
combineCards.py munu_${era}.txt taunu_${name}_lowpt_${era}.txt taunu_${name}_highpt_${era}.txt > tauID_${name}_ptbinned.txt

combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/*_highpt_${era}:r_highpt[1,0,2]"' --PO '"map=^.*/*_lowpt_${era}:r_lowpt[1,0,2]"' -o tauID_${name}_ptbinned.root -i tauID_${name}_ptbinned.txt 

combineTool.py -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --redefineSignalPOIs r_lowpt,r_highpt --robustFit 1 -m 200 -d tauID_${name}_ptbinned.root --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1 -v 2

mv fitDiagnostics.Test.root tauID_${name}_ptbinned_fit.root
rm higgsCombine*

cd -
