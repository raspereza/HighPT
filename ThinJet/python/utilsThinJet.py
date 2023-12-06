import ROOT 
import math
from array import array
import numpy as np
import os

#############################
##### General settings ######
#############################

#############################
##### working dir ###########
#############################
BaseFolder=os.getenv('CMSSW_BASE')+'/src/HighPT/ThinJet/output'

#########################
# folder for picotuples #
#########################
picoFolderFF='/eos/user/r/rasp/output/HighPT_thinjet'
picoFolderTauNu='/eos/user/r/rasp/output/HighPT_thinjet'
picoFolderMuNu='/eos/user/r/rasp/output/HighPT_deepTauV2p5'

#######################
# folders for figures #
#######################
figuresFolderFF = BaseFolder+'/figures/FF'
figuresFolderWMuNu = BaseFolder+'/figures'
figuresFolderWTauNu = BaseFolder+'/figures'
figuresFolderPT = BaseFolder+'/figures'

########################
# folder for datacards #
########################
datacardsFolder = BaseFolder+'/datacards'

fakeFactorFolder = BaseFolder+'/FF'

###################
# Cross sections  #
###################

sampleXSec_2016_postVFP = { 
"DYJetsToLL_M-50" : 6077.22,
"TTTo2L2Nu" : 88.29,
"TTToSemiLeptonic" : 365.35,
"TTToHadronic" : 377.96,  
"WJetsToLNu_HT-100To200" : 1395.0*1.166,
"WJetsToLNu_HT-200To400" : 407.9*1.166,
"WJetsToLNu_HT-400To600" : 57.48*1.166,
"WJetsToLNu_HT-600To800" : 12.87*1.166,
"WJetsToLNu_HT-800To1200" : 5.366*1.166,
"WJetsToLNu_HT-1200To2500" : 1.074*1.166,
"WJetsToLNu" : 61526.7 ,  
"ST_tW_antitop_5f_NoFullyHadronicDecays" : 19.47,
"ST_tW_top_5f_NoFullyHadronicDecays" : 19.47,
"ST_t-channel_antitop_4f_InclusiveDecays" : 80.95,
"ST_t-channel_top_4f_InclusiveDecays" : 136.02,
"WW" : 118.7,
"WZ" : 27.68,
"ZZ" : 12.19,
"ZJetsToNuNu_HT-100To200"   : 304.5,
"ZJetsToNuNu_HT-200To400"   : 91.82,
"ZJetsToNuNu_HT-400To600"   : 13.11,
"ZJetsToNuNu_HT-600To800"   : 3.260,
"ZJetsToNuNu_HT-800To1200"  : 1.499,
"ZJetsToNuNu_HT-1200To2500" : 0.3430,
"WToMuNu_M-200" : 5.702,
"WToTauNu_M-200" : 6.020
}

sampleXSec_2016_preVFP = { 
"DYJetsToLL_M-50" : 6077.22,
"TTTo2L2Nu" : 88.29,
"TTToSemiLeptonic" : 365.35,
"TTToHadronic" : 377.96,  
"WJetsToLNu_HT-100To200" : 1395.0*1.166,
"WJetsToLNu_HT-200To400" : 407.9*1.166,
"WJetsToLNu_HT-400To600" : 57.48*1.166,
"WJetsToLNu_HT-600To800" : 12.87*1.166,
"WJetsToLNu_HT-800To1200" : 5.366*1.166,
"WJetsToLNu_HT-1200To2500" : 1.074*1.166,
"WJetsToLNu" : 61526.7 ,  
"ST_tW_antitop_5f_NoFullyHadronicDecays" : 19.47,
"ST_tW_top_5f_NoFullyHadronicDecays" : 19.47,
"ST_t-channel_antitop_4f_InclusiveDecays" : 80.95,
"ST_t-channel_top_4f_InclusiveDecays" : 136.02,
"WW" : 118.7,
"WZ" : 27.68,
"ZZ" : 12.19,
"ZJetsToNuNu_HT-100To200"   : 304.5,
"ZJetsToNuNu_HT-200To400"   : 91.82,
"ZJetsToNuNu_HT-400To600"   : 13.11,
"ZJetsToNuNu_HT-600To800"   : 3.260,
"ZJetsToNuNu_HT-800To1200"  : 1.499,
"ZJetsToNuNu_HT-1200To2500" : 0.3430,
"WToMuNu_M-200" : 5.702,
"WToTauNu_M-200" : 6.020
}

sampleXSec_2017 = {
"DYJetsToLL_M-50" : 6077.22,
"TTTo2L2Nu" : 88.29,
"TTToSemiLeptonic" : 365.35,
"TTToHadronic" : 377.96,  
"WJetsToLNu_HT-100To200" : 1395.0*1.166,
"WJetsToLNu_HT-200To400" : 407.9*1.166,
"WJetsToLNu_HT-400To600" : 57.48*1.166,
"WJetsToLNu_HT-600To800" : 12.87*1.166,
"WJetsToLNu_HT-800To1200" : 5.366*1.166,
"WJetsToLNu_HT-1200To2500" : 1.074*1.166,
"WJetsToLNu" : 61526.7 ,  
"ST_tW_antitop_5f_NoFullyHadronicDecays" : 19.47,
"ST_tW_top_5f_NoFullyHadronicDecays" : 19.47,
"ST_t-channel_antitop_4f_InclusiveDecays" : 80.95,
"ST_t-channel_top_4f_InclusiveDecays" : 136.02,
"WW" : 118.7,
"WZ" : 27.68,
"ZZ" : 12.19,
"ZJetsToNuNu_HT-100To200"   : 304.5,
"ZJetsToNuNu_HT-200To400"   : 91.82,
"ZJetsToNuNu_HT-400To600"   : 13.11,
"ZJetsToNuNu_HT-600To800"   : 3.260,
"ZJetsToNuNu_HT-800To1200"  : 1.499,
"ZJetsToNuNu_HT-1200To2500" : 0.3430,
"WToMuNu_M-200" : 6.700,
"WToTauNu_M-200" : 7.246
}

sampleXSec_2018 = {
"DYJetsToLL_M-50" : 6077.22,
"TTTo2L2Nu" : 88.29,
"TTToSemiLeptonic" : 365.35,
"TTToHadronic" : 377.96,  
"WJetsToLNu_HT-100To200" : 1395.0*1.166,
"WJetsToLNu_HT-200To400" : 407.9*1.166,
"WJetsToLNu_HT-400To600" : 57.48*1.166,
"WJetsToLNu_HT-600To800" : 12.87*1.166,
"WJetsToLNu_HT-800To1200" : 5.366*1.166,
"WJetsToLNu_HT-1200To2500" : 1.074*1.166,
"WJetsToLNu" : 61526.7 ,  
"ST_tW_antitop_5f_NoFullyHadronicDecays" : 19.47,
"ST_tW_top_5f_NoFullyHadronicDecays" : 19.47,
"ST_t-channel_antitop_4f_InclusiveDecays" : 80.95,
"ST_t-channel_top_4f_InclusiveDecays" : 136.02,
"WW" : 118.7,
"WZ" : 27.68,
"ZZ" : 12.19,
"ZJetsToNuNu_HT-100To200"   : 304.5,
"ZJetsToNuNu_HT-200To400"   : 91.82,
"ZJetsToNuNu_HT-400To600"   : 13.11,
"ZJetsToNuNu_HT-600To800"   : 3.260,
"ZJetsToNuNu_HT-800To1200"  : 1.499,
"ZJetsToNuNu_HT-1200To2500" : 0.3430,
"WToMuNu_M-200" : 6.990,
"WToTauNu_M-200" : 7.246
}

eraSamples = {
"UL2016_postVFP" : sampleXSec_2016_postVFP,
"UL2016_preVFP" : sampleXSec_2016_preVFP,
"UL2017" : sampleXSec_2017,    
"UL2018" : sampleXSec_2018
}

eraLumi = {
    "UL2016" : 36300,
    "UL2016_postVFP" : 16800,
    "UL2016_preVFP"  : 19500,
    "UL2017" : 41480,    
    "UL2018" : 59830
}

##################################
# Working points against leptons # 
# optimized for thin-jet ID      #
##################################
wpVsMu = 'Tight'
wpVsE  = 'Tight'


################
# Data samples #
################

singlemu_2018 = ['SingleMuon_Run2018A','SingleMuon_Run2018B','SingleMuon_Run2018C','SingleMuon_Run2018D']
singlemu_2017 = ['SingleMuon_Run2017B','SingleMuon_Run2017C','SingleMuon_Run2017D','SingleMuon_Run2017E','SingleMuon_Run2017F']
singlemu_2016_preVFP = ['SingleMuon_Run2016B','SingleMuon_Run2016C','SingleMuon_Run2016D','SingleMuon_Run2016E','SingleMuon_Run2016F']
singlemu_2016_postVFP = ['SingleMuon_Run2016F','SingleMuon_Run2016G','SingleMuon_Run2016H']


jetht_2018 = ['JetHT_Run2018A','JetHT_Run2018B','JetHT_Run2018C','JetHT_Run2018D']
jetht_2017 = ['JetHT_Run2017B','JetHT_Run2017C','JetHT_Run2017D','JetHT_Run2017E','JetHT_Run2017F']
jetht_2016_preVFP = ['JetHT_Run2016B','JetHT_Run2016C','JetHT_Run2016D','JetHT_Run2016E','JetHT_Run2016F']
jetht_2016_postVFP = ['JetHT_Run2016F','JetHT_Run2016G','JetHT_Run2016H']


met_2018 = ['MET_Run2018A','MET_Run2018B','MET_Run2018C','MET_Run2018D']
met_2017 = ['MET_Run2017B','MET_Run2017C','MET_Run2017D','MET_Run2017E','MET_Run2017F']
met_2016_preVFP = ['MET_Run2016B','MET_Run2016C','MET_Run2016D','MET_Run2016E','MET_Run2016F']
met_2016_postVFP = ['MET_Run2016F','MET_Run2016G','MET_Run2016H']

singlemu = {
    "UL2016_preVFP": singlemu_2016_preVFP,
    "UL2016_postVFP": singlemu_2016_postVFP,
    "UL2017": singlemu_2017,
    "UL2018": singlemu_2018
}

jetht = {
    "UL2016_preVFP": jetht_2016_preVFP,
    "UL2016_postVFP": jetht_2016_postVFP,
    "UL2017": jetht_2017,
    "UL2018": jetht_2018
}

met = {
    "UL2016_preVFP": met_2016_preVFP,
    "UL2016_postVFP": met_2016_postVFP,
    "UL2017": met_2017,
    "UL2018": met_2018
}

tauVsEleWPs = {
    'VVVLoose': "1",
    'VVLoose' : "2",
    'VLoose'  : "3",
    'Loose'   : "4",
    'Medium'  : "5",
    'Tight'   : "6",
    'VTight'  : "7",
    'VVTight' : "8"
}

tauVsEleIntWPs = {
    'VVVLoose': 1,
    'VVLoose' : 2,
    'VLoose'  : 3,
    'Loose'   : 4,
    'Medium'  : 5,
    'Tight'   : 6,
    'VTight'  : 7,
    'VVTight' : 8
}

tauVsMuWPs = {
    'VLoose'  : "1",
    'Loose'   : "2",
    'Medium'  : "3",
    'Tight'   : "4"
}

tauVsMuIntWPs = {
    'VLoose'  : 1,
    'Loose'   : 2,
    'Medium'  : 3,
    'Tight'   : 4
}

tauWPs = {
    'VVVLoose': "1",
    'VVLoose': "2",
    'VLoose': "3",
    'Loose': "4",
    'Medium': "5",
    'Tight': "6",
    'VTight': "7",
    'VVTight': "8"
}

tauIntWPs = {
    'VVVLoose': 1,
    'VVLoose': 2,
    'VLoose': 3,
    'Loose': 4,
    'Medium': 5,
    'Tight': 6,
    'VTight': 7,
    'VVTight': 8    
}

#############################
# Shape uncertainties (JME) #
#############################
unc_jme = ['JES','Unclustered']

###############################
# Shape uncertainties (taues) #
###############################
unc_taues = ['taues','taues_1pr','taues_1pr1pi0','taues_3pr','taues_3pr1pi0'] 

##################################
### Settings for FF measurements #
##################################
xbinsPt2D = [100, 125, 150, 200, 2000] 
xbinsPt =   [100, 125, 150, 175, 200, 2000]
xbinsPt_Jet = [140, 160, 180, 200, 250, 300, 2000]

ptUncThreshold = 300. # split pt region for stat. uncertainties (<300, >=300.)

ptratio2DCuts = {
    'ptratioLow'   : 'jpt_ratio_2<0.85',
    'ptratioHigh'  : 'jpt_ratio_2>=0.85'
}
ptratio2DThreshold = 0.85

ptratioCuts = {
    'ptratioLow'   : 'jpt_ratio_2<0.85',
    'ptratioHigh'  : 'jpt_ratio_2>=0.85'
}
ptratioThreshold = 0.85

decaymode2DCuts = {
    '1prong'    : 'dm_2==0',
    '1prongPi0' : '(dm_2==1||dm_2==2)',
    '3prong'    : 'dm_2==10',
    '3prongPi0' : 'dm_2==11'
}

decaymodeCuts = {
    '1prong' : '(dm_2==0||dm_2==1)',
    '2prong' : '(dm_2==5||dm_2==6)',
    '3prong' : '(dm_2==10||dm_2==11)'
}

dmCuts = {
    '1prong' : '(dm_1==0||dm_1==1)',
    '2prong' : '(dm_1==5||dm_1==6)',
    '3prong' : '(dm_1==10||dm_1==11)'
}

# histogram labels (W*->tau+v selection)
histLabels = ['','_SB','_mc_wjets','_data_wjets','_data_dijets']
histSysLabels = ['_mc_wjets','_data_wjets','_data_dijets']
ptratioLabels = ['_ptratioLow','_ptratioHigh']
statUncLabels = ['_unc1','_unc2']

XTitle = {
    'mt_jet_1'    : "m_{T} (GeV)",
    'mt_1'        : "m_{T} (GeV)",
    'pt_1'        : "p_{T} (GeV)",
    'eta_1'       : "#eta",
    'jpt_match_1' : "p_{T} (GeV)",
    'jeta_match_1': "#eta",
    'met'         : "E_{T}^{mis} (GeV)",
    'm_1'         : "tau mass (GeV)",
    'jpt_ratio_1' : "p_{T}(#tau)/p_{T}(jet)",
}

#######################################
# Creating shape systematic templates #
#######################################
def ComputeSystematics(h_central, h_sys, name):
    h_up = h_central.Clone(name+"Up")
    h_down = h_central.Clone(name+"Down")
    nbins = h_central.GetNbinsX()
    for i in range(1,nbins+1):
        x_up = h_sys.GetBinContent(i)
        x_central = h_central.GetBinContent(i)
        x_down = x_central
        if x_up>0:
            x_down = x_central*x_central/x_up
        h_up.SetBinContent(i,x_up)
        h_down.SetBinContent(i,x_down)

    return h_up, h_down

def extractBinLabels(pt):
    uncLabel = '_unc1'
    if pt>ptUncThreshold: uncLabel = '_unc2'
    return uncLabel

# Run over set of samples and create histogram
def RunSamples(samples,var,weight,cut,xbins,name):
    print
    print("Running",name,var,weight,cut)
    nbins = len(xbins)-1
    hist = ROOT.TH1D(name,"",nbins,array('d',list(xbins)))
    for sampleName in samples:
        sample = samples[sampleName]
        histsample = sample.CreateHisto(var,weight,cut,xbins,name+"_"+sampleName)
        hist.Add(hist,histsample,1.,1.)
    return hist

# Run over set of samples and create histograms for W*->tau+v channel
# for each sample loop over Tree entries is performed
def RunSamplesTauNu(samples,var,xbins,selection,name):
    print
    print("Running",name,var,selection)
    nbins = len(xbins)-1
    hists = {} # discionary of histograms
    for label in histLabels:
        histname = name + selection + label
        hists[histname] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
    for label in histSysLabels:
        for uncLabel in statUncLabels:
            histname = name + selection + label + uncLabel
            hists[histname] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))

    for sampleName in samples:        
        sample = samples[sampleName]
        histsample = sample.CreateHistosTauNu(var,xbins,selection)
        
        for label in histLabels:
            histname = name + selection + label
            histsamplename = sample.sampleName + selection + label
            hists[histname].Add(hists[histname],histsample[histsamplename],1.,1.)
        for label in histSysLabels:
            for uncLabel in statUncLabels:
                histname = name + selection + label + uncLabel
                histsamplename = sample.sampleName + selection + label + uncLabel
                hists[histname].Add(hists[histname],histsample[histsamplename],1.,1.)

    return hists

def createBins(nbins,xmin,xmax):
    binwidth = (xmax-xmin)/float(nbins)
    bins = []
    for i in range(0,nbins+1):
        xb = xmin + float(i)*binwidth
        bins.append(xb)
    return bins

def zeroBinErrors(hist):
    nbins = hist.GetNbinsX()
    for i in range(1,nbins+1):
        hist.SetBinError(i,0.)

def createUnitHisto(hist,histName):
    nbins = hist.GetNbinsX()
    unitHist = hist.Clone(histName)
    for i in range(1,nbins+1):
        x = hist.GetBinContent(i)
        e = hist.GetBinError(i)
        if x>0:
            rat = e/x
            unitHist.SetBinContent(i,1.)
            unitHist.SetBinError(i,rat)

    return unitHist

def dividePassProbe(passHist,failHist,histName):
    nbins = passHist.GetNbinsX()
    hist = passHist.Clone(histName)
    for i in range(1,nbins+1):
        xpass = passHist.GetBinContent(i)
        epass = passHist.GetBinError(i)
        xfail = failHist.GetBinContent(i)
        efail = failHist.GetBinError(i)
        xprobe = xpass+xfail
        ratio = 1
        eratio = 0
        if xprobe>1e-4:
            ratio = xpass/xprobe
            dpass = xfail*epass/(xprobe*xprobe)
            dfail = xpass*efail/(xprobe*xprobe)
            eratio = math.sqrt(dpass*dpass+dfail*dfail)
        hist.SetBinContent(i,ratio)
        hist.SetBinError(i,eratio)

    return hist

def divideHistos(numHist,denHist,histName):
    nbins = numHist.GetNbinsX()
    hist = numHist.Clone(histName)
    for i in range(1,nbins+1):
        xNum = numHist.GetBinContent(i)
        eNum = numHist.GetBinError(i)
        xDen = denHist.GetBinContent(i)
        eDen = denHist.GetBinError(i)
        ratio = 1
        eratio = 0
        if xNum>1e-7 and xDen>1e-7:
            ratio = xNum/xDen
            rNum = eNum/xNum
            rDen = eDen/xDen
            rratio = math.sqrt(rNum*rNum+rDen*rDen)
            eratio = rratio * ratio
        hist.SetBinContent(i,ratio)
        hist.SetBinError(i,eratio)

    return hist

def histoRatio(numHist,denHist,histName):
    nbins = numHist.GetNbinsX()
    hist = numHist.Clone(histName)
    for i in range(1,nbins+1):
        xNum = numHist.GetBinContent(i)
        eNum = numHist.GetBinError(i)
        xDen = denHist.GetBinContent(i)
        ratio = 1
        eratio = 0
        if xNum>1e-7 and xDen>1e-7:
            ratio = xNum/xDen
            eratio = eNum/xDen
        hist.SetBinContent(i,ratio)
        hist.SetBinError(i,eratio)

    return hist

  
class TauNuCuts:
    def __init__(self,**kwargs):
        self.metCut = kwargs.get('metCut',150.)
        self.etaCut = kwargs.get('etaCut',2.5)
        self.etaJetCut = kwargs.get('etaJetCut',2.3)
        self.ptLowerCut = kwargs.get('ptLowerCut',70.)
        self.ptUpperCut = kwargs.get('ptUpperCut',2000.)
        self.ptJetLowerCut = kwargs.get('ptJetLowerCut',140.)
        self.ptJetUpperCut = kwargs.get('ptJetUpperCut',2000.)
        self.metdphiCut = kwargs.get('metdphiCut',2.8)
        self.antiMu = kwargs.get('antiMu',4)
        self.antiE  = kwargs.get('antiE',2)
        self.dm = kwargs.get('dm','1prong')
        print
        print("Setting cuts for W*->tauv selection")
        print("metCut",self.metCut)
        print("etaCut",self.etaCut)
        print("etaJetCut",self.etaJetCut)
        print("ptLowerCut",self.ptLowerCut)
        print("ptUpperCut",self.ptUpperCut)
        print("ptJetLowerCut",self.ptJetLowerCut)
        print("ptJetUpperCut",self.ptJetUpperCut)
        print("metdphiCut",self.metdphiCut)
        print("antiMu",self.antiMu)
        print("antiE",self.antiE)
        print("dm",self.dm)

class FakeFactorHighPt:

    def __init__(self,filename):
        print
        print('Loading fake factors from file',filename," >>>>>")
        self.fileName = filename
        self.fileFF = ROOT.TFile(self.fileName,"READ")
        self.hists = {}
        self.dmbins = ['1prong','2prong','3prong']
        self.labels = ['dijets','wjets']
        for dmbin in self.dmbins:
            for label in self.labels:                
                name = 'data_' + label + "_" + dmbin
                self.hists[name] = self.fileFF.Get(name)
                print(name,self.hists[name])
            name = 'mc_wjets_' + dmbin
            self.hists[name] = self.fileFF.Get(name)
            print(name,self.hists[name])

    def getWeight(self,pttau,dm,label):
        dmlabel = '1prong'
        if (dm==5 or dm==6): dmlabel = '2prong'
        if (dm==10 or dm==11): dmlabel = '3prong' 
        name = label + "_" + dmlabel
        x = pttau
        nbins = self.hists[name].GetNbinsX()
        lowerEdge = self.hists[name].GetBinLowEdge(1)
        upperEdge = self.hists[name].GetBinLowEdge(nbins+1)
        if pttau<lowerEdge: x = lowerEdge+0.001
        if pttau>upperEdge: x = upperEdge-0.001
        weight = self.hists[name].GetBinContent(self.hists[name].FindBin(x))
        error = self.hists[name].GetBinError(self.hists[name].FindBin(x))
        return weight,error

class sampleHighPt:

    def __init__(self,basefolder,era,channel,samplename,isdata,**kwargs):
        filename = basefolder + "/" + era + "/" + channel + "/" + samplename + ".root"
        self.additionalCut = kwargs.get('additionalCut', '')
        self.sampleName = samplename
        self.sampleFile = ROOT.TFile(filename,"READ")
        #self.sampleTree = self.sampleFile.Get("tree")
        self.norm = 1.0
        self.isdata = isdata
        if isdata:
            self.norm = 1.0
        else:
            xsecSamples = eraSamples[era]
            xsec = xsecSamples[samplename]
            histsumw = self.sampleFile.Get("weightedEvents")
            sumw = histsumw.GetSumOfWeights()
            lumi = eraLumi[era]
            self.norm = xsec*lumi/sumw
        print('sample >>> ',self.sampleName,self.norm,self.additionalCut)

    def CreateHisto(self,var,weight,cut,bins,name):

        nbins = len(bins)-1
        histname = self.sampleName+"_"+name
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
        self.WP_index = tauIntWPs[WP]
        self.tauNuCuts = tauNuCuts

    def CreateHistosTauNu(self,var,bins,selection):

        print("Running over",self.sampleName)
        tree = self.sampleFile.Get("tree")

        # initialization
        nbins = len(bins)-1
        wp_index = self.WP_index
        cuts = self.tauNuCuts
        fakeFactor = self.fakeFactorHighPt

        dmlow = 0
        dmhigh = 1

        if cuts.dm=='2prong':
            dmlow = 5
            dmhigh = 6

        if cuts.dm=='3prong':
            dmlow = 10
            dmhigh = 11

        # creating histograms 
        hists = {}
        for label in histLabels:
            name = self.sampleName + selection + label
            hists[name] = ROOT.TH1D(name,"",nbins,array('d',list(bins)))
        for label in histSysLabels:
            for uncLabel in statUncLabels:
                name = self.sampleName + selection + label + uncLabel
                hists[name] = ROOT.TH1D(name,"",nbins,array('d',list(bins)))

        # floats
        weight        = np.zeros(1,dtype='f')
        pt_1          = np.zeros(1,dtype='f')
        eta_1         = np.zeros(1,dtype='f')
        metdphi_1     = np.zeros(1,dtype='f')
        metdphi_jet_1 = np.zeros(1,dtype='f')
        mt_1          = np.zeros(1,dtype='f')
        mt_jet_1      = np.zeros(1,dtype='f')
        met           = np.zeros(1,dtype='f')
        jpt_ratio_1   = np.zeros(1,dtype='f')
        jpt_match_1   = np.zeros(1,dtype='f')
        jeta_match_1  = np.zeros(1,dtype='f')
        m_1           = np.zeros(1,dtype='f')

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
        idDeepTau2017v2p1VSe_1   = np.zeros(1,dtype='i')
        idDeepTau2017v2p1VSmu_1  = np.zeros(1,dtype='i')
        idDeepTau2017v2p1VSjet_1 = np.zeros(1,dtype='i')
        genmatch_1               = np.zeros(1,dtype='i')
        dm_1                     = np.zeros(1,dtype='i')

        # branches -> 
        # floats 
        tree.SetBranchAddress('met',met)
        tree.SetBranchAddress('metdphi_1',metdphi_1)
        tree.SetBranchAddress('metdphi_jet_1',metdphi_jet_1)
        tree.SetBranchAddress('mt_1',mt_1)
        tree.SetBranchAddress('mt_jet_1',mt_jet_1)
        tree.SetBranchAddress('pt_1',pt_1)
        tree.SetBranchAddress('m_1',m_1)
        tree.SetBranchAddress('weight',weight)
        tree.SetBranchAddress('eta_1',eta_1)
        tree.SetBranchAddress('jpt_ratio_1',jpt_ratio_1)
        tree.SetBranchAddress('jeta_match_1',jeta_match_1)
        tree.SetBranchAddress('jpt_match_1',jpt_match_1)

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
        tree.SetBranchAddress('idDeepTau2017v2p1VSe_1',idDeepTau2017v2p1VSe_1)
        tree.SetBranchAddress('idDeepTau2017v2p1VSmu_1',idDeepTau2017v2p1VSmu_1)
        tree.SetBranchAddress('idDeepTau2017v2p1VSjet_1',idDeepTau2017v2p1VSjet_1)
        tree.SetBranchAddress('dm_1',dm_1)
        if not self.isdata: tree.SetBranchAddress("genmatch_1",genmatch_1)

        nentries = tree.GetEntries()

        # run over entries
        for entry in range(0,nentries):
            tree.GetEntry(entry)

            # mc selection
            lepFake = genmatch_1[0]>=1 and genmatch_1[0]<=4
            genuineTau = genmatch_1[0]==5
            jetFake = genmatch_1[0]==0
            
            if not self.isdata:
                if selection=='_tau' and not genuineTau: continue # genuine taus
                if selection=='_fake' and not jetFake: continue # jet->tau fakes
                if selection=="_lfakes" and not lepFake: continue # l->tau fakes
                if selection=='_notFake' and genmatch_1[0]==0: continue # not jet->tau fakes

            # met filters, trigger, vetos
            if not metfilter[0]: continue
            if not mettrigger[0]: continue
            if extraelec_veto[0]: continue
            if extramuon_veto[0]: continue
            if extratau_veto[0]: continue
            if njets[0]!=0: continue

            dmcut = dm_1[0]==dmlow or dm_1[0]==dmhigh
            if not dmcut: continue

            # kinematic cuts
            if jpt_match_1[0]<cuts.ptJetLowerCut: continue
            if jpt_match_1[0]>cuts.ptJetUpperCut: continue
            if pt_1[0]<cuts.ptLowerCut: continue
            if pt_1[0]>cuts.ptUpperCut: continue
            if math.fabs(jeta_match_1[0])>cuts.etaJetCut: continue
            if math.fabs(eta_1[0])>cuts.etaCut: continue
            if metdphi_jet_1[0]<cuts.metdphiCut: continue
            if met[0]<cuts.metCut: continue

            # tau discriminator against e and mu and jet
            if idDeepTau2017v2p1VSe_1[0]<cuts.antiE: continue
            if idDeepTau2017v2p1VSmu_1[0]<cuts.antiMu: continue
            if idDeepTau2017v2p1VSjet_1[0]<1: continue

            variable = mt_1[0]

            if var=='mt_1': variable = mt_1[0]
            if var=='mt_jet_1': variable = mt_jet_1[0]
            if var=='jpt_match_1': variable = jpt_match_1[0]
            if var=='pt_1': variable = pt_1[0]
            if var=='jeta_match_1': variable = jeta_match_1[0]
            if var=='eta_1': variable = eta_1[0]
            if var=='met': variable = met[0]
            if var=='jpt_ratio_1': variable = jpt_ratio_1[0]
            if var=='m_1': variable = m_1[0]

            # signal region
            if idDeepTau2017v2p1VSjet_1[0]>=wp_index:
                name = self.sampleName + selection
                hists[name].Fill(variable,weight[0])

            # Sideband region (VVVLoose)
            if idDeepTau2017v2p1VSjet_1[0]<2:
                name = self.sampleName + selection + "_SB"
                hists[name].Fill(variable,weight[0])
                
                # find label
                refLabel = extractBinLabels(jpt_match_1[0])

                # applying FF and systematics
                for label in ['mc_wjets','data_wjets','data_dijets']:
                    weightFF,errorFF = fakeFactor.getWeight(pt_1[0],dm_1[0],label)
                    name = self.sampleName + selection + '_' + label
                    hists[name].Fill(variable,weight[0]*weightFF)
                    for uncLabel in statUncLabels:
                        currentLabel = uncLabel
                        name = self.sampleName + selection + "_" + label + currentLabel
                        if currentLabel==refLabel: 
                            hists[name].Fill(variable,weight[0]*(weightFF+errorFF))
                        else:
                            hists[name].Fill(variable,weight[0]*weightFF)

        for hist in hists:
            hists[hist].Scale(self.norm)

        return hists
