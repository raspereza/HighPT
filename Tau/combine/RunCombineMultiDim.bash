#!/bin/bash
WP=$1
subfolder=$2
folder=/afs/cern.ch/work/r/rasp/public/HighPT_deepTauV2p5/datacards
cd ${folder}/${subfolder}
combine -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --redefineSignalPOIs r_lowpt_16APV,r_highpt_16APV,r_lowpt_16,r_highpt_16,r_lowpt_17,r_highpt_17,r_lowpt_18,r_highpt_18 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd ADDNLL_RECURSIVE=0 --X-rtd FITTER_NEW_CROSSING_ALGO --robustFit 1 -m 200 -d tauID_${WP}.root --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy=0 -v 3
mv fitDiagnosticsTest.root tauID_${WP}_multidim.root

cd -
