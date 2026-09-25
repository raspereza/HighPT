#! /usr/bin/env python3
# Author: Alexei Raspereza (August 2024)
# High pT tau ID SF as a function of pT(tau)
import ROOT
import HighPT.Tau.utilsHighPT as utils
from array import array
import math
import HighPT.Tau.stylesHighPT as styles
import os

nBinsPNet = 7
nBinsDeepTau = 6
bkgd = {
    'PNet': [13104,9242,6675,4907,3465,2755,2166],
    'DeepTau': [26824,12072,7738,5193,3523,2357],
}
signal = {
    'PNet': [12264,11765,11151,10298,9287,8642,7913],
    'DeepTau': [12358,11505,10662,9828,8933,7962],
}

def PlotPerformance():


    bkgdPNet = []
    for i in range(0,nBinsPNet):
        bkgdPNet.append(0.001*bkgd['PNet'][i])
    bkgdDeepTau = []
    for	i in range(0,nBinsDeepTau):
    	bkgdDeepTau.append(0.001*bkgd['DeepTau'][i])
    
    graphPNet = ROOT.TGraph(nBinsPNet,array('d',list(signal['PNet'])),array('d',list(bkgdPNet)))
    graphDeepTau = ROOT.TGraph(nBinsDeepTau,array('d',list(signal['DeepTau'])),array('d',list(bkgdDeepTau)))

    graphPNet.SetMarkerColor(2)
    graphPNet.SetLineColor(2)
    graphPNet.SetLineWidth(2)
    graphPNet.SetMarkerSize(1.7)
    graphPNet.SetMarkerStyle(20)
    
    graphDeepTau.SetMarkerColor(4)
    graphDeepTau.SetLineColor(4)
    graphDeepTau.SetLineWidth(2)
    graphDeepTau.SetMarkerSize(1.7)
    graphDeepTau.SetMarkerStyle(21)
    
    sbPNet = []
    sbDeepTau = []
    print('')
    print('S/B (PNet) ->')    
    for i in range(0,nBinsPNet):
        signalPNet = signal['PNet'][i]
        bkgdPNet = bkgd['PNet'][i]
        xPNet = signalPNet/math.sqrt(bkgdPNet)
        sbPNet.append(xPNet)
        print('%1i - %3.1f - %3.1f'%(i,signalPNet,xPNet))

    print('')
    print('S/B (DeepTau) ->')
    for i in range(0,nBinsDeepTau):
        signalDeepTau = signal['DeepTau'][i]
        bkgdDeepTau = bkgd['DeepTau'][i]
        xDeepTau = signalDeepTau/math.sqrt(bkgdDeepTau)
        sbDeepTau.append(xDeepTau)
        print('%1i - %3.1f - %3.1f'%(i,signalDeepTau,xDeepTau))
    print('')
    print('')
    
    graphSBPNet = ROOT.TGraph(nBinsPNet,array('d',list(signal['PNet'])),array('d',list(sbPNet)))
    graphSBDeepTau = ROOT.TGraph(nBinsDeepTau,array('d',list(signal['DeepTau'])),array('d',list(sbDeepTau)))
    
    frame = ROOT.TH2D('frame','',2,7000.,13000.,2,0.,35.)    
    frame.GetYaxis().SetTitle('fakes#times10^{3}')
    frame.GetXaxis().SetTitle('signal (genuine #tau)')
    frame.GetXaxis().SetNdivisions(505)
    frame.GetYaxis().SetTitleOffset(1.2)
    
    # canvas 
    canv = styles.MakeCanvas("canv","",600,600)

    frame.Draw()
    graphPNet.Draw('lpsame')
    graphDeepTau.Draw('lpsame')

    leg = ROOT.TLegend(0.25,0.7,0.48,0.85)
    leg.SetFillColor(0);
    leg.SetTextSize(0.035);
    leg.SetHeader(' W*#rightarrow#tau#nu')
    leg.SetBorderSize(1);
    leg.AddEntry(graphPNet,' PNet','lp')
    leg.AddEntry(graphDeepTau,' DeepTau','lp')
    leg.Draw()

    styles.CMS_label(canv,era='2024')
    canv.SetGridx(True)
    canv.SetGridy(True)
    canv.Modified()
    canv.Update()
    canv.Print('/eos/home-r/rasp/php-plots/plots/HighPt/PNet_DeepTau.png')

    # S/sqrt(B)

    graphSBPNet.SetMarkerColor(2)
    graphSBPNet.SetLineColor(2)
    graphSBPNet.SetLineWidth(2)
    graphSBPNet.SetMarkerSize(1.7)
    graphSBPNet.SetMarkerStyle(20)
    
    graphSBDeepTau.SetMarkerColor(4)
    graphSBDeepTau.SetLineColor(4)
    graphSBDeepTau.SetLineWidth(2)
    graphSBDeepTau.SetMarkerSize(1.7)
    graphSBDeepTau.SetMarkerStyle(21)
    
    frameSB = ROOT.TH2D('frameSB','',4,7000.,13000.,2,70.,180.)    
    frameSB.GetYaxis().SetTitle('sig/#sqrt{bkg}')
    frameSB.GetXaxis().SetTitle('signal (genuine #tau)')
    frameSB.GetYaxis().SetTitleOffset(1.4)
    
    # canvas 
    canvSB = styles.MakeCanvas("canvSB","",600,600)

    frameSB.Draw()
    graphSBPNet.Draw('lpsame')
    graphSBDeepTau.Draw('lpsame')

    legSB = ROOT.TLegend(0.25,0.25,0.48,0.4)
    legSB.SetFillColor(0);
    legSB.SetTextSize(0.035);
    legSB.SetHeader(' W*#rightarrow#tau#nu')
    legSB.SetBorderSize(1);
    legSB.AddEntry(graphSBPNet,' PNet','lp')
    legSB.AddEntry(graphSBDeepTau,' DeepTau','lp')
    legSB.Draw()

    styles.CMS_label(canvSB,era='2024')
    canvSB.SetGridx(True)
    canvSB.SetGridy(True)
    canvSB.Modified()
    canvSB.Update()
    canvSB.Print('/eos/home-r/rasp/php-plots/plots/HighPt/Performance.png')



    
############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    PlotPerformance()
