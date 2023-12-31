#!/bin/bash
WP=$1
subdolder=$2
folder=/afs/cern.ch/work/r/rasp/public/HighPT_deepTauV2p5/datacards
cd ${folder}/${subdolder}

# step 1
combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r_lowpt_16APV,r_highpt_16APV,r_lowpt_16,r_highpt_16,r_lowpt_17,r_highpt_17,r_lowpt_18,r_highpt_18 --saveFitResult -d tauID_${WP}.root -n ".bestfit.singles" --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --saveWorkspace
# step 2
combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r_lowpt_16APV,r_highpt_16APV,r_lowpt_16,r_highpt_16,r_lowpt_17,r_highpt_17,r_lowpt_18,r_highpt_18 --saveFitResult -d higgsCombine.bestfit.singles.MultiDimFit.mH200.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 -n ".bestfit.singles.postfit" --snapshotName MultiDimFit
# step 3
combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r_lowpt_16APV,r_highpt_16APV,r_lowpt_16,r_highpt_16,r_lowpt_17,r_highpt_17,r_lowpt_18,r_highpt_18 --saveFitResult -d higgsCombine.bestfit.singles.MultiDimFit.mH200.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 -n ".bestfit.singles.postfit.byEras" --snapshotName MultiDimFit --freezeNuisanceGroups byEras
# step 4 
combineTool.py -m 200 -M MultiDimFit --redefineSignalPOIs r_lowpt_16APV,r_highpt_16APV,r_lowpt_16,r_highpt_16,r_lowpt_17,r_highpt_17,r_lowpt_18,r_highpt_18 --saveFitResult -d higgsCombine.bestfit.singles.MultiDimFit.mH200.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 -n ".bestfit.singles.postfit.byErasAndBins" --snapshotName MultiDimFit --freezeNuisanceGroups byErasAndBins
mv multidimfit.bestfit.singles.postfit.root multidim_${WP}.root
mv multidimfit.bestfit.singles.postfit.byEras.root multidim_${WP}_byEras.root
mv multidimfit.bestfit.singles.postfit.byErasAndBins.root multidim_${WP}_byErasAndBins.root
rm higgsCombine.*.root
cd -
