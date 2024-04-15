#! /usr/bin/env python3
# Author: Alexei Raspereza (December 2022)
# Checking systematic variations in datacards
import ROOT
import HighPT.Tau.utilsHighPT as utils
from array import array
import HighPT.Tau.stylesHighPT as styles
import os

def PlotSystematics(h_central,h_up,h_down,era,sampleName,sysName,ratioLower,ratioUpper):

    styles.InitData(h_central)
    styles.InitData(h_up)
    styles.InitData(h_down)

    h_up.SetMarkerSize(0)
    h_up.SetLineColor(2)
    h_up.SetMarkerColor(2)
    h_up.SetLineStyle(1)

    h_down.SetMarkerSize(0)
    h_down.SetLineColor(4)
    h_down.SetMarkerColor(4)
    h_down.SetLineStyle(1)

    h_ratio_up = utils.divideHistos(h_up,h_central,'ratio_up')
    h_ratio_down = utils.divideHistos(h_down,h_central,'ratio_down')
    h_ratio = utils.createUnitHisto(h_central,'ratio')
    styles.InitRatioHist(h_ratio)
    h_ratio.GetYaxis().SetRangeUser(ratioLower,ratioUpper)

    print('')
    print('Template %s  systematics %s'%(sampleName,sysName))
    print('')
    print('             down     nom     up')
    print('----------------------------------')
    #      [200, 300]  1091.8  1085.6  1079.4

    nbins = h_central.GetNbinsX()
    for ib in range(1,nbins+1):
        lower = h_central.GetBinLowEdge(ib)
        upper = h_central.GetBinLowEdge(ib+1)
        xcentral = h_central.GetBinContent(ib)
        xup = h_up.GetBinContent(ib)
        xdown = h_down.GetBinContent(ib)
        print('[%3i,%4i]  %6.1f  %6.1f  %6.1f'%(lower,upper,xdown,xcentral,xup))

    utils.zeroBinErrors(h_up)
    utils.zeroBinErrors(h_down)
    utils.zeroBinErrors(h_ratio_up)
    utils.zeroBinErrors(h_ratio_down)

    ymax = h_central.GetMaximum()
    if h_up.GetMaximum()>ymax: ymax = h_up.GetMaximum()
    if h_down.GetMaximum()>ymax: ymax = h_down.GetMaximum()
    h_central.GetYaxis().SetRangeUser(0.,1.2*ymax)
    h_central.GetXaxis().SetLabelSize(0)

    # canvas and pads
    canvas = styles.MakeCanvas("canv","",600,700)
    # upper pad
    upper = ROOT.TPad("upper", "pad",0,0.31,1,1)
    upper.Draw()
    upper.cd()
    styles.InitUpperPad(upper)    
    
    h_central.Draw('e1')
    h_down.Draw('hsame')
    h_up.Draw('hsame')
    h_central.Draw('e1same')
    
    leg = ROOT.TLegend(0.4,0.55,0.7,0.85)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.045)
    leg.SetHeader(era+"  "+sampleName+":"+sysName)
    leg.AddEntry(h_central,'central','lp')
    leg.AddEntry(h_up,'up','l')
    leg.AddEntry(h_down,'down','l')
    leg.Draw()

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
    h_ratio_up.Draw('hsame')
    h_ratio_down.Draw('hsame')
    h_ratio.Draw('e1same')
    nbins = h_ratio.GetNbinsX()
    xmin = h_ratio.GetXaxis().GetBinLowEdge(1)    
    xmax = h_ratio.GetXaxis().GetBinLowEdge(nbins+1)
    line = ROOT.TLine(xmin,1.,xmax,1.)
    line.Draw()
    lower.Modified()
    lower.RedrawAxis()

    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    canvas.Print(utils.baseFolder+"/"era+"sigures/Sys/sys_cards_"+era+"_"+sampleName+"_"+sysName+".png")

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

#####################################################################
#   Systematics :
#   jmet    = JES, Unclustered
#   taues   = taues, taues_1pr taues_1pr1pi0 taues_3pr taues_3pr1pi0    
#   fakes   = sample_variable1_variable2 nonclosure
#   ------
#   WP      = [Loose,Medium,Tight,VTight,VVTight]
#   ------
#   samples = [wtaunu,fake]
# 
#####################################################################
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era',dest='era',default='2023',choices=['UL2016','UL2017','UL2018','2022','2023'])
    parser.add_argument('-c','--channel',dest='channel', default='taunu',)
    parser.add_argument('-s','--sample',dest='sample',default='fake')
    parser.add_argument('-wp','--WP',dest='wp',default='Medium')
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight')
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VVLoose')
    parser.add_argument('-sys','--sysname',dest='sysname', default='wjets_ptratioLow_ptjetLow')
    parser.add_argument('-ymin','--ymin',dest='ymin',default=0.5)
    parser.add_argument('-ymax','--ymax',dest='ymax',default=1.5)
    args = parser.parse_args() 

    basefolder = utils.baseFolder+"/"+args.era+"/datacards"
    filename = "%s_%s.root"%(args.channel,args.era)
    if args.channel=='taunu':
        filename = "%s_%s_%s_%s_%s.root"%(args.channel,args.wp,args.wpVsMu,args.wpVsE,args.era)
    fullpath = basefolder+'/'+filename
    print('')
    if os.path.isfile(fullpath):
        print('Opening file %s'%(fullpath))
    else:
        print('File %s does not exist'%(fullpath))
        exit()
    print('')

    cardsFile = ROOT.TFile(fullpath)
    if cardsFile==None or cardsFile.IsZombie():
        print('File %s cannot be opened'%(fullpath))
        exit()

    name_central=args.channel+"/"+args.sample
    name_up=args.channel+"/"+args.sample+"_"+args.sysname+"Up"
    name_down=args.channel+"/"+args.sample+"_"+args.sysname+"Down"
    hist_central = cardsFile.Get(name_central)
    hist_up = cardsFile.Get(name_up)
    hist_down = cardsFile.Get(name_down)
    if hist_central==None:
        print('Histogram %s is not found'%(name_central))
        exit()
    if hist_up==None:
        print('Histogram %s is not found'%(name_up))
        exit()
    if hist_down==None:
        print('Histogram %s is not found'%(name_down))
        exit()

    print('Plotting histograms : %s  %s  %s'%(name_central,name_up,name_down))

    PlotSystematics(hist_central,
                    hist_up,
                    hist_down,
                    args.era,
                    args.sample,
                    args.sysname,
                    args.ymin,args.ymax)
