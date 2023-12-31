#!/bin/bash
folder=/afs/cern.ch/user/r/rasp/public/HighPT_pt/
cd ${folder}
for WPjet in LooseVsJet MediumVsJet TightVsJet VTightVsJet VVTightVsJet
do
    for WPe in VVLooseVsE TightVsE
    do
	hadd pT_${WPjet}_TightVsMu_${WPe}.root pT_${WPjet}_TightVsMu_${WPe}_UL2016_preVFP.root pT_${WPjet}_TightVsMu_${WPe}_UL2016_postVFP.root pT_${WPjet}_TightVsMu_${WPe}_UL2017.root pT_${WPjet}_TightVsMu_${WPe}_UL2018.root
    done
done
cd -
