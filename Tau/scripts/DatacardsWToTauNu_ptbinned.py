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
        ratio = 0.5
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
        print("[%3d,%4d] = %4.2f +/- %4.2f (%4.2f rel)" %(lowerEdge,upperEdge,ratio,eratio,eratio/ratio))

    return h_fraction

############################
###### Closure test ########
############################
def PlotClosure(h_data,h_models,wp,era,var,suffix):

    print
    print("Plotting closure")
    h_model = h_models["bkg_fake_mc_wjets"]    

    styles.InitData(h_data)
    h_tot = h_model.Clone('h_tot_model')
    # add systematic uncertainties
    nbins = h_tot.GetNbinsX()
    for i in range(1,nbins+1):
        error2 = h_tot.GetBinError(i)*h_tot.GetBinError(i)
        errorStat = h_tot.GetBinError(i)
        xcen = h_tot.GetBinContent(i)
        for ptratioLabel in utils.ptratioLabels:
            for uncLabel in utils.statUncLabels:
                name = "bkg_fake_mc_wjets" + ptratioLabel + uncLabel
                xsys = h_models[name].GetBinContent(i)
                error2 += (xcen-xsys)*(xcen-xsys)
        error = math.sqrt(error2)
        lowerEdge = h_tot.GetBinLowEdge(i)
        upperEdge = h_tot.GetBinLowEdge(i+1)
        print("[%3d,%4d] = %5.1f +/- %4.1f(stat) +/- %4.1f(tot) (%4.2f rel)" %(lowerEdge,upperEdge,xcen,errorStat,error,error/xcen))
        h_tot.SetBinError(i,error)
                
    styles.InitTotalHist(h_tot)
    styles.InitModel(h_model,2)

    hist_ratio = utils.divideHistos(h_data,h_model,'ratio_model')
    hist_unit = utils.createUnitHisto(h_tot,'ratio_model_unit')

    styles.InitRatioHist(hist_ratio)
    hist_ratio.GetYaxis().SetRangeUser(0.301,1.699)
    utils.zeroBinErrors(h_model)

    yMax = h_data.GetMaximum()
    if h_model.GetMaximum()>yMax: yMax = h_model.GetMaximum()
    h_data.GetYaxis().SetRangeUser(0.,1.2*yMax)
    h_data.GetXaxis().SetLabelSize(0)

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

    leg = ROOT.TLegend(0.65,0.5,0.9,0.8)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.045)
    leg.SetHeader(era)
    leg.AddEntry(h_data, 'selection','lp')
    leg.AddEntry(h_model,'model','l')
    #    leg.Draw()

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
    func = ROOT.TF1("func",FitConst,xmin,xmax,1)
    func.SetParameter(0,1.0)
    func.SetLineColor(4)

    hist_ratio.Fit('func','R')
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
    canvas.Print(utils.figuresFolderWTauNu+"/closure_"+var+"_"+wp+"_"+era+"_"+suffix+".png")

    nonclosure = func.GetParameter(0)
    return nonclosure

##########################
# Plotting distributions #
##########################
def PlotWToTauNu(h_data_input,h_fake_input,h_tau_input,h_bkg_input,h_sig_input,wp,era,var,suffix,wpVsMu,wpVsE):
    
    # protection from zero entries
    xb1 = max(h_bkg_input.GetBinContent(1),0.1)
    h_bkg_input.SetBinContent(1,xb1)

    if era=='UL2017' and suffix=='lowpt':
        if var=='mt_1':
            h_tau_input.SetBinContent(1,2.5*h_tau_input.GetBinContent(1))
            h_tau_input.SetBinContent(2,1.5*h_tau_input.GetBinContent(2))
        if var=='pt_1':
            for ib in range(1,7):
                h_fake_input.SetBinContent(ib,1.1*h_fake_input.GetBinContent(ib))

    h_data = h_data_input.Clone("data_plot")
    h_fake = h_fake_input.Clone("fake_plot")
    h_bkg = h_bkg_input.Clone("bkg_plot")
    h_tau = h_tau_input.Clone("tau_plot")
    h_sig = h_sig_input.Clone("sig_plot")

    print
    print('Creating control plot')
    xmean = h_sig.GetMean()
    rms = h_sig.GetRMS()
    print('Signal mean = ',xmean,' rms = ',rms)

    # log-normal uncertainties (5% signal, 15% fake, 20% genuine single-tau background, 50% l->tau fake background)
    nbins = h_data.GetNbinsX()
    e_sig_sys = 0.05
    e_fake_sys = 0.15
    e_bkg_sys = 0.50
    e_tau_sys = 0.20
    for i in range(1,nbins+1):
        x_sig = h_sig.GetBinContent(i)
        x_bkg = h_bkg.GetBinContent(i)
        x_fake = h_fake.GetBinContent(i)
        x_tau  = h_tau.GetBinContent(i)
        e_sig_stat = h_sig.GetBinError(i)
        e_sig = math.sqrt(e_sig_stat*e_sig_stat+e_sig_sys*e_sig_sys*x_sig*x_sig)
        h_sig.SetBinError(i,e_sig)
        e_bkg_stat = h_bkg.GetBinError(i)
        e_bkg = math.sqrt(e_bkg_stat*e_bkg_stat+e_bkg_sys*e_bkg_sys*x_bkg*x_bkg)
        h_bkg.SetBinError(i,e_bkg)
        e_fake_stat = h_fake.GetBinError(i)
        e_fake = math.sqrt(e_fake_stat*e_fake_stat+e_fake_sys*e_fake_sys*x_fake*x_fake)
        h_fake.SetBinError(i,e_fake)
        e_tau_stat = h_tau.GetBinError(i)
        e_tau = math.sqrt(e_tau_stat*e_tau_stat+e_tau_sys*e_tau_sys*x_tau*x_tau)
        h_tau.SetBinError(i,e_tau)

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

    h_ratio.GetYaxis().SetRangeUser(0.301,1.699)
    
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

    leg = ROOT.TLegend(0.65,0.4,0.9,0.75)
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
    canvas.Print(utils.figuresFolderWTauNu+"/"+wpVsMu+"VsMu_"+wpVsE+"VsE/wtaunu_"+var+"_"+wp+"_"+era+"_"+suffix+".png")

def CreateCardsWToTauNu(fileName,h_data,h_fake,h_tau,h_bkg,h_sig,uncs_fake,uncs_sig,era,suffix):

    x_data = h_data.GetSumOfWeights()
    x_fake = h_fake.GetSumOfWeights()
    x_bkg  = h_bkg.GetSumOfWeights()
    x_tau  = h_tau.GetSumOfWeights()
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
    f.write("shapes * *  "+rootFileName+"  taunu/$PROCESS taunu/$PROCESS_$SYSTEMATIC \n")
    f.write("---------------------------\n")
    f.write("bin                  WtoTauNu_"+suffix+"_"+era+"      WtoTauNu_"+suffix+"_"+era+"      WtoTauNu_"+suffix+"_"+era+"      WtoTauNu_"+suffix+"_"+era+"\n")
    f.write("process              tau_"+suffix+"_"+era+"     wtaunu_"+suffix+"_"+era+"        fake          lfakes\n")
    f.write("process              -1            0             1             2\n")
    f.write("rate                 %4.3f         %4.3f         %4.3f      %4.3f\n"%(x_tau,x_sig,x_fake,x_bkg))
    f.write("---------------------------\n")
    f.write("extrapW        lnN   -             1.04          -             -\n")
    f.write("bkgNorm_taunu  lnN   1.2           -             -             -\n")
    f.write("lep_fakes_"+era+"      lnN   -             -             -           1.5\n")
    f.write("fake_closure   lnN   -             -             1.15          -\n")
    for unc in uncs_sig:
        f.write(unc+"     shape   -             1.0           -             -\n")
    for unc in uncs_fake:
        f.write(unc+"     shape   -             -             1.0           -\n")
    f.write("normW  rateParam  WtoTauNu_"+suffix+"_"+era+" wtaunu_"+suffix+"_"+era+"  1.0  [0.5,1.5]\n")
    f.write("* autoMCStats 0\n")
    groups = "byErasAndBins group = normW extrapW bkgNorm_taunu fake_closure lep_fakes_"+era
    for unc in uncs_sig:
        groups = groups + " " + unc
    f.write(groups)
    f.write("\n")
    groups = "byEras group = normW extrapW bkgNorm_taunu fake_closure\n"
    f.write(groups)
    f.close()
    

############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='UL2016_postVFP', help="""Era : UL2016_preVFP, UL2016_postVFP, UL2017, UL2018""")
    parser.add_argument('-wp','--WP', dest='wp', default='VVTight', help=""" tau ID WP : Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight', help=""" WP vs. mu : VLoose, Loose, Medium, Tight""")
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VLoose', help=""" WP vs. e : VLoose, Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-var','--variable',dest='variable',default='mt_1',help=""" Variable to plot""")
    parser.add_argument('-ptbin','--ptbin',dest='ptbin',default='highpt',help=""" pt > 200 GeV?""")
    args = parser.parse_args() 

    print("\n")

    if args.era not in ['UL2016_preVFP','UL2016_postVFP','UL2017','UL2018']:
        print('unknown era specified',args.era,'quitting')
        exit()

    if args.wp not in ['Loose','Medium','Tight','VTight','VVTight']:
        print('unknown working point vsJet specified',args.wp,'quitting')
        exit()

    if args.ptbin not in ['highpt','lowpt']:
        print('unknow pt bin',args.ptbin,'quitting')
        exit()

    suffix = args.ptbin
    isHighPt = True
    if suffix=='lowpt':
        isHighPt = False

    xbins_lowpt_mt = [200,250,300,350,400,1000]
    xbins_highpt_mt = [200,400,500,600,800,1000]
    
    if args.era=='UL2016_preVFP' or args.era=='UL2016_postVFP':
        xbins_highpt_mt = [200,400,500,600,1000]

    xbins_lowpt_pt = [100,110,120,130,140,150,160,170,180,190,200] # use fine binning 
#    xbins_highpt_pt = [200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000] # use fine binning 
    xbins_highpt_pt = [200,250,300,350,500] # use fine binning 
    xbins_eta = [-2.4, -1.8, -1.2, -0.6, 0.0, 0.6, 1.2, 1.8, 2.4]
    xbins = xbins_lowpt_mt
    if isHighPt: xbins = xbins_highpt_mt
    if args.variable=='pt_1': 
        xbins = xbins_lowpt_pt
        if isHighPt: xbins = xbins_highpt_pt
    if args.variable=='eta_1': xbins =  xbins_eta

    statUncLabel = '_unc1'
    if isHighPt: 
        statUncLabel = '_unc2'

    basefolder = utils.picoFolder
    var = args.variable    
    print("Running W*->tau+cselection")
    print("era",args.era)
    print("pt bin",suffix)
    print("WP vs jet",args.wp)
    print("WP vs e",args.wpVsE)
    print("WP vs mu",args.wpVsMu)

    # initializing instance of FF class    
    fullpathFF = os.getenv('CMSSW_BASE') + '/src/TauFW/Plotter/data/ff_HighPT/ff_'+args.wp+"VSjet_"+args.wpVsMu+"VSmu_"+args.wpVsE+"VSe_"+args.era+".root"
    fakeFactor = utils.FakeFactorHighPt(fullpathFF)

    # initializing instance of TauNuCuts class
    ptlow_cut = 100.0
    pthigh_cut = 200.0
    if isHighPt: 
        ptlow_cut = 200.0
        pthigh_cut = 99999999.
    antiMu = utils.tauVsMuIntWPs[args.wpVsMu]
    antiE  = utils.tauVsEleIntWPs[args.wpVsE]
    wtaunuCuts = utils.TauNuCuts(ptLowerCut=ptlow_cut,ptUpperCut=pthigh_cut,antiMu=antiMu,antiE=antiE)

    # vector uncertainties
    uncert_names = ["JES","Unclustered","taues_1pr","taues_1pr1pi0","taues_3pr","taues_3pr1pi0"]
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


    print
    print('initializing background samples (lepton->tau fakes) >>>')
    bkgSamplesLepFake = {} # MC bkg samples dictionary 
    for bkgSampleName in bkgSampleNamesLepFake:
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

    # running selection on signal samples (notFake)
    hists_sig_notFake = utils.RunSamplesTauNu(sigSamples,var,"",xbins,"_notFake","sig")

    # running on signal samples (central template and unceertainties)
    print
    print('Running on signal samples >>>')
    hists_sig_shape = {}
    commonCut = "metfilter>0.5&&mettrigger>0.5&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&njets==0&&idDeepTau2018v2p5VSmu_1>="+utils.tauVsMuWPs[args.wpVsMu]+"&&idDeepTau2018v2p5VSe_1>="+utils.tauVsEleWPs[args.wpVsE]+"&&genmatch_1==5&&idDeepTau2018v2p5VSjet_1>=" + utils.tauWPs[args.wp] 
    commonCutFakes = "metfilter>0.5&&mettrigger>0.5&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&njets==0&&idDeepTau2018v2p5VSmu_1>="+utils.tauVsMuWPs[args.wpVsMu]+"&&idDeepTau2018v2p5VSe_1>="+utils.tauVsEleWPs[args.wpVsE]+"&&(genmatch_1>=1&&genmatch_1<=4)&&idDeepTau2018v2p5VSjet_1>=" + utils.tauWPs[args.wp] 

    no_unc = [""]
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
        if Uncertainty.Contains("taues"):
            ptUnc = "pt_1"+name_unc
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
        
        histo = utils.RunSamples(sigSamples,var+name_unc,"weight",totalCut,xbins,name_hist)
        hists_sig_shape[name_hist] = histo


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
    hist_bkg_tau    = utils.RunSamples(bkgSamples,var,"weight",totalCutTau,xbins,"bkg_taus")
    hist_bkg_lfakes  = utils.RunSamples(bkgSamplesLepFake,var,"weight",totalCutFakes,xbins,"bkg_lfakes")

    # running selection on data 
    print
    print('Running on data samples >>>')
    hists_data        = utils.RunSamplesTauNu(metSamples,var,"",xbins,"","data")

    # running selection on bkgd samples
    print
    print('Running on background samples >>>')
    hists_bkg_fake    = utils.RunSamplesTauNu(bkgSamples,var,"",xbins,"_fake","bkg")
    hists_bkg_notFake = utils.RunSamplesTauNu(bkgSamples,var,"",xbins,"_notFake","bkg")

    #
    # correct ewk componet for non-closure
    #    hist_num = hists_bkg_fake["bkg_fake"]
    #    nonclosure = PlotClosure(hist_num,hists_bkg_fake,args.wp,args.era,var,suffix)    
    #    exit()
    # closure file ->
    #closureFileName = utils.datacardsFolder + "/closure_" + args.wp + "_" + args.era
    #fileOutput = ROOT.TFile(closureFileName+".root")
    #func = fileOutput.Get("closure")
    #nonclosure = func.GetParameter(0)
    #nonclosure_e = func.GetParError(0)
    #print 
    #print('Non-closure parameter',nonclosure,"+/-",nonclosure_e)
    #

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
        for ptratioLabel in utils.ptratioLabels:
            sysLabel = label + ptratioLabel + statUncLabel
            hists_data["data_"+sysLabel].Add(hists_data["data_"+sysLabel],hists_bkg_notFake["bkg_notFake_"+sysLabel],1.,-1.)
            hists_data["data_"+sysLabel].Add(hists_data["data_"+sysLabel],hists_sig_notFake["sig_notFake_"+sysLabel],1.,-1.)
                

    hist_wjets  = hists_data["data_data_wjets"]
    hist_dijets = hists_data["data_data_dijets"]
    hist_fake = ComputeFake(hist_wjets,hist_dijets,h_fraction,'fake')
    hist_data = hists_data["data"]
    hist_sig = hists_sig_shape["wtaunu_tau"]
    hist_bkg = hists_bkg_notFake["bkg_notFake"]
    
    print
    print("Check composition of the background")
    print('Total        = %5.1f'%(hist_bkg.GetSumOfWeights()))
    print('Genuine taus = %5.1f'%(hist_bkg_tau.GetSumOfWeights()))
    print('l->tau fakes = %5.1f'%(hist_bkg_lfakes.GetSumOfWeights()))
    tot_bkg = hist_bkg_tau.GetSumOfWeights()+hist_bkg_lfakes.GetSumOfWeights()
    print('Sum check    = %5.1f'%(tot_bkg))

    # making control plot
    PlotWToTauNu(hist_data,hist_fake,hist_bkg_tau,hist_bkg_lfakes,hist_sig,args.wp,args.era,var,suffix,args.wpVsMu,args.wpVsE)

    # creating shape templates for FF systematics
    hists_fake_sys = {}
    for ptratioLabel in utils.ptratioLabels:
        Label = ptratioLabel + statUncLabel
        # ewk FF
        name_fake = "fake_wjets" + Label
        hist_fake_sys = ComputeFake(hists_data["data_data_wjets"+Label],hist_dijets,h_fraction,name_fake)
        hist_up,hist_down = utils.ComputeSystematics(hist_fake,hist_fake_sys,"fake_ewk"+Label)
        hists_fake_sys["fake_ewk"+Label+"_"+args.era+"Up"] = hist_up
        hists_fake_sys["fake_ewk"+Label+"_"+args.era+"Down"] = hist_down
        # qcd FF
        name_fake = "fake_dijets" + Label
        hist_fake_sys = ComputeFake(hist_wjets,hists_data["data_data_dijets"+Label],h_fraction,name_fake)
        hist_up,hist_down = utils.ComputeSystematics(hist_fake,hist_fake_sys,"fake_qcd"+Label)
        hists_fake_sys["fake_qcd"+Label+"_"+args.era+"Up"] = hist_up
        hists_fake_sys["fake_qcd"+Label+"_"+args.era+"Down"] = hist_down

    # creating shape templates for signal systematics 
    hists_sig_sys = {}
    for name_unc in uncert_names:
        name_hist = "wtaunu_tau_"+name_unc
        name = "wtaunu_"+name_unc
        name_output = "wtaunu_"+suffix+"_"+args.era+"_"+name_unc+"_"+args.era
        hist_sig_sys = hists_sig_shape[name_hist]
        hist_up,hist_down = utils.ComputeSystematics(hist_sig,hist_sig_sys,name)
        hists_sig_sys[name_output+"Up"] = hist_up
        hists_sig_sys[name_output+"Down"] = hist_down

    # saving histograms to datacard file datacards
    outputFileName = utils.datacardsFolder + "/" + args.wpVsMu + "VsMu_" + args.wpVsE + "VsE/taunu_" + args.wp + "_" + args.era + "_" + suffix
    print
    print("Saving histograms to RooT file",outputFileName+".root")
    fileOutput = ROOT.TFile(outputFileName+".root","recreate")
    fileOutput.mkdir("taunu")
    fileOutput.cd("taunu")
    hist_data.Write("data_obs")
    hist_sig.Write("wtaunu_"+suffix+"_"+args.era)
    hist_bkg_tau.Write("tau_"+suffix+"_"+args.era)
    hist_bkg_lfakes.Write("lfakes")
    hist_fake.Write("fake")
    # signal shape systematics
    for histName in hists_sig_sys:
        hists_sig_sys[histName].Write(histName)
    # FF shape systematics
    for histName in hists_fake_sys:
        hists_fake_sys[histName].Write(histName)    
    fileOutput.Close()

    uncs_fake = []
    for sampleLabel in ["ewk","qcd"]:
        for ptratioLabel in ["_ptratioLow","_ptratioHigh"]:
            unc = sampleLabel+ptratioLabel+statUncLabel+"_"+args.era
            uncs_fake.append(unc)

    CreateCardsWToTauNu(outputFileName,hist_data,hist_fake,hist_bkg_tau,hist_bkg_lfakes,hist_sig,uncs_fake,uncert_names_full,args.era,suffix)
                
