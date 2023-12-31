#! /usr/bin/env python
# Author: Alexei Raspereza (December 2022)
# High pT tau ID SF measurements 
# comparison between 
import ROOT
import TauFW.Plotter.HighPT.utilsHighPT as utils
from array import array
import math
import TauFW.Plotter.HighPT.stylesHighPT as styles
import os

binWP = {
    1: 'Loose',
    2: 'Medium',
    3: 'Tight',
    4: 'VTight',
    5: 'VVTight'
}

labelWP = {
    1: 'L',
    2: 'M',
    3: 'T',
    4: 'VT',
    5: 'VVT'
}

def plotComparison(h_v2p1,h_v2p5,era,WPvsMu,WPvsE,ptbin):
    
    styles.InitData(h_v2p1)
    styles.InitData(h_v2p5)

    h_v2p1.SetMarkerStyle(21)
    h_v2p1.SetMarkerColor(2)
    h_v2p1.SetLineColor(2)

    h_v2p1.GetYaxis().SetRangeUser(0.,1.5)
    h_v2p1.GetYaxis().SetTitle("tauID SF")

    h_v2p5.SetMarkerStyle(22)
    h_v2p5.SetMarkerColor(4)
    h_v2p5.SetLineColor(4)

    for ib in range(1,6):
        label = labelWP[ib]
        h_v2p1.GetXaxis().SetBinLabel(ib,label)

    # canvas 
    canv = styles.MakeCanvas("canv","",600,600)

    h_v2p1.Draw("e1")
    h_v2p5.Draw("e1same")

    leg = ROOT.TLegend(0.2,0.2,0.6,0.4)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.038)
    #    labelHeader = ptbin+'pt '+WPvsMu+'VSmu '+WPvsE+'VSe'
    labelHeader = ptbin+'pt '+WPvsMu+'VSmu VVLooseVSe'
    leg.SetHeader(labelHeader)
    leg.AddEntry(h_v2p1,'deepTau2017v2p1','lp')
    leg.AddEntry(h_v2p5,'deepTau2018v2p5','lp')
    leg.Draw()

    styles.CMS_label(canv,era=era)
    canv.Modified()
    canv.Update()
    canv.Print('/afs/cern.ch/user/r/rasp/public/highPT_comp/compDeepTau_'+era+'_'+ptbin+'_'+WPvsMu+'vsMu_'+WPvsE+'vsE.png')


############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-era','--era',dest='era',default='UL2018', help=""" Era : UL2016_preVFP, UL2016_postVFP, UL2017, UL2018 """)
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight', help=""" WP vs. mu : VLoose, Loose, Medium, Tight """)
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VLoose', help=""" WP vs. e : VLoose, Loose, Medium, Tight, VTight, VVTight """)
    parser.add_argument('-ptbin','--ptbin', dest='ptbin', default='high',help=""" pt bin : low, high """)

    args = parser.parse_args() 

    hist_v2p1 = ROOT.TH1D('hist_v2p1','',5,0.5,5.5)
    hist_v2p5 = ROOT.TH1D('hist_v2p5','',5,0.6,5.6)

    for ib in range(1,6):
        wp = binWP[ib]
        v2p1 = utils.tauID_sf[args.era+'_'+wp+'_'+args.wpVsMu+'_'+args.wpVsE]
        x = v2p1[args.ptbin]
        e = v2p1[args.ptbin+'_unc']
        hist_v2p1.SetBinContent(ib,x)
        hist_v2p1.SetBinError(ib,e)
        v2p5 = utils.tauID_sf_v2p5[args.era+'_'+wp+'_'+args.wpVsMu+'_'+args.wpVsE]
        x_v2p5 = v2p5[args.ptbin]
        e_v2p5 = v2p5[args.ptbin+'_unc']
        hist_v2p5.SetBinContent(ib,x_v2p5)
        hist_v2p5.SetBinError(ib,e_v2p5)


    plotComparison(hist_v2p1,hist_v2p5,args.era,args.wpVsMu,args.wpVsE,args.ptbin)
