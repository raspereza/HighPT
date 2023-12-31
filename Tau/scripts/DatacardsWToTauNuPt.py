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

bkgSampleNamesLepFake = ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ','WJetsToLNu','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500','ZJetsToNuNu_HT-100To200','ZJetsToNuNu_HT-200To400','ZJetsToNuNu_HT-400To600','ZJetsToNuNu_HT-600To800','ZJetsToNuNu_HT-800To1200','ZJetsToNuNu_HT-1200To2500']

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
                 wp,era,var,wpVsMu,wpVsE,correct):

    print
    print('Plotting for era',era,'WPvsJet',wp,'WPvsMu',wpVsMu,'WPvsE',wpVsE)
    print('Corrections for bins ->')

    suffix = ''
    if correct:
        suffix = '_corrected'

    nbins = h_data_input.GetNbinsX()
    wp_list = era+"_"+wp+"_"+wpVsMu+"_"+wpVsE

#    only for deepTauV2p1
#    if era=='UL2016_postVFP' or era=='UL2016_preVFP':
#        x_pt_last = utils.corr_last_pt[wp_list]
#        h_data_input.SetBinContent(9,x_pt_last)
#        h_data_input.SetBinError(9,math.sqrt(x_pt_last))
#    if era=='UL2016_preVFP':
#        x_pt_bin8 = utils.corr_prelast_pt[wp_list]
#        print('bin 8',h_data_input.GetBinContent(8))
#        h_data_input.SetBinContent(8,x_pt_bin8)
#        h_data_input.SetBinError(8,math.sqrt(x_pt_bin8))
#    if era=='UL2018':
#        x_pt_bin7 = utils.corr_prelast_pt[wp_list]
#        print('bin 7',h_data_input.GetBinContent(7))
#        h_data_input.SetBinContent(7,x_pt_bin7)
#        h_data_input.SetBinError(7,math.sqrt(x_pt_bin7))

    SFs = utils.tauID_sf_v2p5[wp_list] 
    sf_low = 1.0
    unc_low = 0.1
    sf_high = 1.0
    unc_high = 0.1
    if correct:
        sf_low = SFs['low']
        unc_low = SFs['low_unc']
        sf_high = SFs['high']
        unc_high = SFs['high_unc']
    print('SF_low  = ',sf_low,'+/-',unc_low)
    print('SF_high = ',sf_high,'+/-',unc_high)
    print
    
    h_data = h_data_input.Clone("data_plot")
    h_fake = h_fake_input.Clone("fake_plot")
    h_bkg = h_bkg_input.Clone("bkg_plot")
    h_tau = h_tau_input.Clone("tau_plot")
    h_sig = h_sig_input.Clone("sig_plot")

    # log-normal uncertainties 
    #  5% signal, 
    # 15% fake, 
    # 20% genuine tau background
    # 50% lfakes
    e_sig_sys = 0.05
    e_fake_sys = 0.15
    e_bkg_sys = 0.50
    e_tau_sys = 0.20
    for i in range(1,nbins+1):
        lowEdge = h_sig.GetXaxis().GetBinLowEdge(i)
        sf = sf_low
        sf_unc = unc_low
        if lowEdge>200: 
            sf = sf_high
            sf_unc = unc_high
        h_sig.SetBinContent(i,sf*h_sig.GetBinContent(i))
        h_tau.SetBinContent(i,sf*h_tau.GetBinContent(i))

        x_sig = h_sig.GetBinContent(i)
        x_bkg = h_bkg.GetBinContent(i)
        x_tau = h_tau.GetBinContent(i)
        x_fake = h_fake.GetBinContent(i)
        e_sig_stat = h_sig.GetBinError(i)
        e_sig = math.sqrt(e_sig_stat*e_sig_stat+(e_sig_sys*e_sig_sys+sf_unc*sf_unc)*x_sig*x_sig)
        h_sig.SetBinError(i,e_sig)
        e_bkg_stat = h_bkg.GetBinError(i)
        e_bkg = math.sqrt(e_bkg_stat*e_bkg_stat+e_bkg_sys*e_bkg_sys*x_bkg*x_bkg)
        h_bkg.SetBinError(i,e_bkg)
        e_tau_stat = h_tau.GetBinError(i)
        e_tau = math.sqrt(e_tau_stat*e_tau_stat+(e_tau_sys*e_tau_sys+sf_unc*sf_unc)*x_tau*x_tau)
        h_tau.SetBinError(i,e_tau)
        e_fake_stat = h_fake.GetBinError(i)
        e_fake = math.sqrt(e_fake_stat*e_fake_stat+e_fake_sys*e_fake_sys*x_fake*x_fake)
        h_fake.SetBinError(i,e_fake)


    h_data_x = h_data.Clone('h_data_x')
    h_fake_x = h_fake.Clone('h_fake_x')
    h_sig_x = h_sig.Clone('h_sig_x')
    h_tau_x = h_tau.Clone('h_tau_x')
    h_bkg_x = h_bkg.Clone('h_bkg_x')

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

    rootFile = ''    

    if wpVsE=='VLoose':
        rootFile = utils.figuresFolderPT+"/pT_"+wp+"VsJet_"+wpVsMu+"VsMu_V"+wpVsE+"VsE_"+era+suffix+".root"
    else:
        rootFile = utils.figuresFolderPT+"/pT_"+wp+"VsJet_"+wpVsMu+"VsMu_"+wpVsE+"VsE_"+era+suffix+".root"
    print
    print('Saving histograms to ROOT file',rootFile)
    file = ROOT.TFile(rootFile,'recreate')
    file.cd('')
    h_data_x.Write('h_data')
    h_sig_x.Write('h_sig')
    h_fake_x.Write('h_jfakes')
    h_tau_x.Write('h_tau')
    h_bkg_x.Write('h_lfakes')
    h_tot.Write('h_total')
    file.Close()

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
    parser.add_argument('-correct','--Correct', dest='correct', default=0, help=""" 1 : correct, 0 : doesn't correct""")

    args = parser.parse_args() 

    correct = True
    if args.correct==0: correct = False

    xbins = [100,125,150,175,200,250,300,350,400,500,1000]
    basefolder = utils.picoFolder
    var = "pt_1"

    # initializing instance of FF class    
    fullpathFF = os.getenv('CMSSW_BASE') + '/src/TauFW/Plotter/data/ff_HighPT/ff_'+args.wp+"VSjet_"+args.wpVsMu+"VSmu_"+args.wpVsE+"VSe_"+args.era+".root"
    fakeFactor = utils.FakeFactorHighPt(fullpathFF)

    # initializing instance of TauNuCuts class
    antiMu = utils.tauVsMuIntWPs[args.wpVsMu]
    antiE  = utils.tauVsEleIntWPs[args.wpVsE]
    wtaunuCuts = utils.TauNuCuts(antiMu=antiMu,antiE=antiE)    

    # vector uncertainties
    uncert_names = ["JES","Unclustered","taues_1pr","taues_1pr1pi0","taues_3pr","taues_3pr1pi0"]
    #    uncert_names = ["JES","Unclustered","taues"]
    uncert_names_full = [] # uncertainty names with suffix era
    for unc in uncert_names:
        uncert_names_full.append(unc+"_"+args.era)

    print
    print('initializing data samples >>>')
    metSamples = {} # data samples dictionary
    metNames = utils.met[args.era]
    for metName in metNames:
        metSamples[metName] = utils.sampleHighPt(basefolder,args.era,
                                                      "taunu",metName,True)
        metSamples[metName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print
    print('initializing background samples >>>')
    bkgSamples = {} # MC bkg samples dictionary 
    for bkgSampleName in bkgSampleNames:
        bkgSamples[bkgSampleName] = utils.sampleHighPt(basefolder,args.era,
                                                       "taunu",bkgSampleName,False)
        bkgSamples[bkgSampleName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print('')
    print('initializing background samples (for l->tau fakes) >>>')    
    bkgLepFakesSamples = {} # MC bkg samples disctionary for lepton fakes
    for bkgSampleLepFakeName in bkgSampleNamesLepFake:
        if bkgSampleLepFakeName=='WJetsToLNu':
            bkgLepFakesSamples[bkgSampleLepFakeName] = utils.sampleHighPt(basefolder,args.era,
                                                                          "taunu",bkgSampleLepFakeName,False,additionalCut='HT<100')
        else:
            bkgLepFakesSamples[bkgSampleLepFakeName] = utils.sampleHighPt(basefolder,args.era,
                                                                          "taunu",bkgSampleLepFakeName,False)
        bkgLepFakesSamples[bkgSampleLepFakeName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print
    print('initializing signal samples >>>')
    sigSamples = {} # MC signal samples dictionary 
    for sigSampleName in sigSampleNames:
        sigSamples[sigSampleName] = utils.sampleHighPt(basefolder,args.era,
                                                       "taunu",sigSampleName,False)
        sigSamples[sigSampleName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    # running selection on signal samples (notFake)
    hists_sig_notFake = utils.RunSamplesTauNu(sigSamples,var,"",xbins,"_notFake","sig")

    # running on signal samples (central template and unceertainties)
    print
    commonCut = "metfilter>0.5&&mettrigger>0.5&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&njets==0&&idDeepTau2018v2p5VSmu_1>="+utils.tauVsMuWPs[args.wpVsMu]+"&&idDeepTau2018v2p5VSe_1>="+utils.tauVsEleWPs[args.wpVsE]+"&&genmatch_1==5&&idDeepTau2018v2p5VSjet_1>=" + utils.tauWPs[args.wp]
    commonCutFakes = "metfilter>0.5&&mettrigger>0.5&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&njets==0&&idDeepTau2018v2p5VSmu_1>="+utils.tauVsMuWPs[args.wpVsMu]+"&&idDeepTau2018v2p5VSe_1>="+utils.tauVsEleWPs[args.wpVsE]+"&&(genmatch_1>=1&&genmatch_1<=4)&&idDeepTau2018v2p5VSjet_1>=" + utils.tauWPs[args.wp]

    metCut     = "met>%3.1f"%(wtaunuCuts.metCut)
    ptLowerCut = "pt_1>%3.1f"%(wtaunuCuts.ptLowerCut)
    ptUpperCut = "pt_1<%3.1f"%(wtaunuCuts.ptUpperCut)
    etaCut     = "fabs(eta_1)<%3.1f"%(wtaunuCuts.etaCut)
    metdphiCut = "metdphi_1>%3.1f"%(wtaunuCuts.metdphiCut)
    mtLowerCut = "mt_1>%3.1f"%(wtaunuCuts.mtLowerCut)
    mtUpperCut = "mt_1<%3.1f"%(wtaunuCuts.mtUpperCut)

    kinCuts = metCut+"&&"+ptLowerCut+"&&"+ptUpperCut+"&&"+etaCut+"&&"+metdphiCut+"&&"+mtLowerCut+"&&"+mtUpperCut
    totalCut = commonCut+"&&"+kinCuts
    hist_sig = utils.RunSamples(sigSamples,var,"weight",totalCut,xbins,"sig_tau")

    # running on bkg samples ->
    totalCutTau     = commonCut+"&&"+kinCuts
    totalCutFakes   = commonCutFakes+"&&"+kinCuts
    hist_bkg_tau   = utils.RunSamples(bkgSamples,var,"weight",totalCutTau,xbins,"bkg_tau")
    hist_bkg_lfakes = utils.RunSamples(bkgLepFakesSamples,var,"weight",totalCutFakes,xbins,"bkg_lfakes")

    # running selection on data 
    print
    print('Running on data samples >>>')
    hists_data        = utils.RunSamplesTauNu(metSamples,var,"",xbins,"","data")

    # running selection on bkgd samples
    print
    print('Running on background samples >>>')
    hists_bkg_fake    = utils.RunSamplesTauNu(bkgSamples,var,"",xbins,"_fake","bkg")
    hists_bkg_notFake = utils.RunSamplesTauNu(bkgSamples,var,"",xbins,"_notFake","bkg")

    # compute EWK fraction histogram in the FF aplication region
    h_data_dr = hists_data["data_SB"]
    h_data_dr.Add(h_data_dr,hists_bkg_notFake['bkg_notFake_SB'],1.,-1.)
    h_data_dr.Add(h_data_dr,hists_sig_notFake['sig_notFake_SB'],1.,-1.)
    h_ewk_dr  = hists_bkg_fake["bkg_fake_SB"]
    h_fraction = ComputeEWKFraction(h_data_dr,h_ewk_dr)

    # Create j->tau fake histograms
    # first subtract from data templates notFake contribution estimated with simulated samples
    for label in ["data_wjets","data_dijets"]:
        hists_data["data_"+label].Add(hists_data["data_"+label],hists_bkg_notFake["bkg_notFake_"+label],1.,-1.)
        hists_data["data_"+label].Add(hists_data["data_"+label],hists_sig_notFake["sig_notFake_"+label],1.,-1.)

    hist_wjets  = hists_data["data_data_wjets"]
    hist_dijets = hists_data["data_data_dijets"]
    hist_fake = ComputeFake(hist_wjets,hist_dijets,h_fraction,'fake')
    hist_data = hists_data["data"]
    hist_bkg = hists_bkg_notFake["bkg_notFake"]

    print
    print("Check composition of the background")
    print('Total        = %5.1f'%(hist_bkg.GetSumOfWeights()))
    print('Genuine taus = %5.1f'%(hist_bkg_tau.GetSumOfWeights()))
    print('l->tau fakes = %5.1f'%(hist_bkg_lfakes.GetSumOfWeights()))
    tot_bkg = hist_bkg_tau.GetSumOfWeights()+hist_bkg_lfakes.GetSumOfWeights()
    print('Sum check    = %5.1f'%(tot_bkg))
    print('W*->tau+v    = %5.1f'%(hist_sig.GetSumOfWeights()))

    # making control plot
    PlotWToTauNu(hist_data,hist_fake,hist_bkg_tau,hist_bkg_lfakes,hist_sig,args.wp,args.era,var,args.wpVsMu,args.wpVsE,correct)

