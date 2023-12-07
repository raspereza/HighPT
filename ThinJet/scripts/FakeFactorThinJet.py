#! /usr/bin/env python
# Author: Alexei Raspereza (November 2023)
# Description: computes fake factors 
#              for high pT thin jet fakes

from ROOT import TFile, TH1, TH1D, TCanvas, TLegend, TH2, gROOT, TF1, TVirtualFitter, kCyan, gStyle, TString
import HighPT.ThinJet.utilsThinJet as utils
from array import array
import HighPT.ThinJet.stylesHighPT as styles
import os

#################################
#     definition of cuts        #
#################################
basecutEWK = 'mt_1>50&&iso_1<0.3&&pt_1>30&&fabs(eta_1)<2.4&&metfilter>0.5&&njets==0&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&dphi>2.8&&pt_2>70&&fabs(eta_2)<2.5&&idDeepTau2017v2p1VSjet_2>0&&jpt_match_2>140&&fabs(jeta_match_2)<2.3'

basecutQCD = 'jpt>100&&njets==1&&dphi>2.8&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&pt_2>70&&fabs(eta_2)<2.5&&idDeepTau2017v2p1VSjet_2>0&&jpt_match_2>140&&fabs(jeta_match_2)<2.3'

basecut = {
    "dijets": basecutQCD,
    "wjets" : basecutEWK
}

genFakeCut    = 'genmatch_2==0'
genNotFakeCut = 'genmatch_2!=0'

#########################
# Definition of samples #
#########################

mcSampleNames = ['DYJetsToLL_M-50','TTTo2L2Nu','TTToSemiLeptonic','TTToHadronic','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500','ST_t-channel_antitop_4f_InclusiveDecays','ST_t-channel_top_4f_InclusiveDecays','ST_tW_antitop_5f_NoFullyHadronicDecays','ST_tW_top_5f_NoFullyHadronicDecays','WW','WZ','ZZ']

sigSampleNames = ['WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500']

# Fitting function (tau pt, ptratio bins)
def FitPt(x,par):
    a = 0.01*(x[0]-100.)
    ff = par[0]+par[1]*a+par[2]*a*a
    if x[0]>300:
        ff = par[3]
    return ff

def FitPtConst(x,par):
    ff = par[0]
    if x[0]>200:
        ff = par[1]
    return ff

###########################
# Plotting and fitting FF #
###########################
def DrawFF(hist,era,channel,label,WP,**kwargs):


    isdata = kwargs.get('isdata',True)
    wpVsE  = kwargs.get('wpVsE','TightVsE')
    wpVsMu = kwargs.get('wpVsMu','TightVsMu')

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
        xe = x+e
        if xe>ymax: ymax = xe
        xcorr = 0.5*e
        if x<1e-4: 
            if xcorr<1e-3:
                xcorr = 1e-3 
            hist.SetBinContent(i,xcorr)
            hist.SetBinError(i,xcorr)

    print
    histToPlot = hist.Clone('temp')
    Era = TString(era)

    f1 = TF1("f1",FitPt,xmin,xmax,4)
    f1.SetParameter(0,average)
    f1.SetParameter(1,0)
    f1.SetParameter(2,0)
    f1.SetParameter(3,average)

    canv = styles.MakeCanvas("canv","",700,600)
    hist.Fit('f1',"R")
    canv.SetLogx(True)

    hfit = TH1D("ff_"+labelSample+"_"+channel+"_"+label,"",5000,xmin,xmax)
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
    maxFit = 3.0*hfit.GetMaximum()
    hfit.GetYaxis().SetRangeUser(0.,1.2*ymax)
    hfit.SetTitle(era+" : "+channel+" : "+label)
    hfit.GetXaxis().SetTitle("jet p_{T} [GeV]")
    hfit.GetYaxis().SetTitle("Fake factor")

    hfit.Draw("e2")
    hfitline.Draw("hsame")
    histToPlot.Draw("e1same")

    leg = TLegend(0.5,0.2,0.7,0.4)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.04)
    if isdata: leg.AddEntry(hist,"Data",'lp')
    else: leg.AddEntry(hist,"MC",'lp')
    leg.AddEntry(hfit,'Fit','l')
    leg.Draw()
    canv.RedrawAxis()
    canv.Update()
    canv.Print(utils.figuresFolderFF+'/FF_'+labelSample+"_"+channel+'_'+label+"_"+WP+"_"+era+'.png')
    
    return hfit

def main(outputfile,dataSamples,mcSamples,sigSamples,**kwargs):

    era = kwargs.get("era","UL2018")
    wp = kwargs.get("wp","VVLoose")
    channel = kwargs.get("channel","wjets")
    wpVsE = kwargs.get("wpVsE","Tight")
    wpVsMu = kwargs.get("wpVsMu","Tight")

    print
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print
    print('Computing FF as a function of tau-jet pt in bins of DM',era,wp+"VSjet",wpVsMu+"VSmu",wpVsE+"VSe",channel)
    print
    
    cutTauDen = "idDeepTau2017v2p1VSjet_2<2"
    cutTauNum = "idDeepTau2017v2p1VSjet_2>=" + utils.tauWPs[wp]

    cutTauDen += "&&idDeepTau2017v2p1VSmu_2>=" + utils.tauVsMuWPs[wpVsMu]
    cutTauDen += "&&idDeepTau2017v2p1VSe_2>="  + utils.tauVsEleWPs[wpVsE]

    cutTauNum += "&&idDeepTau2017v2p1VSmu_2>=" + utils.tauVsMuWPs[wpVsMu]
    cutTauNum += "&&idDeepTau2017v2p1VSe_2>="  + utils.tauVsEleWPs[wpVsE]

    ##############
    ## labels ####
    ##############
    binCuts = utils.decaymodeCuts
    
    ##############
    ## Variable ##
    ##############
    var = 'jpt_match_2'

    ############################
    ###### Common cut ##########
    ############################
    commonCut = basecut[channel]

    histsdata = {}
    histssig = {}


    for label in binCuts:
        xbins = []
        print
        print('***************************')
        print('Running over',label)
        print
 
        Era = TString(era)

        xbins=utils.xbinsPt_Jet

        addCut = binCuts[label]
        cut = commonCut + "&&" + addCut

        cutNum = cut + "&&" + cutTauNum
        cutDen = cut + "&&" + cutTauDen
        
        datahistNum = utils.RunSamples(dataSamples,var,"1.0",cutNum,xbins,'data_num_'+label)
        datahistDen = utils.RunSamples(dataSamples,var,"1.0",cutDen,xbins,'data_den_'+label)

        if channel=="wjets":
            cutNumMC = cutNum + "&&" + genNotFakeCut
            cutDenMC = cutDen + "&&" + genNotFakeCut

            mchistNum = utils.RunSamples(mcSamples,var,"weight",cutNumMC,xbins,'mc_num_'+label)
            mchistDen = utils.RunSamples(mcSamples,var,"weight",cutDenMC,xbins,'mc_den_'+label)

            datahistNum.Add(datahistNum,mchistNum,1.,-1.)
            datahistDen.Add(datahistDen,mchistDen,1.,-1.)

        yieldNum = datahistNum.GetSumOfWeights()
        yieldDen = datahistDen.GetSumOfWeights()


        histffdata = utils.divideHistos(datahistNum,datahistDen,'d_'+channel+"_"+label)

        #        nbins = histffdata.GetNbinsX()
        #        for i in range(1,nbins+1):
        #            print(histffdata.GetBinContent(i),histffdataNotTrig.GetBinContent(i))

        histsdata["data_"+channel+"_"+label] = DrawFF(histffdata,era,channel,
                                                      label,args.wp,isdata=True,
                                                      wpVsMu=wpVsMu,wpVsE=wpVsE)

        if channel=="wjets":

            cutNumSig = cutNum + "&&" + genFakeCut
            cutDenSig = cutDen + "&&" + genFakeCut

            sighistNum = utils.RunSamples(sigSamples,var,"weight",cutNumSig,xbins,"sig_num_"+label)
            sighistDen = utils.RunSamples(sigSamples,var,"weight",cutDenSig,xbins,"sig_den_"+label)

            histffsig  = utils.divideHistos(sighistNum,sighistDen,"s_"+channel+"_"+label)

            histssig["mc_"+channel+"_"+label] = DrawFF(histffsig,era,channel,
                                                       label,args.wp,isdata=False,
                                                       wpVsMu=wpVsMu,wpVsE=wpVsE)
                      
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
    parser.add_argument('-e','--era', dest='era', default='UL2018', help="""Era : UL2016_preVFP, UL2016_postVFP, UL2016, UL2017, UL2018""")
    parser.add_argument('-wp','--WP', dest='wp',  default='VVLoose', help="""WP : VVLoose, VLoose, Loose """)
 
    args = parser.parse_args() 


    if args.wp not in ['VVLoose','VLoose','Loose']:
        print('unknown WP',args.wp)
        exit()
    # add when available
    if args.era not in ['UL2016_preVFP','UL2016_postVFP','UL2016','UL2017','UL2018']:
        print('unknown era',args.era)
        exit()

    Eras = ['UL2016_preVFP','UL2016_postVFP']

    basefolder = utils.picoFolderFF

    print
    print('Folder',basefolder,' era',args.era,' WPvsJet',args.wp)
    print

    print('initializing SingleMuon samples >>>')
    singlemuSamples = {} # data samples disctionary
    if args.era=='UL2016':
        for Era in Eras:
            singlemuNames = utils.singlemu[Era]
            for singlemuName in singlemuNames:
                singlemuSamples[singlemuName+'_'+Era] = utils.sampleHighPt(
                    basefolder,Era,"wjets",singlemuName,True)
    else:
        singlemuNames = utils.singlemu[args.era]
        for singlemuName in singlemuNames:
            singlemuSamples[singlemuName] = utils.sampleHighPt(basefolder,args.era,
                                                               "wjets",singlemuName,True)

    print
    print('initializing JetHT samples >>>')
    jethtSamples = {} # data samples disctionary
    if args.era=='UL2016':
        for Era in Eras:
            jethtNames = utils.jetht[Era]
            for jethtName in jethtNames:
                jethtSamples[jethtName+'_'+Era] = utils.sampleHighPt(
                    basefolder,Era,"dijets",jethtName,True)
    else:
        jethtNames = utils.jetht[args.era]
        for jethtName in jethtNames:
            jethtSamples[jethtName] = utils.sampleHighPt(basefolder,args.era,
                                                     "dijets",jethtName,True)

    print
    print('initializing MC samples >>>')
    mcSamples = {} # mc samples dictionary
    if args.era=="UL2016":
        for Era in Eras:
            for mcSampleName in mcSampleNames:
                mcSamples[mcSampleName+'_'+Era] = utils.sampleHighPt(
                    basefolder,Era,"wjets",mcSampleName,False)
    else:
        for mcSampleName in mcSampleNames:
            mcSamples[mcSampleName] = utils.sampleHighPt(
                basefolder,args.era,"wjets",mcSampleName,False)

    print
    print('initializing W+Jets samples >>>') 
    sigSamples = {} # wjets samples dictionary
    if args.era=="UL2016":
        for Era in Eras:
            for sigSampleName in sigSampleNames:
                sigSamples[sigSampleName+'_'+Era] = utils.sampleHighPt(
                    basefolder,Era,"wjets",sigSampleName,False)
    else:
        for sigSampleName in sigSampleNames:
            sigSamples[sigSampleName] = utils.sampleHighPt(
                basefolder,args.era,"wjets",sigSampleName,False)

    fullpathout = utils.fakeFactorFolder+'/ff_'+args.wp+"VSjet_"+args.era+".root"
    outputfile = TFile(fullpathout,'recreate')

    main(outputfile,singlemuSamples,mcSamples,sigSamples,
         wp=args.wp,wpVsE=utils.wpVsE,wpVsMu=utils.wpVsMu,era=args.era,channel="wjets")
        
    main(outputfile,jethtSamples,mcSamples,sigSamples,
         wp=args.wp,wpVsE=utils.wpVsE,wpVsMu=utils.wpVsMu,era=args.era,channel="dijets")

    outputfile.Close()
    print
    print
    print('Fake factors are saved in file',fullpathout)
    print
