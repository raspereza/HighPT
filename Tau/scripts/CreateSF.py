#!/usr/bin/env python3

import ROOT
from array import array

ROOT.gStyle.SetOptStat(0000)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# WPvsJet_WPvsMu_WPvsE
tauSFs = {
    'Medium_Tight_Tight' : {
        '2018_deepTauV2p1' : {'y' : [0.941,0.954], 'ey' : [0.087,0.112]},
        '2018_deepTauV2p5' : {'y' : [0.971,0.982], 'ey' : [0.085,0.091]},
        '2022_deepTauV2p1' : {'y' : [0.967,0.933], 'ey' : [0.082,0.122]},
        '2022_deepTauV2p5' : {'y' : [1.001,0.961], 'ey' : [0.078,0.114]}
    },
    'Medium_Tight_VVLoose' : {
        '2018_deepTauV2p1' : {'y' : [0.911,0.984], 'ey' : [0.095,0.106]},
        '2018_deepTauV2p5' : {'y' : [0.906,1.094], 'ey' : [0.111,0.103]},
        '2022_deepTauV2p1' : {'y' : [1.052,1.076], 'ey' : [0.076,0.133]},
        '2022_deepTauV2p5' : {'y' : [1.040,1.115], 'ey' : [0.071,0.128]}
    },

}

# pt bins central values
x = [145,250]
# lower error 
exl = [45,50]
# upper error
exh = [55,750]

graphs = {}
nbins = 2
frame = ROOT.TH2D('frame','',2,100,1000.1,2,0.5,1.5)
frame.GetXaxis().SetTitle('tau p_{T} (GeV)')
frame.GetYaxis().SetTitle('SF')
frame.GetXaxis().SetNdivisions(505)
frame.GetXaxis().SetMoreLogLabels()
frame.GetXaxis().SetNoExponent()
outputFile = ROOT.TFile('HighPT_TauSF.root','recreate')

for WorkingPoint in tauSFs:
    tauSF_WP = tauSFs[WorkingPoint]
    for era_version in tauSF_WP:
        meas = tauSF_WP[era_version]
        y = meas['y']
        ey = meas['ey']
        graph  = ROOT.TGraphAsymmErrors(nbins,
                                        array('d',list(x)),
				        array('d',list(y)),
                                        array('d',list(exl)),
                                        array('d',list(exh)),
				        array('d',list(ey)),
                                        array('d',list(ey)))
        graph.SetMarkerStyle(20)
        name = f'{WorkingPoint}_{era_version}'
        canv = ROOT.TCanvas(name,'',500,500)
        frame.Draw()
        graph.Draw('pe1same')
        canv.SetLogx(True)
        canv.Update()
        canv.Print(f'{name}.pdf')
        outputFile.cd('')
        graph.Write(f'{name}')

outputFile.Close()




