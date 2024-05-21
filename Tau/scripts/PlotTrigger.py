#! /usr/bin/env python3

import ROOT 
import HighPT.Tau.utilsHighPT as utils
from array import array
import HighPT.Tau.stylesHighPT as styles
import os

def FitFuncConst(x,par):
    return par[0]

def FitFuncInverseQuadratic(x,par):
    return par[0] + par[1]/(x[0]*x[0])

def FitFuncInverseCubic(x,par):
    return par[0] + par[1]/(x[0]*x[0]*x[0])

def FitFuncLinear(x,par):
    return par[0] + par[1]*x[0]

def FitFunc(x,par):
    return par[0] + par[1]*(x[0]-50.) + par[2]/((x[0]-50.)*(x[0]-50.))

def FitFuncErr(x,par):
    return par[0]*ROOT.TMath.Erf(par[1]*(x[0]-par[2]))

def PlotEff(h_data_eff,h_mc_eff,**kwargs):
    wp     = kwargs.get('wp','Medium')
    wpVsE  = kwargs.get('wpVsE','TightVsE')
    wpVsMu = kwargs.get('wpVsMu','TightVsMu')
    era    = kwargs.get('era','UL2016')
    plot    = kwargs.get('plot','cards')

    #    if isdata and channel=='wjets' and era=='UL2017' and label=='ptratioHigh':
    #        hist.SetBinContent(2,2*hist.GetBinContent(2))

    print('')

    styles.InitData(h_data_eff)
    styles.InitData(h_mc_eff)
    
    h_data_eff.SetMarkerSize(1.7)
    h_mc_eff.SetMarkerSize(1.7)

    h_data_eff.SetMarkerColor(2)
    h_mc_eff.SetMarkerColor(4)

    h_data_eff.SetLineColor(2)
    h_mc_eff.SetLineColor(4)

    h_data_eff.GetXaxis().SetTitle('tau p_{T} (GeV)')
    h_data_eff.GetYaxis().SetTitle('Trigger efficiency')

    h_data_eff.GetYaxis().SetRangeUser(0.,1.2)

    nbins = h_data_eff.GetNbinsX()
    xmin = h_data_eff.GetBinLowEdge(1)
    xmax = h_data_eff.GetBinLowEdge(nbins+1)

    p0 = 0.8
    p1 = 0.1
    p2 = 180.0

    if era=='UL2016': p2 = 120.0

    f_data = ROOT.TF1("f_data",FitFuncErr,xmin,xmax,3)
    f_mc   = ROOT.TF1('f_mc',FitFuncErr,xmin,xmax,3)
    f_data.SetParameter(0,p0)
    f_data.SetParameter(1,p1)
    f_data.SetParameter(2,p2)
    f_mc.SetParameter(0,p0)
    f_mc.SetParameter(1,p1)
    f_mc.SetParameter(2,p2)
    f_data.SetLineColor(2)
    f_mc.SetLineColor(4)

    h_data_eff.GetXaxis().SetMoreLogLabels()
    h_data_eff.GetXaxis().SetNoExponent()

    canv = styles.MakeCanvas("canv","",700,600)
    #h_data_eff.Fit('f_data',"R")
    #h_mc_eff.Fit('f_mc','R')

    h_data_eff.Draw("e1")
    h_mc_eff.Draw("e1same")

    leg = ROOT.TLegend(0.7,0.2,0.9,0.4)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.06)
    leg.AddEntry(h_data_eff,"Data",'e1lp')
    leg.AddEntry(h_mc_eff,"MC",'e1lp')
    leg.Draw()
    styles.CMS_label(canv,era=era)
    canv.SetLogx(True)
    canv.RedrawAxis()
    canv.Update()
    canv.Print(utils.baseFolder+'/'+era+'/figures/TauTrigger/TrigEff_'+wp+"VsJet_"+wpVsMu+'VsMu_'+wpVsE+'VsE_'+plot+'.png')

def PlotSF(h_data_eff,h_mc_eff,**kwargs):
    wp = kwargs.get('wp','Medium')
    wpVsE  = kwargs.get('wpVsE','TightVsE')
    wpVsMu = kwargs.get('wpVsMu','TightVsMu')
    era = kwargs.get('era','era')
    plot = kwargs.get('plot','cards')

    print('')
    print('fitting trigger eff SF >>> %s - %sVsJet - %sVsMu - %sVsE'%(era,wp,wpVsMu,wpVsE))
    
    hist = utils.divideHistos(h_data_eff,h_mc_eff,'h_eff')

    styles.InitData(hist)

    print('')
    histToPlot = hist.Clone('temp')
    
    nbins = hist.GetNbinsX()
    xmin = hist.GetBinLowEdge(1)
    xmax = hist.GetBinLowEdge(nbins+1)
    f1 = ROOT.TF1("f1",FitFuncConst,xmin,xmax,1)
    f2 = ROOT.TF1('f2',FitFunc,xmin,xmax,4)
    f1.SetParameter(0,1.0)
#    f1.SetParameter(1,0.0)
    f2.SetParameter(0,1.0)
    f2.SetParameter(1,0.0)
    f2.SetParameter(2,0.0)

    histToPlot.SetMarkerColor(1)
    histToPlot.SetLineColor(1)
    histToPlot.SetMarkerSize(1.7)

    canv = styles.MakeCanvas("canv","",700,600)
    hist.Fit('f1',"R")

    hfit = ROOT.TH1D("hfit","",5000,xmin,xmax)
    ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hfit,0.68)

    hist.Fit('f2','R')
    hfitLinear = ROOT.TH1D("hfit","",5000,xmin,xmax)
    ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hfitLinear,0.68)



    hfitline = hfit.Clone('histline')
    hfitline.SetLineWidth(2)
    hfitline.SetLineColor(4)
    hfitline.SetMarkerSize(0)
    hfitline.SetMarkerStyle(0)
    for i in range(1,hfitline.GetNbinsX()+1): 
        hfitline.SetBinError(i,0)
        relError = hfitLinear.GetBinError(i)/hfitLinear.GetBinContent(i)
        error = hfit.GetBinContent(i)*relError
        hfit.SetBinError(i,error)

    x = hfitLinear.GetBinContent(hfitLinear.FindBin(200.))
    a = hfitLinear.GetBinError(hfitLinear.FindBin(199.))
    b = hfitLinear.GetBinError(hfitLinear.FindBin(999.))
    k = (b-a)/2.

    print('')
    print('SF = %5.3f +/- %5.3f + %5.3f*pT[GeV] max = %5.3f'%(x,a,k,b)) 

    styles.InitModel(hfit,4)
    hfit.SetFillColor(ROOT.kCyan)
    hfit.SetFillStyle(1001)
    hfit.SetLineWidth(2)
    hfit.SetLineColor(4)
    hfit.SetMarkerSize(0)
    hfit.SetMarkerStyle(0)
    hfit.GetYaxis().SetRangeUser(0.,2.)
    hfit.GetXaxis().SetTitle("#tau p_{T} [GeV]")
    hfit.GetYaxis().SetTitle("Trigger eff SF")

    hfit.GetXaxis().SetMoreLogLabels()
    hfit.GetXaxis().SetNoExponent()

    hfit.Draw("e2")
    hfitline.Draw("hsame")
    histToPlot.Draw("e1same")

    leg = ROOT.TLegend(0.7,0.2,0.9,0.4)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.06)
    leg.AddEntry(histToPlot,"SF",'e1lp')
    leg.AddEntry(hfit,'Fit','lf')
    leg.Draw()

    styles.CMS_label(canv,era=era)

    canv.SetLogx(True)
    canv.RedrawAxis()
    canv.Update()
    canv.Print(utils.baseFolder+'/'+era+'/figures/TauTrigger/TrigSF_'+wp+'VsJet_'+wpVsMu+'VsMu_'+wpVsE+'VsE_'+plot+'.png')

def ComputeEff(hists):

    h_data_p = hists['h_data_trig'].Clone('h_data_p')
    h_data_f = hists['h_data_notrig'].Clone('h_data_f')

    h_mc_p = hists['h_sig_trig'].Clone('h_data_p')
    h_mc_f = hists['h_sig_notrig'].Clone('h_data_f')

    
    h_data_p.Add(h_data_p,hists['h_fake_trig'],1.,-1.)
    h_data_p.Add(h_data_p,hists['h_bkg_trig'],1.,-1.)
    h_data_f.Add(h_data_f,hists['h_fake_notrig'],1.,-1.)
    h_data_f.Add(h_data_f,hists['h_bkg_notrig'],1.,-1.)

    h_mc_p.Add(h_mc_p,hists['h_tau_trig'],1.,1.)
    h_mc_f.Add(h_mc_f,hists['h_tau_notrig'],1.,1.)

    h_data_eff = utils.dividePassProbe(h_data_p,h_data_f,'h_data_eff')
    h_mc_eff   = utils.dividePassProbe(h_mc_p,h_mc_f,'h_mc_eff')

    return h_data_eff,h_mc_eff

##########################
# Plotting distributions #
##########################
def PlotWToTauNu(hists,**kwargs):

    wp = kwargs.get("wp","Medium")
    wpVsMu = kwargs.get("wpVsMu","Tight")
    wpVsE = kwargs.get("wpVsE","Tight")
    era = kwargs.get("era","2022")
    trigger = kwargs.get("trigger","_trig")
    plot = kwargs.get("plot","postfit")
    var = 'pt_1'

    h_data = hists['h_data'+trigger].Clone("data_plot")
    h_fake = hists['h_fake'+trigger].Clone("fake_plot")
    h_bkg = hists['h_bkg'+trigger].Clone("bkg_plot")
    h_tau = hists['h_tau'+trigger].Clone("tau_plot")
    h_sig = hists['h_sig'+trigger].Clone("sig_plot")

    # protection from zero entries
    xb1 = max(h_bkg.GetBinContent(1),0.1)
    h_bkg.SetBinContent(1,xb1)

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

    h_ratio.GetYaxis().SetRangeUser(0.001,1.999)
    
    nbins = h_ratio.GetNbinsX()

    utils.zeroBinErrors(h_sig)
    utils.zeroBinErrors(h_bkg)
    utils.zeroBinErrors(h_fake)
    utils.zeroBinErrors(h_tau)

    ymax = h_data.GetMaximum()
    if h_tot.GetMaximum()>ymax: ymax = h_tot.GetMaximum()
    h_data.GetYaxis().SetRangeUser(1.,100*ymax)
    h_data.GetXaxis().SetLabelSize(0)
    h_data.GetYaxis().SetTitle("events / bin")
    h_ratio.GetYaxis().SetTitle("obs/exp")
    h_ratio.GetXaxis().SetTitle(utils.XTitle[var])

    h_data.GetXaxis().SetMoreLogLabels()
    h_data.GetXaxis().SetNoExponent()
    
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

    leg = ROOT.TLegend(0.65,0.4,0.90,0.75)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.047)
    if trigger=='_trig':
        leg.SetHeader("passed")
    else:
        leg.SetHeader("failed")
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
    upper.SetLogx(True)
    upper.SetLogy(True)
    canvas.cd()

    # lower pad
    lower = ROOT.TPad("lower", "pad",0,0,1,0.30)
    lower.Draw()
    lower.cd()
    styles.InitLowerPad(lower)

    h_ratio.GetXaxis().SetMoreLogLabels()
    h_ratio.GetXaxis().SetNoExponent()

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
    lower.SetLogx(True)

    # update canvas 
    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    print('')
    canvas.Print(utils.baseFolder+"/"+era+"/figures/TauTrigger/tauTrigger_"+wp+"VsJet_"+wpVsMu+"VsMu_"+wpVsE+"VsE"+trigger+"_"+plot+".png")


############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='2022', choices=['UL2016','UL2017','UL2018','2022','2023'])
    parser.add_argument('-wp','--WP', dest='wp', default='Tight', choices=['Loose','Medium','Tight']) 
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight', choices=['Loose','Tight'])
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='Tight', choices=['VVLoose','Tight'])
    parser.add_argument('-plot','--Plot', dest='plot', default="postfit", choices=['cards','prefit','postfit'])
    args = parser.parse_args()
    
    fileNameTrig    = utils.baseFolder+'/'+args.era+'/datacards/taunu_'+args.wp+'_'+args.wpVsMu+'_'+args.wpVsE+'_trig.root'
    fileNameNotTrig = utils.baseFolder+'/'+args.era+'/datacards/taunu_'+args.wp+'_'+args.wpVsMu+'_'+args.wpVsE+'_notrig.root'
    fileNameFit     = utils.baseFolder+'/'+args.era+'/datacards/tauTrigger_'+args.wp+"_"+args.wpVsMu+'_'+args.wpVsE+'_fit.root'
    fileCardsTrig    = ROOT.TFile(fileNameTrig)
    fileCardsNotTrig = ROOT.TFile(fileNameNotTrig)
    fileFit          = ROOT.TFile(fileNameFit)
    h_data_pass = fileCardsTrig.Get('taunu/data_obs')
    h_data_fail = fileCardsNotTrig.Get('taunu/data_obs')

    plot = {'prefit':'shapes_prefit','postfit':'shapes_fit_s'}
    files = {'_trig':fileCardsTrig,'_notrig':fileCardsNotTrig}
    filedirs = {'_trig':'ch1','_notrig':'ch2'}
    names = {'h_data' : 'data_obs',
             'h_sig'  : 'wtaunu',
             'h_tau'  : 'tau',
             'h_fake' : 'fake',
             'h_bkg'  : 'lfakes'}
    hists = {}

    for trigLabel in ['_trig','_notrig']:
        for name in names:
            nameHist = names[name]
            if nameHist=='wtaunu' or nameHist=='tau':
                nameHist = names[name] + trigLabel + '_' + args.era
            hists[name+trigLabel] = files[trigLabel].Get('taunu/'+nameHist)
            
    if args.plot in ['prefit', 'postfit']:
        for trigLabel in ['_trig','_notrig']:
            for name in names:
                nameHist = names[name]
                if nameHist=='wtaunu' or nameHist=='tau':
                    nameHist = names[name] + trigLabel + '_' + args.era
                if name=='h_data': continue
                fullPathHist = plot[args.plot]+'/'+filedirs[trigLabel]+'/'+nameHist
                histo = fileFit.Get(plot[args.plot]+'/'+filedirs[trigLabel]+'/'+nameHist)
                nbins = histo.GetNbinsX()
                for ib in range(1,nbins+1):
                    hists[name+trigLabel].SetBinContent(ib,histo.GetBinContent(ib))
                    hists[name+trigLabel].SetBinError(ib,histo.GetBinError(ib))
    
    for trigLabel in ['_trig','_notrig']:
        PlotWToTauNu(hists,
                     trigger=trigLabel,
                     wp=args.wp,
                     wpVsMu=args.wpVsMu,
                     wpVsE=args.wpVsE,
                     plot=args.plot,
                     era=args.era)

    h_data_eff,h_mc_eff = ComputeEff(hists)
    PlotEff(h_data_eff,
            h_mc_eff,
            wp=args.wp,
            wpVsMu=args.
            wpVsMu,
            wpVsE=args.wpVsE,
            era=args.era,
            plot=args.plot)
    PlotSF(h_data_eff,
           h_mc_eff,
           wp=args.wp,
           wpVsMu=args.wpVsMu,
           wpVsE=args.wpVsE,
           era=args.era,
           plot=args.plot)
    
