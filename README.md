# Thin-jet ID SF measurements

## Installation

The measurement will require [Higgs combination package](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git) and [python analysis code](https://github.com/raspereza/HighPT.git) 

Installation proceeds as follows:
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_13
cd CMSSW_10_6_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git checkout v8.2.0
cd ../..
git clone https://github.com/raspereza/HighPT.git HighPT
scramv1 b -j 4
```

After installation is complete change to the directory [`$CMSSW_BASE/src/HighPT/ThinJet`](https://github.com/raspereza/HighPT/tree/main/ThinJet) and run the script:

```
cd $CMSSW_BASE/src/HighPT/ThinJet
./setup.sh
```

This will create in the current directory several subfolders where outputs of the code will be stored:
1. `output/figures` - plots (png files) of data and simulated distributions used in the measurement;
2. `output/figures/FF` - plots of measured fake factors  
3. `output/FF` - root files with fake factors for building fake background model
4. `output/datacards` - datacards used to measure thin jet ID scale factors with [Higgs combination package](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git) 

All scripts at every step of the measurement will be run from the directory [`$CMSSW_BASE/src/HighPT/ThinJet`](https://github.com/raspereza/HighPT/tree/main/ThinJet)


## Measurement strategy

Analysis uses tau leptons as proxy for thin-jets. The data/simulation scale factors for thin-jet identification 
are extracted from two selected samples: 

1. measurement sample `W*->tau+v`
2. sideband sample `W*->mu+v`

The measurement is done by performing simultaneous fit in two regions. The fitted distributions are

1. transverse mass of muon and missing pT in the `W*->mu+v` sideband, and
2. transverse mass of proxy-tau and missing pT in the `W*->tau+v` region.

The fit is performed with two unconstrained rate parameters. One of them accounts for cross section
of highly virtual W production. The analysis probes specific phase space with mass of W* greater than about 300 GeV.
This rate parameter scales both W*->mu+v and W*->tau+v simulated templates. Second parameter is the measured thin-jet ID scale factor. It is apllied to W*->tau+v template and all other smulated processes with genuine selected tau lepton. The measurement is performed individually for 1-prong, 2-prong and 3-prong type of thin-jets.

We recommend to identify thin-jets as taus passing either VVLoose or VLoose WP against jets.
Option with the Loose WP is also interesting can be potentially investigated.

Selection the sideband `W*->mu+v` region:
* exactly one mediumID,
* muon kinematics : pT>140 GeV and |eta|<2.4,
* missing ET > 150 GeV,
* transverse mass of muon and pTmiss > 300 GeV, 
* azimuthal angle between muon and pTmiss > 2.8 radian,
* additional leptons and jets are vetoed.

For the `W*->mu+v` region three templates are saved in datacards for statistical inference: 
1. observed data, 
2. W*->mu+v simulated sample,
3. sum of remaining simulated samples


Selection in the measurement `W*->mu+v` region 
* exactly one tau fulfilling minimal set of ID criteria imposed in NanoAOD
* additionally tau is required to predefined WP against jet and decay mode (1-prong, 2-prong or 3-prong)
* associated HPS jet : pT > 140 GeV, |eta| < 2.3 
* missing ET > 150 GeV
* transverse mass of muon and missing pT > 300 GeV
* azimuthal angle between muon and pTmiss > 2.8 radian,
* additional leptons and jets are vetoed.


For the `W*->tau+v` region five templates are saved in datacards for statistical inference:
1. observed data,
2. W*->tau+v simulated sample,
3. sum of remaining simulated samples with genuine selected tau lepton
4. sum of simulated samples with electron or muon faking tau
5. background with hadronic jet misidentified as tau lepton

While templates 2., 3. and 4. are obtained from simulation, template of background with jets faking taus
is constructed using data. The instrumental sample for that is the sample containing taus that pass
VVVLoose WP against jet, but fail VVLoose. Extrapolation weights are applied to events in this region 
(which we refer to as application region in the following) to predict jet->tau fake background in the 
measurement region. 
Extrapolation weights, also called fake factors) are defined as the ratio: 
```
FF = P(nominal ID)/P(VVVLoose and not VVLoose)
```
where 
1. `P(nominal ID)` is the probability for tau to pass nominal WP against jet (VVLoose or VLoose),
2. `P(VVVLoose and not VVLoose)` is the probability for tau to pass VVVLoose WP but fail VVLoose

The jet->tau fake background in the application region comprises mainly three types of events
1. `Z->vv+jets` (60%)
2. `W->lv+jets`, where l is not reconstructed or out of acceptance (30%)
3. `QCD multijets` (10%)

Given that the largest contributions to the jet->tau fake background come from single boson production
processes, it is reasonable to measure fake factors using as a standard candle Z+jets or W+jets samples. 
In our analysis `W->mu+v+jets` sample is employed for determination of fake factors.

The whole analysis is performed using PicoTuples located on lxplus machine in the folders 
* /eos/user/r/rasp/output/HighPT_thinjet/$ERA/taunu : used for selection of W*->tau+v events 
* /eos/user/r/rasp/output/HighPT_thinjet/$ERA/wjets : used for measuring fake factors with W*+jets sample
* /eos/user/r/rasp/output/HighPT_thinjet/$ERA/dijets : used for measuring fake factors with QCD events (not used in this analysis) 
* /eos/user/r/rasp/output/HighPT_deepTauV2p5/$ERA/munu : used for selection of W*->mu+v events

Apart from executable macros (which are described below), code includes also auxiliarly scripts:
* [HighPT/ThinJet/python/stylesHighPT.py](https://github.com/raspereza/HighPT/blob/main/ThinJet/python/stylesHighPT.py) defines of drawing ROOT styles,
* [HighPT/ThinJet/python/utilsThinJet.py](https://github.com/raspereza/HighPT/blob/main/ThinJet/python/utilsThinJet.py) defines configuration and helper classes : selectors, fake factor reader, processors of histograms, etc. 

## Determination of fake factors

Fake factors are measured in dependence of number of prongs (1-prong, 2-prong or 3-prong) and in dependence of 
HPS jet pT. Measurement is performed using script [HighPT/ThinJet/scripts/FakeFactorThinJet.py](https://github.com/raspereza/HighPT/blob/main/ThinJet/scripts/FakeFactorThinJet.py)
```
./scripts/FakeFactorThinJet.py --era $ERA --WP $WP
```
where 
* `$WP` is WP against jet (VVLoose or VLoose)
* `$ERA` is era (UL2016, UL2017, UL2018)
Example:
```
./scripts/FakeFactorThinJet.py --era UL2017 --WP VLoose
```
The script will measure in one go fake factors as a function of HPS jet pT for all three types of thin-jets (1-prong, 2-prong, 3-prong).
Three sets of fake factors are provided
1. measurements with the data `W->mu+v+(1jet)` sample,
2. measurements with simulted `W->mu+v+(1jet)` sample,
3. measurements with QCD di-jet events.
Set 3) is not used in subsequent steps of the measurement (it is kept for historical reasons).
Set 1) is used to construct jet->tau fake background in the measurement region.
Set 2) is used to perform MC closure test and derive non-closure uncertainty for the jet->tau fake background model. Three sets of fake factors are saved as histograms in RooT files 
```
output/FF/ff_${WP}VSjet_$ERA.root
``` 
There are in total nine histograms save in one RooT file : 3 measurement sets (data_wjets, mc_wjets, data_dijets) x 3 types of thin-jets (1-prong, 2-prong, 3-prong). Each histogram encodes dependence of fake factor on thin-jet pT. These RooT files are used later in the construction of the jet->fake background model in the selected W*->tau+v sample. The fake factors are plotted in files 
```
output/figures/FF/FF_$set_$prong_$WP_$ERA.png`
```
where
* `$set = data_wjets, data_dijets, mc_wjets` (measurement set),
* `$prong = 1-prong, 2-prong or 3-prong` (number of prongs),
* `$WP = VVLoose or VLoose` (WP against jet),
* `$ERA = UL2016, UL2017, UL2018`.

## Selection of W*->mu+v sample

Selection of events in the W*->mu+v sideband region is performed with the script [HighPT/ThinJet/scripts/DatacardsWToMuNu.py](https://github.com/raspereza/HighPT/blob/main/ThinJet/scripts/DatacardsWToMuNu.py). 
```
scripts/DatacardsWToMuNu.py --era $ERA
```
The script will construct templates of the transverse mass distribution of muon and pTmiss for 
1. observed data,
2. simulated W*->mu+v sample,
3. and remaining simulated samples. 

Plot of the distributions is saved in the file 
```
output/figures/wmunu_$ERA.png
```

Datacards and RooT files with shaoes for statistical inference are stored in files 
```
output/datacards/munu_$ERA.txt
output/datacards/munu_$ERA.root
```

## Selection of W*->tau+v sample
Selection of events in the measurement W*->tau+v region is done with script [HighPT/ThinJet/scripts/DatacardsThinJet.py](https://github.com/raspereza/HighPT/blob/main/ThinJet/scripts/DatacardsThinJet.py). 

```
./scripts/DatacardsThinJet.py --era $ERA --prong $prong --WP $WP
```
where 
* `$ERA = UL2016 UL2017 or UL2018`
* `$prong = 1prong, 2prong or 3prong`
* `$WP = VVLoose or VLoose`

The distributions of the transverse mass of tau pTmiss are constructed in the following samples: 

* observed data,
* simulated W*->tau+v events,
* remaining simulated samples with genuine selected tau lepton,
* simulated samples with electron or muon faking tau,
* j->tau background model (obtained by applying fake factors in the application region)
By default distributions of the transverse mass of tau and pTmis are produced.
The scripts provides an option to plot other variables by using flag `--variable`
```
./scripts/DatacardsThinJet.py --era $ERA --prong $prong --WP $WP --variable $variable
```
Available variables for plotting
* `mt_1` : transverse mass of tau and pTmiss
* `mt_jet_1` : transverse mass of HPS jet and pTmiss
* `pt_1` : transverse momentum of tau
* `jpt_match_1` : transverse momentum of HPS jet
* `eta_1` : eta of tau
* `jeta_match_1` : eta of HPS jet
* `met` : missing ET

Plot with distributions are saved in the file:
```
output/figures/wtaunu_$variable_$WP_$prong_$ERA.png
```
Also plots, presenting MC closure test of the jet->tau fake model, are created. Closure test compares selected sample of simulated events with jet faking tau, with the jet->tau background model. Simulated events are dominated by Z->vv+jet and W->lv+jet events. The background model is built by weighting simulated events in the application region with fake factors obtained from simulated W*->mu+v+jets sample. The background model is corrected for non-closure in bins of plotted variable. Size of correction is treated as the shape systematic uncertainty. The MC closure plot is saved in file:
```
output/figures/closure_$variable_$WP_$prong_$ERA.png
``` 

Datacards and RooT files with template shapes are only created for variable `mt_1`.
They are saved in files:
```
output/datacards/taunu_$WP_$prong_$ERA.txt
output/datacards/taunu_$WP_$prong_$ERA.txt
```  

## Fits with combine tool
Fit to extract ID scale factor is run with the script [`HighPT/ThinJet/scripts/RunCombine.py`](https://github.com/raspereza/HighPT/blob/main/ThinJet/scripts/RunCombine.py)
```
./scripts/RunCombine.py --era $ERA --prong $prong --WP $WP
```
Make sure that necessary datacards and RooT files for specified $era, $WP and $prong are created and present in the folder
```
output/datacards
```
The script calls bash macro  [`HighPT/ThinJet/scripts/RunCombineThinJet.bash`](https://github.com/raspereza/HighPT/blob/main/ThinJet/scripts/RunCombineThinJet.bash), which combines datacards `` and runs the fit with the combine utility. The fit results are saved in the RooT file:
```
output/datacards/tauID_$WP_$prong_$ERA_fit.root
```

## Plotter

Plotting of prefit and posfit distributions of `mt_1` is implemented in the script [`HighPT/ThinJet/scripts/PlotThinJet.py`](https://github.com/raspereza/HighPT/blob/main/ThinJet/scripts/PlotThinJet.py)
```
./scripts/PlotThinJet.py --era $ERA --prong $prong --WP $WP --Type $type
```
where $type should be either `postfit` or `prefit`. The script take as an input RooT file with fit results `tauID_$WP_$prong_$ERA_fit.root` and outputs plot of `mt_1` distribution in file 
```
output/figures/wtaunu_VVLoose_1prong_UL2018_postFit[preFit].png
```
The measured tau ID scale factor with uncertainty is reported as an output of the script, for example

```
Measurement of id SF ---->
Era = UL2017  2prong  WP = VVLooseVsJet
id SF = 1.38 +/- 0.39

```

