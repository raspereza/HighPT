#! /usr/bin/env python
# Author: Alexei Raspereza (December 2022)
# High pT tau ID efficiency measurements binned in pT:
# plotting postfit and prefit distributions 
# in the signal region (W*->tau+v) 
import ROOT
import TauFW.Plotter.HighPT.utilsHighPT as utils
from array import array
import math
import TauFW.Plotter.HighPT.stylesHighPT as styles
import os

##########################
# Plotting distributions #
##########################
def Plot(h_data_input,h_tot_input,h_fake_input,h_tau_input,h_bkg_input,h_sig_input,wp,era,var,postFit,suffix,wpVsMu,wpVsE):
    
    h_data = h_data_input.Clone("data_plot")
    h_fake = h_fake_input.Clone("fake_plot")
    h_bkg = h_bkg_input.Clone("bkg_plot")
    h_tau = h_tau_input.Clone("tau_plot")
    h_sig = h_sig_input.Clone("sig_plot")
    h_tot = h_tot_input.Clone("h_tot_plot")

    # x_before = h_sig.GetBinContent(1)
    # x_after = 1.5*x_before
    # x_dif = x_after - x_before
    # x_tot_after = h_tot.GetBinContent(1)+x_dif
    # h_sig.SetBinContent(1,x_after)
    # h_tot.SetBinContent(1,x_tot_after)

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

    h_ratio.GetYaxis().SetRangeUser(0.201,1.799)
    
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

    leg = ROOT.TLegend(0.63,0.4,0.90,0.75)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.047)
    leg.SetHeader(wp)
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_sig,'W#rightarrow #tau#nu','f')
    leg.AddEntry(h_fake,'j#rightarrow#tau misId','f')
    leg.AddEntry(h_tau,'true #tau','f')
    leg.AddEntry(h_bkg,'e/#mu#rightarrow#tau misId','f')
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

    # update canvas 
    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    print
    print('Creating control plot')
    if postFit:
        canvas.Print(utils.figuresFolderWTauNu+"/"+wpVsMu+"VsMu_"+wpVsE+"VsE/wtaunu_"+wp+"_"+era+"_"+suffix+"_postFit.png")
    else:
        canvas.Print(utils.figuresFolderWTauNu+"/"+wpVsMu+"VsMu_"+wpVsE+"VsE/wtaunu_"+wp+"_"+era+"_"+suffix+"_preFit.png")

############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='UL2016_postVFP', help="""Era : UL2016_preVFP, UL2016_postVFP, UL2017, UL2018""")
    parser.add_argument('-wp','--WP', dest='wp', default='Medium', help=""" tau ID WP : Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight', help=""" WP vs. mu : VLoose, Loose, Medium, Tight""")
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VLoose', help=""" WP vs. e : VLoose, Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-var','--variable', dest='variable', default='mt_1', help=""" Variable to plot""")
    parser.add_argument('-post','--PostFit',dest='postfit',default=True, help=""" Postfit (true), Prefit (false) """)
    parser.add_argument('-ptbin','--ptbin',dest='ptbin',default='highpt',help=""" pt bin : lowpt or highpt""")
    args = parser.parse_args()
    suffix = args.ptbin
    if suffix not in ['lowpt','highpt']:
        print('Uknown pt bin',suffix,' available options : lowpt, highpt')
        exit()
    ch = "ch2"
    Era = args.era
    if Era not in ['UL2016_preVFP','UL2016_postVFP','UL2017','UL2018']:
        print('Unknown era',Era,' available options : UL2016_preVFP, UL2016_postVFP, UL2017, UL2018')
        exit()
    if args.era=='UL2016_preVFP':
        if suffix=='lowpt':
            ch = 'ch2'
        else:
            ch = 'ch3'
    if args.era=='UL2016_postVFP':
        if suffix=='lowpt':
            ch = 'ch5'
        else:
            ch = 'ch6'
    if args.era=='UL2017':
        if suffix=='lowpt': 
            ch = 'ch8'
        else:
            ch = 'ch9'
    if args.era=='UL2018':
        if suffix == "lowpt":
            ch = 'ch11'
        else:
            ch = 'ch12'

    basedir = utils.datacardsFolder+"/"+args.wpVsMu+"VsMu_"+args.wpVsE+"VsE"
    fullpathFit = basedir +"/tauID_"+args.wp+"_multidim.root"
    fileFit = ROOT.TFile(fullpathFit,"read")
    #print("fileFit",fileFit)
    fullpathCards = basedir + "/taunu_"+args.wp+"_"+args.era+"_"+suffix+".root" 
    fileCards = ROOT.TFile(fullpathCards,"read")
    #print("fileCards",fileCards)
 
    folder='shapes_prefit'
    if args.postfit:
        folder='shapes_fit_s'

    h_data = fileCards.Get('taunu/data_obs')
    nbins = h_data.GetNbinsX()
    histnames = ['fake','lfakes','tau_'+suffix+'_'+args.era,'wtaunu_'+suffix+'_'+args.era]
    hists = {}
    histsFit = {}
    for histname in histnames:
        hists[histname] = fileCards.Get('taunu/'+histname)
        histsFit[histname] = fileFit.Get(folder+'/'+ch+'/'+histname)
        for i in range(1,nbins+1):
            x = histsFit[histname].GetBinContent(i)
            hists[histname].SetBinContent(i,x)
            hists[histname].SetBinError(i,0.0)

    h_tot  = hists['wtaunu_'+suffix+'_'+args.era].Clone('h_tot')
    h_tot_fit = fileFit.Get(folder+'/'+ch+'/total')
    for i in range(1,nbins+1):
        x = h_tot_fit.GetBinContent(i)
        e = h_tot_fit.GetBinError(i)
        h_tot.SetBinContent(i,x)
        h_tot.SetBinError(i,e)

    Plot(h_data,h_tot,hists['fake'],hists['tau_'+suffix+'_'+args.era],hists['lfakes'],hists['wtaunu_'+suffix+'_'+args.era],args.wp,args.era,args.variable,args.postfit,suffix,args.wpVsMu,args.wpVsE)
