#!/usr/bin/env python

import ROOT
import array

if __name__ == "__main__":

    nbins = 4
    bins = [100,130,160,200,1000]
    labels = ['mht100to130','mht130to160','mht160to200','mhtGt200']
    rootfile = ROOT.TFile("mhtnomu_bins.root","recreate")
    rootfile.cd("")
    hist = ROOT.TH1D("bins","",nbins,array('d',list(bins)))
    for ib in range(1,nbins+1):
        hist.GetXaxis().SetBinLabel(ib,labels[ib-1])

    print
    for ib in range(1,nbins+1):
        label = hist.GetXaxis().GetBinLabel(ib)
        xmin = hist.GetXaxis().GetBinLowEdge(ib)
        xmax = hist.GetXaxis().GetBinLowEdge(ib+1)
        print('[%4i,%4i] %12s'%(xmin,xmax,label))

    rootfile.cd("")
    hist.Write("bins")
    rootfile.Close()
    
    eras = ["UL2016_preVFP","UL2016_postVFP","UL2017","UL2018"]    
    cmssw_base = os.getenv('CMSSW_BASE')
    for era in eras:
        if os.path.isfile('')


    
