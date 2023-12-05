#! /usr/bin/env python
# Author: Alexei Raspereza (December 2022)
# High pT this ID efficiency measurements 
# Plotting macro: signal region (W*->tau+v) 
import ROOT
import TauFW.Plotter.HighPT.utilsThinJet as utils
from array import array
import math
import HighPT.ThinJet.stylesHighPT as styles
import os

##########################
# Plotting distributions #
##########################
def Plot(hists,wp,era,dm,var,text,postFit):
    
    h_data = hists['data'].Clone("data_plot")
    h_fake = hists['fake'].Clone("fake_plot")
    h_bkg = hists['lfakes'].Clone("bkg_plot")
    h_tau = hists['tau'].Clone("tau_plot")
    h_sig = hists['wtaunu'].Clone("sig_plot")
    h_tot = hists['total'].Clone("h_tot_plot")

    styles.InitData(h_data)
    styles.InitHist(h_bkg,"","",ROOT.TColor.GetColor("#6F2D35"),1001)
    styles.InitHist(h_sig,"","",ROOT.TColor.GetColor("#FFCC66"),1001)
    styles.InitHist(h_fake,"","",ROOT.TColor.GetColor("#FFCCFF"),1001)
    styles.InitHist(h_tau,"","",ROOT.TColor.GetColor("#c6f74a"),1001)

    h_tau.Add(h_tau,h_bkg,1.,1.)
    h_fake.Add(h_fake,h_tau,1.,1.)
    h_sig.Add(h_sig,h_fake,1.,1.)
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
    h_data.GetYaxis().SetRangeUser(0.,1.2*ymax)
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

    leg = ROOT.TLegend(0.5,0.4,0.75,0.75)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.047)
    leg.SetHeader(wp+'  '+dm)
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_sig,'W#rightarrow #tau#nu','f')
    leg.AddEntry(h_fake,'j#rightarrow#tau misId','f')
    leg.AddEntry(h_tau,'genuine #tau bkg','f')
    leg.AddEntry(h_bkg,'l#rightarrow#tau fakes','f')
    leg.Draw()

    if postFit:
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextAngle(0)
        latex.SetTextColor(ROOT.kBlack)    
        latex.SetTextSize(0.05)
        latex.DrawLatex(0.45,0.25,text)

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

    # update canvas 
    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    print
    print('Creating control plot')
    if postFit:
        canvas.Print(utils.figuresFolderWTauNu+"/wtaunu_"+wp+"_"+dm+"_"+era+"_postFit.png")
    else:
        canvas.Print(utils.figuresFolderWTauNu+"/wtaunu_"+wp+"_"+dm+"_"+era+"_preFit.png")

############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='UL2017', help="""Era : UL2017, UL2018""")
    parser.add_argument('-wp','--WP', dest='wp', default='VLoose', help=""" tau ID WP : Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-var','--variable', dest='variable', default='mt_1', help=""" Variable to plot""")
    parser.add_argument('-dm','--DM', dest='dm', default='1prong', help=""" Decay mode : 1prong, 2prong, 3prong """)
    
    parser.add_argument('-post','--PostFit',dest='postfit',default=False, help=""" Postfit (true), Prefit (false) """)

    args = parser.parse_args()
    basedir = utils.datacardsFolder
    fullpathFit = basedir+"/tauID_"+args.wp+"_"+args.dm+"_"+args.era+"_fit.root"
    fileFit = ROOT.TFile(fullpathFit,"read")
    fullpathCards = basedir + "/taunu_"+args.wp+"_"+args.dm+"_"+args.era+".root" 
    fileCards = ROOT.TFile(fullpathCards,"read")

    folder='shapes_prefit'
    if args.postfit:
        folder='shapes_fit_s'

    hists = {}
    histsFit = {}
    h_data = fileCards.Get('taunu/data_obs')
    nbins = h_data.GetNbinsX()
    histnames = ['fake','tau','lfakes','wtaunu']
    for histname in histnames:
        hists[histname] = fileCards.Get('taunu/'+histname)
        histsFit[histname] = fileFit.Get(folder+'/ch2/'+histname)
        for i in range(1,nbins+1):
            x = histsFit[histname].GetBinContent(i)
            hists[histname].SetBinContent(i,x)
            hists[histname].SetBinError(i,0.0)

    h_tot  = hists['wtaunu'].Clone('h_tot')
    h_tot_fit = fileFit.Get(folder+'/ch2/total')
    for i in range(1,nbins+1):
        x = h_tot_fit.GetBinContent(i)
        e = h_tot_fit.GetBinError(i)
        h_tot.SetBinContent(i,x)
        h_tot.SetBinError(i,e)

    fitResult = fileFit.Get('fit_s')
    pars = fitResult.floatParsFinal()
    tauId = {}
    tauId_central = 1.0
    tauId_error = 0.2
    for par in pars:
        parname =  par.GetName()
        if parname=='r':
            tauId_central = par.getVal()
            tauId_error = par.getError()
            break

    hists['data'] = h_data
    hists['total'] = h_tot
    text = 'id SF = %4.2f #pm %4.2f '%(tauId_central,tauId_error)
    
    print('id SF = %4.2f +/- %4.2f '%(tauId_central,tauId_error))

    Plot(hists,args.wp,args.era,args.dm,args.variable,text,args.postfit)
    
