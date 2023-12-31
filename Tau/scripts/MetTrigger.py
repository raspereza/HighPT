#! /usr/bin/env python
# Author: Alexei Raspereza (November 2022)
# Description: compute MET trigger efficiencies and SF 
from ROOT import TFile, TH1, TH1D, TCanvas, TLegend, TH2, gROOT
import TauFW.Plotter.HighPT.utilsHighPT as utils
from array import array
import TauFW.Plotter.HighPT.stylesHighPT as styles
import os

####################
# MET trigger cuts #
####################
mettrig   = 'mettrigger>0.5'
nomettrig = 'mettrigger<0.5'

RunMCSampleNames = { 
    "Run2": ['WJetsToLNu','WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500'],
    "Run3": ['WJetsToLNu-4Jets','WJetsToLNu-4Jets_1J','WJetsToLNu-4Jets_2J','WJetsToLNu-4Jets_3J','WJetsToLNu-4Jets_4J','WtoLNu-4Jets_HT-100to400','WtoLNu-4Jets_HT-400to800']
}

def DrawEfficiency(histdata,histmc,era,legend):
    print
    print('drawing efficiency histo >>>',era,legend)

    canv = styles.MakeCanvas("canv"+legend,"",700,600)
    canv.SetLogx(True)

    histmc.SetLineColor(2)
    histmc.SetMarkerColor(2)
    histmc.SetMarkerSize(0.5)

    histdata.SetLineColor(1)
    histdata.SetMarkerColor(1)
    histdata.SetMarkerSize(0.5)
    histdata.GetYaxis().SetRangeUser(0.,1.2)
    histdata.GetXaxis().SetRangeUser(100.,1000.)
    histdata.GetXaxis().SetTitle("E_{T,no #mu}^{mis} [GeV]")
    histdata.GetYaxis().SetTitle("Efficiency")
    histdata.GetXaxis().SetNdivisions(505)
    histdata.GetXaxis().SetMoreLogLabels()
    histdata.GetXaxis().SetNoExponent()
    histdata.SetTitle(legend)
    histdata.Draw('h')
    histmc.Draw('hsame')
    leg = TLegend(0.6,0.3,0.9,0.5)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.045)
    leg.AddEntry(histdata,'Data','l')
    leg.AddEntry(histmc,'MC','l')
    leg.Draw()

    styles.CMS_label(canv,era=era)

    canv.Update()
    canv.Print(utils.figuresFolderMetTrigger+'/mettrig_'+era+'_'+legend+'.png')
    print 

def main(args):

    print

    channel = "munu"
    basefolder = utils.picoFolder
    xbinsLt200 = [100,120,140,160,180,200,220,240,280,1000]
    xbinsGt200 = [100,150,175,200,220,240,260,280,1000]
    basecut = 'met>50&&mt_1>50&&pt_1>30&&fabs(eta_1)<2.1&&metfilter>0.5'
    weight = 'weight'
    var = 'metnomu'
    mhtLabels = {
        'mht100to130': 'mhtnomu>100&&mhtnomu<200',
        'mht130to160': 'mhtnomu>100&&mhtnomu<200',
        'mht160to200': 'mhtnomu>100&&mhtnomu<200',
        'mhtGt200': 'mhtnomu>200',
    }
    mhtBins = {
        'mht100to130' : xbinsLt200,
        'mht130to160' : xbinsLt200,
        'mht160to200' : xbinsLt200,
        'mhtGt200' : xbinsGt200,        
    }

    eras = utils.periods[args.era]
    
    dataSamples = {} # data samples disctionary
    print('Initializing SingleMuon data samples>>>')
    for era in eras: 
        dataSampleNames = utils.singlemu[era]
        for dataSampleName in dataSampleNames:
            name = dataSampleName+'_'+era
            dataSamples[name] = utils.sampleHighPt(basefolder,era,channel,
                                                   dataSampleName,True)

    print
    mcSamples = {} # mc samples dictionary
    print('Initializing W+Jets MC samples>>>')
    for era in eras:
        run = utils.eraRun[era]
        mcSampleNames = RunMCSampleNames[run]
        for mcSampleName in mcSampleNames:
            name = mcSampleName+'_'+era
            if mcSampleName in utils.MCLowHT:
                addCut='(HT<100||HT>800)'
                if mcSampleName in utils.MCPartons0:
                    addCut += '&&NUP_LO==0'
                mcSamples[name] = utils.sampleHighPt(basefolder,era,channel,mcSampleName,False,additionalCut=addCut)
            else:
                mcSamples[name] = utils.sampleHighPt(basefolder,era,channel,mcSampleName,False)
    print
    histsdata = {} # data histo dictionary
    histsmc = {} # mc histo dictionary

    for mhtcut in mhtLabels:

        xbins = mhtBins[mhtcut]
        cutpass = basecut + '&&' + mettrig   + '&&' + mhtLabels[mhtcut]
        cutfail = basecut + '&&' + nomettrig + '&&' + mhtLabels[mhtcut]

        # Data ----->
        datahistpass = utils.RunSamples(dataSamples,var,"1",cutpass,xbins,'data_pass_'+mhtcut)
        datahistfail = utils.RunSamples(dataSamples,var,"1",cutfail,xbins,'data_fail_'+mhtcut)
        histeffdata = utils.dividePassProbe(datahistpass,datahistfail,'data_'+mhtcut)
        histsdata['data_'+mhtcut] = histeffdata
        
        # MC ----->
        mchistpass = utils.RunSamples(mcSamples,var,weight,cutpass,xbins,"mc_pass_"+mhtcut)
        mchistfail = utils.RunSamples(mcSamples,var,weight,cutfail,xbins,"mc_fail_"+mhtcut)
        histeffmc  = utils.dividePassProbe(mchistpass,mchistfail,"mc_"+mhtcut)
        histsmc['mc_'+mhtcut] = histeffmc        

        DrawEfficiency(histeffdata,histeffmc,args.era,mhtcut)

    fullpathout = os.getenv('CMSSW_BASE') + '/src/TauFW/PicoProducer/data/trigger/mettrigger_'+args.era+".root"
    outputfile = TFile(fullpathout,'recreate')
    outputfile.cd('')

    for hist in histsdata:
        histsdata[hist].Write(hist)
    
    for hist in histsmc:
        histsmc[hist].Write(hist)
        
    outputfile.Close()

############
#   MAIN   #
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='UL2018', help=""" Era """,choices=['UL2016','UL2016_preVFP','UL2016_postVFP','UL2017','UL2018','2022'])
    args = parser.parse_args() 

    main(args)



