#!/bin/bash
WP=$1
WPvsMu=$2
WPvsE=$3
folder=/afs/cern.ch/work/r/rasp/public/HighPT_deepTauV2p5/datacards
cd ${folder}
rm munu_trig_UL2016.root 
hadd munu_trig_UL2016.root munu_trig_UL2016_preVFP.root munu_trig_UL2016_postVFP.root
cd ${folder}/${WPvsMu}VsMu_${WPvsE}VsE
for name in trig nottrig
do
    echo ${name}
    rm taunu_${WP}_${name}_UL2016.root
    hadd taunu_${WP}_${name}_UL2016.root taunu_${WP}_${name}_UL2016_preVFP.root taunu_${WP}_${name}_UL2016_postVFP.root
done
cd ${CMSSW_BASE}/src/TauFW/Plotter
./scripts/MergeTrig2016.py --WP ${WP} --WPvsMu ${WPvsMu} --WPvsE ${WPvsE}

