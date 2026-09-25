#! /usr/bin/env python3

import ROOT 
import HighPT.Tau.utilsHighPT as utils
from array import array
import math
import HighPT.Tau.stylesHighPT as styles
import os

sys_signal = ['JES','Unclustered','taues_1pr','taues_1pr1pi0','taues_3pr','taues_3pr1pi0']

opts = ['deeptau','pnet','comb']
#opts = ['deeptau',]
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

fake_samples = ['wjets','dijets']
ptratio = ['ptratioLow','ptratioHigh']
pttau = ['pttauLow','pttauHigh']

names = {'h_data' : 'data_obs',
         'h_sig'  : 'wtaunu',
         'h_tau'  : 'tau',
         'h_fake' : 'fake',
         'h_bkg'  : 'lfakes'}

mc_list = ['h_tau','h_fake','h_bkg']

eff_saturated = {
    'deeptau': (0.92,0.06),
    'pnet': (0.94,0.05),
    'comb': (0.96,0.04),
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



def AddSyst(hists):
    name = 'h_sig'
    for trig in ['_trig','_notrig']:
        #        print('')
        #        print('signal%s'%(trig))
        histName = name + trigLabel
        nbins = hists[histName].GetNbinsX()
        for iB in range(1,nbins+1):
            x_central = hists[histName].GetBinContent(iB)
            xlower = int(hists[histName].GetBinLowEdge(iB)+0.3)
            xupper = int(hists[histName].GetBinLowEdge(iB)+0.3)
            err = hists[histName].GetBinError(iB)
            estat = err
            err2 = err*err
            for sysname in sys_signal:
                histSysName = name + trigLabel + '_' + sysname
                x_sys = hists[histSysName].GetBinContent(iB)
                x_e = x_central - x_sys
                x_e2 = x_e*x_e
                err2 += x_e2
            maximal = 0.9*x_central
            err = min(math.sqrt(err2),maximal)
            hists[histName].SetBinError(iB,err)
            restat = estat/x_central
            retot = err/x_central
            #            print('[%4i,%4i]  %6.1f  %5.3f(stat.)  %5.3f(tot.)'%(xlower,xupper,x_central,restat,retot))

    #    print('')
    name = 'h_fake'
    nbins = hists[histName].GetNbinsX()
    for trig in ['_trig','_notrig']:
        #        print('fake%s'%(trig))
        for iB in range(1,nbins+1):
            histName = name + trigLabel
            err = hists[histName].GetBinError(iB)
            x_central = hists[histName].GetBinContent(iB)
            xlower = int(hists[histName].GetBinLowEdge(iB)+0.3)
            xupper = int(hists[histName].GetBinLowEdge(iB)+0.3)
            err2 = err*err
            estat = err
            for s in fake_samples:
                for r in ptratio:
                    for t in pttau:
                        sysname = '%s_%s_%s'%(s,r,t)
                        histSysName = name + trigLabel + '_' + sysname
                        x_sys = hists[histSysName].GetBinContent(iB)
                        x_e = x_central - x_sys
                        x_e2 = x_e*x_e
                        err2 += x_e2
            maximal = 0.9*x_central
            err = min(math.sqrt(err2),maximal)
            hists[histName].SetBinError(iB,err)
            restat = estat/x_central
            retot = err/x_central
            #            print('[%4i,%4i]  %6.1f  %5.3f(stat.)  %5.3f(tot.)'%(xlower,xupper,x_central,restat,retot))

    data_yield = 0.
    mc_yield = 0.
    sig_yield = 0.
    for trig in ['_trig','_notrig']:
        data_yield += hists['h_data'+trig].GetSumOfWeights()
        sig_yield += hists['h_sig'+trig].GetSumOfWeights()
        for name in mc_list:
            mc_yield += hists[name+trig].GetSumOfWeights()
    scale = (data_yield-mc_yield)/sig_yield
    
    #    print('W->tau+v scale factor = %5.3f'%(scale))
    
    hists['h_sig_trig'].Scale(scale)
    hists['h_sig_notrig'].Scale(scale)
    

def PlotEff(h_data_eff,h_mc_eff,**kwargs):

    wp     = kwargs.get('wp','Medium')
    wpVsE  = kwargs.get('wpVsE','TightVsE')
    wpVsMu = kwargs.get('wpVsMu','TightVsMu')
    era    = kwargs.get('era','2024')
    isData = kwargs.get('isData',True)

    print('')
    nbins = h_data_eff['comb'].GetNbinsX()
    
    for opt in opts:
        styles.InitData(h_data_eff[opt])
        styles.InitData(h_mc_eff[opt])

        h_data_eff[opt].SetMarkerSize(1.2)
        h_mc_eff[opt].SetMarkerSize(1.2)

        h_data_eff[opt].SetMarkerColor(opt_color[opt])
        h_mc_eff[opt].SetMarkerColor(opt_color[opt])

        h_data_eff[opt].SetMarkerStyle(opt_style[opt])
        h_mc_eff[opt].SetMarkerStyle(opt_style[opt])

        h_data_eff[opt].SetLineColor(opt_color[opt])
        h_mc_eff[opt].SetLineColor(opt_color[opt])

        h_data_eff[opt].SetLineWidth(2)
        h_mc_eff[opt].SetLineWidth(2)
        
    h_data_eff['comb'].GetXaxis().SetTitle('tau p_{T} (GeV)')
    h_data_eff['comb'].GetYaxis().SetTitle('Trigger efficiency')
    h_data_eff['comb'].GetYaxis().SetTitleOffset(1.2)
    h_mc_eff['comb'].GetXaxis().SetTitle('tau p_{T} (GeV)')
    h_mc_eff['comb'].GetYaxis().SetTitle('Trigger efficiency')
    h_mc_eff['comb'].GetYaxis().SetTitleOffset(1.2)

    h_data_eff['comb'].GetYaxis().SetRangeUser(0.01,1.29)
    h_data_eff['comb'].GetXaxis().SetRangeUser(99.9,2000)
    h_mc_eff['comb'].GetYaxis().SetRangeUser(0.01,1.29)
    h_mc_eff['comb'].GetXaxis().SetRangeUser(99.9,2000)

    h_data_eff['comb'].GetXaxis().SetMoreLogLabels()
    h_data_eff['comb'].GetXaxis().SetNoExponent()
    h_mc_eff['comb'].GetXaxis().SetMoreLogLabels()
    h_mc_eff['comb'].GetXaxis().SetNoExponent()

    print('')
    if isData:
        print('Data')
    else:
        print('Simulation')
    print('------------+-------------+-------------+-------------+')
    print('pT bin (GeV)|   DeepTau   |     PNet    |    Comb     |')
    print('------------+-------------+-------------+-------------+')    
    for ib in range(1,nbins+1):
        xstring = ''
        x_comb = h_data_eff['comb'].GetBinContent(ib)
        x_pnet = h_data_eff['pnet'].GetBinContent(ib)
        if x_pnet>x_comb:
            h_data_eff['comb'].SetBinContent(ib,x_pnet)
        x_comb = h_mc_eff['comb'].GetBinContent(ib)
        x_pnet = h_mc_eff['pnet'].GetBinContent(ib)
        if x_pnet>x_comb:
            h_mc_eff['comb'].SetBinContent(ib,x_pnet)
        
        if isData:
            xmin = int(h_data_eff['comb'].GetXaxis().GetBinLowEdge(ib)+0.3)
            xmax = int(h_data_eff['comb'].GetXaxis().GetBinLowEdge(ib+1)+0.3)
            xstring = '[%4i,%4i] | %4.2f+/-%4.2f | %4.2f+/-%4.2f | %4.2f+/-%4.2f |'%(xmin,xmax,h_data_eff['deeptau'].GetBinContent(ib),h_data_eff['deeptau'].GetBinError(ib),h_data_eff['pnet'].GetBinContent(ib),h_data_eff['pnet'].GetBinError(ib),h_data_eff['comb'].GetBinContent(ib),h_data_eff['comb'].GetBinError(ib))
        else:
            xmin = int(h_mc_eff['comb'].GetXaxis().GetBinLowEdge(ib)+0.3)
            xmax = int(h_mc_eff['comb'].GetXaxis().GetBinLowEdge(ib+1)+0.3)
            xstring = '[%4i,%4i] | %4.2f+/-%4.2f | %4.2f+/-%4.2f | %4.2f+/-%4.2f |'%(xmin,xmax,h_mc_eff['deeptau'].GetBinContent(ib),h_mc_eff['deeptau'].GetBinError(ib),h_mc_eff['pnet'].GetBinContent(ib),h_mc_eff['pnet'].GetBinError(ib),h_mc_eff['comb'].GetBinContent(ib),h_mc_eff['comb'].GetBinError(ib))
        print(xstring)        
    print('------------+-------------+-------------+-------------+')

    canv_name = 'canvas_mc'
    if isData: canv_name = 'canv_data'
    canv = styles.MakeCanvas(canv_name,"",700,600)

    if isData:
        h_data_eff['comb'].Draw("e1")
        h_data_eff['pnet'].Draw("e1same")
        h_data_eff['deeptau'].Draw("e1same")
    else:
        h_mc_eff['comb'].Draw("e1")
        h_mc_eff['pnet'].Draw("e1same")
        h_mc_eff['deeptau'].Draw("e1same")

    leg = ROOT.TLegend(0.55,0.2,0.9,0.45)
    styles.SetLegendStyle(leg)
    if isData:
        leg.SetHeader('Data')
    else:
        leg.SetHeader('Simulation')
    leg.SetTextSize(0.05)
    if isData:
        leg.AddEntry(h_data_eff['deeptau'],"HPS+DeepTau",'e1lp')
        leg.AddEntry(h_data_eff['pnet'],"PNet",'e1lp')
        leg.AddEntry(h_data_eff['comb'],"Combined",'e1lp')
    else:
        leg.AddEntry(h_mc_eff['deeptau'],"HPS+DeepTau",'e1lp')
        leg.AddEntry(h_mc_eff['pnet'],"PNet",'e1lp')
        leg.AddEntry(h_mc_eff['comb'],"Combined",'e1lp')
        
    leg.Draw()
    styles.CMS_label(canv,era=era)
    canv.SetLogx(True)
    canv.RedrawAxis()
    canv.Update()
    suffix = 'mc'
    if isData:
        suffix = 'data'
    canv.Print('/eos/home-r/rasp/php-plots/plots/HighPt/WTauNuTrig/TrigEff_'+wp+"VsJet_"+wpVsMu+'VsMu_'+wpVsE+'VsE_'+era+'_'+suffix+'.png')

    for opt in opts:
        canv_name = 'canvas_comp_'+opt
        if isData: canv_name = 'canv_data_'+opt
        canv = styles.MakeCanvas(canv_name,"",700,600)

        nbins = h_data_eff[opt].GetNbinsX()
        bins_data = []
        bins_mc = []
        for ib in range(1,nbins+2):
            x_pt = h_data_eff[opt].GetXaxis().GetBinLowEdge(ib)
            bins_mc.append(x_pt)
            bins_data.append(x_pt)

        name_mc = 'hmc_'+opt
        name_data = 'hdata_'+opt
        hmc = utils.createHisto(bins_mc,name_mc)
        hdata = utils.createHisto(bins_data,name_data)
        
        for ib in range(1,nbins+1):
            x_mc = h_mc_eff[opt].GetBinContent(ib)
            e_mc = h_mc_eff[opt].GetBinError(ib)
            hmc.SetBinContent(ib,x_mc)
            hmc.SetBinError(ib,e_mc)
            x_data = h_data_eff[opt].GetBinContent(ib)
            e_data = h_data_eff[opt].GetBinError(ib)
            hdata.SetBinContent(ib,x_data)
            hdata.SetBinError(ib,e_data)

        print('')
        print('Option : %s'%(opt))
        print('------------+-------------+-------------+')
        print('pT bin (GeV)|    Data     | Simulation  |')
        print('------------+-------------+-------------+')    
        for iB in range(1,nbins+1):
            xmin = int(hdata.GetXaxis().GetBinLowEdge(iB)+0.3)
            xmax = int(hdata.GetXaxis().GetBinLowEdge(iB+1)+0.3)
            xdata = hdata.GetBinContent(iB)
            edata = hdata.GetBinError(iB)
            xmc = hmc.GetBinContent(iB)
            emc = hmc.GetBinError(iB)
            xstring = '[%4i,%4i] | %4.2f+/-%4.2f | %4.2f+/-%4.2f |'%(xmin,xmax,xdata,edata,xmc,emc)
            print(xstring)        
        print('------------+-------------+-------------+')
            
        
        styles.InitData(hdata)
        styles.InitData(hmc)

        hdata.SetMarkerSize(1.2)
        hmc.SetMarkerSize(1.2)
        hdata.SetMarkerColor(1)
        hmc.SetMarkerColor(2)
        hdata.SetMarkerStyle(20)
        hmc.SetMarkerStyle(21)
        hdata.SetLineColor(1)
        hmc.SetLineColor(2)
        hdata.SetLineWidth(2)
        hmc.SetLineWidth(2)

        hdata.GetXaxis().SetTitle('tau p_{T} (GeV)')
        hdata.GetYaxis().SetTitle('Trigger efficiency')
        hdata.GetYaxis().SetTitleOffset(1.2)
        hmc.GetXaxis().SetTitle('tau p_{T} (GeV)')
        hmc.GetYaxis().SetTitle('Trigger efficiency')
        hmc.GetYaxis().SetTitleOffset(1.2)

        xmin = hdata.GetXaxis().GetBinLowEdge(1)+5.
        xmax = hdata.GetXaxis().GetBinLowEdge(nbins+1)-5.
        hdata.GetYaxis().SetRangeUser(0.01,1.29)
        hdata.GetXaxis().SetRangeUser(xmin,xmax)
        hmc.GetYaxis().SetRangeUser(0.01,1.29)
        hmc.GetXaxis().SetRangeUser(xmin,xmax)

        hdata.GetXaxis().SetMoreLogLabels()
        hdata.GetXaxis().SetNoExponent()
        hmc.GetXaxis().SetMoreLogLabels()
        hmc.GetXaxis().SetNoExponent()
        
        canv_name = 'canv_'+opt
        canv = styles.MakeCanvas(canv_name,"",700,600)
        
        
        hmc.Draw("e")
        hdata.Draw("esame")
        hmc.Draw("esame")
        
        leg = ROOT.TLegend(0.55,0.2,0.9,0.45)
        styles.SetLegendStyle(leg)
        if opt=='pnet':
            leg.SetHeader('PNet')
        elif opt=='deeptau':
            leg.SetHeader('HPS+DeepTau')
        else:
            leg.SetHeader('Combined')
            leg.SetTextSize(0.05)
        leg.AddEntry(hdata,"Data",'e1lp')
        leg.AddEntry(hmc,"Simulation",'e1lp')
        leg.Draw()
        styles.CMS_label(canv,era=era)
        canv.SetLogx(True)
        canv.RedrawAxis()
        canv.Update()
        suffix = opt+'_comp'
        canv.Print('/eos/home-r/rasp/php-plots/plots/HighPt/WTauNuTrig/TrigEff_'+wp+"VsJet_"+wpVsMu+'VsMu_'+wpVsE+'VsE_'+era+'_'+suffix+'.png')

    
    return True

    
def PlotSF(h_data_eff,h_mc_eff,**kwargs):
    wp = kwargs.get('wp','Medium')
    wpVsE  = kwargs.get('wpVsE','TightVsE')
    wpVsMu = kwargs.get('wpVsMu','TightVsMu')
    era = kwargs.get('era','era')
    opt = kwargs.get('option','comb')

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
        print('[%2i,%2i] : %6.4f +/- %6.4f'%(int(xlow),int(xhigh),x,e))
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


    styles.InitModel(hfit,4)
    hfit.SetFillColor(ROOT.kCyan)
    hfit.SetFillStyle(1001)
    hfit.SetLineWidth(2)
    hfit.SetLineColor(4)
    hfit.SetMarkerSize(0)
    hfit.SetMarkerStyle(0)
    hfit.GetYaxis().SetRangeUser(0.5001,1.4999)
    hfit.GetXaxis().SetTitle("#tau p_{T} [GeV]")
    hfit.GetYaxis().SetTitle("Trigger Efficiency SF")
    hfit.GetYaxis().SetTitleOffset(1.2)

    hfit.GetXaxis().SetMoreLogLabels()
    hfit.GetXaxis().SetNoExponent()

    hfit.Draw("e2")
    hfitline.Draw("hsame")
    histToPlot.Draw("e1same")

    leg = ROOT.TLegend(0.5,0.2,0.7,0.4)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.06)
    if opt=='deeptau':
        leg.SetHeader('HPS+DeepTau')
    elif opt=='pnet':
        leg.SetHeader('PNet')
    else:
        leg.SetHeader('Combined')
    
    leg.AddEntry(histToPlot,"SF",'e1lp')
    leg.AddEntry(hfit,'Fit','lf')
    leg.Draw()

    styles.CMS_label(canv,era=era)

    canv.SetLogx(True)
    canv.RedrawAxis()
    canv.Update()
    canv.Print('/eos/home-r/rasp/php-plots/plots/HighPt/WTauNuTrig/TrigSF_'+era+'_'+wp+'VsJet_'+wpVsMu+'VsMu_'+wpVsE+'VsE_'+opt+'.png')

    return x,a,k,b
    
def ComputeEff(hists,**kwargs):

    opt = kwargs.get('option','comb')
    
    h_data_p = hists['h_data_trig'].Clone('h_data_p')
    h_data_f = hists['h_data_notrig'].Clone('h_data_f')

    h_mc_p = hists['h_sig_trig'].Clone('h_data_p')
    h_mc_f = hists['h_sig_notrig'].Clone('h_data_f')

    nbins = h_data_p.GetNbinsX()
    for ib in range(1,nbins+1):
        # passing probes:
        bkg = hists['h_fake_trig'].GetBinContent(ib)
        ebkg = hists['h_fake_trig'].GetBinContent(ib)
        data = h_data_p.GetBinContent(ib)
        if bkg<0.0:
            hists['h_fake_trig'].SetBinContent(ib,0.)
            hists['h_fake_trig'].SetBinError(ib,0.)
        if bkg>data:
            hists['h_fake_trig'].SetBinContent(ib,0.5*data)
            hists['h_fake_trig'].SetBinError(ib,0.5*ebkg)
        # failing probes:
        bkg = hists['h_fake_notrig'].GetBinContent(ib)
        ebkg = hists['h_fake_notrig'].GetBinContent(ib)
        data = h_data_f.GetBinContent(ib)
        if bkg<0.0:
            hists['h_fake_notrig'].SetBinContent(ib,0.)
            hists['h_fake_notrig'].SetBinError(ib,0.)
        if bkg>data:
            hists['h_fake_notrig'].SetBinContent(ib,0.5*data)
            hists['h_fake_notrig'].SetBinError(ib,0.5*ebkg)
        

            
    h_data_p.Add(h_data_p,hists['h_fake_trig'],1.,-1.)
    h_data_p.Add(h_data_p,hists['h_bkg_trig'],1.,-1.)
    h_data_f.Add(h_data_f,hists['h_fake_notrig'],1.,-1.)
    h_data_f.Add(h_data_f,hists['h_bkg_notrig'],1.,-1.)

    h_mc_p.Add(h_mc_p,hists['h_tau_trig'],1.,1.)
    h_mc_f.Add(h_mc_f,hists['h_tau_notrig'],1.,1.)

    data_eff = utils.dividePassProbe(h_data_p,h_data_f,'h_data_eff')
    mc_eff   = utils.dividePassProbe(h_mc_p,h_mc_f,'h_mc_eff')

    nbins = data_eff.GetNbinsX()
    
    for ib in range(1,nbins+1):
        
        x = data_eff.GetBinContent(ib)
        e = data_eff.GetBinError(ib)
        if x<0.01:
            data_eff.SetBinContent(ib,0.01)
            data_eff.SetBinError(ib,0.01)
        if x>0.99:
            data_eff.SetBinContent(ib,eff_saturated[opt][0])
            data_eff.SetBinError(ib,eff_saturated[opt][1])
            
        x = mc_eff.GetBinContent(ib)
        e = mc_eff.GetBinError(ib)
        if x<0.01:
            mc_eff.SetBinContent(ib,0.01)
            mc_eff.SetBinError(ib,0.01)
        if x>0.99:
            mc_eff.SetBinContent(ib,eff_saturated[opt][0])
            mc_eff.SetBinError(ib,eff_saturated[opt][1])
        if e>0.06:
            mc_eff.SetBinError(ib,0.06)
        e = mc_eff.GetBinError(ib)

    if opt=='deeptau':
        print('')
        print('---------------------------')
        print('deeptau MC efficiency')
        for ib in range(1,nbins+1):
            x = mc_eff.GetBinContent(ib)
            e = mc_eff.GetBinError(ib)
            print('%1i %5.3f+/-%5.3f'%(ib,x,e))
        print('')
        print('---------------------------')
        print('')
        print('')
    return data_eff,mc_eff

##########################
# Plotting distributions #
##########################
def PlotWToTauNu(hists,**kwargs):

    wp = kwargs.get("wp","Medium")
    wpVsMu = kwargs.get("wpVsMu","Tight")
    wpVsE = kwargs.get("wpVsE","Tight")
    era = kwargs.get("era","2024")
    trigger = kwargs.get("trigger","_trig")
    option = kwargs.get("option","comb")
    var = kwargs.get("variable","pt_1")

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

    utils.differentialHisto(h_data)
    utils.differentialHisto(h_sig)
    utils.differentialHisto(h_fake)
    utils.differentialHisto(h_tot)
    for iB in range(1,nbins+1):
        e = h_tot.GetBinError(iB)
        x = h_tot.GetBinContent(iB)
        ratio = e/x
        if ratio>0.2:
            error = 0.2*x
            h_tot.SetBinError(iB,0.2*x)
        e = h_tot.GetBinError(iB)
        err = e
        if trigger=='_trig':
            err = math.sqrt(e*e+0.003*x*x)
        else:
            err = math.sqrt(e*e+0.002*x*x)
        h_tot.SetBinError(iB,err)
        e = h_tot.GetBinError(iB)
        x = h_tot.GetBinContent(iB)
        ratio = e/x
        print('%1i %6.1f+/-%6.1f  : %5.3f'%(iB,x,e,ratio))
    
    h_ratio = utils.histoRatio(h_data,h_tot,'ratio')
    h_tot_ratio = utils.createUnitHisto(h_tot,'tot_ratio')

    styles.InitRatioHist(h_ratio)

    h_ratio.GetYaxis().SetRangeUser(0.501,1.499)
    
    nbins = h_ratio.GetNbinsX()

    utils.zeroBinErrors(h_sig)
    utils.zeroBinErrors(h_bkg)
    utils.zeroBinErrors(h_fake)
    utils.zeroBinErrors(h_tau)

    h_data.GetXaxis().SetLabelSize(0)
    h_data.GetYaxis().SetTitle("dN/dp_{T} (GeV^{-1})")
    h_data.GetYaxis().SetTitleOffset(1.2)
    h_ratio.GetYaxis().SetTitle("obs/exp")
    h_ratio.GetXaxis().SetTitle(utils.XTitle[var])

    h_data.GetXaxis().SetMoreLogLabels()
    h_data.GetXaxis().SetNoExponent()
        
    ymax = h_tot.GetMaximum()
    ymin = h_tot.GetMinimum()

    h_data.GetYaxis().SetRangeUser(0.1*ymin,50.0*ymax)
    
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
    h_data.Draw('e1same')
    h_tot.Draw('e2same')

    leg = ROOT.TLegend(0.6,0.52,0.8,0.78)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.05)
    if trigger=='_trig':
        leg.SetHeader("passing probes")
    else:
        leg.SetHeader("failing probes")
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_sig,'genuine #tau','f')
    leg.AddEntry(h_fake,'misID #tau','f')
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
    canvas.Print("/eos/home-r/rasp/php-plots/plots/HighPt/WTauNuTrig/tauTrigger_"+era+"_"+wp+"VsJet_"+wpVsMu+"VsMu_"+wpVsE+"VsE"+trigger+"_"+option+".png")


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

        hists = {}
        files = {'_trig': fileCardsTrig[opt], '_notrig': fileCardsNotTrig[opt]}
        for trigLabel in ['_trig','_notrig']:
            for name in names:
                nameBase = names[name]
                nameHist = nameBase
                if nameBase=='wtaunu' or nameBase=='tau':
                    nameHist = nameBase + trigLabel + '_' + args.era
                full_name = name+trigLabel
                hists[full_name] = files[trigLabel].Get('taunu/'+nameHist)
                if nameBase=='wtaunu':
                    for sysname in sys_signal:
                        nameHist = nameBase + trigLabel + '_' + args.era + '_' + sysname + '_' + args.era + 'Up'
                        full_name = name + trigLabel + '_' +sysname
                        hists[full_name] = files[trigLabel].Get('taunu/'+nameHist)
                if nameBase=='fake':
                    for s in fake_samples:
                        for r in ptratio:
                            for t in pttau:
                                sysName = '%s_%s_%s%s_%sUp'%(s,r,t,trigLabel,args.era)
                                nameHist = nameBase+'_'+sysName
                                full_name = '%s%s_%s_%s_%s'%(name,trigLabel,s,r,t)
                                hists[full_name] = files[trigLabel].Get('taunu/'+nameHist)
                                
        AddSyst(hists)

        h_data_eff[opt],h_mc_eff[opt] = ComputeEff(hists,option=opt)
        for trigLabel in ['_trig','_notrig']:
            PlotWToTauNu(hists,
                         wp=args.wp,
                         wpVsMu=args.wpVsMu,
                         wpVsE=args.wpVsE,
                         era=args.era,
                         trigger=trigLabel,
                         option=opt)
            
    stauts = PlotEff(h_data_eff,
                     h_mc_eff,
                     wp=args.wp,
                     wpVsMu=args.wpVsMu,
                     wpVsE=args.wpVsE,
                     era=args.era,
                     isData=True)
    
    status = PlotEff(h_data_eff,
                     h_mc_eff,
                     wp=args.wp,
                     wpVsMu=args.wpVsMu,
                     wpVsE=args.wpVsE,
                     era=args.era,
                     isData=False)

    sf = {}
    a = {}
    k = {}
    b = {}
    for opt in opts:
        sf[opt],a[opt],k[opt],b[opt] = PlotSF(h_data_eff[opt],
                                              h_mc_eff[opt],               
                                              wp=args.wp,
                                              wpVsE=args.wpVsE,
                                              wpVsMu=args.wpVsMu,
                                              era=args.era,
                                              option=opt)
        
    print('')
    print('----------')
    print('%sVSjet %sVSmu %sVSe'%(args.wp,args.wpVsMu,args.wpVsE))
    for opt in opts:
        print('%7s : SF = %6.4f +/- %6.4f + %6.4f*pT[GeV]   max = %5.3f'%(opt,sf[opt],a[opt],abs(k[opt]),b[opt])) 
