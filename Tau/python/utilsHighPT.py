import ROOT 
import math
from array import array
import numpy as np
import os

#############################
##### General settings ######
#############################

#########################
# folder for picotuples #
#########################
picoFolder = '/eos/user/r/rasp/output/HighPT_2023'
#picoFolder = '/eos/user/r/rasp/output/HighPT_2022'
#picoFolder='/eos/user/r/rasp/output/HighPT_deepTauV2p5'
#picoFolder='/eos/user/r/rasp/output/HighPT'

#######################
#    base folder      #
#######################
baseFolder = '/afs/cern.ch/work/r/rasp/HighPT_2023'

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
# folder for FF        #
########################
fakeFactorsFolder = baseFolder+'/FF'

#########################
# folder for MetTrigger #
#########################
metTriggerFolder = baseFolder+'/MetTrigger'

########################
# folder for datacards #
########################
datacardsFolder = baseFolder+'/datacards'

###################
# Cross sections  #
###################

sampleXSec_2016 = { 
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
    "Zto2Nu-4Jets_HT-100to200" : 304.5, # needs to be updated
    "Zto2Nu-4Jets_HT-200to400" : 91.82, # needs to be updated
    "Zto2Nu-4Jets_HT-400to800" : 16.37, # needs to be updated
    "Zto2Nu-4Jets_HT-800to1500" : 1.84, # needs to be updated
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
    "WtoNuTau" : 7.869,
}

sampleXSec_2023 = {
    "DYto2L-4Jets_MLL-50" : 5455.0*kfactor_dy,
    "DYto2L-4Jets_MLL-50_1J" : 978.3*kfactor_dy,
    "DYto2L-4Jets_MLL-50_2J" : 315.1*kfactor_dy,
    "DYto2L-4Jets_MLL-50_3J" : 93.7*kfactor_dy,
    "DYto2L-4Jets_MLL-50_4J" : 45.4*kfactor_dy,
    "WtoLNu-4Jets" : 55300.*kfactor_wj,
    "WtoLNu-4Jets_1J" : 9128.*kfactor_wj,
    "WtoLNu-4Jets_2J" : 2922.*kfactor_wj,
    "WtoLNu-4Jets_3J" : 861.3*kfactor_wj,
    "WtoLNu-4Jets_4J" : 415.4*kfactor_wj,
    "WtoLNu_HT100to400" : 1640.0*kfactor_wj, # 2167.04 
    "WtoLNu_HT400to800" : 60.32*kfactor_wj, # 84.20
    "Zto2Nu-4Jets_HT-100to200" : 304.5, # needs to be updated
    "Zto2Nu-4Jets_HT-200to400" : 91.82, # needs to be updated
    "Zto2Nu-4Jets_HT-400to800" : 16.37, # needs to be updated
    "Zto2Nu-4Jets_HT-800to1500" : 1.84, # needs to be updated
    "TTto2L2Nu" : 80.9*kfactor_ttbar, 
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
    "WtoNuTau" : 7.869,
}

eraRun = {
    "UL2016_preVFP"  : "Run2",
    "UL2016_postVFP" : "Run2",
    "UL2017"         : "Run2",
    "UL2018"         : "Run2",
    "2022"           : "2022",
    "2022_postEE"    : "2022",
    "2023C"          : "2023",
    "2023D"          : "2023"
}

periods = {
    "UL2016_preVFP" : ["UL2016_preVFP"],
    "UL2016_postVFP" : ["UL2016_postVFP"],
    "UL2016" : ["UL2016_preVFP","UL2016_postVFP"],
    "UL2017" : ["UL2017"],
    "UL2018" : ["UL2018"],
    "2022"   : ["2022","2022_postEE"],
    "2022_preEE"   : ["2022"],
    "2022_postEE"  : ["2022_postEE"],
    "2023C"  : ["2023C"],
    "2023D"  : ["2023D"],
    "2023"   : ["2023C","2023D"],
}

eraSamples = {
    "UL2016_postVFP" : sampleXSec_2016,
    "UL2016_preVFP" : sampleXSec_2016,
    "UL2017" : sampleXSec_2017,
    "UL2018" : sampleXSec_2018,
    "2022"   : sampleXSec_2022,
    "2022_preEE"  : sampleXSec_2022,
    "2022_postEE" : sampleXSec_2022,
    "2023C" : sampleXSec_2023,
    "2023D" : sampleXSec_2023,
} 

eraLumi = {
    "UL2016" : 36300,
    "UL2016_postVFP" : 16800,
    "UL2016_preVFP"  : 19500,
    "UL2017" : 41480,    
    "UL2018" : 59830,
    "2022" : 8077,
    "2022_postEE" : 27007,
    "2023C" : 17650,
    "2023D" : 9451
}

################
# Data samples #
################

singlemu_2023D = ['Muon_Run2023D']
singlemu_2023C = ['Muon_Run2023C']
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

met_2023D = ['JetMet_Run2023D']
met_2023C = ['JetMet_Run2023C']
met_2022_postEE = ['JetMet_Run2022E','JetMet_Run2022F','JetMet_Run2022G']
met_2022 = ['JetMet_Run2022C','JetMet_Run2022D']
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
    "2022_postEE" : singlemu_2022_postEE,
    "2023C" : singlemu_2023C,
    "2023D" : singlemu_2023D
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
    "UL2018": met_2018,
    "2022"  : met_2022,
    "2022_postEE" : met_2022_postEE,
    "2023C" : met_2023C,
    "2023D" : met_2023D
}


MCPartons0 = ['WJetsToLNu-4Jets','WtoLNu-4Jets']

MCLowHT = [
    'WJetsToLNu',
    'WJetsToLNu-4Jets',
    'WJetsToLNu-4Jets_1J',
    'WJetsToLNu-4Jets_2J',
    'WJetsToLNu-4Jets_3J',
    'WJetsToLNu-4Jets_4J',
    'WtoLNu-4Jets',
    'WtoLNu-4Jets_1J',
    'WtoLNu-4Jets_2J',
    'WtoLNu-4Jets_3J',
    'WtoLNu-4Jets_4J',
]


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
unc_jme = ['JES','JER','Unclustered']

###############################
# Shape uncertainties (taues) #
###############################
unc_taues = ['taues_1pr','taues_1pr1pi0','taues_3pr','taues_3pr1pi0'] 

###############################
# Shape uncertainties (all)   #
###############################
uncs = ['JES','JER','Unclustered','taues_1pr','taues_1pr1pi0','taues_3pr','taues_3pr1pi0']

##################################
### Settings for FF measurements #
##################################

xbinsPt = { 
    'pt_2' : [100, 125, 150, 175, 200, 2000],
    'jpt_match_2' : [100, 125, 150, 200, 300, 2000]
}

xbinsPtTrig = { 
    'pt_2' : [100, 200, 2000],
    'jpt_match_2' : [100, 300, 2000]
}

variableLabel = {
    'pttau' : 'pt_2',
    'ptjet' : 'jpt_match_2',
    'mtau'  : 'm_2'
}

ptUncThreshold = {
    'pttau' : 200.0, # split pt region for FF stat. uncertainties (<200, >=200.)
    'ptjet' : 300.0 # split jet pt region for FF stat. uncertainties (<200, >=200.)
}

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
    'incl'     : [0.0,0.2,0.4,0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8], 
    '1prong'   : [0, 1.],
    '1prongPi0': [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8],
    '3prong'   : [0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
    '3prongPi0': [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
}

# histogram labels (W*->tau+v selection)
regionLabels = ['SR','SB']
sampleLabels = ['data_wjets','mc_wjets']
trigLabels = ['trig','notrig']
selLabels = ['all','fake','notFake','lepFake','tau']

XTitle = {
    'mt_1'  : "m_{T} (GeV)",
    'pt_1'  : "tau p_{T} (GeV)",
    'pt_2'  : "tau p_{T} (GeV)",
    'jpt_match_1' : "jet p_{T} (GeV)",
    'jpt_match_2' : "jet p_{T} (GeV)",
    'eta_1' : "#eta",
    'met'   : "E_{T}^{mis} (GeV)",
    'm_1'   : "tau mass (GeV)",
    'm_2'   : "tau mass (GeV)",
}

def makeBaseName(var,wp,wpVsMu,wpVsE,era):
    basename = '%s_%sVsJet_%sVsMu_%sVsE_%s'%(var,wp,wpVsMu,wpVsE,era)
    return basename

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

