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

bkgSampleNamesLepFake = ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500','ZJetsToNuNu_HT-100To200','ZJetsToNuNu_HT-200To400','ZJetsToNuNu_HT-400To600','ZJetsToNuNu_HT-600To800','ZJetsToNuNu_HT-800To1200','ZJetsToNuNu_HT-1200To2500']
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
                 wp,era,var,wpVsMu,wpVsE,trigger):
    
    # protection from zero entries
    xb1 = max(h_bkg_input.GetBinContent(1),0.1)
    h_bkg_input.SetBinContent(1,xb1)

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
        leg.SetHeader(wp+" (passed)")
    else:
        leg.SetHeader(wp+" (failed)")
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
    print
    print('Creating control plot')
    canvas.Print(utils.figuresFolderWTauNu+"/"+wpVsMu+"VsMu_"+wpVsE+"VsE/wtaunu_"+wp+trigger+"_"+era+".png")

def CreateCardsWToTauNu(fileName,h_data,h_fake,h_tau,h_bkg,h_sig,uncs_fake,uncs_sig,trigger):

    x_data = h_data.GetSumOfWeights()
    x_fake = h_fake.GetSumOfWeights()
    x_tau  = h_tau.GetSumOfWeights()
    x_bkg  = h_bkg.GetSumOfWeights()    
    x_sig  = h_sig.GetSumOfWeights() 

    cardsFileName = fileName + ".txt"
    rootFileName = fileName + ".root"
    f = open(cardsFileName,"w")
    f.write("imax 1    number of channels\n")
    f.write("jmax *    number of backgrounds\n")
    f.write("kmax *    number of nuisance parameters\n")
    f.write("---------------------------\n")
    f.write("observation   %3.1f\n"%(x_data))
    f.write("---------------------------\n")
    f.write("shapes * *  "+rootFileName+"  taunu"+trigger+"/$PROCESS taunu"+trigger+"/$PROCESS_$SYSTEMATIC \n")
    f.write("---------------------------\n")
    f.write("bin                  W"+trigger+"      W"+trigger+"      W"+trigger+"      W"+trigger+"\n")
    f.write("process              tau           wtaunu        fake          lfakes\n")
    f.write("process              -1            0             1             2\n")
    f.write("rate                 %4.3f         %4.3f      %4.3f      %4.3f\n"%(x_tau,x_sig,x_fake,x_bkg))
    f.write("---------------------------\n")
    f.write("extrapW        lnN   -             1.04          -             -\n")
    f.write("bkgNorm_taunu  lnN   1.2           -             -             -\n")
    f.write("lep_fakes      lnN   -             -             -           1.5\n")
    f.write("fake_closure"+trigger+"   lnN   -             -             1.15          -\n")
    for unc in uncs_sig:
        f.write(unc+"     shape   -             1.0           -             -\n")
    for unc in uncs_fake:
        f.write(unc+trigger+"     shape   -             -             1.0           -\n")
    f.write("normW  rateParam  W"+trigger+" wtaunu  1.0  [0.5,1.5]\n")
    f.write("* autoMCStats 0\n")
    groups = "sysUnc group = normW extrapW bkgNorm_taunu lep_fakes"
    for unc in uncs_sig:
        groups =  groups + " " + unc
    f.write(groups+"\n")
    f.close()
    

############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='UL2018', help="""Era : UL2016_preVFP, UL2016_postVFP, UL2017, UL2018""")
    parser.add_argument('-wp','--WP', dest='wp', default='Medium', help=""" tau ID WP : Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight', help=""" WP vs. mu : VLoose, Loose, Medium, Tight""")
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VLoose', help=""" WP vs. e : VLoose, Loose, Medium, Tight, VTight, VVTight""")

    args = parser.parse_args() 
    xbins = [100,120,140,160,180,200,250,300,400,2000]
    if args.era=="UL2016_preVFP" or args.era=="UL2016_postVFP":
        xbins = [100,120,140,160,200,250,400,2000]

    basefolder = utils.picoFolder
    var = 'pt_1'

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
#        uncert_names_full.append(unc+"_"+args.era)
        uncert_names_full.append(unc)

    print
    print('initializing data samples >>>')
    metSamples = {} # data samples dictionary
    metNames = utils.met[args.era]
    for metName in metNames:
        metSamples[metName] = utils.sampleHighPt(basefolder,args.era,
                                                      "taunu",metName,True)
        metSamples[metName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print
    print('initializing background samples (for genuine taus) >>>')
    bkgSamples = {} # MC bkg samples dictionary 
    for bkgSampleName in bkgSampleNames:
        bkgSamples[bkgSampleName] = utils.sampleHighPt(basefolder,args.era,
                                                       "taunu",bkgSampleName,False)
        bkgSamples[bkgSampleName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print
    print('initializing background samples (for lepton->tau fakes) >>>')
    bkgSamplesLepFake = {} # MC bkg samples dictionary 
    for bkgSampleName in bkgSampleNamesLepFake:
        if bkgSampleName=='WJetsToLNu':
            bkgSamplesLepFake[bkgSampleName] = utils.sampleHighPt(basefolder,args.era,
                                                                  "taunu",bkgSampleName,False,additionalCut='HT<100&&pt_1<200')
        else:
            bkgSamplesLepFake[bkgSampleName] = utils.sampleHighPt(basefolder,args.era,
                                                                  "taunu",bkgSampleName,False)
        bkgSamplesLepFake[bkgSampleName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print
    print('initializing signal samples >>>')
    sigSamples = {} # MC signal samples dictionary 
    for sigSampleName in sigSampleNames:
        sigSamples[sigSampleName] = utils.sampleHighPt(basefolder,args.era,
                                                       "taunu",sigSampleName,False)
        sigSamples[sigSampleName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    # running on signal samples (central template and unceertainties)
    print
    print('Running on signal samples >>>')
    hists_sig_shape = {}

    cutTrig = "(tautrigger1>0.5||tautrigger2>0.5)"
    cutNotTrig = "(!"+cutTrig+")"

    commonCut = "metfilter>0.5&&mettrigger>0.5&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&njets==0&&idDeepTau2017v2p1VSmu_1>="+utils.tauVsMuWPs[args.wpVsMu]+"&&idDeepTau2017v2p1VSe_1>="+utils.tauVsEleWPs[args.wpVsE]+"&&genmatch_1==5&&idDeepTau2017v2p1VSjet_1>=" + utils.tauWPs[args.wp]
    commonCutFakes = "metfilter>0.5&&mettrigger>0.5&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&njets==0&&idDeepTau2017v2p1VSmu_1>="+utils.tauVsMuWPs[args.wpVsMu]+"&&idDeepTau2017v2p1VSe_1>="+utils.tauVsEleWPs[args.wpVsE]+"&&(genmatch_1>=1&&genmatch_1<=4)&&idDeepTau2017v2p1VSjet_1>=" + utils.tauWPs[args.wp]
    no_unc = [""]
    histosToCheck = {}
    lst = no_unc + uncert_names
    for name in lst:

        name_unc = ""
        name_hist = "wtaunu_tau"
        if name!="": 
            name_unc = "_"+name+"Up"
            name_hist = "wtaunu_tau_"+name
        
        metUnc = "met"+name_unc
        ptUnc = "pt_1"
        Uncertainty = ROOT.TString(name_unc)
        var_unc = var
        if Uncertainty.Contains("taues"):
            ptUnc = "pt_1"+name_unc
            var_unc = var+name_unc
        mtUnc = "mt_1"+name_unc
        metdphiUnc = "metdphi_1"+name_unc

        metCut     = metUnc+">%3.1f"%(wtaunuCuts.metCut)
        ptLowerCut = ptUnc+">%3.1f"%(wtaunuCuts.ptLowerCut)
        ptUpperCut = ptUnc+"<%3.1f"%(wtaunuCuts.ptUpperCut)
        etaCut     = "fabs(eta_1)<%3.1f"%(wtaunuCuts.etaCut)
        metdphiCut = metdphiUnc+">%3.1f"%(wtaunuCuts.metdphiCut)
        mtLowerCut = mtUnc+">%3.1f"%(wtaunuCuts.mtLowerCut)
        mtUpperCut = mtUnc+"<%3.1f"%(wtaunuCuts.mtUpperCut)

        uncertCut = metCut+"&&"+ptLowerCut+"&&"+ptUpperCut+"&&"+etaCut+"&&"+metdphiCut+"&&"+mtLowerCut+"&&"+mtUpperCut
        totalCut = commonCut+"&&"+uncertCut

        totalCutTrig = totalCut+"&&"+cutTrig
        totalCutNotTrig = totalCut+"&&"+cutNotTrig
        
        histoTrig = utils.RunSamples(sigSamples,var_unc,"weight",totalCutTrig,xbins,name_hist+"_trig")
        histoNotTrig = utils.RunSamples(sigSamples,var_unc,"weight",totalCutNotTrig,xbins,name_hist+"_nottrig")
        if name=='':
            histoTotal = utils.RunSamples(sigSamples,var_unc,"weight",totalCut,xbins,name_hist)
            histosToCheck['check_total'] = histoTotal
            histosToCheck['check_trig'] = histoTrig
            histosToCheck['check_nottrig'] = histoNotTrig

        hists_sig_shape[name_hist+"_trig"] = histoTrig
        hists_sig_shape[name_hist+"_nottrig"] = histoNotTrig
        
    print('')
    print('Checking sum for signal')
    print('signal (passed trigger)',histosToCheck['check_trig'].GetSumOfWeights())
    print('signal (failed trigger)',histosToCheck['check_nottrig'].GetSumOfWeights())
    sumcheck = histosToCheck['check_trig'].GetSumOfWeights() + histosToCheck['check_nottrig'].GetSumOfWeights()
    print('Sum',histosToCheck['check_total'].GetSumOfWeights(),sumcheck)
    print('')

    # running on bkg samples ->
    metCut     = "met>%3.1f"%(wtaunuCuts.metCut)
    ptLowerCut = "pt_1>%3.1f"%(wtaunuCuts.ptLowerCut)
    ptUpperCut = "pt_1<%3.1f"%(wtaunuCuts.ptUpperCut)
    etaCut     = "fabs(eta_1)<%3.1f"%(wtaunuCuts.etaCut)
    metdphiCut = "metdphi_1>%3.1f"%(wtaunuCuts.metdphiCut)
    mtLowerCut = "mt_1>%3.1f"%(wtaunuCuts.mtLowerCut)
    mtUpperCut = "mt_1<%3.1f"%(wtaunuCuts.mtUpperCut)

    kinCuts = metCut+"&&"+ptLowerCut+"&&"+ptUpperCut+"&&"+etaCut+"&&"+metdphiCut+"&&"+mtLowerCut+"&&"+mtUpperCut
    totalCutTau     = commonCut+"&&"+kinCuts
    totalCutFakes   = commonCutFakes+"&&"+kinCuts
    totalCutTauTrig = totalCutTau+"&&"+cutTrig
    totalCutTauNotTrig = totalCutTau+"&&"+cutNotTrig
    totalCutFakesTrig = totalCutFakes+"&&"+cutTrig
    totalCutFakesNotTrig = totalCutFakes+"&&"+cutNotTrig

    hist_bkg_tau = {}
    hist_bkg_lfakes = {}

    hist_bkg_tau["bkg_tau_trig"]   = utils.RunSamples(bkgSamples,var,"weight",totalCutTauTrig,xbins,"bkg_tau_trig")
    hist_bkg_tau["bkg_tau_nottrig"]   = utils.RunSamples(bkgSamples,var,"weight",totalCutTauNotTrig,xbins,"bkg_tau_nottrig")
    hist_bkg_lfakes["bkg_lfakes_trig"] = utils.RunSamples(bkgSamplesLepFake,var,"weight",totalCutFakesTrig,xbins,"bkg_lfakes_trig")
    hist_bkg_lfakes["bkg_lfakes_nottrig"] = utils.RunSamples(bkgSamplesLepFake,var,"weight",totalCutFakesNotTrig,xbins,"bkg_lfakes_nottrig")

    # running selection on data 
    print
    print('Running on data samples >>>')
    hists_data        = utils.RunSamplesTauNu(metSamples,var,"",xbins,"","data")

    # running selection on bkgd samples
    print
    print('Running on background samples >>>')
    hists_bkg_fake      = utils.RunSamplesTauNu(bkgSamplesLepFake,var,"",xbins,"_fake","bkg")
    hists_bkg_notFake   = utils.RunSamplesTauNu(bkgSamplesLepFake,var,"",xbins,"_notFake","bkg")

    # compute EWK fraction
    h_data_dr_trig = hists_data["data_SB_trig"]
    h_data_dr_nottrig = hists_data["data_SB_nottrig"]
    h_data_dr_trig.Add(h_data_dr_trig,hists_bkg_notFake['bkg_notFake_SB_trig'],1.,-1.)
    h_data_dr_nottrig.Add(h_data_dr_nottrig,hists_bkg_notFake['bkg_notFake_SB_nottrig'],1.,-1.)
    h_ewk_dr_trig  = hists_bkg_fake["bkg_fake_SB_trig"]
    h_ewk_dr_nottrig = hists_bkg_fake["bkg_fake_SB_nottrig"]
    h_fraction = {}
    h_fraction["frac_trig"] = ComputeEWKFraction(h_data_dr_trig,h_ewk_dr_trig)
    h_fraction["frac_nottrig"] = ComputeEWKFraction(h_data_dr_nottrig,h_ewk_dr_nottrig)

    # Create j->tau fake histograms
    # first subtract from data templates notFake contribution estimated with simulated samples
    for labelFF in ["_data_wjets","_data_dijets"]:
        for labelTrig in utils.trigLabels:
            label = labelFF + labelTrig
            hists_data["data"+label].Add(hists_data["data"+label],hists_bkg_notFake["bkg_notFake"+label],1.,-1.)
            for ptratioLabel in utils.ptratioLabels:
                for uncLabel in utils.statUncLabels:
                    sysLabel = labelFF + ptratioLabel + uncLabel + labelTrig
                    hists_data["data"+sysLabel].Add(hists_data["data"+sysLabel],hists_bkg_notFake["bkg_notFake"+sysLabel],1.,-1.)

    hist_data = {}
    hist_sig = {}
    hist_fakes = {}
    hist_wjets = {}
    hist_dijets = {}
    for labelTrig in utils.trigLabels:
        hist_wjets['wjets'+labelTrig]  = hists_data['data_data_wjets'+labelTrig]
        hist_dijets['dijets'+labelTrig] = hists_data['data_data_dijets'+labelTrig]
        hist_fakes['fake'+labelTrig] = ComputeFake(hist_wjets['wjets'+labelTrig],hist_dijets['dijets'+labelTrig],h_fraction['frac'+labelTrig],'fake'+labelTrig)
        hist_data['data'+labelTrig] = hists_data['data'+labelTrig]
        hist_sig['sig'+labelTrig] = hists_sig_shape['wtaunu_tau'+labelTrig]
        hist_bkg = hists_bkg_notFake['bkg_notFake']
        print
        print('Check composition of the background',labelTrig)
        print('Total        = %5.1f'%(hist_bkg.GetSumOfWeights()))
        print('Genuine taus = %5.1f'%(hist_bkg_tau['bkg_tau'+labelTrig].GetSumOfWeights()))
        print('l->tau fakes = %5.1f'%(hist_bkg_lfakes['bkg_lfakes'+labelTrig].GetSumOfWeights()))
        tot_bkg = hist_bkg_tau['bkg_tau'+labelTrig].GetSumOfWeights()+hist_bkg_lfakes['bkg_lfakes'+labelTrig].GetSumOfWeights()
        print('Sum check    = %5.1f'%(tot_bkg))
        print('W*->tau+v    = %5.1f'%(hist_sig['sig'+labelTrig].GetSumOfWeights()))

        # making control plot
        PlotWToTauNu(hist_data['data'+labelTrig],
                     hist_fakes["fake"+labelTrig],
                     hist_bkg_tau['bkg_tau'+labelTrig],
                     hist_bkg_lfakes['bkg_lfakes'+labelTrig],
                     hist_sig['sig'+labelTrig],
                     args.wp,args.era,var,args.wpVsMu,args.wpVsE,labelTrig)

    # creating shape templates for FF systematics
    hists_fake_sys = {}
    for ptratioLabel in utils.ptratioLabels:
        for uncLabel in utils.statUncLabels:
            for trigLabel in utils.trigLabels:
                Label = ptratioLabel + uncLabel + trigLabel
                # ewk FF
                name_fake = 'fake_wjets' + Label
                hist_fake_sys = ComputeFake(hists_data['data_data_wjets'+Label],hist_dijets['dijets'+trigLabel],h_fraction['frac'+trigLabel],name_fake)
                hist_up,hist_down = utils.ComputeSystematics(hist_fakes['fake'+trigLabel],hist_fake_sys,'fake_ewk'+Label)
                hists_fake_sys['fake_ewk'+Label+'Up'] = hist_up
                hists_fake_sys['fake_ewk'+Label+'Down'] = hist_down
                # qcd FF
                name_fake = 'fake_dijets' + Label
                hist_fake_sys = ComputeFake(hist_wjets['wjets'+trigLabel],hists_data['data_data_dijets'+Label],h_fraction['frac'+trigLabel],name_fake)
                hist_up,hist_down = utils.ComputeSystematics(hist_fakes['fake'+trigLabel],hist_fake_sys,'fake_qcd'+Label)
                hists_fake_sys['fake_qcd'+Label+'Up'] = hist_up
                hists_fake_sys['fake_qcd'+Label+'Down'] = hist_down

    # -----------------------------------------------
    # creating shape templates for signal systematics
    # -----------------------------------------------
    hists_sig_sys_trig = {}
    hists_sig_sys_nottrig = {}
    for name_unc in uncert_names:
        for trigLabel in utils.trigLabels:
            name_hist = 'wtaunu_tau_'+name_unc+trigLabel
            name = 'wtaunu_'+name_unc
            name_output = 'wtaunu_'+name_unc
            hist_sig_sys = hists_sig_shape[name_hist]
            hist_up,hist_down = utils.ComputeSystematics(hist_sig['sig'+trigLabel],hist_sig_sys,name)
            if trigLabel=='_trig':
                hists_sig_sys_trig[name_output+'Up'] = hist_up
                hists_sig_sys_trig[name_output+'Down'] = hist_down
            else:
                hists_sig_sys_nottrig[name_output+'Up'] = hist_up
                hists_sig_sys_nottrig[name_output+'Down'] = hist_down


    # saving histograms to datacard file datacards
    for trigLabel in utils.trigLabels:
        outputFileName = utils.datacardsFolder+"/"+args.wpVsMu+"VsMu_"+args.wpVsE+"VsE/taunu_"+args.wp+trigLabel+"_"+args.era
        print
        print("Saving histograms to RooT file",outputFileName+".root")
        fileOutput = ROOT.TFile(outputFileName+".root","recreate")
        fileOutput.mkdir("taunu"+trigLabel)
        fileOutput.cd("taunu"+trigLabel)
        hist_data['data'+trigLabel].Write("data_obs")
        hist_sig['sig'+trigLabel].Write("wtaunu")
        hist_bkg_tau['bkg_tau'+trigLabel].Write("tau")
        hist_bkg_lfakes['bkg_lfakes'+trigLabel].Write("lfakes")
        hist_fakes['fake'+trigLabel].Write("fake")

        # signal shape systematics
        if trigLabel=='_trig':
            for histName in hists_sig_sys_trig:
                hists_sig_sys_trig[histName].Write(histName)
        else:
            for histName in hists_sig_sys_nottrig:
                hists_sig_sys_nottrig[histName].Write(histName)

        # FF shape systematics
        for histName in hists_fake_sys:            
            if trigLabel in histName: hists_fake_sys[histName].Write(histName)    
            
        fileOutput.Close()

        uncs_fake = []
        for sampleLabel in ["ewk","qcd"]:
            for ptratioLabel in ["_ptratioLow","_ptratioHigh"]:
                for statUnc in ["_unc1","_unc2"]:
                    unc = sampleLabel+ptratioLabel+statUnc
                    uncs_fake.append(unc)

        CreateCardsWToTauNu(outputFileName,
                            hist_data['data'+trigLabel],
                            hist_fakes['fake'+trigLabel],
                            hist_bkg_tau['bkg_tau'+trigLabel],
                            hist_bkg_lfakes['bkg_lfakes'+trigLabel],
                            hist_sig['sig'+trigLabel],
                            uncs_fake,uncert_names_full,trigLabel)
                
