import ROOT 
import math
from array import array
import numpy as np

#############################
##### General settings ######
#############################

#########################
# folder for picotuples #
#########################
picoFolder = '/eos/user/r/rasp/output/HighPT_2022'
#picoFolder='/eos/user/r/rasp/output/HighPT_deepTauV2p5'
#picoFolder='/eos/user/r/rasp/output/HighPT'

#######################
#    base folder      #
#######################
baseFolder = '/afs/cern.ch/work/r/rasp/HighPT_2022'

#######################
# folders for figures #
#######################
figuresFolder = baseFolder+'/figures'
figuresFolderFF = figuresFolder+'/FF'
figuresFolderMetTrigger = figuresFolder+'/MetTrigger'
figuresFolderSys = figuresFolder+'/Sys'
figuresFolderWMuNu = figuresFolder+'/WMuNu'
figuresFolderWTauNu = figuresFolder+'/WTauNu'
figuresFolderPT = figuresFolder+'/PT'

########################
# folder for datacards #
########################
fakeFactorsFolder = baseFolder+'/FF'

########################
# folder for datacards #
########################
datacardsFolder = baseFolder+'/datacards'

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
    "WToMuNu_M-200" : 6.850,
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
    "WToMuNu_M-200" : 6.850,
    "WToTauNu_M-200" : 7.246
}

kfactor_dy=6282.6/5455.0 # LO->NNLO+NLO_EW k-factor computed for 13.6 TeV
kfactor_wj=63425.1/55300 # LO->NNLO+NLO_EW k-factor computed for 13.6 TeV
kfactor_ttbar=923.6/762.1 # NLO->NNLO k-factor computed for 13.6 TeV
kfactor_ww=1.524 # LO->NNLO+NLO_EW computed for 13.6 TeV
kfactor_zz=1.524 # LO->NNLO+NLO_EW computed for 13.6 TeV
kfactor_wz=1.414 # LO->NNLO+NLO_EW computed for 13.6 TeV 

sampleXSec_2022 = {
    "DYto2L-4Jets_MLL-50" : 5455.0*kfactor_dy,
    "DYto2L-4Jets_MLL-50_1J" : 978.3*kfactor_dy,
    "DYto2L-4Jets_MLL-50_2J" : 315.1*kfactor_dy,
    "DYto2L-4Jets_MLL-50_3J" : 93.7*kfactor_dy,
    "DYto2L-4Jets_MLL-50_4J" : 45.4*kfactor_dy,
    "WJetsToLNu-4Jets" : 55300.*kfactor_wj,
    "WJetsToLNu-4Jets_1J" : 9128.*kfactor_wj,
    "WJetsToLNu-4Jets_2J" : 2922.*kfactor_wj,
    "WJetsToLNu-4Jets_3J" : 861.3*kfactor_wj,
    "WJetsToLNu-4Jets_4J" : 415.4*kfactor_wj,
    "WtoLNu-4Jets_HT-100to400" : 1640.0*kfactor_wj, # 2167.04 
    "WtoLNu-4Jets_HT-400to800" : 60.32*kfactor_wj, # 84.20
    "TTTo2L2Nu" : 80.9*kfactor_ttbar, 
    "TTto4Q" : 346.4*kfactor_ttbar, 
    "TTtoLNu2Q" : 334.8*kfactor_ttbar,
    "TBbarQ_t-channel" : 123.8, 
    "TbarBQ_t-channel" : 75.47, 
    "TWminustoLNu2Q" : 15.8,
    "TWminusto2L2Nu" : 3.8, 
    "TbarWplustoLNu2Q" : 15.9, 
    "TbarWplusto2L2Nu" : 3.8,
    "WW" : 80.23*kfactor_ww,
    "WZ" : 29.1*kfactor_wz,
    "ZZ" : 12.75*kfactor_zz,
    "WtoMuNu" : 7.206,
    "WtoNuTau" : 7.469,
}

eraRun = {
    "UL2016_preVFP"  : "Run2",
    "UL2016_postVFP" : "Run2",
    "UL2017"         : "Run2",
    "UL2018"         : "Run2",
    "2022"           : "Run3",
    "2022_postEE"    : "Run3"
}

periods = {
    "UL2016_preVFP" : ["UL2016_preVFP"],
    "UL2016_postVFP" : ["UL2016_postVFP"],
    "UL2016" : ["UL2016_preVFP","UL2016_postVFP"],
    "UL2017" : ["UL2017"],
    "UL2018" : ["UL2018"],
    "2022"   : ["2022","2022_postEE"]    
}

eraSamples = {
    "UL2016_postVFP" : sampleXSec_2016_postVFP,
    "UL2016_preVFP" : sampleXSec_2016_preVFP,
    "UL2017" : sampleXSec_2017,    
    "UL2018" : sampleXSec_2018,
    "2022"   : sampleXSec_2022,
    "2022_postEE" : sampleXSec_2022
} 

eraLumi = {
    "UL2016" : 36300,
    "UL2016_postVFP" : 16800,
    "UL2016_preVFP"  : 19500,
    "UL2017" : 41480,    
    "UL2018" : 59830,
    "2022" : 8077,
    "2022_postEE" : 27007
}

################
# Data samples #
################

singlemu_2022_postEE = ['Muon_Run2022E','Muon_Run2022F','Muon_Run2022G']
singlemu_2022 = ['SingleMuon_Run2022C','Muon_Run2022C','Muon_Run2022D']
singlemu_2018 = ['SingleMuon_Run2018A','SingleMuon_Run2018B','SingleMuon_Run2018C','SingleMuon_Run2018D']
singlemu_2017 = ['SingleMuon_Run2017B','SingleMuon_Run2017C','SingleMuon_Run2017D','SingleMuon_Run2017E','SingleMuon_Run2017F']
singlemu_2016_preVFP = ['SingleMuon_Run2016B','SingleMuon_Run2016C','SingleMuon_Run2016D','SingleMuon_Run2016E','SingleMuon_Run2016F']
singlemu_2016_postVFP = ['SingleMuon_Run2016F','SingleMuon_Run2016G','SingleMuon_Run2016H']


jetht_2018 = ['JetHT_Run2018A','JetHT_Run2018B','JetHT_Run2018C','JetHT_Run2018D']
jetht_2017 = ['JetHT_Run2017B','JetHT_Run2017C','JetHT_Run2017D','JetHT_Run2017E','JetHT_Run2017F']
jetht_2016_preVFP = ['JetHT_Run2016B','JetHT_Run2016C','JetHT_Run2016D','JetHT_Run2016E','JetHT_Run2016F']
jetht_2016_postVFP = ['JetHT_Run2016F','JetHT_Run2016G','JetHT_Run2016H']

met_2022_postEE = ['JetMet_2022E','JetMet_2022F','JetMet_2022G']
met_2022 = ['JetMet_2022C','JetMet2022D']
met_2018 = ['MET_Run2018A','MET_Run2018B','MET_Run2018C','MET_Run2018D']
met_2017 = ['MET_Run2017B','MET_Run2017C','MET_Run2017D','MET_Run2017E','MET_Run2017F']
met_2016_preVFP = ['MET_Run2016B','MET_Run2016C','MET_Run2016D','MET_Run2016E','MET_Run2016F']
met_2016_postVFP = ['MET_Run2016F','MET_Run2016G','MET_Run2016H']

singlemu = {
    "UL2016_preVFP": singlemu_2016_preVFP,
    "UL2016_postVFP": singlemu_2016_postVFP,
    "UL2017": singlemu_2017,
    "UL2018": singlemu_2018,
    "2022" : singlemu_2022,
    "2022_postEE" : singlemu_2022_postEE
}

jetht = {
    "UL2016_preVFP": jetht_2016_preVFP,
    "UL2016_postVFP": jetht_2016_postVFP,
    "UL2017": jetht_2017,
    "UL2018": jetht_2018
}

MCPartons0 = ['WJetsToLNu-4Jets']
MCLowHT = [
    'WJetsToLNu',
    'WJetsToLNu-4Jets',
    'WJetsToLNu-4Jets_1J',
    'WJetsToLNu-4Jets_2J',
    'WJetsToLNu-4Jets_3J',
    'WJetsToLNu-4Jets_4J'
]


met = {
    "UL2016_preVFP": met_2016_preVFP,
    "UL2016_postVFP": met_2016_postVFP,
    "UL2017": met_2017,
    "UL2018": met_2018,
    "2022"  : met_2022,
    "2022_postEE" : met_2022_postEE
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
    'Loose': "4",
    'Medium': "5",
    'Tight': "6",
    'VTight': "7",
    'VVTight': "8"
}

tauIntWPs = {
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
xbinsPt_2016 =   [100, 125, 200, 2000]
ptUncThreshold = 200. # split pt region for stat. uncertainties (<200, >=200.)

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

decayModeCuts = {
    '1prong'    : 'dm_2==0',
    '1prongPi0' : '(dm_2==1||dm_2==2)',
    '3prong'    : 'dm_2==10',
    '3prongPi0' : 'dm_2==11'
}

decayProngCuts = {
    '1prong' : '(dm_2==0||dm_2==1||dm_2==2)',
    '2prong' : '(dm_2==5||dm_2==6)',
    '3prong' : '(dm_2==10||dm_2==11)'
}

xbinsMass = {
    '1prongPi0': [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8],
    '3prong'   : [0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
    '3prongPi0': [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
}

# histogram labels (W*->tau+v selection)
histLabels = ['','_SB','_mc_wjets','_data_wjets','_data_dijets']
trigLabels = ['_trig','_nottrig']
histSysLabels = ['_mc_wjets','_data_wjets','_data_dijets']
ptratioLabels = ['_ptratioLow','_ptratioHigh']
statUncLabels = ['_unc1','_unc2']

XTitle = {
    'mt_1'  : "m_{T} (GeV)",
    'pt_1'  : "p_{T} (GeV)",
    'eta_1' : "#eta",
    'met'   : "E_{T}^{mis} (GeV)",
    'm_1'   : "tau mass (GeV)",
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

def extractBinLabels(pt,ptratio):
    ratLabel = '_ptratioLow'
    #    if ptratio>=ptratioThresholds[0] and ptratio<ptratioThresholds[1]: ratLabel = '_ptratioMedium'
    #    if ptratio>=ptratioThresholds[1]: ratLabel = '_ptratioHigh'
    if ptratio>=ptratioThreshold: ratLabel = '_ptratioHigh'
    uncLabel = '_unc1'
    if pt>ptUncThreshold: uncLabel = '_unc2'
    return ratLabel, uncLabel

# Run over set of samples and create histogram
def RunSamples(samples,var,weight,cut,xbins,name):
    print
    print("Running",name,var,weight,cut)
    nbins = len(xbins)-1
    hist = ROOT.TH1D(name,"",nbins,array('d',list(xbins)))
    for sampleName in samples:
        sample = samples[sampleName]
        histsample = sample.CreateHisto(var,weight,cut,xbins,name)
        hist.Add(hist,histsample,1.,1.)
    return hist

# Run over set of samples and create histograms for W*->tau+v channel
# for each sample loop over Tree entries is performed
def RunSamplesTauNu(samples,var,unc,xbins,selection,name):
    print
    print("Running",name,var,unc,selection)
    nbins = len(xbins)-1
    hists = {} # discionary of histograms
    for label in histLabels:
        histname = name + selection + unc + label
        hists[histname] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
        for trigLabel in trigLabels:
            histname = name + selection + unc + label + trigLabel
            hists[histname] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
    for label in histSysLabels:
        for ptratioLabel in ptratioLabels:
            for uncLabel in statUncLabels:
                histname = name + selection + unc + label + ptratioLabel + uncLabel
                hists[histname] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))
                for trigLabel in trigLabels:
                    histname = name + selection + unc + label + ptratioLabel + uncLabel + trigLabel
                    hists[histname] = ROOT.TH1D(histname,"",nbins,array('d',list(xbins)))

    for sampleName in samples:        
        sample = samples[sampleName]
        histsample = sample.CreateHistosTauNu(var,unc,xbins,selection)
        
        for label in histLabels:
            histname = name + selection + unc + label
            histsamplename = sample.sampleName + selection + unc + label
            hists[histname].Add(hists[histname],histsample[histsamplename],1.,1.)
            for trigLabel in trigLabels:
                histname = name + selection + unc + label + trigLabel
                histsamplename = sample.sampleName + selection + unc + label + trigLabel
                hists[histname].Add(hists[histname],histsample[histsamplename],1.,1.)
        for label in histSysLabels:
            for ptratioLabel in ptratioLabels:
                for uncLabel in statUncLabels:
                    histname = name + selection + unc + label + ptratioLabel + uncLabel
                    histsamplename = sample.sampleName + selection + unc + label + ptratioLabel + uncLabel
                    hists[histname].Add(hists[histname],histsample[histsamplename],1.,1.)
                    for trigLabel in trigLabels:
                        histname = name + selection + unc + label + ptratioLabel + uncLabel + trigLabel
                        histsamplename = sample.sampleName + selection + unc + label + ptratioLabel + uncLabel + trigLabel
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
        self.metCut = kwargs.get('metCut',120.)
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

class FakeFactorHighPt:

    def __init__(self,filename):
        print
        print('Loading fake factors from file',filename," >>>>>")
        self.fileName = filename
        self.fileFF = ROOT.TFile(self.fileName,"READ")
        self.hists = {}
        self.trigbins = ['','_trig','_nottrig']
        self.labels = ['dijets','wjets']
        #self.ptbins = ['ptratioLow','ptratioMedium','ptratioHigh']
        self.ptbins = ['ptratioLow','ptratioHigh']
        for ptbin in self.ptbins:
            for trigbin in self.trigbins:
                for label in self.labels:                
                    name = 'data_' + label + "_" + ptbin + trigbin
                    self.hists[name] = self.fileFF.Get(name)
                    print(name,self.hists[name])
                name = 'mc_wjets_' + ptbin + trigbin
                self.hists[name] = self.fileFF.Get(name)
                print(name,self.hists[name])

    def getWeight(self,pttau,ptratio,label,triglabel):
        ptlabel = 'ptratioLow'
        if ptratio>=ptratioThreshold: ptlabel = 'ptratioHigh'
        name = label + "_" + ptlabel + triglabel
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
        self.sampleName = samplename + "_" + era
        self.sampleFile = ROOT.TFile(filename,"READ")
        if self.sampleFile.IsZombie():
            print("")
            print('File %s is not found '%(filename))
            print('for specified era : %s'%(era))
            print('check if variable "PicoFolder" in file utilsHighPT.py is correctly set')
            print('it is currently set to %s'%(picoFolder))
            print('or check naming of samples')
            print("")
            exit()
        #self.sampleTree = self.sampleFile.Get("tree")
        self.norm = 1.0
        self.isdata = isdata
        if isdata:
            self.norm = 1.0
        else:
            xsecSamples = eraSamples[era]
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
            lumi = eraLumi[era]
            self.norm = xsec*lumi/sumw
        
        print('%s : %s : norm = %7.3f : %s'%(era,samplename,self.norm,self.additionalCut))

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
        self.WP_index = tauIntWPs[WP]
        self.tauNuCuts = tauNuCuts

    def CreateHistosTauNu(self,var,unc,bins,selection):

        print("Running over",self.sampleName)
        tree = self.sampleFile.Get("tree")

        # initialization
        nbins = len(bins)-1
        wp_index = self.WP_index
        cuts = self.tauNuCuts
        fakeFactor = self.fakeFactorHighPt

        # creating histograms 
        hists = {}
        for label in histLabels:
            name = self.sampleName + selection + unc + label
            hists[name] = ROOT.TH1D(name,"",nbins,array('d',list(bins)))
            for trigbin in trigLabels:
                nametrig = self.sampleName + selection + unc + label + trigbin
                hists[nametrig] = ROOT.TH1D(nametrig,"",nbins,array('d',list(bins)))
        for label in histSysLabels:
            for ptratioLabel in ptratioLabels:
                for uncLabel in statUncLabels:
                    name = self.sampleName + selection + unc + label + ptratioLabel + uncLabel
                    hists[name] = ROOT.TH1D(name,"",nbins,array('d',list(bins)))
                    for trigbin in trigLabels:
                        nametrig = self.sampleName + selection + unc + label + ptratioLabel + uncLabel + trigbin
                        hists[nametrig] = ROOT.TH1D(nametrig,"",nbins,array('d',list(bins)))
        # floats
        weight      = np.zeros(1,dtype='f')
        pt_1        = np.zeros(1,dtype='f')
        eta_1       = np.zeros(1,dtype='f')
        metdphi_1   = np.zeros(1,dtype='f')
        mt_1        = np.zeros(1,dtype='f')
        met         = np.zeros(1,dtype='f')
        jpt_ratio_1 = np.zeros(1,dtype='f')
        jpt_match_1 = np.zeros(1,dtype='f')
        m_1         = np.zeros(1,dtype='f')

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

        # branches -> 
        # floats 
        tree.SetBranchAddress('met',met)
        tree.SetBranchAddress('metdphi_1',metdphi_1)
        tree.SetBranchAddress('mt_1',mt_1)
        tree.SetBranchAddress('pt_1',pt_1)
        tree.SetBranchAddress('m_1',m_1)
        tree.SetBranchAddress('weight',weight)
        tree.SetBranchAddress('eta_1',eta_1)
        tree.SetBranchAddress('jpt_ratio_1',jpt_ratio_1)
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
        tree.SetBranchAddress('idDeepTau2018v2p5VSe_1',idDeepTau2018v2p5VSe_1)
        tree.SetBranchAddress('idDeepTau2018v2p5VSmu_1',idDeepTau2018v2p5VSmu_1)
        tree.SetBranchAddress('idDeepTau2018v2p5VSjet_1',idDeepTau2018v2p5VSjet_1)
        if not self.isdata: tree.SetBranchAddress("genmatch_1",genmatch_1)

        nentries = tree.GetEntries()

        # run over entries
        for entry in range(0,nentries):
            tree.GetEntry(entry)

            # mc selection
            lepFake = genmatch_1[0]==1 or genmatch_1[0]==2 or genmatch_1[0]==3 or genmatch_1[0]==4
            genuineTau = genmatch_1[0]==5
            jetFake = genmatch_1[0]==0
            
            if not self.isdata:
                if selection=='_tau' and not genuineTau: continue # genuine taus
                if selection=='_fake' and not jetFake: continue # jet->tau fakes
                if selection=="_lfake" and not lfake: continue # l->tau fakes
                if selection=='_notFake' and genmatch_1[0]==0: continue # not jet->tau fakes

            # met filters, trigger, vetos
            if not metfilter[0]: continue
            if not mettrigger[0]: continue
            if extraelec_veto[0]: continue
            if extramuon_veto[0]: continue
            if extratau_veto[0]: continue
            if njets[0]!=0: continue

            # kinematic cuts
            if pt_1[0]<cuts.ptLowerCut: continue
            if pt_1[0]>cuts.ptUpperCut: continue
            if math.fabs(eta_1[0])>cuts.etaCut: continue
            if mt_1[0]<cuts.mtLowerCut: continue
            if mt_1[0]>cuts.mtUpperCut: continue
            if metdphi_1[0]<cuts.metdphiCut: continue
            if met[0]<cuts.metCut: continue

            # tau discriminator against e and mu and jet
            if idDeepTau2018v2p5VSe_1[0]<cuts.antiE: continue
            if idDeepTau2018v2p5VSmu_1[0]<cuts.antiMu: continue
            if idDeepTau2018v2p5VSjet_1[0]<1: continue

            variable = mt_1[0]
            if var=='pt_1': variable = pt_1[0]
            if var=='eta_1': variable = eta_1[0]
            if var=='met': variable = met[0]
            if var=='m_1': variable = m_1[0]

            tautrigger = tautrigger1[0] or tautrigger2[0]
            triglabel = '_nottrig'
            if tautrigger: triglabel = '_trig'

            # signal region
            if idDeepTau2018v2p5VSjet_1[0]>=wp_index:
                name = self.sampleName + selection + unc
                nametrig = self.sampleName + selection + triglabel
                hists[name].Fill(variable,weight[0])
                hists[nametrig].Fill(variable,weight[0])

            # Sideband region (VVVLoose and not Loose)
            if idDeepTau2018v2p5VSjet_1[0]<4:
                name = self.sampleName + selection + unc + "_SB"
                nametrig = self.sampleName + selection + unc + "_SB" + triglabel
                hists[name].Fill(variable,weight[0])
                hists[nametrig].Fill(variable,weight[0])
                
                # find label
                refRatioLabel, refUncLabel = extractBinLabels(pt_1[0],jpt_ratio_1[0])
                refLabel = refRatioLabel+refUncLabel

                # applying FF and systematics
                for label in ['mc_wjets','data_wjets','data_dijets']:
                    weightFF,errorFF = fakeFactor.getWeight(pt_1[0],jpt_ratio_1[0],label,'')
                    weightFFtrig,errorFFtrig = fakeFactor.getWeight(pt_1[0],jpt_ratio_1[0],label,triglabel)
                    name = self.sampleName + selection + unc + '_' + label
                    hists[name].Fill(variable,weight[0]*weightFF)
                    nametrig = self.sampleName + selection + unc + "_" + label + triglabel
                    hists[nametrig].Fill(variable,weight[0]*weightFFtrig)
                    for ptratioLabel in ptratioLabels:
                        for uncLabel in statUncLabels:
                            currentLabel = ptratioLabel+uncLabel
                            name = self.sampleName + selection + unc + "_" + label + currentLabel
                            nametrig = self.sampleName + selection + unc + "_" + label + currentLabel + triglabel
                            if currentLabel==refLabel: 
                                hists[name].Fill(variable,weight[0]*(weightFF+errorFF))
                                hists[nametrig].Fill(variable,weight[0]*(weightFFtrig+errorFFtrig))
                            else:
                                hists[name].Fill(variable,weight[0]*weightFF)
                                hists[nametrig].Fill(variable,weight[0]*weightFFtrig)

        for hist in hists:
            hists[hist].Scale(self.norm)

        return hists
