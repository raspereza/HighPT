#! /usr/bin/env python
# Author: Alexei Raspereza (December 2023)
# thin-jet ID SF measurements 
# Datacards producer for the signal region (W*->tau+v) 
import ROOT
import HighPT.ThinJet.utilsThinJet as utils
from array import array
import math
import HighPT.ThinJet.stylesHighPT as styles
import os

#################################
#     definition of samples     #
#################################
taubkgSampleNames = ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ','ZJetsToNuNu_HT-100To200','ZJetsToNuNu_HT-200To400','ZJetsToNuNu_HT-400To600','ZJetsToNuNu_HT-600To800','ZJetsToNuNu_HT-800To1200','ZJetsToNuNu_HT-1200To2500']

bkgSampleNames = ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500','ZJetsToNuNu_HT-100To200','ZJetsToNuNu_HT-200To400','ZJetsToNuNu_HT-400To600','ZJetsToNuNu_HT-600To800','ZJetsToNuNu_HT-800To1200','ZJetsToNuNu_HT-1200To2500']

sigSampleNames = ['WToTauNu_M-200']

def FitConst(x,par):
    return par[0]

##################################
# computing j->tau fake template #
################################## 
def ComputeFake(h_wjets,h_closure,name):
    nbins = h_wjets.GetNbinsX()
    hist = h_wjets.Clone(name)
    histUp = h_wjets.Clone(name+"Up")
    histDown = h_wjets.Clone(name+"Down")
    print
    print('Computing fake histogram ->',name)
    for i in range(1,nbins+1):
        x_corr = h_closure.GetBinContent(i)
        x_wjets = h_wjets.GetBinContent(i)
        e_wjets = h_wjets.GetBinError(i)
        x_fakes_down = x_wjets
        e_fakes = e_wjets * x_corr
        x_fakes = x_wjets * x_corr
        x_fakes_up = x_wjets * x_corr * x_corr
        histDown.SetBinContent(i,x_fakes_down)
        histDown.SetBinError(i,e_fakes)
        hist.SetBinContent(i,x_fakes)
        hist.SetBinError(i,e_fakes)
        histUp.SetBinContent(i,x_fakes_up)
        histUp.SetBinError(i,e_fakes)
        lowerEdge = hist.GetBinLowEdge(i)
        upperEdge = hist.GetBinLowEdge(i+1)
        print("[%3d,%4d] = %7.1f +/- %5.1f" %(lowerEdge,upperEdge,x_fakes,e_fakes))

    print
    return hist,histUp,histDown

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
        print("[%3d,%4d] = %4.2f +/- %4.2f (%4.2f rel) ; Data = %6.0f ; MC = %6.1f" %(lowerEdge,upperEdge,ratio,eratio,eratio/ratio,xdata,xmc))

    return h_fraction

############################
###### Closure test ########
############################
def PlotClosure(h_models,wp,era,var,dm):

    print
    print("Plotting closure")

    h_data  = h_models["bkg_fake"]
    h_model = h_models["bkg_fake_mc_wjets"]    
    
    styles.InitData(h_data)
    h_tot = h_model.Clone('h_tot_model')
    # add systematic uncertainties
    nbins = h_tot.GetNbinsX()
    for i in range(1,nbins+1):
        error2 = h_tot.GetBinError(i)*h_tot.GetBinError(i)
        errorStat = h_tot.GetBinError(i)
        xcen = h_tot.GetBinContent(i)
        dcen = h_data.GetBinContent(i)
        derr = h_data.GetBinError(i)
        for uncLabel in utils.statUncLabels:
            name = "bkg_fake_mc_wjets" + uncLabel
            xsys = h_models[name].GetBinContent(i)
            error2 += (xcen-xsys)*(xcen-xsys)
        error = math.sqrt(error2)
        lowerEdge = h_tot.GetBinLowEdge(i)
        upperEdge = h_tot.GetBinLowEdge(i+1)
        print("[%3d,%4d] = %5.1f +/- %4.1f(stat) +/- %5.1f(tot) : %5.1f +/- %5.1f" %(lowerEdge,upperEdge,xcen,errorStat,error,dcen,derr))
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

    leg = ROOT.TLegend(0.5,0.5,0.8,0.8)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.045)
    leg.SetHeader(era+' '+wp+' '+dm)
    leg.AddEntry(h_data, 'selection','lp')
    leg.AddEntry(h_model,'model','l')
    leg.Draw()

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
    canvas.Print(utils.figuresFolderWTauNu+"/closure_"+var+"_"+wp+"_"+dm+"_"+era+".png")

    nonclosure = func.GetParameter(0)
    outputFileName = utils.datacardsFolder+"/closure_"+var+"_"+wp+"_"+dm+"_"+era
    print
    print("Saving fit function to RooT file",outputFileName+".root")
    fileOutput = ROOT.TFile(outputFileName+".root","recreate")
    fileOutput.cd("")
    h_data.Write('data')
    h_model.Write('model')
    func.Write("closure")
    fileOutput.Close()
    
    return nonclosure,hist_ratio

##########################
# Plotting distributions #
##########################
def PlotWToTauNu(h_data_input,h_fake_input,h_tau_input,h_bkg_input,h_sig_input,wp,era,var,dm):
    
    # protection from zero entries
    xb1 = max(h_bkg_input.GetBinContent(1),0.1)
    h_bkg_input.SetBinContent(1,xb1)

    h_data = h_data_input.Clone("data_plot")
    h_fake = h_fake_input.Clone("fake_plot")
    h_bkg = h_bkg_input.Clone("bkg_plot")
    h_tau = h_tau_input.Clone("tau_plot")
    h_sig = h_sig_input.Clone("sig_plot")

    # log-normal uncertainties 
    #  5% signal, 
    # 10% fake, 
    # 20% genuine tau background
    # 50% lfakes
    nbins = h_data.GetNbinsX()
    e_sig_sys = 0.05
    e_fake_sys = 0.1
    e_bkg_sys = 0.5
    e_tau_sys = 0.2
    print
    print('Plotting distribution of',var)
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
        print("[%3d,%4d] = %6.1f : %5.0f" %(lowerEdge,upperEdge,x_model,x_data))


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

    leg = ROOT.TLegend(0.55,0.4,0.75,0.75)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.047)
    leg.SetHeader(wp+' '+dm)
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
    canvas.Print(utils.figuresFolderWTauNu+"/wtaunu_"+var+"_"+wp+"_"+dm+"_"+era+".png")

def CreateCardsWToTauNu(fileName,h_data,h_fake,h_tau,h_bkg,h_sig,uncs_fake,uncs_sig):

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
    f.write("shapes * *  "+rootFileName+"  taunu/$PROCESS taunu/$PROCESS_$SYSTEMATIC \n")
    f.write("---------------------------\n")
    f.write("bin                  WtoTauNu      WtoTauNu      WtoTauNu      WtoTauNu\n")
    f.write("process              tau           wtaunu        fake          lfakes\n")
    f.write("process              -1            0             1             2\n")
    f.write("rate                 %4.3f         %4.3f      %4.3f      %4.3f\n"%(x_tau,x_sig,x_fake,x_bkg))
    f.write("---------------------------\n")
    f.write("extrapW        lnN   -             1.04          -             -\n")
    f.write("bkgNorm_taunu  lnN   1.2           -             -             -\n")
    f.write("lep_fakes      lnN   -             -             -           1.5\n")
    f.write("FFclosure shape      -             -             1.0           -\n")
    for unc in uncs_sig:
        f.write(unc+"     shape   -             1.0           -             -\n")
    for unc in uncs_fake:
        f.write(unc+"     shape   -             -             1.0           -\n")
    f.write("normW  rateParam  WtoTauNu wtaunu  1.0  [0.5,1.5]\n")
    f.write("* autoMCStats 0\n")
    f.close()
    

############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='UL2017', help="""Era : UL2016_preVFP, UL2016_postVFP, UL2017, UL2018""")
    parser.add_argument('-wp','--WP', dest='wp', default='VVLoose', help=""" tau ID WP : VVLoose, VLoose, Loose """)
    parser.add_argument('-prong','--prong', dest='dm', default='1prong', help=""" Decay mode : 1prong, 2prong, 3prong """)
    parser.add_argument('-var','--variable',dest='variable',default='mt_1',help=""" Variable to plot""")

    args = parser.parse_args() 

    Eras = ['UL2016_preVFP','UL2016_postVFP'] # UL2016 = UL2016_preVFP + UL2016_postVFP 

    Prongs = ['1prong', '2prong', '3prong']
    Variables = ['mt_1','mt_jet_1','pt_1','jpt_match_1','eta_1','jeta_match_1','met','jpt_ratio_1']
    WorkingPoints = ['VVLoose','VLoose','Loose']

    if args.variable not in Variables: 
        print('unspecified variable',args.variable)
        print('available options',Variables)
        exit(1)

    if args.wp not in WorkingPoints:
        print('unspecified WP',args.wp)
        print('available options',WorkingPoints)
        exit(1)

    if args.era not in ['UL2016_preVFP','UL2016_postVFP','UL2016','UL2017','UL2018']:
        print('unspecified era',args.era)
        print('available options',Eras)
        exit(1)

    if args.dm not in Prongs:
        print('unspecified prong',args.dm)
        print('available options',Prongs)
        exit(1)



    wpVsMu = utils.wpVsMu
    wpVsE  = utils.wpVsE
    xbins_mt = [300,400,500,600,800,1200]
    xbins_pt = [100,150,200,250,300,400,600]
    xbins_met = [150,200,300,400,500,600]
    xbins_pt_ratio = [0.0, 0.2, 0.4, 0.5 ,0.6, 0.7, 0.8, 0.9, 1.0, 1.2]
    xbins_eta = [-2.4, -1.8, -1.2, -0.6, 0.0, 0.6, 1.2, 1.8, 2.4]

    xbins = xbins_mt
    if args.variable=='jpt_ratio_1': xbins_pt_ratio
    if args.variable=='mt_jet_1': xbins = xbins_mt
    if args.variable=='pt_1': xbins = xbins_pt
    if args.variable=='eta_1': xbins =  xbins_eta
    if args.variable=='jpt_match_1': xbins = xbins_pt
    if args.variable=='jeta_match_1': xbins = xbins_eta
    if args.variable=='met': xbins = xbins_met

    basefolder = utils.picoFolderTauNu
    var = args.variable    

    # initializing instance of FF class    
    fullpathFF = utils.fakeFactorFolder + '/ff_'+args.wp+"VSjet_"+args.era+".root"
    fakeFactor = utils.FakeFactorHighPt(fullpathFF)

    # initializing instance of TauNuCuts class
    antiMu = utils.tauVsMuIntWPs[wpVsMu]
    antiE  = utils.tauVsEleIntWPs[wpVsE]
    decaymode = args.dm
    wtaunuCuts = utils.TauNuCuts(antiMu=antiMu,antiE=antiE,dm=decaymode)    

    # definition of cuts
    commonCut = "metfilter>0.5&&mettrigger>0.5&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&njets==0&&idDeepTau2017v2p1VSmu_1>="+utils.tauVsMuWPs[wpVsMu]+"&&idDeepTau2017v2p1VSe_1>="+utils.tauVsEleWPs[wpVsE]+"&&idDeepTau2017v2p1VSjet_1>=" + utils.tauWPs[args.wp] + "&&" + utils.dmCuts[args.dm]

    commonCutTau       = commonCut + "&&genmatch_1==5"
    commonCutLFakes    = commonCut + "&&(genmatch_1>=1&&genmatch_1<=4)"
    commonCutJFakes    = commonCut + "&&genmatch_1==0"
    commonCutNotJFakes = commonCut + "&&(genmatch_1>=1&&genmatch_1<=5)"

    # vector uncertainties
    uncert_names = utils.unc_jme
    uncert_names_full = [] # uncertainty names with suffix era
    for unc in uncert_names:
        uncert_names_full.append(unc+"_"+args.era)

    print
    print('initializing data samples >>>')
    metSamples = {} # data samples dictionary
    if args.era=='UL2016':
        for Era in Eras:
            metNames = utils.met[Era]
            for metName in metNames:
                metSamples[metName+'_'+Era] = utils.sampleHighPt(
                    basefolder,Era,"taunu",metName,True)
                metSamples[metName+'_'+Era].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)
    else:
        metNames = utils.met[args.era]
        for metName in metNames:
            metSamples[metName] = utils.sampleHighPt(basefolder,args.era,
                                                     "taunu",metName,True)
            metSamples[metName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print
    print('initializing background samples >>>')
    bkgSamples = {} # MC bkg samples dictionary 
    if args.era=='UL2016':
        for Era in Eras:
            for bkgSampleName in bkgSampleNames:
                bkgSamples[bkgSampleName+'_'+Era] = utils.sampleHighPt(
                    basefolder,Era,"taunu",bkgSampleName,False)
                bkgSamples[bkgSampleName+'_'+Era].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)
    else:
        for bkgSampleName in bkgSampleNames:
            bkgSamples[bkgSampleName] = utils.sampleHighPt(basefolder,args.era,
                                                           "taunu",bkgSampleName,False)
            bkgSamples[bkgSampleName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print
    print('initializing background samples (for taus) >>>')
    taubkgSamples = {} # MC bkg samples dictionary 
    if args.era=='UL2016':
        for Era in Eras:
            for bkgSampleName in taubkgSampleNames:
                taubkgSamples[bkgSampleName+'_'+Era] = utils.sampleHighPt(
                    basefolder,Era,"taunu",bkgSampleName,False)
                taubkgSamples[bkgSampleName+'_'+Era].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)
    else:
        for bkgSampleName in taubkgSampleNames:
            taubkgSamples[bkgSampleName] = utils.sampleHighPt(basefolder,args.era,
                                                              "taunu",bkgSampleName,False)
            taubkgSamples[bkgSampleName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    print
    print('initializing signal samples >>>')
    sigSamples = {} # MC signal samples dictionary 
    if args.era=='UL2016':
        for Era in Eras:
            for sigSampleName in sigSampleNames:
                sigSamples[sigSampleName+'_'+Era] = utils.sampleHighPt(
                    basefolder,Era,"taunu",sigSampleName,False)
                sigSamples[sigSampleName+'_'+Era].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)

    else:
        for sigSampleName in sigSampleNames:
            sigSamples[sigSampleName] = utils.sampleHighPt(basefolder,args.era,
                                                           "taunu",sigSampleName,False)
            sigSamples[sigSampleName].SetTauNuConfig(fakeFactor,args.wp,wtaunuCuts)


    # running on signal samples (central template and uncertainties)
    print
    print('Running on signal samples >>>')
    hists_sig_shape = {}
    no_unc = [""]
    lst = no_unc + uncert_names
    for name in lst:

        name_unc = ""
        name_hist = "wtaunu_tau"
        if name!="": 
            name_unc = "_"+name+"Up"
            name_hist = "wtaunu_tau_"+name
        
        metUnc = "met"+name_unc
        metdphiUnc = "metdphi_jet_1"+name_unc

        metCut     = metUnc+">%3.1f"%(wtaunuCuts.metCut)
        ptLowerCut = "pt_1>%3.1f"%(wtaunuCuts.ptLowerCut)
        ptUpperCut = "pt_1<%3.1f"%(wtaunuCuts.ptUpperCut)
        ptJetLowerCut = "jpt_match_1>%3.1f"%(wtaunuCuts.ptJetLowerCut)
        ptJetUpperCut = "jpt_match_1<%3.1f"%(wtaunuCuts.ptJetUpperCut)
        etaCut     = "fabs(eta_1)<%3.1f"%(wtaunuCuts.etaCut)
        etaJetCut  = "fabs(jeta_match_1)<%3.1f"%(wtaunuCuts.etaJetCut)
        metdphiCut = metdphiUnc+">%3.1f"%(wtaunuCuts.metdphiCut)

        uncertCut = metCut+"&&"+ptJetLowerCut+"&&"+ptJetUpperCut+"&&"+ptLowerCut+"&&"+ptUpperCut+"&&"+etaCut+"&&"+etaJetCut+"&&"+metdphiCut
        totalCut = commonCutTau+"&&"+uncertCut
        
        histo = utils.RunSamples(sigSamples,var+name_unc,"weight",totalCut,xbins,name_hist)
        hists_sig_shape[name_hist] = histo
        
    # running on bkg samples ->
    metCut     = "met>%3.1f"%(wtaunuCuts.metCut)
    ptLowerCut = "pt_1>%3.1f"%(wtaunuCuts.ptLowerCut)
    ptUpperCut = "pt_1<%3.1f"%(wtaunuCuts.ptUpperCut)
    ptJetLowerCut = "jpt_match_1>%3.1f"%(wtaunuCuts.ptJetLowerCut)
    ptJetUpperCut = "jpt_match_1<%3.1f"%(wtaunuCuts.ptJetUpperCut)
    etaCut     = "fabs(eta_1)<%3.1f"%(wtaunuCuts.etaCut)
    etaJetCut  = "fabs(jeta_match_1)<%3.1f"%(wtaunuCuts.etaJetCut)
    metdphiCut = "metdphi_jet_1>%3.1f"%(wtaunuCuts.metdphiCut)

    kinCuts = metCut+"&&"+ptJetLowerCut+"&&"+ptJetUpperCut+"&&"+ptLowerCut+"&&"+ptUpperCut+"&&"+etaCut+"&&"+etaJetCut+"&&"+metdphiCut
    totalCutTau       = commonCutTau+"&&"+kinCuts
    totalCutLFakes    = commonCutLFakes+"&&"+kinCuts
    totalCutJFakes    = commonCutJFakes+"&&"+kinCuts
    totalCutNotJFakes = commonCutNotJFakes+"&&"+kinCuts
    hist_bkg_tau      = utils.RunSamples(taubkgSamples,var,"weight",totalCutTau,xbins,"bkg_tau")
    hist_bkg_lfakes   = utils.RunSamples(bkgSamples,var,"weight",totalCutLFakes,xbins,"bkg_lfakes")
    #    hist_bkg_jfakes   = utils.RunSamples(bkgSamples,var,"weight",totalCutJFakes,xbins,"bkg_jfakes")
    #    hist_bkg_notfakes = utils.RunSamples(bkgSamples,var,"weight",totalCutNotJFakes,xbins,"bkg_notfakes")

    # running selection on bkgd samples
    print
    print('Running on background samples >>>')
    hists_bkg_fake    = utils.RunSamplesTauNu(bkgSamples,var,xbins,"_fake","bkg")
    hists_bkg_notFake = utils.RunSamplesTauNu(bkgSamples,var,xbins,"_notFake","bkg")
    sig_wtaunu        = hists_sig_shape["wtaunu_tau"]

    print
    print("Check composition of simulated events:")
    print('l->tau fakes          = %7.1f'%(hist_bkg_lfakes.GetSumOfWeights()))
    print('genuine taus (not W*) = %7.1f'%(hist_bkg_tau.GetSumOfWeights()))
    print('W*->tau+v             = %7.1f'%(sig_wtaunu.GetSumOfWeights()))
    #    print('j->tau fakes     = %7.1f : %7.1f'%(hist_bkg_jfakes.GetSumOfWeights(),hists_bkg_fake['bkg_fake'].GetSumOfWeights()))
    #    print('not j->tau fakes = %7.1f : %7.1f'%(hist_bkg_notfakes.GetSumOfWeights(),hists_bkg_notFake['bkg_notFake'].GetSumOfWeights()))
    print

    # running selection on data 
    print
    print('Running on data samples >>>')
    hists_data        = utils.RunSamplesTauNu(metSamples,var,xbins,"","data")

    # correct ewk componet for non-closure
    hist_num = hists_bkg_fake["bkg_fake"]
    nonclosure,h_closure = PlotClosure(hists_bkg_fake,args.wp,args.era,var,args.dm)

    # Create j->tau fake histograms
    # first subtract from data templates notFake contribution estimated with simulated samples
    label = "data_wjets"
    hists_data["data_"+label].Add(hists_data["data_"+label],hists_bkg_notFake["bkg_notFake_"+label],1.,-1.)
    for uncLabel in utils.statUncLabels:
        sysLabel = label + uncLabel
        hists_data["data_"+sysLabel].Add(hists_data["data_"+sysLabel],hists_bkg_notFake["bkg_notFake_"+sysLabel],1.,-1.)
                
    hist_wjets  = hists_data["data_data_wjets"]
    hist_dijets = hists_data["data_data_dijets"]
    hist_fake,hist_fake_up,hist_fake_down = ComputeFake(hist_wjets,h_closure,'fake')
    hist_data = hists_data["data"]
    hist_sig = hists_sig_shape["wtaunu_tau"]
    hist_bkg = hists_bkg_notFake["bkg_notFake"]


    # making control plot
    PlotWToTauNu(hist_data,hist_fake,hist_bkg_tau,hist_bkg_lfakes,hist_sig,args.wp,args.era,var,args.dm)

    if args.variable!='mt_1':
        exit(1)

    # creating shape templates for FF systematics
    hists_fake_sys = {}
    for uncLabel in utils.statUncLabels:
        Label = uncLabel
        # ewk FF
        name_fake = "fake_wjets" + Label
        hist_fake_sys,hUp,hDown = ComputeFake(hists_data["data_data_wjets"+Label],h_closure,name_fake)
        hist_up,hist_down = utils.ComputeSystematics(hist_fake,hist_fake_sys,"fake_ewk"+Label)
        hists_fake_sys["fake_ewk"+Label+"Up"] = hist_up
        hists_fake_sys["fake_ewk"+Label+"Down"] = hist_down


    # creating shape templates for signal systematics 
    hists_sig_sys = {}
    for name_unc in uncert_names:
        name_hist = "wtaunu_tau_"+name_unc
        name = "wtaunu_"+name_unc
        name_output = "wtaunu_"+name_unc+"_"+args.era
        hist_sig_sys = hists_sig_shape[name_hist]
        hist_up,hist_down = utils.ComputeSystematics(hist_sig,hist_sig_sys,name)
        hists_sig_sys[name_output+"Up"] = hist_up
        hists_sig_sys[name_output+"Down"] = hist_down


    # saving histograms to datacard file datacards
    outputFileName = utils.datacardsFolder+"/taunu_"+args.wp+"_"+args.dm+"_"+args.era
    print
    print("Saving histograms to RooT file",outputFileName+".root")
    fileOutput = ROOT.TFile(outputFileName+".root","recreate")
    fileOutput.mkdir("taunu")
    fileOutput.cd("taunu")
    hist_data.Write("data_obs")
    hist_sig.Write("wtaunu")
    hist_bkg_tau.Write("tau")
    hist_bkg_lfakes.Write("lfakes")
    hist_fake.Write("fake")
    hist_fake_up.Write("fake_FFclosureUp");
    hist_fake_down.Write("fake_FFclosureDown");
    # signal shape systematics
    for histName in hists_sig_sys:
        hists_sig_sys[histName].Write(histName)
    # FF shape systematics
    for histName in hists_fake_sys:
        hists_fake_sys[histName].Write(histName)    
    fileOutput.Close()

    uncs_fake = ["ewk_unc1","ewk_unc2"]
    CreateCardsWToTauNu(outputFileName,hist_data,hist_fake,hist_bkg_tau,hist_bkg_lfakes,hist_sig,uncs_fake,uncert_names_full)
                
