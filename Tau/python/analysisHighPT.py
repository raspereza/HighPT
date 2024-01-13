import ROOT 
import math
from array import array
import numpy as np
import os
import HighPT.Tau.utilsHighPT as utils

# Cus for tau+nu selection
class TauNuCuts:
    def __init__(self,**kwargs):
        self.metCut = kwargs.get('metCut',120.)
        self.metNoMuCut = kwargs.get('metNoMuCut',120.)
        self.mhtNoMuCut = kwargs.get('mhtNoMuCut',120.)
        self.mtLowerCut = kwargs.get('mtLowerCut',200.)
        self.mtUpperCut = kwargs.get('mtUpperCut',2000.)
        self.etaCut = kwargs.get('etaCut',2.3)
        self.ptLowerCut = kwargs.get('ptLowerCut',100.)
        self.ptUpperCut = kwargs.get('ptUpperCut',2000.)
        self.metdphiCut = kwargs.get('metdphiCut',2.8)
        self.antiMu = kwargs.get('antiMu',4)
        self.antiE  = kwargs.get('antiE',2)
        print
        print("Setting cuts for W*->tauv selection")
        print("metCut",self.metCut)
        print("mtLowerCut",self.mtLowerCut)
        print("mtUpperCut",self.mtUpperCut)
        print("etaCut",self.etaCut)
        print("ptLowerCut",self.ptLowerCut)
        print("ptUpperCut",self.ptUpperCut)
        print("metdphiCut",self.metdphiCut)
        print("antiMu",self.antiMu)
        print("antiE",self.antiE)

# Run over set of samples and create histogram
def RunSamples(samples,var,cut,xbins,name,**kwargs):
    #    print
    #    print("Running",name,var,weight,cut)
    weight = kwargs.get('weight','weight')
    nbins = len(xbins)-1
    hist = ROOT.TH1D(name,"",nbins,array('d',list(xbins)))
    for sampleName in samples:
        sample = samples[sampleName]
        histsample = sample.CreateHisto(var,weight,cut,xbins,name)
        hist.Add(hist,histsample,1.,1.)
    return hist

# Run over set of samples and create histograms for W*->tau+v channel
# for each sample loop over Tree entries is performed
def RunSamplesTauNu(samples,var,xbins,name,**kwargs):
    #    print
    #    print("Running",name,var,unc,selection)
    uncert_name = kwargs.get('uncert_name','')
    uncert_up = kwargs.get('uncert_up',True)
    nbins = len(xbins)-1
    hists = {} # discionary of histograms

    first = True
    for sampleName in samples:
        if uncert_name=='':
            print("Running on sample %s"%(sampleName))
        else:
            print("Running on sample %s with %s uncertainty"%(sampleName,uncert_name))
        sample = samples[sampleName]
        nameSample = sample.getSampleName()
        histsample = sample.CreateHistosTauNu(var,xbins,uncert_name=uncert_name,uncert_up=uncert_up)
        if first:
            for hist in histsample:
                namehist = name + '_' + hist
                hists[namehist] = histsample[hist].Clone(namehist)
            first = False
        else:
            for hist in histsample:
                namehist = name	+ '_' +	hist
                hists[namehist].Add(hists[namehist],histsample[hist])


#    for hist in hists:
#        print(hist)
    return hists
        
class sampleHighPt:

    def __init__(self,basefolder,era,channel,samplename,isdata,**kwargs):
        filename = basefolder + "/" + era + "/" + channel + "/" + samplename + ".root"
        if not os.path.isfile(filename):
            print("")
            print('File %s is not found '%(filename))
            print('for specified era : %s'%(era))
            print('check if variable "PicoFolder" in file utilsHighPT.py is correctly set')
            print('or check naming of samples')
            print("")
            exit()
        self.applyHTcut = kwargs.get('applyHTcut',False)
        self.additionalCut = kwargs.get('additionalCut', '')
        self.sampleName = samplename + "_" + era
        self.sampleFile = ROOT.TFile(filename,"READ")
        #self.sampleTree = self.sampleFile.Get("tree")
        self.norm = 1.0
        self.isdata = isdata
        self.regionLabels = ['SR','SB']
        self.selLabels = ['all','fake','notFake','lepFake','tau']
        if isdata:
            self.norm = 1.0
        else:
            xsecSamples = utils.eraSamples[era]
            sampleNotFound = True
            for xsecSample in xsecSamples:
                if samplename==xsecSample: 
                    sampleNotFound = False
            if sampleNotFound:
                print("")
                print('Sample %s is not found in xsec dictionary for era %s'%(samplename,era))
                print('Available samples and cross sections are')
                for xsecSample in xsecSamples:
                    print('%s : %3.1f'%(xsecSample,xsecSamples[xsecSample]))
                print("")
                exit()
            xsec = xsecSamples[samplename]
            histsumw = self.sampleFile.Get("weightedEvents")
            sumw = histsumw.GetSumOfWeights()
            lumi = utils.eraLumi[era]
            self.norm = xsec*lumi/sumw
        
        print('%s : %s : norm = %7.3f : %s'%(era,samplename,self.norm,self.additionalCut))


        
    def getSampleName(self):
        return self.sampleName
        
    def CreateHisto(self,var,weight,cut,bins,name):

        nbins = len(bins)-1
        histname = self.sampleName+'_'+name
        hist = ROOT.TH1D(histname,"",nbins,array('d',list(bins)))
        cutstring = weight+"*("+cut+")"
        tree = self.sampleFile.Get("tree")
        if (self.additionalCut!=''):
            cutstring = weight+"*("+cut+"&&"+self.additionalCut+")"
        tree.Draw(var+">>"+histname,cutstring)
        hist.Scale(self.norm)
        return hist

    def SetTauNuConfig(self,fakeFactorHighPt,WP,tauNuCuts):
        self.fakeFactorHighPt = fakeFactorHighPt
        self.WP_index = utils.tauIntWPs[WP]
        self.tauNuCuts = tauNuCuts

    def DeclareHistos(self,nbins,xbins):
        
        self.ffLabels = self.fakeFactorHighPt.getLabelList()
        self.trigLabels = self.fakeFactorHighPt.getTriggerList()
        self.uncLabels = self.fakeFactorHighPt.getUncertaintyList()

        hists = {}
        
        for sellabel in self.selLabels:
            for label in self.regionLabels:
                name = '%s_%s'%(sellabel,label)
                histname = self.sampleName+'_'+name
                hists[name] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
                for trigLabel in self.trigLabels:
                    name = '%s_%s_%s'%(sellabel,label,trigLabel)
                    histname = self.sampleName+'_'+name
                    hists[name] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
            for label in self.ffLabels:
                name = '%s_%s'%(sellabel,label)
                histname = self.sampleName+'_'+name
                hists[name] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
                for uncLabel in self.uncLabels:
                    name = '%s_%s_%s'%(sellabel,label,uncLabel)
                    histname = self.sampleName+'_'+name
                    hists[name] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
                for trigLabel in self.trigLabels:
                    name = '%s_%s_%s'%(sellabel,label,trigLabel)
                    histname = self.sampleName+'_'+name
                    hists[name] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
                    for uncLabel in self.uncLabels:
                        name = '%s_%s_%s_%s'%(sellabel,label,trigLabel,uncLabel)
                        histname = self.sampleName+'_'+name
                        hists[name] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
#        for hist in hists:
#            print(hist)
        return hists

    def CreateHistosTauNu(self,var,bins,**kwargs):

        uncert_name = kwargs.get('uncert_name','')
        uncert_up = kwargs.get('uncert_up',True)
        uncert_var = 'Down'
        if uncert_up: uncert_var = 'Up'
        uncert = uncert_name+uncert_var
        
        if uncert_name!='':
            if uncert_name not in utils.uncs:
                print('sampleHighPt::CreateHistosTauNu -> sample : %s'%(self.sampleName))
                print('Uknown uncertainty specified : %s'%(uncert_name))
                print('Available options : ',utils.uncs)
                print
                exit()
            
        tree = self.sampleFile.Get("tree")

        # initialization
        nbins = len(bins)-1
        wp_index = self.WP_index
        cuts = self.tauNuCuts
        fakeFactor = self.fakeFactorHighPt

        # creating histograms 
        hists = self.DeclareHistos(nbins,bins)

        # floats
        weight      = np.zeros(1,dtype='f')
        pt_1        = np.zeros(1,dtype='f')
        eta_1       = np.zeros(1,dtype='f')
        metdphi_1   = np.zeros(1,dtype='f')
        mt_1        = np.zeros(1,dtype='f')
        met         = np.zeros(1,dtype='f')
        metnomu     = np.zeros(1,dtype='f')
        mhtnomu     = np.zeros(1,dtype='f')
        jpt_ratio_1 = np.zeros(1,dtype='f')
        jpt_match_1 = np.zeros(1,dtype='f')
        m_1         = np.zeros(1,dtype='f')
        HT          = np.zeros(1,dtype='f')
        
        # booleans
        mettrigger     = np.zeros(1,dtype='?')
        metfilter      = np.zeros(1,dtype='?')
        tautrigger1    = np.zeros(1,dtype='?')
        tautrigger2    = np.zeros(1,dtype='?')
        extramuon_veto = np.zeros(1,dtype='?')
        extraelec_veto = np.zeros(1,dtype='?')
        extratau_veto  = np.zeros(1,dtype='?')
        
        # integers
        njets                    = np.zeros(1,dtype='i')
        idDeepTau2018v2p5VSe_1   = np.zeros(1,dtype='i')
        idDeepTau2018v2p5VSmu_1  = np.zeros(1,dtype='i')
        idDeepTau2018v2p5VSjet_1 = np.zeros(1,dtype='i')
        genmatch_1               = np.zeros(1,dtype='i')
        dm_1                     = np.zeros(1,dtype='i')
        npartons                 = np.zeros(1,dtype='i')
        
        # branches -> 
        # floats

        # uncertainty dependent
        if uncert_name=='':
            tree.SetBranchAddress('met',met)
            tree.SetBranchAddress('metdphi_1',metdphi_1)
            tree.SetBranchAddress('mt_1',mt_1)
            tree.SetBranchAddress('pt_1',pt_1)
            tree.SetBranchAddress('m_1',m_1)
        else:
            if 'taues' in uncert:
                tree.SetBranchAddress('met_'+uncert,met)
                tree.SetBranchAddress('metdphi_1_'+uncert,metdphi_1)
                tree.SetBranchAddress('mt_1_'+uncert,mt_1)
                tree.SetBranchAddress('pt_1_'+uncert,pt_1)
                tree.SetBranchAddress('m_1_'+uncert,m_1)
            else:
                tree.SetBranchAddress('met_'+uncert,met)
                tree.SetBranchAddress('metdphi_1_'+uncert,metdphi_1)
                tree.SetBranchAddress('mt_1_'+uncert,mt_1)
                tree.SetBranchAddress('pt_1',pt_1)
                tree.SetBranchAddress('m_1',m_1)
                

        tree.SetBranchAddress('metnomu',metnomu)
        tree.SetBranchAddress('mhtnomu',mhtnomu)
        tree.SetBranchAddress('weight',weight)
        tree.SetBranchAddress('eta_1',eta_1)
        tree.SetBranchAddress('jpt_ratio_1',jpt_ratio_1)
        tree.SetBranchAddress('jpt_match_1',jpt_match_1)
        tree.SetBranchAddress('dm_1',dm_1)
        
        # booleans
        tree.SetBranchAddress('mettrigger',mettrigger)
        tree.SetBranchAddress('metfilter',metfilter)
        tree.SetBranchAddress('extramuon_veto',extramuon_veto)
        tree.SetBranchAddress('extraelec_veto',extraelec_veto)
        tree.SetBranchAddress('extratau_veto',extratau_veto)
        tree.SetBranchAddress('tautrigger1',tautrigger1)
        tree.SetBranchAddress('tautrigger2',tautrigger2)

        # integers
        tree.SetBranchAddress('njets',njets)
        tree.SetBranchAddress('idDeepTau2018v2p5VSe_1',idDeepTau2018v2p5VSe_1)
        tree.SetBranchAddress('idDeepTau2018v2p5VSmu_1',idDeepTau2018v2p5VSmu_1)
        tree.SetBranchAddress('idDeepTau2018v2p5VSjet_1',idDeepTau2018v2p5VSjet_1)
        if not self.isdata:
            tree.SetBranchAddress("genmatch_1",genmatch_1)
            tree.SetBranchAddress("HT",HT)
            tree.SetBranchAddress("NUP_LO",npartons)
            
        nentries = tree.GetEntries()

        # run over entries
        for entry in range(0,nentries):
            tree.GetEntry(entry)

            if not self.isdata:
                if self.applyHTcut and HT[0]>100 and HT[0]<800: continue

            # met filters, trigger, vetos
            if not metfilter[0]: continue
            if not mettrigger[0]: continue
            if extraelec_veto[0]: continue
            if extramuon_veto[0]: continue
            if extratau_veto[0]: continue
            if njets[0]!=0: continue

            dmcut = dm_1[0]==0 or dm_1[0]==1 or dm_1[0]==10 or dm_1[0]==11
            if not dmcut: continue
            
            # kinematic cuts
            if pt_1[0]<cuts.ptLowerCut: continue
            if pt_1[0]>cuts.ptUpperCut: continue
            if math.fabs(eta_1[0])>cuts.etaCut: continue
            if mt_1[0]<cuts.mtLowerCut: continue
            if mt_1[0]>cuts.mtUpperCut: continue
            if metdphi_1[0]<cuts.metdphiCut: continue
            if met[0]<cuts.metCut: continue
            if metnomu[0]<cuts.metNoMuCut: continue
            if mhtnomu[0]<cuts.mhtNoMuCut: continue
            
            # tau discriminator against e and mu and jet
            if idDeepTau2018v2p5VSe_1[0]<cuts.antiE: continue
            if idDeepTau2018v2p5VSmu_1[0]<cuts.antiMu: continue
            if idDeepTau2018v2p5VSjet_1[0]<1: continue

            variable = mt_1[0]
            if var=='pt_1': variable = pt_1[0]
            if var=='eta_1': variable = eta_1[0]
            if var=='met': variable = met[0]
            if var=='m_1': variable = m_1[0]

            # mc selection
            lepFake = genmatch_1[0]==1 or genmatch_1[0]==2 or genmatch_1[0]==3 or genmatch_1[0]==4
            genuineTau = genmatch_1[0]==5
            jetFake = genmatch_1[0]==0
            notJetFake = not jetFake

            # generator map
            selFlags = {}
            selFlags['all'] = True
            selFlags['fake'] = False
            selFlags['notFake'] = False
            selFlags['lepFake'] = False
            selFlags['tau'] = False
            
            if not self.isdata:
                if jetFake: selFlags['fake'] = True
                if notJetFake: selFlags['notFake'] = True
                if lepFake: selFlags['lepFake'] = True
                if genuineTau: selFlags['tau'] = True
                
            tautrigger = tautrigger1[0] or tautrigger2[0]
            trigFlags = {}
            trigFlags['trig'] = tautrigger
            trigFlags['notrig'] = not tautrigger

            # signal region
            if idDeepTau2018v2p5VSjet_1[0]>=wp_index:

                for selFlag in selFlags:
                    if selFlags[selFlag]:
                        name = selFlag + '_SR'
                        hists[name].Fill(variable,weight[0])
                        for trigFlag in trigFlags:
                            if trigFlags[trigFlag]:
                                nametrig = selFlag + '_SR_' + trigFlag
                                hists[nametrig].Fill(variable,weight[0])

            # sideband region
            if idDeepTau2018v2p5VSjet_1[0]<4:

                for selFlag in selFlags:
                    if selFlags[selFlag]:
                        name = selFlag + '_SB'
                        hists[name].Fill(variable,weight[0])
                        for trigFlag in trigFlags:
                            if trigFlags[trigFlag]:
                                nametrig = selFlag + '_SB_' + trigFlag
                                hists[nametrig].Fill(variable,weight[0])

                # applying fake factors
                fakeFactor.setVal(pttau=pt_1[0],
                                  ptjet=jpt_match_1[0],
                                  ptratio=jpt_ratio_1[0],
                                  mtau=m_1[0],
                                  dm=dm_1[0])

                # inclusive FF
                for label in self.ffLabels:
                    ffweights = fakeFactor.getWeight(label=label,
                                                     sample='incl')
                    for selFlag in selFlags:
                        if selFlags[selFlag]:
                            for ffname in ffweights:
                                if ffname=='central':
                                    name = '%s_%s'%(selFlag,label)
                                else:
                                    name = '%s_%s_%s'%(selFlag,label,ffname)
                                hists[name].Fill(variable,weight[0]*ffweights[ffname])

                # trigger dependent FF
                for trigFlag in trigFlags:
                    if trigFlags[trigFlag]:
                        for label in self.ffLabels:
                            ffweights = fakeFactor.getWeight(label=label,
                                                             sample=trigFlag)
                            for selFlag in selFlags:
                                if selFlags[selFlag]:
                                    for ffname in ffweights:
                                        if ffname=='central':
                                            name = '%s_%s_%s'%(selFlag,label,trigFlag)
                                        else:
                                            name = '%s_%s_%s_%s'%(selFlag,label,trigFlag,ffname)
                                        hists[name].Fill(variable,weight[0]*ffweights[ffname])
                                        

        for hist in hists:
            hists[hist].Scale(self.norm)

        return hists
