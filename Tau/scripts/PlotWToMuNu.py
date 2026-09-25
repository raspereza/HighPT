#! /usr/bin/env python3
# Author: Alexei Raspereza (December 2022)
# High pT tau ID efficiency measurements 
# Plotting macro: control region (W*->mu+v) 
import ROOT
import HighPT.Tau.utilsHighPT as utils
from array import array
import math
import HighPT.Tau.stylesHighPT as styles
import os

##########################
# Plotting distributions #
##########################
def Plot(h_data_input,h_tot_input,h_bkg_input,h_sig_input,era,var,postFit):

    h_data = h_data_input.Clone("data")
    h_sig = h_sig_input.Clone("signal")
    h_bkg = h_bkg_input.Clone("background")
    h_tot = h_tot_input.Clone("total")
    styles.InitData(h_data)
    styles.InitHist(h_bkg,"","",ROOT.TColor.GetColor("#6F2D35"),1001)
    styles.InitHist(h_sig,"","",ROOT.TColor.GetColor("#FFCC66"),1001)

    h_sig.Add(h_sig,h_bkg,1.,1.)
    styles.InitTotalHist(h_tot)

    h_ratio = utils.histoRatio(h_data,h_tot,'ratio')
    h_tot_ratio = utils.createUnitHisto(h_tot,'tot_ratio')

    styles.InitRatioHist(h_ratio)
    h_ratio.GetYaxis().SetRangeUser(0.801,1.199)
    
    utils.zeroBinErrors(h_sig)
    utils.zeroBinErrors(h_bkg)

    ymax = h_data.GetMaximum()
    if h_tot.GetMaximum()>ymax: ymax = h_tot.GetMaximum()

    h_data.GetYaxis().SetRangeUser(0.,1.2*ymax)
    h_data.GetXaxis().SetLabelSize(0)
    h_data.GetYaxis().SetTitle("events / bin")
    h_ratio.GetYaxis().SetTitle("obs/exp")
    h_ratio.GetXaxis().SetTitle(utils.XTitle[var])

    # canvas and pads
    canvas = styles.MakeCanvas("canv","",600,700)
    # upper pad
    upper = ROOT.TPad("upper", "pad",0,0.31,1,1)
    upper.Draw()
    upper.cd()
    styles.InitUpperPad(upper)    
    
    h_data.Draw('e1')
    h_sig.Draw('hsame')
    h_bkg.Draw('hsame')
    h_data.Draw('e1same')
    h_tot.Draw('e2same')

    leg = ROOT.TLegend(0.5,0.4,0.8,0.7)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.047)
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_sig,'W#rightarrow #mu#nu','f')
    leg.AddEntry(h_bkg,'bkg','f')
    leg.Draw()

    styles.CMS_label(upper,era=era)

    upper.Draw("SAME")
    upper.RedrawAxis()
    upper.Modified()
    upper.Update()
    canvas.cd()

    # lower pad
    lower = ROOT.TPad("lower", "pad",0,0,1,0.30)
    lower.Draw()
    lower.cd()
    styles.InitLowerPad(lower)

    h_ratio.Draw('e1')
    h_tot_ratio.Draw('e2same')
    h_ratio.Draw('e1same')
    nbins = h_ratio.GetNbinsX()
    xmin = h_ratio.GetXaxis().GetBinLowEdge(1)    
    xmax = h_ratio.GetXaxis().GetBinLowEdge(nbins+1)
    line = ROOT.TLine(xmin,1.,xmax,1.)
    line.SetLineStyle(1)
    line.SetLineWidth(2)
    line.SetLineColor(4)
    line.Draw()
    lower.Modified()
    lower.RedrawAxis()

    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    print
    print('Creating control plot')
    if postFit:
        canvas.Print(utils.baseFolder+"/"+era+"/figures/WMuNu/wmunu_"+era+"_postFit.png")
    else:
        canvas.Print(utils.baseFolder+"/"+era+"/figures/WMuNu/wmunu_"+era+"_preFit.png")

############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='2024', choices=['UL2016','UL2017','UL2018','2022','2023','2024'])
    parser.add_argument('-wp','--WP', dest='wp', default='Medium',choices=['Loose','Medium','Tight'])
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight',choices=['VLoose','Tight'])
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VVLoose',choices=['VVLoose','Tight'])
    parser.add_argument('-var','--variable', dest='variable', default='mt_1')
    parser.add_argument('-post','--postfit',dest='postfit',action='store_true')
    parser.add_argument('-ff_par','--ff_par',dest='ff_par',default='pttau',choices=['pttau','ptjet'])
    parser.add_argument('-ff','--fake_factors',dest='ff',default='comb',choices=['comb','wjets','dijets'])
    parser.add_argument('-m','--meas',dest='meas',default='ptbinned',choices=['incl','ptbinned'])

    args = parser.parse_args()

    fullpathFit = '%s/%s/datacards_%s_%s_%s_%s/'%(utils.baseFolder,args.era,args.ff,args.wp,args.wpVsMu,args.wpVsE)
    filenameCards = '%s/%s/datacards_munu/munu_%s.root'%(utils.baseFolder,args.era,args.era)
    suffixFit = 'ptbinned'
    filenameFit = '%s/tauID_%s_%s_%s_%s_%s_%s_fit.root'%(fullpathFit,args.ff_par,args.ff,args.wp,args.wpVsMu,args.wpVsE,args.meas)
    fileFit = ROOT.TFile(filenameFit,"read")
    fileCards = ROOT.TFile(filenameCards,"read")

    folder='shapes_prefit'
    if args.postfit:
        folder='shapes_fit_s'

    h_data = fileCards.Get('munu/data_obs')
    nbins = h_data.GetNbinsX()
    histnames = ['bkg_munu','wmunu']
    hists = {}
    histsFit = {}
    for histname in histnames:
        hists[histname] = fileCards.Get('munu/'+histname)
        histsFit[histname] = fileFit.Get(folder+'/ch1/'+histname)
        for i in range(1,nbins+1):
            x = histsFit[histname].GetBinContent(i)
            hists[histname].SetBinContent(i,x)
            hists[histname].SetBinError(i,0.0)

    h_tot  = hists['wmunu'].Clone('h_tot')
    h_tot_fit = fileFit.Get(folder+'/ch1/total')
    for i in range(1,nbins+1):
        x = h_tot_fit.GetBinContent(i)
        e = h_tot_fit.GetBinError(i)
        h_tot.SetBinContent(i,x)
        h_tot.SetBinError(i,e)

    Plot(h_data,h_tot,hists['bkg_munu'],hists['wmunu'],args.era,args.variable,args.postfit)
