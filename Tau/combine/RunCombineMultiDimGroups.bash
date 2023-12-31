#!/bin/bash
era=UL20${1}
WP=$2
folder=/afs/cern.ch/work/r/rasp/public/HighPT_ptbinned/datacards
cd ${folder}
# step 1
combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r_lowpt_${1},r_highpt_${1} --saveFitResult -d tauID_${WP}_${era}.root -n ".bestfit.singles" --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --saveWorkspace
# step 2
combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r_lowpt_${1},r_highpt_${1} --saveFitResult -d higgsCombine.bestfit.singles.MultiDimFit.mH200.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 -n ".bestfit.singles.postfit" --snapshotName MultiDimFit
# step 3
combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r_lowpt_${1},r_highpt_${1} --saveFitResult -d higgsCombine.bestfit.singles.MultiDimFit.mH200.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 -n ".bestfit.singles.postfit.byEras" --snapshotName MultiDimFit --freezeNuisanceGroups byEras
# step 4 
combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r_lowpt_${1},r_highpt_${1} --saveFitResult -d higgsCombine.bestfit.singles.MultiDimFit.mH200.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 -n ".bestfit.singles.postfit.byErasAndBins" --snapshotName MultiDimFit --freezeNuisanceGroups byErasAndBins
mv multidimfit.bestfit.singles.postfit.root multidim_${era}_${WP}.root
mv multidimfit.bestfit.singles.postfit.byEras.root multidim_${era}_${WP}_byEras.root
mv multidimfit.bestfit.singles.postfit.byErasAndBins.root multidim_${era}_${WP}_byErasAndBins.root
rm higgsCombine.*.root
cd -
