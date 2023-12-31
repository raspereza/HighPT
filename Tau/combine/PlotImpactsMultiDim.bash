#!/bin/bash
datacards=$1
poi=$2
folder=/afs/cern.ch/work/r/rasp/public/HighPT_ptbinned/datacards
cd ${folder}
plotImpacts.py -i impacts_${datacards}_${poi}.json -o impacts_${datacards}_${poi}
cd -
