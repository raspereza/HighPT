#! /usr/bin/env python
# Author: Alexei Raspereza (November 2022)
# Description: computes fake factors 
#              for high pT jet->tau fakes

from ROOT import TFile, TH1, TH1D, TCanvas, TLegend, TH2, gROOT, TF1, TVirtualFitter, kCyan, gStyle, TString
import TauFW.Plotter.HighPT.utilsHighPT as utils
from array import array
import TauFW.Plotter.HighPT.stylesHighPT as styles
import os

#################################
#     definition of cuts        #
#################################
basecutEWK = 'mt_1>50&&iso_1<0.3&&pt_1>30&&fabs(eta_1)<2.4&&metfilter>0.5&&njets==0&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&dphi>2.4&&pt_2>100&&fabs(eta_2)<2.3&&idDeepTau2018v2p5VSjet_2>0&&idDeepTau2018v2p5VSe_2>=4&&idDeepTau2018v2p5VSmu_2>=1'

basecutQCD = 'jpt>100&&njets==1&&dphi>2.4&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&pt_2>100&&fabs(eta_2)<2.3&&idDeepTau2018v2p5VSjet_2>0&&idDeepTau2018v2p5VSe_2>=4&&idDeepTau2018v2p5VSmu_2>=1'

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
    "Run3" : ['DYto2L-4Jets_MLL-50','TTTo2L2Nu','TTtoLNu2Q','TTto4Q','TBbarQ_t-channel','TbarBQ_t-channel','TWminustoLNu2Q','TWminusto2L2Nu','TbarWplustoLNu2Q','TbarWplusto2L2Nu','WW','WZ','ZZ','WJetsToLNu-4Jets','WJetsToLNu-4Jets_1J','WJetsToLNu-4Jets_2J','WJetsToLNu-4Jets_3J','WJetsToLNu-4Jets_4J','WtoLNu-4Jets_HT-100to400','WtoLNu-4Jets_HT-400to800']
}

RunSigSampleNames = {
    'Run2' : ['WJetsToLNu','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500'],
    'Run3' : ['WJetsToLNu-4Jets','WJetsToLNu-4Jets_1J','WJetsToLNu-4Jets_2J','WJetsToLNu-4Jets_3J','WJetsToLNu-4Jets_4J','WtoLNu-4Jets_HT-100to400','WtoLNu-4Jets_HT-400to800']
}
# Fitting function (tau pt, ptratio bins)
def FitPt(x,par):
    a = 0.01*(x[0]-100.)
    ff = par[0]+par[1]*a
    if x[0]>200:
        ff = par[2]
    return ff

def FitPtConst(x,par):
    ff = par[0]
    if x[0]>200:
        ff = par[1]
    return ff

def FitPtConst2016(x,par):
    ff = par[0]
    if x[0]>150:
        ff = par[1]
    return ff

# Fitting function (mass, DM bins)
def FitMass(x,par):
    ff = par[0]+par[1]*x[0]+par[2]*x[0]*x[0]
    return ff

###########################
# Plotting and fitting FF #
###########################
def DrawFF(hist,era,channel,label,WP,**kwargs):


    isdata = kwargs.get('isdata',True)
    mode   = kwargs.get('mode',0)
    wpVsE  = kwargs.get('wpVsE','TightVsE')
    wpVsMu = kwargs.get('wpVsMu','TightVsMu')
    trigger = kwargs.get('trigger','_incl')

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
    for i in range(1,nbins+1):
        x = hist.GetBinContent(i)
        e = hist.GetBinError(i)
        xcorr = 0.5*e
        if x<1e-4: 
            if xcorr<1e-3:
                xcorr = 1e-3 
            hist.SetBinContent(i,xcorr)
            hist.SetBinError(i,xcorr)
            #            print(i,hist.GetBinContent(i),hist.GetBinError(i))

    print
    histToPlot = hist.Clone('temp')
    Era = TString(era)

    if mode==0 or mode==2:
        if trigger=='_trig' and channel=='wjets':
            if Era.Contains('UL2016'):
                f1 = TF1("f1",FitPtConst2016,xmin,xmax,2)
                f1.SetParameter(0,average)
                f1.SetParameter(1,average)
            else:
                f1 = TF1("f1",FitPtConst,xmin,xmax,2)
                f1.SetParameter(0,average)
                f1.SetParameter(1,average)
        else:
            if Era.Contains('UL2016') and channel=='wjets':
                f1 = TF1("f1",FitPtConst,xmin,xmax,2)
                f1.SetParameter(0,average)
                f1.SetParameter(1,average)
            else:
                f1 = TF1("f1",FitPt,xmin,xmax,3)
                f1.SetParameter(0,average)
                f1.SetParameter(1,0)
                f1.SetParameter(2,ymax)
    elif mode==1:
        f1 = TF1("f1",FitMass,xmin,xmax,3)
        f1.SetParameter(0,average)
        f1.SetParameter(1,0)
        f1.SetParameter(2,0)    


    canv = styles.MakeCanvas("canv","",700,600)
    hist.Fit('f1',"R")
    if mode==1: canv.SetLogx(False)
    else: canv.SetLogx(True)

    hfit = TH1D("ff_"+labelSample+"_"+channel+"_"+label+trigger,"",5000,xmin,xmax)
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
    maxFit = 1.5*hfit.GetMaximum()
    hfit.GetYaxis().SetRangeUser(0.,maxFit)
    hfit.SetTitle(era+" : "+channel+" : "+label)
    if mode==1: hfit.GetXaxis().SetTitle("#tau mass [GeV]")
    else: hfit.GetXaxis().SetTitle("#tau p_{T} [GeV]")
    hfit.GetYaxis().SetTitle("Fake factor")

    hfit.Draw("e2")
    hfitline.Draw("hsame")
    histToPlot.Draw("e1same")

    if mode==0 or mode==2: leg = TLegend(0.5,0.15,0.7,0.3)
    else: leg = TLegend(0.23,0.2,0.43,0.4)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.04)
    if isdata: leg.AddEntry(hist,"Data",'lp')
    else: leg.AddEntry(hist,"MC",'lp')
    leg.AddEntry(hfit,'Fit','l')
    leg.Draw()
    styles.CMS_label(canv,era=era,extraText='Internal')

    canv.RedrawAxis()
    canv.Update()
    canv.Print(utils.figuresFolderFF+'/FF_'+labelSample+"_"+channel+'_'+label+trigger+"_"+WP+'_'+wpVsMu+'VsMu_'+wpVsE+'VsE_'+era+'.png')
    
    return hfit

def main(outputfile,dataSamples,mcSamples,sigSamples,**kwargs):

    era = kwargs.get("era","UL2018")
    wp = kwargs.get("wp","Medium")
    channel = kwargs.get("channel","wjets")
    mode = kwargs.get("mode",0)
    wpVsE = kwargs.get("wpVsE","Loose")
    wpVsMu = kwargs.get("wpVsMu","Loose")

    print
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print
    if mode==0: 
        print('Computing FF as a function of tau pT in bins of pt_tau/pt_jet',era,wp+"VSjet",wpVsMu+"VSmu",wpVsE+"VSe",channel)
    elif mode==1: 
        print('Computing FF as a function of tau mass in bins of DM',era,wp+"VSjet",wpVsMu+"VSmu",wpVsE+"VSe",channel)
    else: 
        print('Computing FF as a function of jet pT in bins of DM',era,wp+"VSjet",wpVsMu+"VSmu",wpVsE+"VSe",channel)
    print
    
    cutTrigger = "(tautrigger1>0.5||tautrigger2>0.5)"
    cutNotTrigger = "(!" + cutTrigger +")"
        
    cutTauDen = "idDeepTau2018v2p5VSjet_2<4"
    cutTauNum = "idDeepTau2018v2p5VSjet_2>=" + utils.tauWPs[wp]

    cutTauDen += "&&idDeepTau2018v2p5VSmu_2>=" + utils.tauVsMuWPs[wpVsMu]
    cutTauDen += "&&idDeepTau2018v2p5VSe_2>="  + utils.tauVsEleWPs[wpVsE]

    cutTauNum += "&&idDeepTau2018v2p5VSmu_2>=" + utils.tauVsMuWPs[wpVsMu]
    cutTauNum += "&&idDeepTau2018v2p5VSe_2>="  + utils.tauVsEleWPs[wpVsE]

    ##############
    ## labels ####
    ##############
    binCuts = {}
    if mode==0: binCuts = utils.ptratioCuts
    elif mode==1: binCuts = utils.decaymodeCuts
    else:
        for ptrat in utils.ptratio2DCuts:
            for dm in utils.decaymode2DCuts:
                binCuts[ptrat+"_"+dm] = utils.ptratio2DCuts[ptrat] + "&&" + utils.decaymode2DCuts[dm]
    
    ##############
    ## Variable ##
    ##############
    var = 'pt_2'
    if mode==1: var = 'm_2'

    ############################
    ###### Common cut ##########
    ############################
    commonCut = basecut[channel]

    histsdata = {}
    histssig = {}
    xbinsT = [100,200,2000]
    if era=='UL2016_preVFP' or era=='UL2016_postVFP':
        xbinsT = [100,150,2000]


    for label in binCuts:
        xbins = []
        print
        print('***************************')
        print('Running over',label)
        print

        Era = TString(era)

        if mode==0:
            if Era.Contains('UL2016') and channel=='wjets':
                xbins=utils.xbinsPt_2016
            else:
                xbins=utils.xbinsPt
        elif mode==1: xbins=utils.xbinsMass[label]
        else: xbins=utils.xbinsPt2D

        addCut = binCuts[label]
        cut = commonCut + "&&" + addCut

        cutNum = cut + "&&" + cutTauNum
        cutDen = cut + "&&" + cutTauDen
        
        cutNumTrig = cutNum + "&&" + cutTrigger
        cutDenTrig = cutDen + "&&" + cutTrigger

        cutNumNotTrig = cutNum + "&&" + cutNotTrigger
        cutDenNotTrig = cutDen + "&&" + cutNotTrigger
        
        datahistNum = utils.RunSamples(dataSamples,var,"1.0",cutNum,xbins,'data_num_'+label)
        datahistDen = utils.RunSamples(dataSamples,var,"1.0",cutDen,xbins,'data_den_'+label)

        xbinsTrig = xbins
        if channel=='wjets':
            xbinsTrig = xbinsT

        datahistNumTrig = utils.RunSamples(dataSamples,var,"1.0",cutNumTrig,xbinsTrig,'data_num_trig_'+label)
        datahistDenTrig = utils.RunSamples(dataSamples,var,"1.0",cutDenTrig,xbinsTrig,'data_den_trig_'+label)

        datahistNumNotTrig = utils.RunSamples(dataSamples,var,"1.0",cutNumNotTrig,xbins,'data_num_nottrig_'+label)
        datahistDenNotTrig = utils.RunSamples(dataSamples,var,"1.0",cutDenNotTrig,xbins,'data_den_nottrig_'+label)

        if channel=="wjets":
            cutNumMC = cutNum + "&&" + genNotFakeCut
            cutDenMC = cutDen + "&&" + genNotFakeCut

            cutNumMCTrig = cutNumMC + "&&" + cutTrigger
            cutDenMCTrig = cutDenMC + "&&" + cutTrigger

            cutNumMCNotTrig = cutNumMC + "&&" + cutNotTrigger
            cutDenMCNotTrig = cutDenMC + "&&" + cutNotTrigger

            mchistNum = utils.RunSamples(mcSamples,var,"weight",cutNumMC,xbins,'mc_num_'+label)
            mchistDen = utils.RunSamples(mcSamples,var,"weight",cutDenMC,xbins,'mc_den_'+label)

            xbinsTrig = xbins
            if channel=='wjets':
                xbinsTrig = xbinsT

            mchistNumTrig = utils.RunSamples(mcSamples,var,"weight",cutNumMCTrig,xbinsTrig,'mc_num_trig'+label)
            mchistDenTrig = utils.RunSamples(mcSamples,var,"weight",cutDenMCTrig,xbinsTrig,'mc_den_trig'+label)

            mchistNumNotTrig = utils.RunSamples(mcSamples,var,"weight",cutNumMCNotTrig,xbins,'mc_num_nottrig'+label)
            mchistDenNotTrig = utils.RunSamples(mcSamples,var,"weight",cutDenMCNotTrig,xbins,'mc_den_nottrig'+label)

            datahistNum.Add(datahistNum,mchistNum,1.,-1.)
            datahistDen.Add(datahistDen,mchistDen,1.,-1.)

            datahistNumTrig.Add(datahistNumTrig,mchistNumTrig,1.,-1.)
            datahistDenTrig.Add(datahistDenTrig,mchistDenTrig,1.,-1.)

            datahistNumNotTrig.Add(datahistNumNotTrig,mchistNumNotTrig,1.,-1.)
            datahistDenNotTrig.Add(datahistDenNotTrig,mchistDenNotTrig,1.,-1.)

            
        yieldNum = datahistNum.GetSumOfWeights()
        yieldDen = datahistDen.GetSumOfWeights()

        yieldNumTrig = datahistNumTrig.GetSumOfWeights()
        yieldDenTrig = datahistDenTrig.GetSumOfWeights()

        yieldNumNotTrig = datahistNumNotTrig.GetSumOfWeights()
        yieldDenNotTrig = datahistDenNotTrig.GetSumOfWeights()

        checkNum = yieldNumTrig + yieldNumNotTrig
        checkDen = yieldDenTrig + yieldDenNotTrig

        #        print('Incl   ',yieldNum,yieldDen)
        #        print('Trig   ',yieldNumTrig,yieldDenTrig)
        #        print('NotTrig',yieldNumNotTrig,yieldDenNotTrig)
        #        print('Check  ',checkNum,checkDen)
        #        print

        histffdata = utils.divideHistos(datahistNum,datahistDen,'d_'+channel+"_"+label)
        histffdataTrig = utils.divideHistos(datahistNumTrig,datahistDenTrig,'d_'+channel+"_trig_"+label)
        histffdataNotTrig = utils.divideHistos(datahistNumNotTrig,datahistDenNotTrig,'d_'+channel+"_nottrig_"+label)

        #        nbins = histffdata.GetNbinsX()
        #        for i in range(1,nbins+1):
        #            print(histffdata.GetBinContent(i),histffdataNotTrig.GetBinContent(i))

        histsdata["data_"+channel+"_"+label] = DrawFF(histffdata,era,channel,
                                                      label,args.wp,mode=mode,isdata=True,
                                                      wpVsMu=wpVsMu,wpVsE=wpVsE,trigger='_incl')
        histsdata["data_"+channel+"_"+label+"_trig"] = DrawFF(histffdataTrig,era,channel,
                                                              label,args.wp,mode=mode,isdata=True,
                                                              wpVsMu=wpVsMu,wpVsE=wpVsE,trigger='_trig')
        histsdata["data_"+channel+"_"+label+"_nottrig"] = DrawFF(histffdataNotTrig,era,channel,
                                                                 label,args.wp,mode=mode,isdata=True,
                                                                 wpVsMu=wpVsMu,wpVsE=wpVsE,trigger='_nottrig')
        if channel=="wjets":

            cutNumSig = cutNum + "&&" + genFakeCut
            cutDenSig = cutDen + "&&" + genFakeCut

            cutNumSigTrig = cutNumSig + "&&" + cutTrigger
            cutDenSigTrig = cutDenSig + "&&" + cutTrigger

            cutNumSigNotTrig = cutNumSig + "&&" + cutNotTrigger
            cutDenSigNotTrig = cutDenSig + "&&" + cutNotTrigger

            sighistNum = utils.RunSamples(sigSamples,var,"weight",cutNumSig,xbins,"sig_num_"+label)
            sighistDen = utils.RunSamples(sigSamples,var,"weight",cutDenSig,xbins,"sig_den_"+label)

            sighistNumTrig = utils.RunSamples(sigSamples,var,"weight",cutNumSigTrig,xbinsT,"sig_num_"+label+"_trig")
            sighistDenTrig = utils.RunSamples(sigSamples,var,"weight",cutDenSigTrig,xbinsT,"sig_den_"+label+"_trig")

            sighistNumNotTrig = utils.RunSamples(sigSamples,var,"weight",cutNumSigNotTrig,xbins,"sig_num_"+label+"_nottrig")
            sighistDenNotTrig = utils.RunSamples(sigSamples,var,"weight",cutDenSigNotTrig,xbins,"sig_den_"+label+"_nottrig")

            histffsig  = utils.divideHistos(sighistNum,sighistDen,"s_"+channel+"_"+label)
            histffsigTrig  = utils.divideHistos(sighistNumTrig,sighistDenTrig,"s_"+channel+"_"+label+"_trig")
            histffsigNotTrig  = utils.divideHistos(sighistNumNotTrig,sighistDenNotTrig,"s_"+channel+"_"+label+"_nottrig")

            histssig["mc_"+channel+"_"+label] = DrawFF(histffsig,era,channel,
                                                       label,args.wp,mode=mode,isdata=False,
                                                       wpVsMu=wpVsMu,wpVsE=wpVsE,trigger='_incl')
            histssig["mc_"+channel+"_"+label+"_trig"] = DrawFF(histffsigTrig,era,channel,
                                                               label,args.wp,mode=mode,isdata=False,
                                                               wpVsMu=wpVsMu,wpVsE=wpVsE,trigger="_trig")
            histssig["mc_"+channel+"_"+label+"_nottrig"] = DrawFF(histffsigNotTrig,era,channel,
                                                                  label,args.wp,mode=mode,isdata=False,
                                                                  wpVsMu=wpVsMu,wpVsE=wpVsE,trigger="_nottrig")
                      
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
    parser.add_argument('-e','--era', dest='era', default='UL2018', help="""Era : UL2016_preVFP, UL2016_postVFP, UL2017, UL2018""")
    parser.add_argument('-wp','--WP', dest='wp',  default='Medium', help="""WP : Loose, Medium, Tight, 
VTight, VVTight """)
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu',  default='Tight', help="""WP vs. mu : VLoose Loose, Medium, Tight """)
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE',  default='VLoose', help="""WP : VVVLoose, Loose, Medium, Tight, VTight, VVTight """)
    args = parser.parse_args() 

    if args.wp not in ['Loose','Medium','Tight','VTight','VVTight']:
        print('unknown WP',args.wp)
        exit()
    if args.era not in ['UL2016_preVFP','UL2016_postVFP','UL2017','UL2018','2022']:
        print('unknown era',args.era)
        exit()

    basefolder = utils.picoFolder

    eras = utils.periods[args.era]

    print('initializing SingleMuon samples >>>')
    singlemuSamples = {} # data samples disctionary
    for era in eras:
        singlemuNames = utils.singlemu[era]
        for singlemuName in singlemuNames:
            name = singlemuName + '_' + era
            singlemuSamples[singlemuName] = utils.sampleHighPt(basefolder,era,
                                                               "wjets",singlemuName,True)

    #    print
    #    print('initializing JetHT samples >>>')
    #    jethtSamples = {} # data samples disctionary
    #    jethtNames = utils.jetht[args.era]
    #    for jethtName in jethtNames:
    #        jethtSamples[jethtName] = utils.sampleHighPt(basefolder,args.era,
    #                                                     "dijets",jethtName,True)

    print
    print('initializing MC samples >>>')
    mcSamples = {} # mc samples dictionary
    for era in eras:
        run = utils.eraRun[era]
        mcSampleNames = RunMCSampleNames[run]
        for mcSampleName in mcSampleNames:
            name = mcSampleName + '_' + era
            if mcSampleName in utils.MCLowHT:
                addCut='(HT<100||HT>800)'
                if mcSampleName in utils.MCPartons0:
                    addCut += '&&NUP_LO==0'
                mcSamples[name] = utils.sampleHighPt(basefolder,era,"wjets",mcSampleName,
                                                     False,additionalCut=addCut)
            else:
                mcSamples[name] = utils.sampleHighPt(basefolder,era,"wjets",mcSampleName,
                                                     False)
    print
    print('initializing W+Jets samples >>>') 
    sigSamples = {} # wjets samples dictionary
    for era in eras:
        run = utils.eraRun[era]
        sigSampleNames = RunSigSampleNames[run]
        for sigSampleName in sigSampleNames:
            name = sigSampleName + '_' + era
            if sigSampleName in utils.MCLowHT:
                addCut='(HT<100||HT>800)'
                if sigSampleName in utils.MCPartons0:
                    addCut += '&&NUP_LO==0'
                sigSamples[name] = utils.sampleHighPt(basefolder,era,"wjets",sigSampleName,
                                                      False,additionalCut=addCut)
            else:
                sigSamples[name] = utils.sampleHighPt(basefolder,era,"wjets",sigSampleName,
                                                      False)

    fullpathout = utils.fakeFactorsFolder + '/ff_'+args.wp+"VSjet_"+args.wpVsMu+"VSmu_"+args.wpVsE+"VSe_"+args.era+".root"
    if not os.path.isdir(utils.fakeFactorsFolder):
        print('folder for fake factors does not exist')
        print('create folder for fake factors : %s'%())
    outputfile = TFile(fullpathout,'recreate')


    #   mode of measurement ->
    #   mode = 0 : FF as a function of pT(tau) in bins of pT(tau)/pT(jet), 
    #   mode = 1 : FF as a function of tau mass in bins of tau DM (1prPi0, 3pr, 3prPi0)
    #   mode = 2 : FF as a function of pT(jet) in bins tau DM
    
    main(outputfile,singlemuSamples,mcSamples,sigSamples,
         wp=args.wp,wpVsE=args.wpVsE,wpVsMu=args.wpVsMu,era=args.era,channel="wjets",mode=0)
    #main(outputfile,singlemuSamples,mcSamples,sigSamples,
    #     wp=args.wp,wpVsE=args.wpVsE,wpVsMu=args.wpVsMu,era=args.era,channel="wjets",mode=1)
    #main(outputfile,singlemuSamples,mcSamples,sigSamples,
    #     wp=args.wp,wpVsE=args.wpVsE,wpVsMu=args.wpVsMu,era=args.era,channel="wjets",mode=2)
    
        
    #    main(outputfile,jethtSamples,mcSamples,sigSamples,
    #         wp=args.wp,wpVsE=args.wpVsE,wpVsMu=args.wpVsMu,era=args.era,channel="dijets",mode=0)

    outputfile.Close()
    print("")
    print('Fake factors are save in file %s'%(fullpathout))
    print("")

