#! /usr/bin/env python3
# Author: Alexei Raspereza (December 2022)
# High pT tau ID SF measurements 
# Datacards producer for the signal region (W*->tau+v) 
import ROOT
import os
from array import array
import math
import HighPT.Tau.utilsHighPT as utils
import HighPT.Tau.stylesHighPT as styles
import HighPT.Tau.analysisHighPT as analysis
from HighPT.Tau.FakeFactor import FakeFactorHighPt

#################################
#     definition of samples     #
#################################
BkgSampleNames = { 
    'Run2' : ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ','ZJetsToNuNu_HT-100To200','ZJetsToNuNu_HT-200To400','ZJetsToNuNu_HT-400To600','ZJetsToNuNu_HT-600To800','ZJetsToNuNu_HT-800To1200','ZJetsToNuNu_HT-1200To2500'],

    '2022' :  ['DYto2L-4Jets_MLL-50','TTTo2L2Nu','TTtoLNu2Q','TTto4Q','TWminustoLNu2Q','TWminusto2L2Nu','TbarWplustoLNu2Q','TbarWplusto2L2Nu','WW','WZ','ZZ','Zto2Nu-4Jets_HT-100to200','Zto2Nu-4Jets_HT-200to400','Zto2Nu-4Jets_HT-400to800','Zto2Nu-4Jets_HT-800to1500'],

    '2023' : ['DYto2L-4Jets_MLL-50','TTto2L2Nu','TTtoLNu2Q','TTto4Q','TWminustoLNu2Q','TWminusto2L2Nu','TbarWplustoLNu2Q','TbarWplusto2L2Nu','WW','WZ','ZZ','Zto2Nu-4Jets_HT-100to200','Zto2Nu-4Jets_HT-200to400','Zto2Nu-4Jets_HT-400to800','Zto2Nu-4Jets_HT-800to1500']
}

WBkgSampleNames = {
    'Run2' : ['WJetsToLNu'],

    '2022' : ['WJetsToLNu-4Jets_1J','WJetsToLNu-4Jets_2J','WJetsToLNu-4Jets_3J','WJetsToLNu-4Jets_4J','WtoLNu-4Jets_HT-100to400','WtoLNu-4Jets_HT-400to800'],

    '2023' : ['WtoLNu-4Jets_1J','WtoLNu-4Jets_2J','WtoLNu-4Jets_3J','WtoLNu-4Jets_4J','WtoLNu_HT100to400','WtoLNu_HT400to800']
}

SigSampleNames = { 
    'Run2' : ['WToTauNu_M-200'],
    '2022' : ['WtoNuTau'],
    '2023' : ['WtoNuTau']
}

def FitRatio(x,par):
#    a = 0.01*(x[0]-100.)
#    return par[0]+par[1]*a+par[2]*a*a
    return par[0]

def CorrectForNonClosure(hist,ratio,name):
    
    histCentral = hist.Clone(name);
    nbins = hist.GetNbinsX();
    for ib in range(1,nbins+1):
        x = hist.GetBinContent(ib)
        e = hist.GetBinError(ib)
        r = ratio.GetBinContent(ib)
        central = x*r
        centralE = e*r
        histCentral.SetBinContent(ib,central)
        histCentral.SetBinError(ib,centralE)
    return histCentral


##################################
# computing j->tau fake template #
################################## 
def ComputeFake(h_wjets,h_dijets,h_fraction,name):
    nbins = h_wjets.GetNbinsX()
    hist = h_wjets.Clone(name)
    print('')
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
        hist.SetBinContent(i,x_fakes)
        hist.SetBinError(i,e_fakes)
        lowerEdge = hist.GetBinLowEdge(i)
        upperEdge = hist.GetBinLowEdge(i+1)
        print("[%3d,%4d] = %6.1f +/- %4.1f" %(lowerEdge,upperEdge,x_fakes,e_fakes))

    return hist

##################################
# compute EWK fraction histogram #
# in FF application region       #
##################################
def ComputeEWKFraction(h_data,h_mc,var):

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
        if var in ['eta_1','phi_1','metphi']:
            print("[%5.2f,%5.2f] = %4.2f +/- %4.2f (%4.2f rel) -> Data = %6.0f : MC = %6.0f" %(lowerEdge,upperEdge,ratio,eratio,eratio/ratio,xdata,xmc))
        else:
            print("[%3d,%4d] = %4.2f +/- %4.2f (%4.2f rel) -> Data = %6.0f : MC = %6.0f" %(lowerEdge,upperEdge,ratio,eratio,eratio/ratio,xdata,xmc))

    return h_fraction

############################
###### Closure test ########
############################
def PlotClosure(hists,**kwargs): 

    wp = kwargs.get('wp','Medium') 
    era = kwargs.get('era','2023') 
    var = kwargs.get('var','mt_1')
    basename = kwargs.get('basename','bkgd')
    uncs = kwargs.get('uncs',[''])
    wpVsMu = kwargs.get('wpVsMu') 
    wpVsE = kwargs.get('wpVsE')
    suffix = kwargs.get('suffix','')

    print('')
    print('Plotting closure')
    h_data = hists[basename+'_fake_SR']
    h_model = hists[basename+"_fake_mc_wjets"]    
    
    styles.InitData(h_data)
    h_tot = h_model.Clone('h_tot_model')
    # add systematic uncertainties
    print("           =      Data      :    Model")
    nbins = h_tot.GetNbinsX()
    for i in range(1,nbins+1):
        error2 = h_tot.GetBinError(i)*h_tot.GetBinError(i)
        errorStat = h_tot.GetBinError(i)
        xcen = h_tot.GetBinContent(i)
        xdata = h_data.GetBinContent(i)
        edata = h_data.GetBinError(i)
        for unc in uncs:
            name = basename + "_fake_mc_wjets_" + unc
            xsys = hists[name].GetBinContent(i)
            error2 += (xcen-xsys)*(xcen-xsys)
        error = math.sqrt(error2)
        lowerEdge = h_tot.GetBinLowEdge(i)
        upperEdge = h_tot.GetBinLowEdge(i+1)
        if var in['eta_1','phi_1','metphi']:
            print("[%5.2f,%5.2f] = %5.1f +/- %4.1f : %5.1f +/- %4.1f" %(lowerEdge,upperEdge,xdata,edata,xcen,error))
        else:
            print("[%3d,%4d] = %5.1f +/- %4.1f : %5.1f +/- %4.1f" %(lowerEdge,upperEdge,xdata,edata,xcen,error))
        h_tot.SetBinError(i,error)
                
    styles.InitTotalHist(h_tot)
    styles.InitModel(h_model,2)

    hist_ratio = utils.divideHistos(h_data,h_model,'ratio_model')
    hist_unit = utils.createUnitHisto(h_tot,'ratio_model_unit')

    styles.InitRatioHist(hist_ratio)
    hist_ratio.GetYaxis().SetRangeUser(0.001,1.999)
    utils.zeroBinErrors(h_model)

    yMax = h_data.GetMaximum()
    if h_model.GetMaximum()>yMax: yMax = h_model.GetMaximum()
    h_data.GetYaxis().SetRangeUser(0.,1.2*yMax)
    h_data.GetXaxis().SetLabelSize(0)
    h_model.GetYaxis().SetTitle('events/bin')

    # canvas
    canvas = styles.MakeCanvas("canv_cl","",600,700)
    # upper panel
    upper = ROOT.TPad("upper_cl","pad",0,0.31,1,1)
    upper.Draw()
    upper.cd()
    styles.InitUpperPad(upper)
    h_data.Draw("e1")
    h_model.Draw("hsame")
    h_tot.Draw("e2same")
    h_data.Draw("e1same")

    leg = ROOT.TLegend(0.53,0.25,0.78,0.5)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.043)
    leg.SetHeader('%s,%s,%s'%(wp,wpVsMu,wpVsE))
    leg.AddEntry(h_data, 'selection','lp')
    leg.AddEntry(h_model,'model','l')
    leg.Draw()

    styles.CMS_label(upper,era=era,extraText='Simulation')

    upper.Draw("SAME")
    upper.RedrawAxis()
    upper.Modified()
    upper.Update()
    canvas.cd()

    # lower panel
    lower = ROOT.TPad("lower", "pad",0,0,1,0.30)
    lower.Draw()
    lower.cd()
    styles.InitLowerPad(lower)

    xmin = hist_ratio.GetXaxis().GetBinLowEdge(1)    
    xmax = hist_ratio.GetXaxis().GetBinLowEdge(nbins+1)
    func = ROOT.TF1("func",FitRatio,xmin,xmax,1)
    func.SetParameter(0,1.0)
    #    func.SetParameter(1,0.0)
    #    func.SetParameter(2,0.0)
    func.SetLineColor(4)

    hist_ratio.GetXaxis().SetTitle(utils.XTitle[var])
    hist_ratio.GetYaxis().SetTitle('ratio')

    hist_fit = hist_ratio.Clone('hist_fit')
    hist_fit.Fit('func','R')
    hist_ratio.Draw('e1')
    hist_unit.Draw('e2same')
    hist_ratio.Draw('e1same')
    nbins = hist_ratio.GetNbinsX()
    line = ROOT.TLine(xmin,1.,xmax,1.)
    line.SetLineStyle(1)
    line.SetLineWidth(2)
    line.SetLineColor(2)
    line.Draw()
    lower.Modified()
    lower.RedrawAxis()

    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    canvas.Print(utils.baseFolder+"/"+era+"/figures/WTauNu/closure_"+var+suffix+"_"+wp+"VsJet_"+wpVsMu+"VsMu_"+wpVsE+"VsE"+".png")

    return hist_ratio

##########################
# Plotting distributions #
##########################
def PlotWToTauNu(hists,**kwargs):

    wp = kwargs.get('wp','Medium')
    era = kwargs.get('era','2023')
    var = kwargs.get('var','mt_1')
    plotLegend = kwargs.get('plotLegend',True)
    wpVsMu = kwargs.get('wpVsMu','Tight')
    wpVsE = kwargs.get('wpVsE','Tight')
    suffix = kwargs.get('suffix','')

    h_data = hists['hist_data'].Clone("data_plot")
    h_fake = hists['hist_fake'].Clone("fake_plot")
    h_bkg = hists['hist_bkg_lfakes'].Clone("bkg_plot")
    h_tau = hists['hist_bkg_tau'].Clone("tau_plot")
    h_sig = hists['hist_sig'].Clone("sig_plot")

    # log-normal uncertainties 
    #  5% signal, 
    # 10% fake, 
    # 20% genuine tau background
    # 50% lfakes
    nbins = h_data.GetNbinsX()
    e_sig_sys = 0.05
    e_fake_sys = 0.15
    e_bkg_sys = 0.50
    e_tau_sys = 0.20
    print('')
    print('Plotting distribution of',var)
    print('            - data :   mc')
#    print('[ 200, 300] = 1993 : 1942')
    for i in range(1,nbins+1):
        x_sig = h_sig.GetBinContent(i)
        x_bkg = h_bkg.GetBinContent(i)
        x_tau = h_tau.GetBinContent(i)
        x_fake = h_fake.GetBinContent(i)
        e_sig_stat = h_sig.GetBinError(i)
        x_data = h_data.GetBinContent(i)
        x_model = x_sig + x_bkg + x_tau + x_fake
        e_sig = math.sqrt(e_sig_stat*e_sig_stat+e_sig_sys*e_sig_sys*x_sig*x_sig)
        h_sig.SetBinError(i,e_sig)
        e_bkg_stat = h_bkg.GetBinError(i)
        e_bkg = math.sqrt(e_bkg_stat*e_bkg_stat+e_bkg_sys*e_bkg_sys*x_bkg*x_bkg)
        h_bkg.SetBinError(i,e_bkg)
        e_tau_stat = h_tau.GetBinError(i)
        e_tau = math.sqrt(e_tau_stat*e_tau_stat+e_tau_sys*e_tau_sys*x_tau*x_tau)
        h_tau.SetBinError(i,e_tau)
        e_fake_stat = h_fake.GetBinError(i)
        e_fake = math.sqrt(e_fake_stat*e_fake_stat+e_fake_sys*e_fake_sys*x_fake*x_fake)
        h_fake.SetBinError(i,e_fake)
        lowerEdge = h_data.GetBinLowEdge(i)
        upperEdge = h_data.GetBinLowEdge(i+1)
        if var in ['eta_1','phi_1','metphi']:
            print("[%5.2f,%5.2f] = %4.0f : %4.0f" %(lowerEdge,upperEdge,x_model,x_data))
        else:
            print("[%4i,%4i] = %4.0f : %4.0f" %(lowerEdge,upperEdge,x_model,x_data))

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

    h_ratio.GetYaxis().SetRangeUser(0.01,1.99)
    
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

    h_dummy = ROOT.TH1D('dummy','',2,0,1)
    h_dummy.SetMarkerSize(0)
    h_dummy.SetMarkerColor(0)

    leg = ROOT.TLegend(0.58,0.2,0.83,0.6)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.042)
    leg.SetHeader('%s,%s,%s'%(wp,wpVsMu,wpVsE))
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_sig,'W#rightarrow #tau#nu','f')
    leg.AddEntry(h_fake,'j#rightarrow#tau misId','f')
    leg.AddEntry(h_tau,'true #tau','f')
    leg.AddEntry(h_bkg,'e/#mu#rightarrow#tau misId','f')
    if plotLegend: leg.Draw()

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
    print('')
    canvas.Print(utils.baseFolder+"/"+era+"/figures/WTauNu/wtaunu_"+var+suffix+"_"+wp+"VsJet_"+wpVsMu+"VsMu_"+wpVsE+"VsE"+".png")

def CreateCardsWToTauNu(fileName,h_data,h_fake,h_tau,h_bkg,h_sig,uncs_fake,uncs_sig,suffix):

    x_data = h_data.GetSumOfWeights()
    x_fake = h_fake.GetSumOfWeights()
    x_tau  = h_tau.GetSumOfWeights()
    x_bkg  = h_bkg.GetSumOfWeights()    
    x_sig  = h_sig.GetSumOfWeights() 

    cardsFileName = fileName + ".txt"
    rootFileName = fileName + ".root"
    f = open(cardsFileName,"w")
    f.write("imax 1  number of channels\n")
    f.write("jmax *  number of backgrounds\n")
    f.write("kmax *  number of nuisance parameters\n")
    f.write("---------------------------\n")
    f.write("observation %3.1f\n"%(x_data))
    f.write("---------------------------\n")
    f.write("shapes * * "+rootFileName+"  taunu/$PROCESS taunu/$PROCESS_$SYSTEMATIC \n")
    f.write("---------------------------\n")
    f.write("bin       WtoTauNu%s  WtoTauNu%s  WtoTauNu%s  WtoTauNu%s\n"%(suffix,suffix,suffix,suffix))
    f.write("process   tau%s       wtaunu%s    fake        lfakes\n"%(suffix,suffix))
    f.write("process   -1          0           1           2\n")
    f.write("rate      %4.3f       %4.3f       %4.3f       %4.3f\n"%(x_tau,x_sig,x_fake,x_bkg))
    f.write("---------------------------\n")
    f.write("extrapW        lnN   -             1.04          -             -\n")
    f.write("bkgNorm_taunu  lnN   1.2           -             -             -\n")
    f.write("lep_fakes      lnN   -             -             -           1.5\n")
    for unc in uncs_sig:
        f.write(unc+"     shape   -             1.0           -             -\n")
    for unc in uncs_fake:
        f.write(unc+"     shape   -             -             1.0           -\n")
    f.write("normW  rateParam  WtoTauNu%s wtaunu%s  1.0  [0.5,1.5]\n"%(suffix,suffix))
    f.write("* autoMCStats 0\n")
    groups = "sysUnc group = normW extrapW bkgNorm_taunu lep_fakes"
    for unc in uncs_sig:
        groups = groups + " " + unc
    for unc in uncs_fake:
        groups = groups + " " + unc
    f.write(groups+"\n")
    f.close()

############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser

    def confirm_arguments(parsed_args):
        print("Parsed arguments:")
        print("Era:", parsed_args.era)
        print("WPvsJet:", parsed_args.wp)
        print("WPvsMu:", parsed_args.wpVsMu)
        print("WPvsE:", parsed_args.wpVsE)
        print("Variable:", parsed_args.variable)
        print("Fake factors:", parsed_args.ff)
        print("Measurement:", parsed_args.meas)
        
        confirmation = input("Are these arguments correct? (yes/no): ").strip().lower()
        return confirmation == "yes"

    def adjust_arguments():
        parser = ArgumentParser()
        parser.add_argument('-e','--era', dest='era', default='2023',choices=['UL2016','UL2017','UL2018','2022','2023'])
        parser.add_argument('-wp','--WP', dest='wp', default='Medium',choices=['Loose','Medium','Tight','VTight','VVTight'])
        parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight',choices=['VLoose','Tight'])
        parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VVLoose',choices=['VVLoose','Tight'])
        parser.add_argument('-var','--variable',dest='variable',default='mt_1',choices=['mt_1','met','pt_1','eta_1','phi_1','jpt_match_1','mt_jet_1','metphi'])
        parser.add_argument('-ff','--fake_factors',dest='ff',default='comb',choices=['comb','wjets','dijets'])
        parser.add_argument('-m','--meas',dest='meas',default='incl',choices=['incl','lowpt','highpt'])

        args = parser.parse_args()

        print("Options to adjust arguments:")
        print("1. Change era")
        print("2. Change WPvsJet")
        print("3. Change WPvsMu")
        print("4. Change WPvsE")
        print("5. Change variable to plot")
        print("6. Change fake factors to use")
        print("7. Change measurement to perform")                        
        print("8. Confirm and proceed")

        while True:
            choice = input("Enter your choice (1-8): ").strip()
            if choice == "1":
                args.era = input("Enter the era (UL2016, UL2017, UL2018, 2022, 2023): ").strip()
            elif choice == "2":
                args.wp = input("Enter the WPvsJet (Loose, Medium, Tight, VTight, VVTight): ").strip()
            elif choice == "3":
                args.wpVsMu = input("Enter the WPvsMu (VLoose, Tight): ").strip()
            elif choice == "4":
                args.wpVsE = input("Enter the WPvsE (VVLoose, Tight): ").strip()
            elif choice == "5":
                args.variable = input("Enter the variable to plot (mt_1, pt_1, met, phi_1, eta_1, metphi): ").strip()               
            elif choice == "6":
                args.ff = input("Enter the fake factors to use (comb, wjets, dijets): ").strip()
            elif choice == "7":
                args.meas = input("Enter the measurement to perform (incl, lowpt, highpt): ").strip()                         
            elif choice == "8":
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
        return args

    if __name__ == "__main__":
        while True:
            args = adjust_arguments()
            if confirm_arguments(args):
                break

 
    xbins_mt  = [200,300,400,500,600,800,1200]
    xbins_pt  = [100,130,160,190,220,250,300,400,500,700]
    xbins_jpt = [100,140,180,220,260,300,400,500,700]
    xbins_met = [100,150,200,250,300,400,500,700]
    xbins_mt_lowpt = [200,250,300,350,400,1000]
    xbins_mt_highpt = [200,400,500,600,700,900,1200]

    xbins_phi = utils.createBins(14,-3.14,3.14)
    xbins_metphi = utils.createBins(14,-3.14,3.14)
    xbins_eta = utils.createBins(14,-2.3,2.3)

    xbins = xbins_mt
    ptMin = 100.
    ptMax = 2000.
    suffix = '_'+args.era
    if args.variable=='mt_1' or args.variable=='mt_jet_1':
        if args.meas=='lowpt': 
            xbins = xbins_mt_lowpt
            ptMin = 100.
            ptMax = 200.
            suffix = '_'+args.meas+'_'+args.era
        elif args.meas=='highpt':
            xbins = xbins_mt_highpt
            ptMin = 200.
            ptMax = 2000.
            suffix = '_'+args.meas+'_'+args.era

    plotLegend = True
    if args.variable=='pt_1': xbins = xbins_pt
    if args.variable=='met': xbins = xbins_met
    if args.variable=='jpt_match_1':
        xbins = xbins_jpt
    if args.variable=='eta_1': 
        xbins =  xbins_eta
        plotLegend = False
    if args.variable=='phi_1': 
        xbins = xbins_phi
        plotLegend = False
    if args.variable=='metphi':
        xbins = xbins_metphi
        plotLegend = False

    basefolder = utils.picoFolder+'/'+args.era
    var = args.variable    

    ff = args.ff

    # initializing instance of FakeFactorHighPT class    
    fullpathFF = utils.baseFolder+'/'+args.era+'/FF/ff_'+args.wp+"VSjet_"+args.wpVsMu+"VSmu_"+args.wpVsE+"VSe_"+args.era+".root"
    samples = []
    with_dijets = False
    if ff=='wjets':
        samples.append('wjets')
    elif ff=='dijets':
        samples.append('dijets')
        with_dijets = True
    else:
        samples.append('wjets')
        samples.append('dijets')
        with_dijets = True
    
    fakeFactor = FakeFactorHighPt(filename=fullpathFF,
                                  variable1='pttau',
                                  variable2='ptratio',
                                  with_dijets=with_dijets)

    # initializing instance of TauNuCuts class
    antiMu = utils.tauVsMuIntWPs[args.wpVsMu]
    antiE  = utils.tauVsEleIntWPs[args.wpVsE]
    hotJetVeto = False
    if args.era=='2023': hotJetVeto = True
    wtaunuCuts = analysis.TauNuCuts(antiMu=antiMu,
                                    antiE=antiE,
                                    ptLowerCut=ptMin,
                                    ptUpperCut=ptMax,
                                    hotJetVeto=hotJetVeto)    

    # vector uncertainties
    uncert_names = utils.uncs

    # eras
    eras = utils.periods[args.era]

    print('')
    print('initializing data samples >>>')
    metSamples = {} 
    for era in eras:
        metNames = utils.met[era]
        for metName in metNames:
            name = metName
            metSamples[name] = analysis.sampleHighPt(basefolder,era,
                                                      "taunu",metName,True)
            metSamples[name].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print('')
    print('initializing W background samples >>>')
    wbkgSamples = {}
    for era in eras:
        run = utils.eraRun[era]
        wbkgSampleNames = WBkgSampleNames[run]
        for wbkgSampleName in wbkgSampleNames:
            name = wbkgSampleName + '_' + era
            if wbkgSampleName in utils.MCLowHT:
                wbkgSamples[name] = analysis.sampleHighPt(basefolder,era,
                                                          "taunu",wbkgSampleName,
                                                          False,additionalCut="(HT<100||HT>800)",
                                                          applyHTcut=True)
            else:
                wbkgSamples[name] = analysis.sampleHighPt(basefolder,era,
                                                          "taunu",wbkgSampleName,
                                                          False)
            wbkgSamples[name].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print('')
    print('initializing background samples >>>')
    bkgSamples = {}
    for era in eras:
        run = utils.eraRun[era]
        bkgSampleNames = BkgSampleNames[run]
        for bkgSampleName in bkgSampleNames:
            name = bkgSampleName + '_' + era
            bkgSamples[name] = analysis.sampleHighPt(basefolder,era,
                                                     "taunu",bkgSampleName,
                                                     False)
            bkgSamples[name].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print('')
    print('initializing signal samples >>>')
    sigSamples = {} 
    for era in eras:
        run = utils.eraRun[era]
        sigSampleNames = SigSampleNames[run]
        for sigSampleName in sigSampleNames:
            name = sigSampleName + '_' + era
            sigSamples[name] = analysis.sampleHighPt(basefolder,era,
                                                     "taunu",sigSampleName,False)
            sigSamples[name].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    # defining baseline cuts
    commonCut = "metfilter>0.5&&mettrigger>0.5&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&njets==0&&idDeepTau2018v2p5VSmu_1>="+utils.tauVsMuWPs[args.wpVsMu]+"&&idDeepTau2018v2p5VSe_1>="+utils.tauVsEleWPs[args.wpVsE]+"&&genmatch_1==5&&idDeepTau2018v2p5VSjet_1>=" + utils.tauWPs[args.wp]

    vetoHotSpot = "!(eta_1>%5.3f&&eta_1<%5.3f&&phi_1>%5.3f&&phi_1<%5.3f)"%(wtaunuCuts.etaHotMin,wtaunuCuts.etaHotMax,wtaunuCuts.phiHotMin,wtaunuCuts.phiHotMax)
    
    if args.era=='2023':
        commonCut += "&&hotjet_veto<0.5&&"+vetoHotSpot

    # running on signal samples (central template and unceertainties)
    print('')
    print('Running on signal samples >>>')
    hists_sig = {}
    lst = ['']
    if var in ['mt_1','mt_jet_1']: 
        lst += uncert_names
    for name in lst:

        name_unc = ""
        name_hist = "wtaunu"
        if name!="": 
            name_unc = "_"+name+"Up"
            name_hist = "wtaunu_"+name

        var_unc=var
        if var in ['mt_jet_1']:
            if name in ['JES','Unclustered']:
                var_unc=var+name_unc
        else:
            var_unc=var+name_unc
        
        metUnc = "met"+name_unc
        ptUnc = "pt_1"
        Uncertainty = ROOT.TString(name_unc)
        if Uncertainty.Contains("taues"):
            ptUnc = "pt_1"+name_unc
        mtUnc = "mt_1"+name_unc
        metdphiUnc = "metdphi_1"+name_unc

        metNoMuCut = "metnomu>%3.1f"%(wtaunuCuts.metNoMuCut)
        mhtNoMuCut = "mhtnomu>%3.1f"%(wtaunuCuts.mhtNoMuCut)
        metCut     = metUnc+">%3.1f"%(wtaunuCuts.metCut)
        ptLowerCut = ptUnc+">%3.1f"%(wtaunuCuts.ptLowerCut)
        ptUpperCut = ptUnc+"<%3.1f"%(wtaunuCuts.ptUpperCut)
        etaCut     = "fabs(eta_1)<%3.1f"%(wtaunuCuts.etaCut)
        metdphiCut = metdphiUnc+">%3.1f"%(wtaunuCuts.metdphiCut)
        mtLowerCut = mtUnc+">%3.1f"%(wtaunuCuts.mtLowerCut)
        mtUpperCut = mtUnc+"<%3.1f"%(wtaunuCuts.mtUpperCut)

        uncertCut =metNoMuCut+"&&"+mhtNoMuCut+"&&"+metCut+"&&"+ptLowerCut+"&&"+ptUpperCut+"&&"+etaCut+"&&"+metdphiCut+"&&"+mtLowerCut+"&&"+mtUpperCut
        totalCut = commonCut+"&&"+uncertCut+"&&genmatch_1==5"
        
        histo = analysis.RunSamples(sigSamples,var_unc,totalCut,xbins,name_hist)
        print('Running for signal sample %s'%(name_hist))
        hists_sig[name_hist] = histo

    # running selection ->
    print('')
    hists_data = analysis.RunSamplesTauNu(metSamples,var,xbins,"data")
    print('')
    hists_bkg  = analysis.RunSamplesTauNu(bkgSamples,var,xbins,"bkg")
    print('')
    hists_wbkg = analysis.RunSamplesTauNu(wbkgSamples,var,xbins,"wbkg")
    
    # summing up TTbar+SingleTop+DY+W backgrounds
    hists_totbkg = {}
    for histname in hists_bkg:
        hists_totbkg['tot'+histname] = hists_bkg[histname].Clone('tot'+histname)
        hists_totbkg['tot'+histname].Add(hists_totbkg['tot'+histname],hists_wbkg['w'+histname],1.,1.)

    # compute non-closure
    fake_uncs = fakeFactor.getUncertaintyList()
    nonclosure = PlotClosure(hists_totbkg,
                             basename='totbkg',
                             wp=args.wp,
                             era=args.era,
                             var=var,
                             wpVsMu=args.wpVsMu,
                             wpVsE=args.wpVsE,
                             uncs=fake_uncs,
                             suffix=suffix)
    
    # compute EWK fraction histogram in the FF aplication region
    h_data_dr = hists_data["data_all_SB"]
    h_data_dr.Add(h_data_dr,hists_totbkg['totbkg_notFake_SB'],1.,-1.)
    h_ewk_dr  = hists_totbkg["totbkg_fake_SB"]
    h_fraction = ComputeEWKFraction(h_data_dr,h_ewk_dr,var)

    # Create j->tau fake histograms
    hists_fake_sample_raw = {} 
    hists_fake_sample = {}
    print('')
    for sample in samples:
        hist_data_sample = hists_data['data_all_data_'+sample]
        hist_totbkg_sample = hists_totbkg['totbkg_notFake_data_'+sample]
        print('fake background %s : data = %4.0f   subtracted MC = %4.0f'%(sample,hist_data_sample.GetSumOfWeights(),hist_totbkg_sample.GetSumOfWeights()))
        hist_data_sample.Add(hist_data_sample,hist_totbkg_sample,1.,-1.)
        hists_fake_sample_raw[sample] = hist_data_sample 
        hists_fake_sample[sample] = CorrectForNonClosure(hist_data_sample,nonclosure,'fake')

    if ff=='comb': 
        hist_fake = ComputeFake(hists_fake_sample['wjets'],
                                hists_fake_sample['dijets'],
                                h_fraction,
                                'hist_fake')
        hist_fake_raw = ComputeFake(hists_fake_sample_raw['wjets'],
                                    hists_fake_sample_raw['dijets'],
                                    h_fraction,
                                    'hist_fake')
    else:
        hist_fake = hists_fake_sample[ff]
        hist_fake_raw = hists_fake_sample_raw[ff]
            
    
    # data histogram
    hist_data = hists_data["data_all_SR"]
    # signal histogram
    hist_sig = hists_sig["wtaunu"]
    # MC histograms
    hist_bkg_tau = hists_totbkg["totbkg_tau_SR"]
    hist_bkg_lfakes = hists_totbkg["totbkg_lepFake_SR"]
    hist_bkg_fakes = hists_totbkg["totbkg_fake_SR"]
    hist_bkg = hists_totbkg["totbkg_all_SR"] 
    tot_bkg = hist_bkg_tau.GetSumOfWeights()+hist_bkg_lfakes.GetSumOfWeights()+hist_bkg_fakes.GetSumOfWeights()
    
    print('')
    print("Check composition of MC")
    print('Total        = %4.0f'%(hist_bkg.GetSumOfWeights()))
    print('Genuine taus = %4.0f'%(hist_bkg_tau.GetSumOfWeights()))
    print('l->tau fakes = %4.0f'%(hist_bkg_lfakes.GetSumOfWeights()))
    print('j->tau fakes = %4.0f'%(hist_bkg_fakes.GetSumOfWeights()))
    print('Sum check    = %4.0f'%(tot_bkg))

    hist_bkg_tau = hists_bkg['bkg_tau_SR']
    print('')
    print('JetFakes = %4.0f'%(hist_fake.GetSumOfWeights()))
    print('LepFakes = %4.0f'%(hist_bkg_lfakes.GetSumOfWeights()))
    print('Taus     = %4.0f'%(hist_bkg_tau.GetSumOfWeights()))
    print('W*->tauv = %4.0f'%(hist_sig.GetSumOfWeights()))
    total = hist_fake.GetSumOfWeights()+hist_bkg_lfakes.GetSumOfWeights()+hist_bkg_tau.GetSumOfWeights()+hist_sig.GetSumOfWeights()
    print('')
    print('Total    = %4.0f'%(total))
    print('Data     = %4.0f'%(hist_data.GetSumOfWeights()))

    # making control plot
    histsToPlot = {}
    histsToPlot['hist_data'] = hist_data
    histsToPlot['hist_fake'] = hist_fake
    histsToPlot['hist_bkg_tau'] = hist_bkg_tau
    histsToPlot['hist_bkg_lfakes'] = hist_bkg_lfakes
    histsToPlot['hist_sig'] = hist_sig    
    PlotWToTauNu(histsToPlot,
                 wp=args.wp,
                 era=args.era,
                 var=var,
                 plotLegend=plotLegend,
                 wpVsMu=args.wpVsMu,
                 wpVsE=args.wpVsE,
                 suffix=suffix)

    if not var in['mt_1','mt_jet_1']:
        exit()

    # creating shape templates for fake model systematics
    hists_fake_sys = {}

    hist_closure_up,hist_closure_down = utils.ComputeSystematics(hist_fake,hist_fake_raw,'fake_nonclosure')
    name_sys = 'nonclosure_%s'%(args.era)
    names_fake_sys = [name_sys]
    hists_fake_sys['%sUp'%(name_sys)] = hist_closure_up
    hists_fake_sys['%sDown'%(name_sys)] = hist_closure_down
    # statistical uncertainties
    for sample in samples: # wjets, dijets
        for unc in fake_uncs:
            name_sys = sample+'_'+unc+'_'+args.era        
            data_sys = hists_data['data_all_data_%s_%s'%(sample,unc)]
            bkg_sys  = hists_totbkg['totbkg_notFake_data_%s_%s'%(sample,unc)]
            data_sys.Add(data_sys,bkg_sys,1.,-1.)
            hist_corr_x = CorrectForNonClosure(data_sys,nonclosure,name_sys)
            hist_corr = hist_corr_x 
            if ff=='comb':
                hist1 = hist_corr_x
                hist2 = hists_fake_sample['dijets']
                if sample=='dijets':
                    hist1 = hists_fake_sample['wjets']
                    hist2 = hist_corr_x
                hist_corr = ComputeFake(hist1,
                                        hist2,
                                        h_fraction,
                                        'hist_corr_%s_%s'%(sample,unc))
            
            hist_up,hist_down = utils.ComputeSystematics(hist_fake,hist_corr,'fake_%s_%s'%(sample,unc))
            names_fake_sys.append(name_sys)
            hists_fake_sys['%sUp'%(name_sys)] = hist_up
            hists_fake_sys['%sDown'%(name_sys)] = hist_down

    # creating shape templates for signal systematics 
    hists_sig_sys = {}
    names_sig_sys = []
    for unc in uncert_names:
        name_hist = 'wtaunu_'+unc
        name_sys = unc+'_'+args.era
        hist_sig_sys = hists_sig[name_hist]
        hist_up,hist_down = utils.ComputeSystematics(hist_sig,hist_sig_sys,name)
        names_sig_sys.append(name_sys)
        hists_sig_sys["%sUp"%(name_sys)] = hist_up
        hists_sig_sys["%sDown"%(name_sys)] = hist_down

    # # saving histograms to datacard file datacards
    # fileName = "taunu_"+args.wp+"_"+args.wpVsMu+"_"+args.wpVsE+suffix
    # outputFileName = utils.baseFolder+'/'+args.era+"/datacards/"+fileName
    
    # saving histograms to datacard file datacards
    FF = args.ff+"_"+args.wp+"_"+args.wpVsMu+"_"+args.wpVsE
    fileName = "taunu_"+FF+suffix
    outputFileName = utils.baseFolder + "/" + args.era + "/datacards_"+ FF + "/" + fileName
    # from IPython import embed 
    # embed()
    # Create the output directory if it doesn't exist
    if not os.path.exists(os.path.dirname(outputFileName)):
        print("The directory for datacards storage doesn't exist, it will be created here:", utils.baseFolder + "/" + args.era + "/datacards_"+ FF)
        os.makedirs(os.path.dirname(outputFileName))
    print("")
    print("Saving histograms to RooT file %s.root"%(outputFileName))
    fileOutput = ROOT.TFile(outputFileName+".root","recreate")
    fileOutput.mkdir("taunu")
    fileOutput.cd("taunu")
    hist_data.Write("data_obs")
    hist_sig.Write("wtaunu%s"%(suffix))
    hist_bkg_tau.Write("tau%s"%(suffix))
    hist_bkg_lfakes.Write("lfakes")
    hist_fake.Write("fake")
    # signal shape systematics
    for histName in hists_sig_sys:
        hists_sig_sys[histName].Write('wtaunu%s_%s'%(suffix,histName))
    # FF shape systematics
    for histName in hists_fake_sys:
        hists_fake_sys[histName].Write('fake_%s'%(histName))    
    fileOutput.Close()

    print("Saving datacards to ascii file %s.txt"%(outputFileName))
    CreateCardsWToTauNu(outputFileName,
                        hist_data,
                        hist_fake,
                        hist_bkg_tau,
                        hist_bkg_lfakes,
                        hist_sig,
                        names_fake_sys,
                        names_sig_sys,
                        suffix)
                