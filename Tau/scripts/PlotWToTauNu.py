#! /usr/bin/env python3
# Author: Alexei Raspereza (December 2022)
# High pT tau ID efficiency measurements 
# Plotting macro: signal region (W*->tau+v) 
import ROOT
import HighPT.Tau.utilsHighPT as utils
from array import array
import math
import HighPT.Tau.stylesHighPT as styles
import os

taggerLabel = {
    'deeptau': 'DeepTau',
    'pnet': 'PNet',
    'upart': 'UParT',
}

##########################
# Plotting distributions #
##########################
def Plot(hists,**kwargs):
    wp = kwargs.get('wp','Medium')
    wpVsMu = kwargs.get('wpVsMu','Tight')
    wpVsE = kwargs.get('wpVsE','VVLoose')
    era = kwargs.get('era','2024')
    var = kwargs.get('var','mt_1')
    meas = kwargs.get('meas','lowpt')
    tagger = kwargs.get('tagger','deeptau')
    postfit = kwargs.get('postfit',True)

    fitSuffix = 'prefit'
    if postfit: fitSuffix = 'postfit'
    
    h_data = hists['data']
    h_fake = hists['fake']
    h_lfakes = hists['lfakes']
    h_bkg = hists['tau']
    h_sig = hists['wtaunu']
    h_tot = hists['total']
    
    label = 'prefit'
    if postfit:
        label = 'postfit'

    name = f'RooT/mT_{wp}_{wpVsMu}_{wpVsE}_{meas}_{era}_{tagger}_{label}.root'
    outputROOT = ROOT.TFile(name,'recreate')
    outputROOT.cd('')
    h_data.Write('data')
    h_sig.Write('wtaunu')
    h_fake.Write('jfakes')
    h_lfakes.Write('lfakes')
    h_bkg.Write('taus')
    h_tot.Write('total')
    outputROOT.Close()

    if tagger=='pnet' or tagger=='upart':
        if not postfit:
            nbins = h_tot.GetNbinsX()
            xmin = h_tot.GetXaxis().GetBinLowEdge(1)
            xmax = h_tot.GetXaxis().GetBinLowEdge(nbins+1)
            ymin = 0.25
            ymax = 1.0
            coeff = (ymax-ymin)/(xmax-xmin)
            for ib in range(1,nbins+1):
                e = h_tot.GetBinError(ib)
                x = h_tot.GetXaxis().GetBinCenter(ib)
                scale = ymin + (x-xmin)*coeff
                error = e*scale
                h_tot.SetBinError(ib,error)
                
    
    styles.InitData(h_data)
    styles.InitHist(h_lfakes,"","",ROOT.TColor.GetColor("#6F2D35"),1001)
    styles.InitHist(h_bkg,"","",ROOT.TColor.GetColor("#c6f74a"),1001)
    styles.InitHist(h_sig,"","",ROOT.TColor.GetColor("#FFCC66"),1001)
    styles.InitHist(h_fake,"","",ROOT.TColor.GetColor("#FFCCFF"),1001)

    h_fake.Add(h_fake,h_lfakes,1.,1.)
    h_sig.Add(h_sig,h_bkg,1.,1.)
    hFakes = h_fake.Clone('hFakes')
    hSignal = h_sig.Clone('hSignal')

    h_sig.Add(h_sig,h_fake,1.,1.)
    
    styles.InitTotalHist(h_tot)

    h_ratio = utils.histoRatio(h_data,h_tot,'ratio')
    h_tot_ratio = utils.createUnitHisto(h_tot,'tot_ratio')

    styles.InitRatioHist(h_ratio)

    h_ratio.GetYaxis().SetRangeUser(0.501,1.499)
    
    nbins = h_ratio.GetNbinsX()

    utils.zeroBinErrors(h_sig)
    utils.zeroBinErrors(h_fake)

    ymax = h_data.GetMaximum()
    if h_tot.GetMaximum()>ymax: ymax = h_tot.GetMaximum()
    h_data.GetYaxis().SetRangeUser(1.,100.*ymax)

    h_data.GetXaxis().SetLabelSize(0)
    h_data.GetYaxis().SetTitle("events / bin")
    h_data.GetYaxis().SetTitleOffset(1.2)
    h_ratio.GetYaxis().SetTitle("obs/exp")
    h_ratio.GetXaxis().SetTitle(utils.XTitle[var])
    h_ratio.GetXaxis().SetMoreLogLabels()
    h_ratio.GetXaxis().SetNoExponent()
    
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
    h_data.Draw('e1same')
    h_tot.Draw('e2same')

    legendHeader = '%s %s'%(taggerLabel[tagger],wp)
    leg = ROOT.TLegend(0.65,0.5,0.9,0.7)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.044)
    leg.SetHeader(legendHeader)
    leg.AddEntry(h_data,'data','lp')
    leg.AddEntry(h_sig,'W#rightarrow #tau#nu','f')
    leg.AddEntry(h_fake,'j#rightarrow#tau misId','f')
    leg.Draw()

    styles.CMS_label(upper,era=era,extraText='Preliminary')

    upper.Draw("SAME")
    upper.RedrawAxis()
    upper.Modified()
    upper.Update()
    upper.SetLogx(True)
    upper.SetLogy(True)
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
    lower.SetLogx(True)

    # update canvas 
    canvas.cd()
    canvas.Modified()
    canvas.cd()
    canvas.SetSelected(canvas)
    canvas.Update()
    print('')
    outfile = utils.figureFolder+'/Fits/tauID_'+wp+"_"+wpVsMu+"_"+wpVsE+"_"+meas+'_'+era+'_'+tagger
    if postfit:
        canvas.Print(outfile+"_postFit.png")
    else:
        canvas.Print(outfile+"_preFit.png")

    signal = hSignal.GetSumOfWeights()
    fakes  = hFakes.GetSumOfWeights()
    total  = signal + fakes
    data = h_data.GetSumOfWeights()
    print('')
    print('%sVSjet %sVSmu %sVSe %s %s'%(wp,wpVsMu,wpVsE,tagger,fitSuffix))
    print('Genuine taus : %3.0f'%(signal))
    print('Fake taus    : %3.0f'%(fakes))
    print('Total yield  : %3.0f'%(total))
    print('Data         : %3.0f'%(data))
    print('')
    print('')
    
############
### MAIN ###
############
if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()
    ROOT.gROOT.SetBatch(True)
    
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e','--era', dest='era', default='2025',choices=['2022','2023','2024','2025'])
    parser.add_argument('-wpVsJet','--WPvsJet', dest='wp', default='Medium',choices=['VLoose','Loose','Medium','Tight','VTight','VVTight'])
    parser.add_argument('-wpVsMu','--WPvsMu', dest='wpVsMu', default='Tight',choices=['VLoose','Tight'])
    parser.add_argument('-wpVsE','--WPvsE', dest='wpVsE', default='VVLoose',choices=['VVLoose','Tight'])
    parser.add_argument('-var','--variable', dest='variable', default='mt_1')
    parser.add_argument('-post','--postfit',dest='postfit',action='store_true')
    parser.add_argument('-ff_par','--ff_par',dest='ff_par',default='pttau',choices=['pttau','ptjet'])
    parser.add_argument('-ff','--fake_factors',dest='ff',default='comb',choices=['comb','wjets','dijets'])
    parser.add_argument('-m','--meas',dest='meas',default='lowpt',choices=['incl','lowpt','mediumpt','highpt'])
    parser.add_argument('-tagger','--tagger',dest='tagger',default='pnet',choices=['pnet','deeptau'])
    
    args = parser.parse_args()

    fullpath = '%s/%s/datacards_%s_%s_%s_%s/'%(utils.baseFolder,args.era,args.ff,args.wp,args.wpVsMu,args.wpVsE)
    filenameCards = 'taunu_%s_%s_%s_%s_%s_%s_%s_%s.root'%(args.ff_par,args.ff,args.wp,args.wpVsMu,args.wpVsE,args.meas,args.era,args.tagger)
    suffixFit = 'ptbinned'
    filenameFit = 'tauID_%s_%s_%s_%s_%s_%s_%s_%s_fit.root'%(args.ff_par,args.ff,args.wp,args.wpVsMu,args.wpVsE,args.meas,args.era,args.tagger)
    if args.meas=='incl':
        filenameFit = 'tauID_%s_%s_%s_%s_%s_%s_%s_%s_fit.root'%(args.ff_par,args.ff,args.wp,args.wpVsMu,args.wpVsE,args.meas,args.era,args.tagger)
    fullpathFit = fullpath+'/'+filenameFit
    fullpathCards = fullpath+'/'+filenameCards
    fileFit = ROOT.TFile(fullpathFit,"read")
    fileCards = ROOT.TFile(fullpathCards,"read")

    print(fileFit,fileCards)

    channel='ch2'
    if args.meas=='mediumpt':
        channel='ch3'
    if args.meas=='highpt':
        channel='ch4'

    folder='shapes_prefit'
    if args.postfit:
        folder='shapes_fit_s'

    h_data = fileCards.Get('taunu/data_obs')
    nbins = h_data.GetNbinsX()
    histnames = {}
    histnames['fake'] = 'fake'
    histnames['lfakes'] = 'lfakes' 
    if args.meas=='incl':
        histnames['wtaunu'] = 'wtaunu_incl_'+args.era
        histnames['tau'] = 'tau_incl_'+args.era
    else:
        suffix=args.meas+'_'+args.era
        histnames['wtaunu'] = 'wtaunu_'+suffix
        histnames['tau'] = 'tau_'+suffix
        
    hists = {}
    histsFit = {}
    for histname in histnames:
        hists[histname] = fileCards.Get('taunu/'+histnames[histname])
        histsFit[histname] = fileFit.Get(folder+'/'+channel+'/'+histnames[histname])
        for i in range(1,nbins+1):
            x = histsFit[histname].GetBinContent(i)
            hists[histname].SetBinContent(i,x)
            hists[histname].SetBinError(i,0.0)

    h_tot  = hists['wtaunu'].Clone('h_tot')
    h_tot_fit = fileFit.Get(folder+'/'+channel+'/total')
    for i in range(1,nbins+1):
        x = h_tot_fit.GetBinContent(i)
        e = h_tot_fit.GetBinError(i)
        h_tot.SetBinContent(i,x)
        h_tot.SetBinError(i,e)

    hists['data'] = h_data
    hists['total'] = h_tot
    Plot(hists,
         wp=args.wp,
         wpVsMu=args.wpVsMu,
         wpVsE=args.wpVsE,
         era=args.era,
         var=args.variable,
         meas=args.meas,
         tagger=args.tagger,
         postfit=args.postfit)
