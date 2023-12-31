#! /usr/bin/env python
# Author: Alexei Raspereza (December 2022)
# High pT tau ID SF measurements 
# Datacards producer for the signal region (W*->tau+v) 
import ROOT
import TauFW.Plotter.HighPT.utilsHighPT as utils
from array import array
import math
import TauFW.Plotter.HighPT.stylesHighPT as styles
import os

#################################
#     definition of samples     #
#################################
bkgSampleNames = ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ','ZJetsToNuNu_HT-100To200','ZJetsToNuNu_HT-200To400','ZJetsToNuNu_HT-400To600','ZJetsToNuNu_HT-600To800','ZJetsToNuNu_HT-800To1200','ZJetsToNuNu_HT-1200To2500']

#bkgSampleNamesLepFake = ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ','WJetsToLNu','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500','ZJetsToNuNu_HT-100To200','ZJetsToNuNu_HT-200To400','ZJetsToNuNu_HT-400To600','ZJetsToNuNu_HT-600To800','ZJetsToNuNu_HT-800To1200','ZJetsToNuNu_HT-1200To2500']

bkgSampleNamesLepFake = ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ','WJetsToLNu','ZJetsToNuNu_HT-100To200','ZJetsToNuNu_HT-200To400','ZJetsToNuNu_HT-400To600','ZJetsToNuNu_HT-600To800','ZJetsToNuNu_HT-800To1200','ZJetsToNuNu_HT-1200To2500']

sigSampleNames = ['WToTauNu_M-200']

def FitConst(x,par):
    return par[0]

##################################
# computing j->tau fake template #
################################## 
def ComputeFake(h_wjets,h_dijets,h_fraction,name):
    nbins = h_wjets.GetNbinsX()
    hist = h_wjets.Clone(name)
    print
    print('Computing fake histogram ->',name)
    for i in range(1,nbins+1):
        x_wjets = h_wjets.GetBinContent(i)
        e_wjets = h_wjets.GetBinError(i)
        x_dijets = h_dijets.GetBinContent(i)
        e_dijets = h_dijets.GetBinError(i)
        x_fract = h_fraction.GetBinContent(i)
        e_fract = h_fraction.GetBinError(i)
        x_fakes = x_wjets*x_fract + x_dijets*(1-x_fract)
        r_wjets = e_wjets*x_fract
        r_dijets = e_dijets*(1-x_fract)
        r_fract = (x_wjets-x_dijets)*e_fract
        e_fakes = math.sqrt(r_wjets*r_wjets+r_dijets*r_dijets+r_fract*r_fract)
        if x_fakes<0: 
            x_fakes = 0.1
            e_fakes = 0.1
        hist.SetBinContent(i,x_fakes)
        hist.SetBinError(i,e_fakes)
        lowerEdge = hist.GetBinLowEdge(i)
        upperEdge = hist.GetBinLowEdge(i+1)
        print("[%3d,%4d] = %6.1f +/- %4.1f (%4.2f rel)" %(lowerEdge,upperEdge,x_fakes,e_fakes,e_fakes/x_fakes))

    return hist

##################################
# compute EWK fraction histogram #
# in FF application region       #
##################################
def ComputeEWKFraction(h_data,h_mc):

    print
    print('Computing EWK fraction')
    nbins = h_data.GetNbinsX()
    h_fraction = h_data.Clone('fraction')
    for i in range(1,nbins+1):
        xdata = h_data.GetBinContent(i)
        edata = h_data.GetBinError(i)
        xmc = h_mc.GetBinContent(i)
        emc = h_mc.GetBinError(i)
        ratio = 1
        eratio = 0
        if xdata>0:
            ratio = xmc/xdata
            rdata = edata/xdata
            rmc = emc/xmc 
            rratio = math.sqrt(rdata*rdata+rmc*rmc)
            eratio = ratio * rratio
        if ratio>1.0:
            ratio = 1.0
            eratio = 0.0
        h_fraction.SetBinContent(i,ratio)
        h_fraction.SetBinError(i,eratio)
        lowerEdge = h_fraction.GetBinLowEdge(i)
        upperEdge = h_fraction.GetBinLowEdge(i+1)
        print("[%3d,%4d] = %4.2f +/- %4.2f (%4.2f rel) ; Data = %5.1f ; MC = %5.1f" %(lowerEdge,upperEdge,ratio,eratio,eratio/ratio,xdata,xmc))

    return h_fraction

##########################
# Plotting distributions #
##########################
def PlotWToTauNu(h_data_input,h_fake_input,h_tau_input,h_bkg_input,h_sig_input,
                 wp,era,var,wpVsMu,wpVsE,suffix):

    print
    print('Plotting for era',era,'WPvsJet',wp,'WPvsMu',wpVsMu,'WPvsE',wpVsE)

    nbins = h_data_input.GetNbinsX()
    wp_list = era+"_"+wp+"_"+wpVsMu+"_"+wpVsE
    
    h_data = h_data_input.Clone("data_plot")
    h_fake = h_fake_input.Clone("fake_plot")
    h_bkg = h_bkg_input.Clone("bkg_plot")
    h_tau = h_tau_input.Clone("tau_plot")
    h_sig = h_sig_input.Clone("sig_plot")

    styles.InitData(h_data)
    styles.InitHist(h_bkg,"","",ROOT.TColor.GetColor("#6F2D35"),1001)
    styles.InitHist(h_sig,"","",ROOT.TColor.GetColor("#FFCC66"),1001)
    styles.InitHist(h_fake,"","",ROOT.TColor.GetColor("#FFCCFF"),1001)
    styles.InitHist(h_tau,"","",ROOT.TColor.GetColor("#c6f74a"),1001)

    h_tau.Add(h_tau,h_bkg,1.,1.)
    h_fake.Add(h_fake,h_tau,1.,1.)
    h_sig.Add(h_sig,h_fake,1.,1.)
    h_tot = h_sig.Clone("total")
    styles.InitTotalHist(h_tot)

    h_ratio = utils.histoRatio(h_data,h_tot,'ratio')
    h_tot_ratio = utils.createUnitHisto(h_tot,'tot_ratio')

    styles.InitRatioHist(h_ratio)

    h_ratio.GetYaxis().SetRangeUser(0.501,1.499)
    
    nbins = h_ratio.GetNbinsX()

    utils.zeroBinErrors(h_sig)
    utils.zeroBinErrors(h_bkg)
    utils.zeroBinErrors(h_fake)
    utils.zeroBinErrors(h_tau)

    ymax = h_data.GetMaximum()
    if h_tot.GetMaximum()>ymax: ymax = h_tot.GetMaximum()
    h_data.GetYaxis().SetRangeUser(1.0,5.0*ymax)
    h_data.GetXaxis().SetLabelSize(0)
    h_data.GetYaxis().SetTitle("events / bin")
    h_ratio.GetYaxis().SetTitle("obs/exp")
    h_ratio.GetXaxis().SetTitle(utils.XTitle[var])
    
    # canvas 
    canvas = styles.MakeCanvas("canv","",600,700)

    # upper pad
    upper = ROOT.TPad("upper", "pad",0,0.31,1,1)
    upper.Draw()
    upper.cd()
    styles.InitUpperPad(upper)    
    
    h_data.Draw('e1')
    h_sig.Draw('hsame')
    h_fake.Draw('hsame')
    h_tau.Draw('hsame')
    h_bkg.Draw('hsame')
    h_data.Draw('e1same')
    h_tot.Draw('e2same')

    leg = ROOT.TLegend(0.7,0.45,0.9,0.75)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.043)
    leg.SetHeader(wp)
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_sig,'W#rightarrow #tau#nu','f')
    leg.AddEntry(h_fake,'j#rightarrow#tau misId','f')
    leg.AddEntry(h_tau,'true #tau','f')
    leg.AddEntry(h_bkg,'e/#mu#rightarrow#tau misId','f')
    leg.Draw()

    styles.CMS_label(upper,era=era)

    upper.SetLogy(True)
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

    # update canvas 
    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    print
    print('Creating control plot')
    if wpVsE=='VLoose':
        canvas.Print(utils.figuresFolderPT+"/pT_"+wp+"VsJet_"+wpVsMu+"VsMu_V"+wpVsE+"VsE_"+era+suffix+".png")
    else:
        canvas.Print(utils.figuresFolderPT+"/pT_"+wp+"VsJet_"+wpVsMu+"VsMu_"+wpVsE+"VsE_"+era+suffix+".png")


############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='Run2', help="""Era : UL2016_preVFP, UL2016_postVFP, UL2017, UL2018, Run2""")
    parser.add_argument('-wp','--WP', dest='wp', default='Medium', help=""" tau ID WP : Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight', help=""" WP vs. mu : VLoose, Loose, Medium, Tight""")
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VLoose




', help=""" WP vs. e : VLoose, Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-corrected','--Corrected',dest='corrected',default=1, help=""" 0 : non-corrected, 1 : corrected """)
    
    args = parser.parse_args() 
    var = "pt_1"

    suffix = ''
    if args.corrected==1 : suffix = '_corrected'


    rootFile = ''
    if args.wpVsE=='VLoose':
        rootFile = utils.figuresFolderPT+"/pT_"+args.wp+"VsJet_"+args.wpVsMu+"VsMu_V"+args.wpVsE+"VsE_"+args.era+suffix+".root"
    else:
        rootFile = utils.figuresFolderPT+"/pT_"+args.wp+"VsJet_"+args.wpVsMu+"VsMu_"+args.wpVsE+"VsE_"+args.era+suffix+".root"

    inputfile = ROOT.TFile(rootFile,'READ')
    hist_data = inputfile.Get('h_data')
    hist_fake = inputfile.Get('h_jfakes')
    hist_sig = inputfile.Get('h_sig')
    hist_bkg_tau = inputfile.Get('h_tau')
    hist_bkg_lfakes = inputfile.Get('h_lfakes')

    # making control plot
    PlotWToTauNu(hist_data,hist_fake,hist_bkg_tau,hist_bkg_lfakes,hist_sig,
                 args.wp,args.era,var,args.wpVsMu,args.wpVsE,suffix)

