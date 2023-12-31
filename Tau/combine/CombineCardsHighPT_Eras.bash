#!/bin/bash
WP=$1
subfolder=$2
folder=/afs/cern.ch/work/r/rasp/public/HighPT_deepTauV2p5/datacards
cd ${folder}
cp munu* ${subfolder}
cd ${subfolder}
combineCards.py munu_UL2016_preVFP.txt taunu_${WP}_UL2016_preVFP_lowpt.txt taunu_${WP}_UL2016_preVFP_highpt.txt munu_UL2016_postVFP.txt taunu_${WP}_UL2016_postVFP_lowpt.txt taunu_${WP}_UL2016_postVFP_highpt.txt munu_UL2017.txt taunu_${WP}_UL2017_lowpt.txt taunu_${WP}_UL2017_highpt.txt munu_UL2018.txt taunu_${WP}_UL2018_lowpt.txt taunu_${WP}_UL2018_highpt.txt > tauID_${WP}.txt
cd -
