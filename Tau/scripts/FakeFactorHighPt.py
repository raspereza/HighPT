#! /usr/bin/env python3
# Author: Alexei Raspereza (November 2022)
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
basecutEWK = 'mt_1>50&&iso_1<0.15&&pt_1>30&&fabs(eta_1)<2.4&&metfilter>0.5&&njets==0&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&dphi>2.4&&pt_2>100&&fabs(eta_2)<2.3&&idDeepTau2018v2p5VSjet_2>0&&idDeepTau2018v2p5VSe_2>0&&idDeepTau2018v2p5VSmu_2>0'

basecutQCD = 'jpt>100&&njets==1&&dphi>2.4&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&pt_2>90&&fabs(eta_2)<2.3&&idDeepTau2018v2p5VSjet_2>0&&idDeepTau2018v2p5VSe_2>0&&idDeepTau2018v2p5VSmu_2>0'

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
}

RunSigSampleNames = {
    'Run2' : ['WJetsToLNu','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500'],

    '2022' : ['WJetsToLNu-4Jets_1J','WJetsToLNu-4Jets_2J','WJetsToLNu-4Jets_3J','WJetsToLNu-4Jets_4J','WtoLNu-4Jets_HT-100to400','WtoLNu-4Jets_HT-400to800'],

    '2023' : ['WtoLNu-4Jets_1J','WtoLNu-4Jets_2J','WtoLNu-4Jets_3J','WtoLNu-4Jets_4J','WtoLNu_HT100to400','WtoLNu_HT400to800'],
}

# Fitting function (tau pt, ptratio bins)
def FitPt(x,par):
    a = 0.01*(x[0]-100.)
    ff = par[0]+par[1]*a
    if x[0]>par[2]:
        ff = par[3]
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

    pttau_bins = [0,200,10000]
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
    channel = kwargs.get('channel','channel')
    wp = kwargs.get('wp','Medium')
    wpVsE  = kwargs.get('wpVsE','TightVsE')
    wpVsMu = kwargs.get('wpVsMu','TightVsMu')
    trigger = kwargs.get('trigger','incl')
    era = kwargs.get('era','2023')

    labelSample = "mc"
    color = 2
    if isdata: 
        color = 1
        labelSample = "data"

    print
    print('fitting FF histo >>>',era,channel,label,labelSample)
    

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
        if x<1e-4 or x>0.9:     
            xcorr = 0.5*hist.GetBinContent(i-1)
            hist.SetBinContent(i,xcorr)
            hist.SetBinError(i,0.75*xcorr)
            
    print('')

    histToPlot = hist.Clone('temp')

    if variable1=='pttau' or variable1=='ptjet':
        if trigger=='incl':
            f1 = TF1("f1",FitPt,xmin,xmax,4)
            f1.SetParameter(0,average)
            f1.SetParameter(1,0.)
            f1.FixParameter(2,utils.ptUncThreshold[variable1])
            f1.SetParameter(3,average)
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

    leg = TLegend(0.25,0.7,0.5,0.9)
    styles.SetLegendStyle(leg)
    leg.SetHeader(label)
    leg.SetTextSize(0.04)
    if isdata: leg.AddEntry(hist,"Data",'lp')
    else: leg.AddEntry(hist,"MC",'lp')
    leg.AddEntry(hfit,'Fit','l')
    leg.Draw()
    styles.CMS_label(canv,era=era,extraText='Internal')

    canv.RedrawAxis()
    canv.Update()
    outdir = utils.baseFolder
    png_file='FF_%s_%s_%s_%s_%s_%s_%s_%s'%(labelSample,
                                           channel,
                                           variable1,
                                           label,
                                           trigger,
                                           wp,
                                           wpVsMu,
                                           wpVsE);
    canv.Print('%s/%s/figures/FF/%s.png'%(utils.baseFolder,era,png_file))
    
    return hfit

def main(outputfile,dataSamples,mcSamples,sigSamples,**kwargs):

    era = kwargs.get("era","2023")
    wp = kwargs.get("wp","Medium")
    channel = kwargs.get("channel","wjets")
    wpVsE = kwargs.get("wpVsE","Loose")
    wpVsMu = kwargs.get("wpVsMu","Loose")
    variable1 = kwargs.get("variable1","pttau")
    variable2 = kwargs.get("variable2","ptratio")

    print('')
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print('')
    print('Computing FF as a function of %s in bins of %s for era %s'%(variable1,variable2,era))
    print('%sVsJet  %sVsMu  %sVsE'%(wp,wpVsMu,wpVsE))
    
    cutTrigger = "(tautrigger1>0.5||tautrigger2>0.5)"
    cutNotTrigger = "(!" + cutTrigger +")"
        
    cutTauDen = "idDeepTau2018v2p5VSjet_2<4"
    cutTauNum = "idDeepTau2018v2p5VSjet_2>=" + utils.tauWPs[wp]

    cutTauDen += "&&idDeepTau2018v2p5VSmu_2>=" + utils.tauVsMuWPs[wpVsMu]
    cutTauDen += "&&idDeepTau2018v2p5VSe_2>="  + utils.tauVsEleWPs[wpVsE]

    cutTauNum += "&&idDeepTau2018v2p5VSmu_2>=" + utils.tauVsMuWPs[wpVsMu]
    cutTauNum += "&&idDeepTau2018v2p5VSe_2>="  + utils.tauVsEleWPs[wpVsE]

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
                                     wp=wp,
                                     variable1=variable1,
                                     variable2=variable2,
                                     isdata=True,
                                     wpVsMu=wpVsMu,
                                     wpVsE=wpVsE,
                                     trigger=trigLabel)

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
                                        wp=wp,
                                        variable1=variable1,
                                        variable2=variable2,
                                        isdata=False,
                                        wpVsMu=wpVsMu,
                                        wpVsE=wpVsE,
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
    parser.add_argument('-e','--era', dest='era', default='2023',choices=['UL2016','UL2017','UL2018','2022','2023'])
    parser.add_argument('-wp','--WP', dest='wp',  default='Medium',choices=['Loose','Medium','Tight','VTight','VVTight'])
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu',  default='Tight',choices=['VLoose','Tight'])
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE',  default='VVLoose',choices=['VVLoose','Tight'])
    args = parser.parse_args() 

    basefolder = utils.picoFolder+'/'+args.era

    eras = utils.periods[args.era]

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
        print('create folder for fake factors : %s'%(FFfolder))
        exit()

    FFfilename='ff_'+args.wp+"VSjet_"+args.wpVsMu+"VSmu_"+args.wpVsE+"VSe_"+args.era+".root"
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
                 wp=args.wp,
                 wpVsE=args.wpVsE,
                 wpVsMu=args.wpVsMu,
                 era=args.era,
                 channel=channel,
                 variable1=var1,
                 variable2='ptratio')

        for var1 in ['pttau','ptjet','mtau']:
            main(outputfile,
                 dataSamples[channel],
                 mcSamples,
                 sigSamples,
                 wp=args.wp,
                 wpVsE=args.wpVsE,
                 wpVsMu=args.wpVsMu,
                 era=args.era,
                 channel=channel,
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

