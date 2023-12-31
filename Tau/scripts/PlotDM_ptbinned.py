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

sigSampleNames = ['WToTauNu_M-200']

############################
###### DM fractions ########
############################
def PlotDM(h_input_sig,wp,era,suffix,wpVsMu,wpVsE):

    print
    print("Plotting DM fractions ",era,suffix,wp,wpVsMu,wpVsE)

    h_sig = h_input_sig.Clone('h_signal')
    styles.InitModel(h_sig,2)
    yMax = h_sig.GetMaximum()
    h_sig.GetYaxis().SetRangeUser(0.,1.2*yMax)

    norm = h_sig.GetSumOfWeights()
    h_sig.Scale(1.0/norm)
    
    decaymodes = {
        1: '1pr   ',
        2: '1prpi0',
        3: '3pr   ',
        4: '3prpi0'
    }

    
    nbins = h_sig.GetNbinsX()
    checksum = 0
    for ib in range(1,nbins+1):
        h_sig.GetXaxis().SetBinLabel(ib,decaymodes[ib])
        content = h_sig.GetBinContent(ib)
        error   = h_sig.GetBinError(ib)
        checksum += content
        print(decaymodes[ib]," : %4.3f +/- %4.3f"%(content,error))

    x1 = h_sig.GetBinContent(1)
    x2 = h_sig.GetBinContent(2)
    x3 = h_sig.GetBinContent(3)
    x4 = h_sig.GetBinContent(4)
    
    print("checksum %4.2f"%(checksum))
    # canvas
    canvas = styles.MakeCanvas("canv_"+suffix+"_"+era,"",600,700)
    h_sig.Draw('h')
    canvas.Print(utils.figuresFolderWTauNu+"/"+wpVsMu+"VsMu_"+wpVsE+"VsE/dm_"+wp+"_"+era+"_"+suffix+".png")
    
    print

    x = {}
    x[1] = x1
    x[2] = x2
    x[3] = x3
    x[4] = x4

    return x

############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-wp','--WP', dest='wp', default='Medium', help=""" tau ID WP : Loose, Medium, Tight, VTight, VVTight""")
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight', help=""" WP vs. mu : VLoose, Loose, Medium, Tight""")
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VLoose', help=""" WP vs. e : VLoose, Loose, Medium, Tight, VTight, VVTight""")
    args = parser.parse_args()

    print

    eras = ['UL2016_preVFP','UL2016_postVFP','UL2017','UL2018']
    ptbins = ['lowpt','highpt']
    label_eras = {
        'UL2016_preVFP': '16APV',
        'UL2016_postVFP': '16   ',
        'UL2017': '17   ',
        'UL2018': '18   '
    }

    results = {}

    xbins = [-0.5,0.5,9.5,10.5,11.5]

    basefolder = utils.picoFolder

    order = {}
    n = 0

    print
    print("WP vs jet",args.wp)
    print("WP vs e",args.wpVsE)
    print("WP vs mu",args.wpVsMu)

    for era in eras:
        sigSamples = {} # MC signal samples dictionary 
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        for sigSampleName in sigSampleNames:
            sigSamples[sigSampleName] = utils.sampleHighPt(basefolder,era,
                                                       "taunu",sigSampleName,False)

        for suffix in ptbins: 
            # initializing instance of TauNuCuts class
            ptlow_cut = 100.0
            pthigh_cut = 200.0
            if suffix=='highpt': 
                ptlow_cut = 200.0
                pthigh_cut = 99999999.

            antiMu = utils.tauVsMuIntWPs[args.wpVsMu]
            antiE  = utils.tauVsEleIntWPs[args.wpVsE]
            wtaunuCuts = utils.TauNuCuts(ptLowerCut=ptlow_cut,ptUpperCut=pthigh_cut,antiMu=antiMu,antiE=antiE)

            commonCut = "metfilter>0.5&&mettrigger>0.5&&extraelec_veto<0.5&&extramuon_veto<0.5&&extratau_veto<0.5&&njets==0&&idDeepTau2018v2p5VSmu_1>="+utils.tauVsMuWPs[args.wpVsMu]+"&&idDeepTau2018v2p5VSe_1>="+utils.tauVsEleWPs[args.wpVsE]+"&&genmatch_1==5&&idDeepTau2018v2p5VSjet_1>=" + utils.tauWPs[args.wp] 
            metCut     = "met>%3.1f"%(wtaunuCuts.metCut)
            ptLowerCut = "pt_1>%3.1f"%(wtaunuCuts.ptLowerCut)
            ptUpperCut = "pt_1<%3.1f"%(wtaunuCuts.ptUpperCut)
            etaCut     = "fabs(eta_1)<%3.1f"%(wtaunuCuts.etaCut)
            metdphiCut = "metdphi_1>%3.1f"%(wtaunuCuts.metdphiCut)
            mtLowerCut = "mt_1>%3.1f"%(wtaunuCuts.mtLowerCut)
            mtUpperCut = "mt_1<%3.1f"%(wtaunuCuts.mtUpperCut)
            kinCut = metCut+"&&"+ptLowerCut+"&&"+ptUpperCut+"&&"+etaCut+"&&"+metdphiCut+"&&"+mtLowerCut+"&&"+mtUpperCut
            totalCut = commonCut+"&&"+kinCut        
            histo_signal = utils.RunSamples(sigSamples,"dm_1","weight",totalCut,xbins,"wtaunu")
            x = PlotDM(histo_signal,args.wp,era,suffix,args.wpVsMu,args.wpVsE)
            label = 'r_' + suffix + '_' + label_eras[era]
            results[label] = x
            order[n] = label
            n += 1
            
    print
    print
    print("Plotting DM fractions %sVSjet, %sVSmu, %sVSe"%(args.wp,args.wpVsMu,args.wpVsE))
    for i in range(0,n):
        result = order[i]
        x = results[result]
        print("%s = %5.3f,  %5.3f,  %5.3f,  %5.3f"%(result,x[1],x[2],x[3],x[4]))


