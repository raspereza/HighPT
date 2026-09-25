#! /usr/bin/env python3
# Author: Alexei Raspereza (November 2024)
# Description: computes fake factors 
#              for high pT jet->tau fakes

from ROOT import TFile, TH1, TH1D, TCanvas, TLegend, TH2, gROOT, TF1, TVirtualFitter, kCyan, gStyle, TString
import HighPT.Tau.utilsHighPT as utils
import HighPT.Tau.stylesHighPT as styles
import HighPT.Tau.analysisHighPT as analysis
import os
from array import array

#################################
#     definition of cuts        #
#################################

basecutEWK = 'mt_1>50&&iso_1<0.15&&pt_1>30&&fabs(eta_1)<2.4&&metfilter>0.5&&njets==0&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&dphi>2.4&&pt_2>100&&fabs(eta_2)<2.5'
basecutQCD = 'jpt>100&&njets==1&&dphi>2.4&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&pt_2>90&&fabs(eta_2)<2.5'

basecut = {
    "dijets": basecutQCD,
    "wjets" : basecutEWK
}

genFakeCut    = 'genmatch_2==0'
genNotFakeCut = 'genmatch_2!=0'

#########################
# Definition of samples #
#########################
RunMCSampleNames = {
    "Run2" : ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','WJetsToLNu','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ'],

    "2022" : ['DYto2L-4Jets_MLL-50','TTTo2L2Nu','TTtoLNu2Q','TTto4Q','TBbarQ_t-channel','TbarBQ_t-channel','TWminustoLNu2Q','TWminusto2L2Nu','TbarWplustoLNu2Q','TbarWplusto2L2Nu','WW','WZ','ZZ','WJetsToLNu-4Jets_1J','WJetsToLNu-4Jets_2J','WJetsToLNu-4Jets_3J','WJetsToLNu-4Jets_4J','WtoLNu-4Jets_HT-100to400','WtoLNu-4Jets_HT-400to800'],

    "2023" : ['DYto2L-4Jets_MLL-50','TTto2L2Nu','TTtoLNu2Q','TTto4Q','TWminustoLNu2Q','TWminusto2L2Nu','TbarWplustoLNu2Q','TbarWplusto2L2Nu','WW','WZ','ZZ','WtoLNu-4Jets_1J','WtoLNu-4Jets_2J','WtoLNu-4Jets_3J','WtoLNu-4Jets_4J','WtoLNu_HT100to400','WtoLNu_HT400to800'],

    "2024" : ['DYto2Mu_Bin-MLL-50to120','DYto2Mu_Bin-MLL-120to200','DYto2Tau_Bin-MLL-50to120','DYto2Tau_Bin-MLL-120to200','WW','WZ','ZZ','WtoLNu-2Jets_Bin-1J-PTLNu-100to200','WtoLNu-2Jets_Bin-1J-PTLNu-200to400','WtoLNu-2Jets_Bin-1J-PTLNu-400to600','WtoLNu-2Jets_Bin-1J-PTLNu-600','WtoLNu-2Jets_Bin-2J-PTLNu-100to200','WtoLNu-2Jets_Bin-2J-PTLNu-200to400','WtoLNu-2Jets_Bin-2J-PTLNu-400to600','WtoLNu-2Jets_Bin-2J-PTLNu-600','TTto2L2Nu','TTtoLNu2Q','TWminusto2L2Nu','TWminustoLNu2Q','TbarWplusto2L2Nu','TbarWplustoLNu2Q'],
    
    "2025" : ['DYto2Mu_Bin-MLL-50to120','DYto2Mu_Bin-MLL-120to200','DYto2Tau_Bin-MLL-50to120','DYto2Tau_Bin-MLL-120to200','WW','WZ','ZZ','WtoLNu-2Jets_Bin-1J-PTLNu-100to200','WtoLNu-2Jets_Bin-1J-PTLNu-200to400','WtoLNu-2Jets_Bin-1J-PTLNu-400to600','WtoLNu-2Jets_Bin-1J-PTLNu-600','WtoLNu-2Jets_Bin-2J-PTLNu-100to200','WtoLNu-2Jets_Bin-2J-PTLNu-200to400','WtoLNu-2Jets_Bin-2J-PTLNu-400to600','WtoLNu-2Jets_Bin-2J-PTLNu-600','TTto2L2Nu','TTtoLNu2Q','TWminusto2L2Nu','TWminustoLNu2Q','TbarWplusto2L2Nu','TbarWplustoLNu2Q'],
    
}

RunSigSampleNames = {
    'Run2' : ['WJetsToLNu','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500'],

    '2022' : ['WJetsToLNu-4Jets_1J','WJetsToLNu-4Jets_2J','WJetsToLNu-4Jets_3J','WJetsToLNu-4Jets_4J','WtoLNu-4Jets_HT-100to400','WtoLNu-4Jets_HT-400to800'],

    '2023' : ['WtoLNu-4Jets_1J','WtoLNu-4Jets_2J','WtoLNu-4Jets_3J','WtoLNu-4Jets_4J','WtoLNu_HT100to400','WtoLNu_HT400to800'],

    '2024' : ['WtoLNu-2Jets_Bin-1J-PTLNu-100to200','WtoLNu-2Jets_Bin-1J-PTLNu-200to400','WtoLNu-2Jets_Bin-1J-PTLNu-400to600','WtoLNu-2Jets_Bin-1J-PTLNu-600','WtoLNu-2Jets_Bin-2J-PTLNu-100to200','WtoLNu-2Jets_Bin-2J-PTLNu-200to400','WtoLNu-2Jets_Bin-2J-PTLNu-400to600','WtoLNu-2Jets_Bin-2J-PTLNu-600'],
    
    '2025' : ['WtoLNu-2Jets_Bin-1J-PTLNu-100to200','WtoLNu-2Jets_Bin-1J-PTLNu-200to400','WtoLNu-2Jets_Bin-1J-PTLNu-400to600','WtoLNu-2Jets_Bin-1J-PTLNu-600','WtoLNu-2Jets_Bin-2J-PTLNu-100to200','WtoLNu-2Jets_Bin-2J-PTLNu-200to400','WtoLNu-2Jets_Bin-2J-PTLNu-400to600','WtoLNu-2Jets_Bin-2J-PTLNu-600'],
    
}

# Fitting function (tau pt, ptratio bins)
def FitPt(x,par):
    arg = x[0]
    if arg>utils.ptUncThreshold['pttau']:
        arg = utils.ptUncThreshold['pttau']
    a = 0.01*(arg-100.)
    ff = par[0]+par[1]*a+par[2]*a*a+par[3]*a*a*a
    return ff

def FitPtConst(x,par):
    ff = par[0]
    if x[0]>par[1]:
        ff = par[2]
    return ff

def FitConst(x,par):
    ff = par[0]
    return ff

# Fitting function (mass, DM bins)
def FitMass(x,par):
    ff = par[0]+par[1]*x[0]+par[2]*x[0]*x[0]
    return ff

def AuxiliaryHistograms():
    histos = {}

    pttau_bins = [0,300,10000]
    pttauHist = TH1D("pttau","pttau",2,array('d',list(pttau_bins)))
    pttauHist.GetXaxis().SetBinLabel(1,"pttauLow")
    pttauHist.GetXaxis().SetBinLabel(2,"pttauHigh")
    histos['pttau'] = pttauHist

    ptjet_bins = [0,300,10000]
    ptjetHist = TH1D("ptjet","ptjet",2,array('d',list(ptjet_bins)))
    ptjetHist.GetXaxis().SetBinLabel(1,"ptjetLow")
    ptjetHist.GetXaxis().SetBinLabel(2,"ptjetHigh")
    histos['ptjet'] = ptjetHist

    ptratio_bins = [0,0.85,100]
    ptratioHist = TH1D("ptratio","ptratio",2,array('d',list(ptratio_bins)))
    ptratioHist.GetXaxis().SetBinLabel(1,"ptratioLow")
    ptratioHist.GetXaxis().SetBinLabel(2,"ptratioHigh")
    histos['ptratio'] = ptratioHist

    dm_bins = [-0.5,0.5,9.5,10.5,21.5]
    dmHist = TH1D("dm","dm",4,array('d',list(dm_bins)))
    dmHist.GetXaxis().SetBinLabel(1,'1prong')
    dmHist.GetXaxis().SetBinLabel(2,'1prongPi0')
    dmHist.GetXaxis().SetBinLabel(3,'3prong')
    dmHist.GetXaxis().SetBinLabel(4,'3prongPi0')
    histos['dm'] = dmHist

    return histos

###########################
# Plotting and fitting FF #
###########################
def DrawFF(hist,**kwargs):

    isdata = kwargs.get('isdata',True)
    variable1 = kwargs.get('variable1','pttau')
    variable2 = kwargs.get('variable2','ptratio')
    label = kwargs.get('label','ptratioLow')
    channel = kwargs.get('channel','wjets')
    option = kwargs.get('option','comb')
    WPvsJet= kwargs.get('WPvsJet','Medium')
    WPvsE  = kwargs.get('WPvsE','TightVsE')
    WPvsMu = kwargs.get('WPvsMu','TightVsMu')
    trigger = kwargs.get('trigger','incl')
    tagger = kwargs.get('tagger','deeptau')
    era = kwargs.get('era','2025')

    labelSample = "mc"
    color = 2
    if isdata: 
        color = 1
        labelSample = "data"
    
    #    from IPython import embed
    
    print('')
    print('fitting FF histo >>>',era,channel,label,labelSample)
    #    embed()

    styles.InitData(hist)

    # assert bin content > 0 
    nbins = hist.GetNbinsX()
    xmin = hist.GetXaxis().GetBinLowEdge(1)
    xmax = hist.GetXaxis().GetBinLowEdge(nbins+1)
    ymax = hist.GetMaximum()
    ymin = hist.GetMinimum()
    average = 0.5*(ymin+ymax)
    maximum = 0
    for i in range(1,nbins+1):
        x = hist.GetBinContent(i)
        e = hist.GetBinError(i)
        xe = x+e
        if xe>maximum:
            maximum = xe
        #        print(i,hist.GetBinContent(i),hist.GetBinError(i))
        if x<1e-5 or x>0.9:     
            xcorr = 0.5*hist.GetBinError(i)
            hist.SetBinContent(i,xcorr)
            hist.SetBinError(i,0.75*xcorr)
            
    print('')

    histToPlot = hist.Clone('temp')

    if variable1=='pttau' or variable1=='ptjet':
        if trigger=='incl':
            #            contentLastBin = hist.GetBinContent(hist.GetNbinsX())
            f1 = TF1("f1",FitPt,xmin,xmax,4)
            f1.SetParameter(0,average)
            f1.SetParameter(1,0.)
            f1.SetParameter(2,0.)
            f1.SetParameter(3,0.)
        else:
            f1 = TF1("f1",FitPtConst,xmin,xmax,3)
            f1.SetParameter(0,average)
            f1.FixParameter(1,utils.ptUncThreshold[variable1])
            f1.SetParameter(2,average)
    else:
        if label=='1prong':
            f1 = TF1("f1",FitConst,xmin,xmax,1)
            f1.SetParameter(0,average)
        else:
            f1 = TF1("f1",FitMass,xmin,xmax,3)
            f1.SetParameter(0,average)
            f1.SetParameter(1,0)
            f1.SetParameter(2,0)    

    canv = styles.MakeCanvas("canv","",700,600)
    hist.Fit('f1',"R")
    if variable1=='mtau': canv.SetLogx(False)
    else: canv.SetLogx(True)

    hfit = TH1D("ff_"+labelSample+"_"+channel+"_"+variable1+"_"+label+"_"+trigger,"",5000,xmin,xmax)
    TVirtualFitter.GetFitter().GetConfidenceIntervals(hfit,0.68)

    hfitline = hfit.Clone('histline')
    hfitline.SetLineWidth(2)
    hfitline.SetLineColor(4)
    hfitline.SetMarkerSize(0)
    hfitline.SetMarkerStyle(0)
    for i in range(1,hfitline.GetNbinsX()+1): hfitline.SetBinError(i,0)

    styles.InitModel(hfit,4)
    hfit.SetFillColor(kCyan)
    hfit.SetFillStyle(1001)
    hfit.SetLineWidth(2)
    hfit.SetLineColor(4)
    hfit.SetMarkerSize(0)
    hfit.SetMarkerStyle(0)
    maxFit = hfit.GetMaximum()
    
    hfit.GetYaxis().SetRangeUser(0.,1.5*maximum)
    if variable1=='mtau': hfit.GetXaxis().SetTitle("#tau mass [GeV]")
    elif variable1=='ptjet': hfit.GetXaxis().SetTitle("jet p_{T} [GeV]")
    else: hfit.GetXaxis().SetTitle("#tau p_{T} [GeV]")
    hfit.GetYaxis().SetTitle("Fake factor")

    hfit.Draw("e2")
    hfitline.Draw("hsame")
    histToPlot.Draw("e1same")

    leg = TLegend(0.22,0.7,0.5,0.9)
    styles.SetLegendStyle(leg)
    leg.SetHeader('%s:%s:%s:%s'%(channel,tagger,label,trigger))
    leg.SetTextSize(0.035)
    if isdata: leg.AddEntry(hist,"Data",'lp')
    else: leg.AddEntry(hist,"MC",'lp')
    leg.AddEntry(hfit,'Fit','l')
    leg.Draw()
    styles.CMS_label(canv,era=era,extraText='Internal')

    canv.RedrawAxis()
    canv.Update()


    if variable1=='pttau' and variable2=='ptratio':
        png_file='%s_%s_%s_%s_%s_%s_%s_%s_%s'%(labelSample,
                                               channel,
                                               variable1,
                                               label,
                                               WPvsJet,
                                               WPvsMu,
                                               WPvsE,
                                               trigger,
                                               option);
        
        
        outdir = '%s/FF/%s/%s'%(utils.figureFolder,era,tagger)
        outfilename = outdir+'/'+png_file+'.png'
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        canv.Print(outfilename)
    
    return hfit

def main(outputfile,dataSamples,mcSamples,sigSamples,**kwargs):

    era = kwargs.get("era","2024")
    WPvsJet= kwargs.get("WPvsJet","Medium")
    channel = kwargs.get("channel","wjets")
    WPvsE = kwargs.get("WPvsE","Loose")
    WPvsMu = kwargs.get("WPvsMu","Loose")
    variable1 = kwargs.get("variable1","pttau")
    variable2 = kwargs.get("variable2","ptratio")
    tagger = kwargs.get("tagger","deeptau")
    option = kwargs.get("option","comb")

    print('')
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print('')
    print('Computing FF as a function of %s in bins of %s for era %s'%(variable1,variable2,era))
    print('%sVsJet  %sVsMu  %sVsE'%(WPvsJet,WPvsMu,WPvsE))


    cutTrigger = "(tautrigger1>0.5||tautrigger2>0.5||tautrigger3>0.5||tautrigger4>0.5)"
    if option=='deeptau':
        cutTrigger = "(tautrigger1>0.5)"
    elif option=='pnet':
        cutTrigger = "(tautrigger2>0.5||tautrigger3>0.5||tautrigger4>0.5)"
    cutNotTrigger = "(!" + cutTrigger +")"


    #    cutTrigger = "tautrigger1>-0.5"
    #    cutNotTrigger = "tautrigger1>-0.5"
    
    cutDMs = '(dm_2==0||dm_2==1||dm_2==10||dm_2==11)'
    cutNotDMs = 'dm_2!=0&&dm_2!=1&&dm_2!=10&&dm_2!=11'

    cutAntiLepDeepTau = "idDeepTau2018v2p5VSmu_2>=" + utils.tauVsMuWPs[WPvsMu]
    cutAntiLepDeepTau += "&&idDeepTau2018v2p5VSe_2>="  + utils.tauVsEleWPs[WPvsE]
    cutAntiLepDeepTau += "&&" + cutDMs

    cutTauDen = ""
    cutTauNum = ""
    
    qConfPNet = '&&fabs(qConfPNet_2)>0.2'
    qConfUParT = '&&fabs(qConfUParT_2)>0.2'

    if tagger=='deeptau':
        relaxedTauId = utils.RelaxedDeepTau[WPvsJet]
        sWP = utils.tauWPs[relaxedTauId]
        cutTauDen = cutAntiLepDeepTau
        cutTauNum = cutAntiLepDeepTau
        cutTauDen += "&&idDeepTau2018v2p5VSjet_2<%s&&idDeepTau2018v2p5VSjet_2>0"%(sWP)
        cutTauNum += "&&idDeepTau2018v2p5VSjet_2>=" + utils.tauWPs[WPvsJet]
        cutTauDen += cutDMs
        cutTauNum += cutDMs
    elif tagger=='pnet_hps' or 'pnet':
        relaxedTauId = utils.RelaxedPNet[WPvsJet]
        cutAntiLepPNet = "rawPNetVSmu_2>%6.4f"%(utils.PNetVSmuWPs[WPvsMu])
        cutAntiLepPNet += "&&rawPNetVSe_2>%6.4f"%(utils.PNetVSeWPs[WPvsE])        
        cutTauDen = cutAntiLepPNet
        cutTauNum = cutAntiLepPNet 
        cutTauDen += "&&rawPNetVSjet_2<%5.3f&&rawPNetVSjet_2>%5.3f"%(utils.PNetVSjetWPs[relaxedTauId],utils.PNetVSjetWPs['VVVLoose'])
        cutTauNum += "&&rawPNetVSjet_2>=%5.3f"%(utils.PNetVSjetWPs[WPvsJet])
        if tagger=='pnet_hps':
            cutTauDen += cutsDM
            cutTauNum += cutsDM
        #        cutTauDen += qConfPNet
        #        cutTauNum += qConfPNet
    else:
        relaxedTauId = utils.RelaxedUParT[WPvsJet]
        cutAntiLepUParT = "rawUParTVSmu_2>%6.4f"%(utils.UParTVSmuWPs[WPvsMu])
        cutAntiLepUParT += "&&rawUParTVSe_2>%6.4f"%(utils.UParTVSeWPs[WPvsE])
        cutTauDen = cutAntiLepUParT
        cutTauNum = cutAntiLepUParT 
        cutTauDen += "&&rawUParTVSjet_2<%5.3f&&rawPNetVSjet_2>%5.3f"%(utils.UParTVSjetWPs[relaxedTauId],utils.PNetVSjetWPs['VVVLoose'])
        cutTauNum += "&&rawUParTVSjet_2>=%5.3f"%(utils.UParTVSjetWPs[WPvsJet])
        #        cutTauDen += qConfUParT
        #        cutTauNum += qConfUParT
        
    ######################
    ## labels of cuts ####
    ######################
    binCuts = {}
    if variable2=='ptratio': 
        binCuts = utils.ptratioCuts
    else: 
        binCuts = utils.decayModeCuts
    
    ##############
    ## Variable ##
    ##############
    var = utils.variableLabel[variable1]

    ############################
    ###### Common cut ##########
    ############################
    commonCut = basecut[channel]

    # hotjet veto in 2023
    if era=='2023':
        commonCut += '&&hotjet_veto<0.5'

    histsdata = {}
    histssig = {}

    trigLabels = ['incl','trig','notrig']
    if variable2=='dm':
        trigLabels = ['incl']

    for label in binCuts:
        xbins = []
        xbinsTrig = []
        print('')
        print('***************************')
        print('Running over',label)
        print('')

        if variable1=='mtau': 
            xbins=utils.xbinsMass[label]
            xbinsTrig = xbins
        else: 
            xbins=utils.xbinsPt[var]
            xbinsTrig = utils.xbinsPtTrig[var]

        addCut = binCuts[label]
        cut = commonCut + "&&" + addCut

        cutNumerator = cut + "&&" + cutTauNum
        cutDenominator = cut + "&&" + cutTauDen

        cutNumIncl = cutNumerator
        cutDenIncl = cutDenominator
        
        cutNumTrig = cutNumIncl + "&&" + cutTrigger
        cutDenTrig = cutDenIncl + "&&" + cutTrigger

        cutNumNotTrig = cutNumIncl + "&&" + cutNotTrigger
        cutDenNotTrig = cutDenIncl + "&&" + cutNotTrigger

        cutNum = {
            'incl' : cutNumIncl,
            'trig' : cutNumTrig,
            'notrig' : cutNumNotTrig
        }
        cutDen = {
            'incl' : cutDenIncl,
            'trig' : cutDenTrig,
            'notrig' : cutDenNotTrig
        }

        Bins = {
            'incl' : xbins,
            'trig' : xbinsTrig,
            'notrig' : xbinsTrig,
        }

        datahistNum = {}
        datahistDen = {}
        for trigLabel in trigLabels:        

            nameNum = 'data_num_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
            nameDen = 'data_den_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
            datahistNum[trigLabel] = analysis.RunSamples(dataSamples,
                                                         var,
                                                         cutNum[trigLabel],
                                                         Bins[trigLabel],
                                                         nameNum)
            datahistDen[trigLabel] = analysis.RunSamples(dataSamples,
                                                         var,
                                                         cutDen[trigLabel],
                                                         Bins[trigLabel],
                                                         nameDen)

        if channel=="wjets":

            cutNumMCIncl = cutNumerator + "&&" + genNotFakeCut
            cutDenMCIncl = cutDenominator + "&&" + genNotFakeCut

            cutNumMCTrig = cutNumMCIncl + "&&" + cutTrigger
            cutDenMCTrig = cutDenMCIncl + "&&" + cutTrigger

            cutNumMCNotTrig = cutNumMCIncl + "&&" + cutNotTrigger
            cutDenMCNotTrig = cutDenMCIncl + "&&" + cutNotTrigger

            cutNumMC = {
                'incl' : cutNumMCIncl,
                'trig' : cutNumMCTrig,
                'notrig' : cutNumMCNotTrig
            }
            cutDenMC = {
                'incl' : cutDenMCIncl,
                'trig' : cutDenMCTrig,
                'notrig' : cutDenMCNotTrig
            }

            for trigLabel in trigLabels:        

                nameNum = 'mc_num_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
                nameDen = 'mc_den_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
                mchistNum = analysis.RunSamples(mcSamples,var,cutNumMC[trigLabel],Bins[trigLabel],nameNum)
                mchistDen = analysis.RunSamples(mcSamples,var,cutDenMC[trigLabel],Bins[trigLabel],nameDen)

                datahistNum[trigLabel].Add(datahistNum[trigLabel],mchistNum,1.,-1.)
                datahistDen[trigLabel].Add(datahistDen[trigLabel],mchistDen,1.,-1.)

        
        if variable2=='ptratio':
            yieldNum = datahistNum['incl'].GetSumOfWeights()
            yieldDen = datahistDen['incl'].GetSumOfWeights()

            yieldNumTrig = datahistNum['trig'].GetSumOfWeights()
            yieldDenTrig = datahistDen['trig'].GetSumOfWeights()

            yieldNumNotTrig = datahistNum['notrig'].GetSumOfWeights()
            yieldDenNotTrig = datahistDen['notrig'].GetSumOfWeights()

            checkNum = yieldNumTrig + yieldNumNotTrig
            checkDen = yieldDenTrig + yieldDenNotTrig

            print('cross check ->')
            print('Incl   ',yieldNum,yieldDen)
            print('Trig   ',yieldNumTrig,yieldDenTrig)
            print('NotTrig',yieldNumNotTrig,yieldDenNotTrig)
            print('Check  ',checkNum,checkDen)

        nbins = datahistNum['incl'].GetNbinsX()
        print('')
        print('Checking content in data %s'%(label))
        for ib in range(1,nbins+1):
            num = datahistNum['incl'].GetBinContent(ib)
            den = datahistDen['incl'].GetBinContent(ib)
            print('bin %1i   num = %5.0f   den = %5.0f'%(ib,num,den))
        print('')


        
        for trigLabel in trigLabels:
            nameff = 'data_ff_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
            histffdata = utils.divideHistos(datahistNum[trigLabel],
                                            datahistDen[trigLabel],
                                            nameff)
            name = 'data_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
            histsdata[name] = DrawFF(histffdata,
                                     era=era,
                                     channel=channel,
                                     label=label,
                                     WPvsJet=WPvsJet,
                                     variable1=variable1,
                                     variable2=variable2,
                                     isdata=True,
                                     WPvsMu=WPvsMu,
                                     WPvsE=WPvsE,
                                     tagger=tagger,
                                     trigger=trigLabel,
                                     option=option)

        if channel=="wjets":

            cutNumSigIncl = cutNumerator + "&&" + genFakeCut
            cutDenSigIncl = cutDenominator + "&&" + genFakeCut

            cutNumSigTrig = cutNumSigIncl + "&&" + cutTrigger
            cutDenSigTrig = cutDenSigIncl + "&&" + cutTrigger

            cutNumSigNotTrig = cutNumSigIncl + "&&" + cutNotTrigger
            cutDenSigNotTrig = cutDenSigIncl + "&&" + cutNotTrigger

            cutNumSig = {
                'incl' : cutNumSigIncl,
                'trig' : cutNumSigTrig,
                'notrig' : cutNumSigNotTrig
            }

            cutDenSig = {
                'incl' : cutDenSigIncl,
                'trig' : cutDenSigTrig,
                'notrig' : cutDenSigNotTrig
            }

            for trigLabel in trigLabels:
                nameNum = 'sig_num_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
                nameDen = 'sig_den_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
                sighistNum = analysis.RunSamples(sigSamples,var,cutNumSig[trigLabel],Bins[trigLabel],nameNum)
                sighistDen = analysis.RunSamples(sigSamples,var,cutDenSig[trigLabel],Bins[trigLabel],nameDen)
                nameff = 'sig_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
                histffsig  = utils.divideHistos(sighistNum,
                                                sighistDen,
                                                nameff)
                name = 'mc_'+channel+'_'+variable1+'_'+label+'_'+trigLabel
                histssig[name] = DrawFF(histffsig,
                                        era=era,
                                        channel=channel,
                                        label=label,
                                        WPvsJet=WPvsJet,
                                        variable1=variable1,
                                        variable2=variable2,
                                        isdata=False,
                                        WPvsMu=WPvsMu,
                                        WPvsE=WPvsE,
                                        tagger=tagger,
                                        trigger=trigLabel)

    outputfile.cd('')
    for hist in histsdata:
        histsdata[hist].Write(hist)
    
    if channel=="wjets":
        for hist in histssig:
            histssig[hist].Write(hist)
        
############
#   MAIN   #
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2024', choices=['UL2016', 'UL2017', 'UL2018', '2022', '2023','2024','2025'])
    parser.add_argument('-WPvsJet', '--WPvsJet', dest='WPvsJet', default='Medium', choices=['VLoose','Loose', 'Medium', 'Tight', 'VTight', 'VVTight','SuperTight','KiloTight','MegaTight'])
    parser.add_argument('-WPvsMu', '--WPvsMu', dest='WPvsMu', default='Tight', choices=['VLoose', 'Tight'])
    parser.add_argument('-WPvsE', '--WPvsE', dest='WPvsE', default='VVLoose', choices=['VVLoose', 'Tight'])
    parser.add_argument('-tagger', '--tagger', dest='tagger', default='pnet', choices=['deeptau','pnet','pnet_hps','upart'])
    parser.add_argument('-trg_option','--trg_option',dest='option', default='comb', choices=['comb','deeptau','pnet'])
    args = parser.parse_args() 

    basefolder = utils.picoFolder

    eras = utils.periods[args.era]
    def confirm_arguments(parsed_args):
        print("Parsed arguments:")
        print("Era:", parsed_args.era)
        print("WPvsJet:", parsed_args.WPvsJet)
        print("WPvsMu:", parsed_args.WPvsMu)
        print("WPvsE:", parsed_args.WPvsE)
        print("Tau Tagger:", parsed_args.tagger)
        print("Trigger option:",parsed_args.option)
        
        confirmation = input("Are these arguments correct? (yes/no): ").strip().lower()
        return confirmation == "yes"

    def adjust_arguments():
        parser = ArgumentParser()
        parser.add_argument('-e', '--era', dest='era', default='2024', choices=['UL2016', 'UL2017', 'UL2018', '2022', '2023','2024','2025'])
        parser.add_argument('-WPvsJet', '--WPvsJet', dest='WPvsJet', default='Medium', choices=['VLoose','Loose', 'Medium', 'Tight', 'VTight', 'VVTight','SuperTight','KiloTight','MegaTight'])
        parser.add_argument('-WPvsMu', '--WPvsMu', dest='WPvsMu', default='Tight', choices=['VLoose', 'Tight'])
        parser.add_argument('-WPvsE', '--WPvsE', dest='WPvsE', default='VVLoose', choices=['VVLoose', 'Tight'])        
        parser.add_argument('-tagger', '--tagger', dest='tagger', default='pnet', choices=['deeptau','pnet','pnet_hps','upart'])
        parser.add_argument('-trg_option', '--trg_option', dest='option', default='comb', choices=['comb', 'deeptau','pnet'])
        
        args = parser.parse_args()

        print("Options to adjust arguments:")
        print("1. Change era")
        print("2. Change WPvsJet")
        print("3. Change WPvsMu")
        print("4. Change WPvsE")
        print("5. Trigger option")
        print("6. Tau Tagger")
        print("7. Confirm and proceed")

        while True:
            choice = input("Enter your choice (1-7): ").strip()
            if choice == "1":
                args.era = input("Enter the era (UL2016, UL2017, UL2018, 2022, 2023, 2024, 2025): ").strip()
            elif choice == "2":
                args.WPvsJet= input("Enter the WPvsJet (VLoose, Loose, Medium, Tight, VTight, VVTight): ").strip()
            elif choice == "3":
                args.WPvsMu = input("Enter the WPvsMu (VLoose, Tight): ").strip()
            elif choice == "4":
                args.WPvsE = input("Enter the WPvsE (VVLoose, Tight): ").strip()
            elif choice == "5":
                args.option = input("Enter the trigger option (deeptau, pnet, comb): ").strip()
            elif choice == "6":
                args.tagger = input("Enter the tagger option (deeptau, pnet, pnet_hps): ").strip()
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

        return args

    if __name__ == "__main__":
        while True:
            args = adjust_arguments()
            if confirm_arguments(args):
                break


    print('initializing SingleMuon samples >>>')
    singlemuSamples = {} # data samples disctionary
    for era in eras:
        singlemuNames = utils.singlemu[era]
        for singlemuName in singlemuNames:
            name = singlemuName + '_' + era
            singlemuSamples[name] = analysis.sampleHighPt(basefolder,era,
                                                          "wjets",singlemuName,True)

    print('')
    print('initializing JetHT samples >>>')
    jethtSamples = {} # data samples disctionary
    for era in eras:
        jethtNames = utils.jetht[era]
        for jethtName in jethtNames:
            name = jethtName + '_' + era
            jethtSamples[name] = analysis.sampleHighPt(basefolder,era,
                                                       "dijets",jethtName,True)

    print('')
    print('initializing MC samples >>>')
    mcSamples = {} # mc samples dictionary
    for era in eras:
        run = utils.eraRun[era]
        mcSampleNames = RunMCSampleNames[run]
        for mcSampleName in mcSampleNames:
            name = mcSampleName + '_' + era
            if mcSampleName in utils.MCLowHT:
                addCut='(HT<100||HT>800)'
                mcSamples[name] = analysis.sampleHighPt(basefolder,era,"wjets",mcSampleName,
                                                     False,additionalCut=addCut)
            else:
                mcSamples[name] = analysis.sampleHighPt(basefolder,era,"wjets",mcSampleName,
                                                     False)
    print('')
    print('initializing W+Jets samples >>>') 
    sigSamples = {} # wjets samples dictionary
    for era in eras:
        run = utils.eraRun[era]
        sigSampleNames = RunSigSampleNames[run]
        for sigSampleName in sigSampleNames:
            name = sigSampleName + '_' + era
            if sigSampleName in utils.MCLowHT:
                addCut='(HT<100||HT>800)'
                sigSamples[name] = analysis.sampleHighPt(basefolder,era,"wjets",sigSampleName,
                                                      False,additionalCut=addCut)
            else:
                sigSamples[name] = analysis.sampleHighPt(basefolder,era,"wjets",sigSampleName,
                                                      False)

    FFfolder = utils.baseFolder+'/'+args.era+'/FF'
    if not os.path.isdir(FFfolder):
        print('folder for fake factors does not exist')
        os.makedirs(FFfolder)
        print('folder for fake factors is created : %s'%(FFfolder))


    FFfilename='ff_'+args.WPvsJet+"VSjet_"+args.WPvsMu+"VSmu_"+args.WPvsE+"VSe_"+args.era+"_"+args.tagger+"_"+args.option+".root"
    fullpathout=FFfolder+'/'+FFfilename
    outputfile = TFile(fullpathout,'recreate')
    #   measurements ->
    channels = ['wjets','dijets']
    dataSamples = {
        'wjets' : singlemuSamples,
        'dijets' : jethtSamples
    }
    for channel in channels:
        for var1 in ['pttau','ptjet']:
            main(outputfile,
                 dataSamples[channel],
                 mcSamples,
                 sigSamples,
                 WPvsJet=args.WPvsJet,
                 WPvsE=args.WPvsE,
                 WPvsMu=args.WPvsMu,
                 era=args.era,
                 channel=channel,
                 tagger=args.tagger,
                 option=args.option,
                 variable1=var1,
                 variable2='ptratio')


        for var1 in ['pttau','ptjet','mtau']:
            main(outputfile,
                 dataSamples[channel],
                 mcSamples,
                 sigSamples,
                 WPvsJet=args.WPvsJet,
                 WPvsE=args.WPvsE,
                 WPvsMu=args.WPvsMu,
                 era=args.era,
                 channel=channel,
                 tagger=args.tagger,
                 option=args.option,
                 variable1=var1,
                 variable2='dm')
    
    outputfile.cd('')
    hists = AuxiliaryHistograms()
    for hist in hists:
        hists[hist].Write(hist)
    outputfile.Close()

    print("")
    print('Fake factors are save in file %s'%(fullpathout))
    print("")

