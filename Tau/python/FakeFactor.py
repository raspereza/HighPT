import ROOT 
import math
from array import array
import numpy as np
import os

class FakeFactorHighPt:

    def __init__(self,**kwargs):
        print
        self.fileName = kwargs.get('filename','None')
        print('Loading fake factors from file %s'%(self.fileName))
        if not os.path.isfile(self.fileName):
            print('FakeFactorHighPt : file %s does not exist'%(self.fileName))
            exit()
        self.fileFF = ROOT.TFile(self.fileName,"READ")

        self.variable1 = kwargs.get('variable1','pttau')
        self.variable2 = kwargs.get('variable2','ptratio')

        if self.variable1 not in ['pttau','ptjet','mtau']:
            print('FakeFactorHighPt : undefined variable1 %s'%(self.variable1))
            print('                   available options : pttau, ptjet, mtau')
            exit()

        if self.variable2 not in ['ptratio','dm']:
            print('FakeFactorHighPt : undefined variable2 %s'%(self.variable2))
            print('                   available options : ptratio, dm')
            exit()

        if self.variable1=='mtau' and self.variable2=='ptratio':
            print('FakeFactorHighPt : no measurement exist for (mtau,ptratio) bins')
            exit()
            
        self.with_dijets = kwargs.get('with_dijets',False)
        
        self.samples = ['incl','trig','notrig']
        self.triglabels = ['trig','notrig']
        self.labels = ['data_wjets','mc_wjets']

        if self.with_dijets:
            self.labels.append('data_dijets')

        self.ptjet_histo = self.fileFF.Get('ptjet')
        self.ptjet_nbins = self.ptjet_histo.GetNbinsX()

        self.pttau_histo = self.fileFF.Get('pttau')
        self.pttau_nbins = self.pttau_histo.GetNbinsX()

        self.ptratio_histo = self.fileFF.Get('ptratio')
        self.ptratio_nbins = self.ptratio_histo.GetNbinsX()

        self.dm_histo = self.fileFF.Get('dm')
        self.dm_nbins = self.dm_histo.GetNbinsX()

        # internal variables
        # initialized
        self.ptratio = 0.9
        self.pttau = 150.0
        self.ptjet = 200.0
        self.dm = 0
        self.mtau = 1.0

        self.var2_histo = self.ptratio_histo
        self.var2_nbins = self.ptratio_nbins
        if self.variable2=='dm':
            self.var2_histo = self.dm_histo
            self.var2_nbins = self.dm_nbins

        self.var2_min = self.var2_histo.GetBinLowEdge(1)+0.01
        self.var2_max = self.var2_histo.GetBinLowEdge(1+self.var2_nbins)-0.01
            
        self.var1_histo = self.pttau_histo
        self.var1_nbins = self.pttau_nbins
        if self.variable1=='ptjet':
            self.var1_histo = self.ptjet_histo
            self.var1_nbins = self.ptjet_nbins

        self.var1_min = self.var1_histo.GetBinLowEdge(1)+0.01
        self.var1_max = self.var1_histo.GetBinLowEdge(1+self.var1_nbins)-0.01
            
        self.uncs = []
        self.hists = {}
        for label in self.labels:
            for var in ['pttau','ptjet']:
                for ib in range(1,self.ptratio_nbins+1):
                    binname = self.ptratio_histo.GetXaxis().GetBinLabel(ib)
                    for sample in self.samples:
                        histname = '%s_%s_%s_%s'%(label,var,binname,sample)                        
                        self.hists[histname] = self.fileFF.Get(histname)
                        # print(histname,self.hists[histname])

        for label in self.labels:
            for var in ['pttau','ptjet','mtau']:
                for ib in range(1,self.dm_nbins+1):
                    binname = self.dm_histo.GetXaxis().GetBinLabel(ib)
                    histname = '%s_%s_%s_incl'%(label,var,binname)
                    self.hists[histname] = self.fileFF.Get(histname)
                    # print(histname,self.hists[histname])

    def getLabelList(self):
        return self.labels

    def getSampleList(self):
        return self.samples

    def getTriggerList(self):
        return self.triglabels

    def getUncertaintyList(self):
        self.uncs = []
        if self.variable2=='dm':
            if self.variable1=='mtau':
                for ib in range(1,self.dm_nbins+1):
                    binname = self.dm_histo.GetXaxis().GetBinLabel(ib)
                    name = binname
                    self.uncs.append(name)
            else:
                for ib in range(1,self.dm_nbins+1):
                    binname = self.dm_histo.GetXaxis().GetBinLabel(ib)
                    for ptbin in range(1,self.var1_nbins+1):
                        ptname = self.var1_histo.GetXaxis().GetBinLabel(ptbin)
                        name = '%s_%s'%(binname,ptname)
                        self.uncs.append(name)
        else:
            for ib in range(1,self.ptratio_nbins+1):
                binname = self.ptratio_histo.GetXaxis().GetBinLabel(ib)
                for ptbin in range(1,self.var1_nbins+1):
                    ptname = self.var1_histo.GetXaxis().GetBinLabel(ptbin)
                    name = '%s_%s'%(binname,ptname)
                    self.uncs.append(name)
                            
        return self.uncs

    # setting values
    def setVal(self,**kwargs):
        self.pttau = kwargs.get('pttau',self.pttau)
        self.ptjet = kwargs.get('ptjet',self.ptjet)
        self.ptratio = kwargs.get('ptratio',self.ptratio)
        self.dm = kwargs.get('dm',self.dm)
        self.mtau = kwargs.get('mtau',self.mtau)

    # getting weight
    def getWeight(self,**kwargs):

        label = kwargs.get('label','data_wjets')
        sample   = kwargs.get('sample','incl')
        
        weights = {}
        if label not in self.labels:
            print('FakeFactorHighPt  - undefined label : %s'%(label))
            print('Available options : ',self.labels)
            print('FakeFactorHighPt  - returning 0 items')
            return weights
        
        if sample not in self.samples:
            print('FakeFactorHighPt  - undefined trigger option : %s'%(sample))
            print('Available options : ',self.samples)
            print('FakeFactorHighPt  -  returning 0 items')
            return weights
        
        # only inclusive measurements in dm bins are available
        if self.variable2=='dm':
            sample = 'incl'
            
        var1 = self.pttau
        if self.variable1=='ptjet':
            var1 = self.ptjet
        elif self.variable1=='mtau':
            var1 = self.mtau
        
        var2 = self.ptratio
        if self.variable2=='dm': 
            var2 = self.dm

        y = min(self.var2_max,max(self.var2_min,var2))
        bin_var2 = self.var2_histo.FindBin(y)
        binname = self.var2_histo.GetXaxis().GetBinLabel(bin_var2)

        name = '%s_%s_%s_%s'%(label,self.variable1,binname,sample)
        nbins = self.hists[name].GetNbinsX()
        xmin = self.hists[name].GetBinLowEdge(1) + 0.01
        xmax = self.hists[name].GetBinLowEdge(nbins+1) - 0.01

        x = min(xmax,max(xmin,var1))
        weight = self.hists[name].GetBinContent(self.hists[name].FindBin(x))
        error = self.hists[name].GetBinError(self.hists[name].FindBin(x))

        weights['central'] = weight
        ptbin = self.var1_histo.FindBin(x)
        ptname = self.var1_histo.GetXaxis().GetBinLabel(ptbin)

        unc_label = ''
        if self.variable2=='dm':
            if self.variable1=='mtau':
                unc_label = binname
            else:
                unc_label = '%s_%s'%(binname,ptname)
        else:
            unc_label = '%s_%s'%(binname,ptname)
                
        for unc in self.uncs:
            if unc==unc_label:
                weights[unc] = weight + error
            else:
                weights[unc] = weight
        
        return weights
