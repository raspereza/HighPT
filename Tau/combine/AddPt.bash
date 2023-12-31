#!/bin/bash
folder=/afs/cern.ch/user/r/rasp/public/HighPT_deepTauV2p5/PT
cd $folder
# pT_MediumVsJet_TightVsMu_TightVsE_UL2017.root
for wplep in TightVsMu_VVLooseVsE TightVsMu_TightVsE
do
    for wp in MediumVsJet
    do
	echo "++++"
	rm pT_${wp}_${wplep}_Run2.root 
	hadd pT_${wp}_${wplep}_Run2.root pT_${wp}_${wplep}_UL2016_preVFP.root pT_${wp}_${wplep}_UL2016_postVFP.root pT_${wp}_${wplep}_UL2017.root pT_${wp}_${wplep}_UL2018.root
    done
    for wp in LooseVsJet MediumVsJet TightVsJet VTightVsJet VVTightVsJet
    do
	echo "++++"
	rm pT_${wp}_${wplep}_Run2_corrected.root 
	hadd pT_${wp}_${wplep}_Run2_corrected.root pT_${wp}_${wplep}_UL2016_preVFP_corrected.root pT_${wp}_${wplep}_UL2016_postVFP_corrected.root pT_${wp}_${wplep}_UL2017_corrected.root pT_${wp}_${wplep}_UL2018_corrected.root	
    done
done
cd -
