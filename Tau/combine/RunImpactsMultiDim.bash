#!/bin/bash
WP=$1
subfolder=$2
poi=$3
folder=/afs/cern.ch/work/r/rasp/public/HighPT_deepTauV2p5/datacards
cd ${folder}/${subfolder}
echo $PWD
ls -ltr tauID_${WP}.root
#combineTool.py -M Impacts --redefineSignalPOIs ${poi} -d tauID_${WP}.root -m 200 --robustFit 1 --doInitialFit
#combineTool.py -M Impacts --redefineSignalPOIs ${poi} -d tauID_${WP}.root -m 200 --robustFit 1 --doFits
#combineTool.py -M Impacts --redefineSignalPOIs ${poi} -d tauID_${WP}.root -m 200 -o impacts_${WP}_${poi}.json
plotImpacts.py -i impacts_${WP}_${poi}.json -o impacts_${WP}_${poi}
cd -
