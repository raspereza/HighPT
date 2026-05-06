#! /usr/bin/env python3

import ROOT 
import HighPT.Tau.utilsHighPT as utils
from array import array
import math
import HighPT.Tau.stylesHighPT as styles
import os

opts = ['deeptau','pnet','comb']
opt_color = {
    'deeptau': ROOT.kBlack,
    'pnet': ROOT.kBlue,
    'comb': ROOT.kRed,
}
opt_style = {
    'deeptau': 20,
    'pnet': 21,
    'comb': 22,
}

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
    era    = kwargs.get('era','2024')
    isData    = kwargs.get('isData',True)

    print('')
    nbins = h_data_eff['comb'].GetNbinsX()
    """
    if wpVsE=='TightVsE':
        h_data_eff.SetBinContent(nbins,0.8*h_data_eff.GetBinContent(nbins))
    else:
        h_data_eff.SetBinContent(nbins,0.76*h_data_eff.GetBinContent(nbins))
        
    h_data_eff.SetBinContent(1,3.5*h_data_eff.GetBinContent(1))
    """
    
    for opt in opts:
        styles.InitData(h_data_eff[opt])
        styles.InitData(h_mc_eff[opt])

        h_data_eff[opt].SetMarkerSize(1.2)
        h_mc_eff[opt].SetMarkerSize(1.2)
        h_data_eff[opt].SetMarkerColor(opt_color[opt])
        h_mc_eff[opt].SetMarkerColor(opt_color[opt])
        h_data_eff[opt].SetLineColor(opt_color[opt])
        h_mc_eff[opt].SetLineColor(opt_color[opt])
        h_data_eff[opt].SetLineStyle(opt_style[opt])
        h_mc_eff[opt].SetLineStyle(opt_style[opt])

    h_data_eff['comb'].GetXaxis().SetTitle('tau p_{T} (GeV)')
    h_data_eff['comb'].GetYaxis().SetTitle('Trigger efficiency')
    h_data_eff['comb'].GetXaxis().SetTitle('tau p_{T} (GeV)')
    h_data_eff['comb'].GetYaxis().SetTitle('Trigger efficiency')

    h_data_eff['comb'].GetYaxis().SetRangeUser(0.,1.2)
    h_mc_eff['comb'].GetYaxis().SetRangeUser(0.,1.2)

    h_data_eff['comb'].GetXaxis().SetMoreLogLabels()
    h_data_eff['comb'].GetXaxis().SetNoExponent()
    h_mc_eff['comb'].GetXaxis().SetMoreLogLabels()
    h_mc_eff['comb'].GetXaxis().SetNoExponent()

    canv = styles.MakeCanvas("canv","",700,600)

    if isData:
        h_data_eff['comb'].Draw("e1")
        h_data_eff['pnet'].Draw("e1same")
        h_data_eff['deeptau'].Draw("e1same")
    else:
        h_mc_eff['comb'].Draw("e1")
        h_mc_eff['pnet'].Draw("e1same")
        h_mc_eff['deeptau'].Draw("e1same")

    leg = ROOT.TLegend(0.7,0.2,0.9,0.45)
    #    styles.SetLegendStyle(leg)
    if isData:
        leg.SetHeader('Data')
    else:
        leg.SetHeader('Simulation')
    leg.SetTextSize(0.05)
    if isData:
        leg.AddEntry(h_data_eff['deeptau'],"HPS",'e1lp')
        leg.AddEntry(h_data_eff['pnet'],"PNet",'e1lp')
        leg.AddEntry(h_data_eff['comb'],"Combined",'e1lp')
    else:
        leg.AddEntry(h_mc_eff['deeptau'],"HPS",'e1lp')
        leg.AddEntry(h_mc_eff['pnet'],"PNet",'e1lp')
        leg.AddEntry(h_mc_eff['comb'],"Combined",'e1lp')
    leg.Draw()
    styles.CMS_label(canv,era=era)
    canv.SetLogx(True)
    canv.SetGridx(True)
    canv.SetGridy(True)
    canv.RedrawAxis()
    canv.Update()
    suffix = 'mc'
    if isData:
        suffix = 'data'
    canv.Print('/eos/home-r/rasp/php-plots/plots/HighPt/WTauNuTrig/TrigEff_'+wp+"VsJet_"+wpVsMu+'VsMu_'+wpVsE+'VsE_'+era+'_'+suffix+'.png')

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

    if wpVsE=='Tight':
        if plot=='prefit':
            hist.SetBinContent(1,0.68)
        else:
            hist.SetBinContent(7,0.93)
    else:
        if plot=='prefit':
            hist.SetBinContent(1,0.75)
    
    print('')
    histToPlot = hist.Clone('temp')
    
    nbins = hist.GetNbinsX()
    xmin = hist.GetBinLowEdge(1)
    xmax = hist.GetBinLowEdge(nbins+1)
    f1 = ROOT.TF1("f1",FitFuncConst,xmin,xmax,1)
    f2 = ROOT.TF1('f2',FitFunc,xmin,xmax,3)
    f1.SetParameter(0,1.0)
#    f1.SetParameter(1,0.0)
    f2.SetParameter(0,1.0)
    f2.SetParameter(1,0.0)
    f2.SetParameter(2,0.0)

    histToPlot.SetMarkerColor(1)
    histToPlot.SetLineColor(1)
    histToPlot.SetMarkerSize(1.7)

    print('')
    print('Scale factors ->')
    nbins = histToPlot.GetNbinsX()
    for ib in range(1,nbins+1):
        xlow = histToPlot.GetBinLowEdge(ib)
        xhigh = histToPlot.GetBinLowEdge(ib+1) - 1.0
        x = histToPlot.GetBinContent(ib)
        e = histToPlot.GetBinError(ib)
        print('[%2i,%2i] : %5.3f +/- %5.3f'%(int(xlow),int(xhigh),x,e))
    print('')
    
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
    a = hfitLinear.GetBinError(hfitLinear.FindBin(200.))
    b = hfitLinear.GetBinError(hfitLinear.FindBin(999.))
    k = (b-a)

    print('')
    print('SF = %5.3f +/- %5.3f + %5.3f*pT[GeV]   max = %5.3f'%(x,a,k,b)) 

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
    canv.Print('/eos/home-r/rasp/php-plots/plots/HighPt/WTauNuTrig/TrigSF_'+wp+'VsJet_'+wpVsMu+'VsMu_'+wpVsE+'VsE_'+plot+'.png')

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

    data_eff = utils.dividePassProbe(h_data_p,h_data_f,'h_data_eff')
    mc_eff   = utils.dividePassProbe(h_mc_p,h_mc_f,'h_mc_eff')

    return data_eff,mc_eff

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
    
    nbins = h_data.GetNbinsX()
    
    # protection from zero entries
    xb1 = max(h_bkg.GetBinContent(1),0.1)
    h_bkg.SetBinContent(1,xb1)

    styles.InitData(h_data)
    styles.InitHist(h_bkg,"","",ROOT.TColor.GetColor("#6F2D35"),1001)
    styles.InitHist(h_sig,"","",ROOT.TColor.GetColor("#FFCC66"),1001)
    styles.InitHist(h_fake,"","",ROOT.TColor.GetColor("#FFCCFF"),1001)
    styles.InitHist(h_tau,"","",ROOT.TColor.GetColor("#c6f74a"),1001)

#    h_tau.Add(h_tau,h_bkg,1.,1.)
    h_fake.Add(h_fake,h_bkg,1.,1.)
    h_sig.Add(h_sig,h_tau,1.,1.)
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
    h_data.GetYaxis().SetRangeUser(1.01,100*ymax)
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
#    h_tau.Draw('hsame')
#    h_bkg.Draw('hsame')
    h_data.Draw('e1same')
    h_tot.Draw('e2same')

    leg = ROOT.TLegend(0.65,0.4,0.90,0.75)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.05)
    if trigger=='_trig':
        leg.SetHeader("passing probes")
    else:
        leg.SetHeader("failing probes")
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_sig,'genuine #tau','f')
    leg.AddEntry(h_fake,'misID #tau','f')
#    leg.AddEntry(h_sig,'W#rightarrow #tau#nu','f')
#    leg.AddEntry(h_fake,'j#rightarrow#tau misId','f')
#    leg.AddEntry(h_tau,'true #tau','f')
#    leg.AddEntry(h_bkg,'e/#mu#rightarrow#tau misId','f')
    leg.Draw()

    styles.CMS_label(upper,era=era,PosX=33)

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
    canvas.Print("/eos/home-r/rasp/php-plots/plots/HighPt/WTauNuTrig/tauTrigger_"+wp+"VsJet_"+wpVsMu+"VsMu_"+wpVsE+"VsE"+trigger+"_"+plot+".png")


############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='2024', choices=['UL2016','UL2017','UL2018','2022','2023','2024'])
    parser.add_argument('-wp','--WP', dest='wp', default='Medium', choices=['Loose','Medium','Tight','VTight','VVTight']) 
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight', choices=['VLoose','Tight'])
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VVLoose', choices=['VVLoose','Tight'])
    args = parser.parse_args()

    fileCardsTrig = {}
    fileCardsNotTrig = {}
    
    for opt in opts:    
        fileNameTrig = utils.baseFolder+'/'+args.era+'/datacards/taunu_'+args.wp+'_'+args.wpVsMu+'_'+args.wpVsE+'_'+opt+'_trig.root'
        fileNameNotTrig = utils.baseFolder+'/'+args.era+'/datacards/taunu_'+args.wp+'_'+args.wpVsMu+'_'+args.wpVsE+'_'+opt+'_notrig.root'
        fileCardsTrig[opt]    = ROOT.TFile(fileNameTrig)
        fileCardsNotTrig[opt] = ROOT.TFile(fileNameNotTrig)

    h_data_eff = {}
    h_mc_eff = {}
    
    for opt in opts:    

        h_data_pass = fileCardsTrig[opt].Get('taunu/data_obs')
        h_data_fail = fileCardsNotTrig[opt].Get('taunu/data_obs')

        names = {'h_data' : 'data_obs',
                 'h_sig'  : 'wtaunu',
                 'h_tau'  : 'tau',
                 'h_fake' : 'fake',
                 'h_bkg'  : 'lfakes'}
        hists = {}
        files = {'_trig': fileCardsTrig[opt], '_notrig': fileCardsNotTrig[opt]}
        for trigLabel in ['_trig','_notrig']:
            for name in names:
                nameHist = names[name]
                if nameHist=='wtaunu' or nameHist=='tau':
                    nameHist = names[name] + trigLabel + '_' + args.era
                full_name = name+trigLabel
                hists[full_name] = files[trigLabel].Get('taunu/'+nameHist)

        h_data_eff[opt],h_mc_eff[opt] = ComputeEff(hists)


    nbins = h_data_eff['comb'].GetNbinsX()
    print('')
    print('Data')
    for ib in range(1,nbins+1):
        xmin = int(h_data_eff['comb'].GetXaxis().GetBinLowEdge(ib)+0.3)
        xmax = int(h_data_eff['comb'].GetXaxis().GetBinLowEdge(ib+1)+0.3)
        xstring = '[%4i,%4i] | %4.2f+/-%4.2f | %4.2f+/-%4.2f | %4.2f+/-%4.2f |'%(xmin,xmax,h_data_eff['deeptau'].GetBinContent(ib),h_data_eff['deeptau'].GetBinError(ib),h_data_eff['pnet'].GetBinContent(ib),h_data_eff['pnet'].GetBinError(ib),h_data_eff['comb'].GetBinContent(ib),h_data_eff['comb'].GetBinError(ib))
        print(xstring)

    print('')
    print('Simulation')
    for ib in range(1,nbins+1):
        xmin = int(h_mc_eff['comb'].GetXaxis().GetBinLowEdge(ib)+0.3)
        xmax = int(h_mc_eff['comb'].GetXaxis().GetBinLowEdge(ib+1)+0.3)
        xstring = '[%4i,%4i] | %4.2f+/-%4.2f | %4.2f+/-%4.2f | %4.2f+/-%4.2f |'%(xmin,xmax,h_mc_eff['deeptau'].GetBinContent(ib),h_mc_eff['deeptau'].GetBinError(ib),h_mc_eff['pnet'].GetBinContent(ib),h_mc_eff['pnet'].GetBinError(ib),h_mc_eff['comb'].GetBinContent(ib),h_mc_eff['comb'].GetBinError(ib))
        print(xstring)
    exit()
    
    PlotEff(h_data_eff,
            h_mc_eff,
            wp=args.wp,
            wpVsMu=args.wpVsMu,
            wpVsE=args.wpVsE,
            era=args.era,
            isData=True)
    
    PlotEff(h_data_eff,
            h_mc_eff,
            wp=args.wp,
            wpVsMu=args.wpVsMu,
            wpVsE=args.wpVsE,
            era=args.era,
            isData=False)
    
