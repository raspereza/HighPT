#!/bin/bash
datacards=$1
subfolder=$2
dir=/afs/cern.ch/work/r/rasp/public/HighPT_deepTauV2p5/datacards
cd ${dir}/${subfolder}
combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO 'map=.*/*_highpt_UL2016_preVFP:r_highpt_16APV[1,0,2]' --PO 'map=.*/*_lowpt_UL2016_preVFP:r_lowpt_16APV[1,0,2]' --PO 'map=.*/*_highpt_UL2016_postVFP:r_highpt_16[1,0,2]' --PO 'map=.*/*_lowpt_UL2016_postVFP:r_lowpt_16[1,0,2]' --PO 'map=.*/*_highpt_UL2017:r_highpt_17[1,0,2]' --PO 'map=.*/*_lowpt_UL2017:r_lowpt_17[1,0,2]' --PO 'map=.*/*_highpt_UL2018:r_highpt_18[1,0,2]' --PO 'map=.*/*_lowpt_UL2018:r_lowpt_18[1,0,2]' -o "${datacards}.root" -i ${datacards}.txt -m 200
cd -
