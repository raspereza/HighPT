#!/bin/bash
era=$1
WP=$2
folder=/afs/cern.ch/work/r/rasp/public/HighPT_ptbinned/datacards
cd ${folder}
combineCards.py munu_${era}.txt taunu_${WP}_${era}_lowpt.txt taunu_${WP}_${era}_highpt.txt > tauID_${WP}_${era}.txt
cd -
