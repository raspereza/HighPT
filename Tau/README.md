# High pT tau ID SF measurements

## Installation

The measurement will require [Higgs combination package](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git), [Combine Harvester package](https://github.com/cms-analysis/CombineHarvester.git)  and [python analysis code](https://github.com/raspereza/HighPT.git) 

Installation proceeds as follows:
```
export SCRAM_ARCH=el9_amd64_gcc12
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git checkout v10.4.2
cd ../..
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
git checkout v3.0.0-pre1
git clone https://github.com/raspereza/HighPT.git HighPT
scramv1 b -j 4
```

All scripts at every step of the measurement will be run from the directory [`src/HighPT/Tau`](https://github.com/raspereza/HighPT/tree/main/Tau)

## Overview of measurement strategy

Analysis uses sample of highly virtual W boson decaying to tau lepton. The data/simulation scale factors for high pT tau identification are extracted from two selected samples: 

1. measurement sample `W*->tau+v`
2. sideband sample `W*->mu+v`

The measurement is done by performing simultaneous fit in the so sideband and measurement regions. The fitted distributions are

1. transverse mass of muon and missing pT in the `W*->mu+v` sideband, and
2. transverse mass of tau and missing pT in the `W*->tau+v` measurement regions.

The fit is performed with two or more unconstrained rate parameters. One of them accounts for rate 
of highly virtual W production. The analysis probes specific phase space with mass of W* greater than 200 GeV. This rate parameter scales both W*->mu+v and W*->tau+v simulated templates. Other parameters are related to tau ID scale factors. They are apllied to W*->tau+v template and all other smulated processes with genuine selected tau lepton. The measurement can be performed either inclusively for the entire sample of tau leptons with pT > 100 GeV or differentially in tau pT bins with the default pt binning is `[100,150,250,Inf]`. In the case of inclusive measurement, only one rate parameter is associated with the tau ID scale factor. In the differential measurement, an individual rate parameter is assigned for each pT measurement bin. 

Selection the sideband `W*->mu+v` region:
* Trigger : HLT_IsoMu24
* exactly one mediumID muon,
* muon kinematics : pT>120 GeV and |eta|<2.1,
* missing ET > 130 GeV,
* transverse mass of muon and pTmiss > 200 GeV, 
* azimuthal angle between muon and pTmiss > 2.8 radian,
* additional leptons and jets are vetoed.
The `W*->mu+v` selection criteria are defined in the script [src/HighPT/Tau/scripts/DatacardsWToMuNu.py](https://github.com/raspereza/HighPT/blob/main/Tau/scripts/DatacardsWToMuNu.py)

For the `W*->mu+v` region three templates are saved in datacards for statistical inference: 
1. observed data, 
2. W*->mu+v simulated sample,
3. sum of remaining simulated samples

Selection in the measurement `W*->tau+v` region:
* Trigger : HLT_PFMETNoMu120_PFMHTNoMu120_IDTight
* exactly one tau fulfilling minimal set of ID criteria imposed in NanoAOD
* additionally tau is required to pass predefined selection criteria of DeepTau or PNet algorithms 
* tau pT > 100 GeV, |eta| < 2.4 
* missing ET > 130 GeV
* transverse mass of muon and missing pT > 200 GeV
* azimuthal angle between muon and pTmiss > 2.8 radian,
* additional leptons and jets are vetoed.
The `W*->tau+v` selection criteria are defined in the script [src/HighPT/Tau/scripts/DatacardsWToTauNu.py](https://github.com/raspereza/HighPT/blob/main/Tau/scripts/DatacardsWToTauNu.py) 
Optionally, one could apply cuts on tau pT to define measurement bin. The instruction on running this scripts are given below.

For the `W*->tau+v` region five templates are saved in datacards for statistical inference:
1. observed data,
2. W*->tau+v simulated sample,
3. sum of remaining simulated samples with genuine selected tau lepton
4. sum of simulated samples with electron or muon faking tau
5. background with hadronic jet misidentified as tau lepton

While templates 2., 3. and 4. are obtained from simulation, template of background with jets faking taus is constructed using data. The instrumental sample for that is the sample containing tau candidates that pass relaxed working point (WP) against jet, but fail nominal. Extrapolation weights are applied to events in this region (which we refer to as application region, AR) to predict jet->tau fake background in the measurement region. Extrapolation weights, called fake factors (FF), are defined as the ratio: 
```
FF = P(nominal ID)/P(relaxed and !nominal)
```
where 
1. `P(nominal)` is the probability for fake tau candidate to pass nominal WP against jet,
2. `P(relaxed and !nominal)` is the probability for fake tau candidate to pass nominal WP but fail relaxed.
For both DeepTau and PNet tau taggers, relaxed ID criteria are associated with the VVVLoose WP against jet.  

The jet->tau fake background in the application region comprises mainly three types of events
1. `Z->vv+jet`, invisible decay of the Z boson gives rise to the missing ET;
2. `W->lv+jet`, where l is not reconstructed or out of acceptance;
3. `QCD multijets`.

Given that the largest contributions to the jet->tau fake background come from single boson production
and QCD multijet events, it is reasonable to measure fake factors separately for QCD and electroweak (EW) single-boson production. We denote these FFs as FF(QCD) and FF(EW). They are measured using as a standard candles `W(->mu+v)+jet` and `dijets` samples. FFs are computed using script [src/HighPT/Tau/scripts/FakeFactorHighPt.py](https://github.com/raspereza/HighPT/blob/main/Tau/scripts/FakeFactorHighPt.py). The FFs are parameterized in several ways. For the nominal analysis, FF(QCD) and FF(EW) are measured in as a function of pT(tau) in bins of ratio pT(au)/pT(AK4jet), where pT(AK4jet) is the transverse momentum of AK4 jet seeding tau. Other kinds of parameterizations were used in the past for auxiliary and exploratory studies. 

The FF(QCD) and FF(EW) are applied as weights to events in the AR to construct templates Fakes_QCD and Fakes_EW. The distribution of the combined jet->tau fake background for a given inspected/inference variable `x` is obtained by weighting templates Fakes_QCD and Fakes_EW with `x`-dependent fractions of QCD and non-QCD (EW) events.
```
Fakes(x) = f_QCD(x)*Fakes_QCD(x)+(1-f_QCD(x))*Fakes_EW(x)
```
Given limited statistical power of QCD multijet MC samples and imperfect simulation of multijet production, estimation of fractions of QCD and EW events in AR relies on data and MC samples of non-QCD processes. The total contribution from j->tau fakes in AR is computed by subtracting from data contribution from genuine taus and light leptons faking taus estimated from MC : N(jet->tau) = N(data) - N(MC,tau or l->tau). The fraction of QCD events is then defined as `f_QCD = ( N(jet->tau) - N(MC,jet->tau) )/N(jet->tau)`, where as fraction of f_nonQCD is computed as `1-f_QCD`. 

The whole analysis on 2024 and 2025 datasets is performed using as inputs specialized plain tuples (picotuples in the terminology of Tau POG) produced from NANOAOD(SIM) and stored on lxplus EOS storage area. Four types of picotuples obtained with dedicated selections, are needed for the measurements.  

* /eos/cms/store/group/phys_tau/rasp/HighPT/$ERA/taunu : pre-selected tau+MET events; they are used to construct templates and monitor control plots in the `W*->tau+v` measurement regions; 
* /eos/cms/store/group/phys_tau/rasp/HighPT/$ERA/wjets : pre-selected `W(->mu+v)+jet` events; used for measuring FF(EW).
* /eos/cms/store/group/phys_tau/rasp/HighPT/$ERA/dijets : pre-selected `dijets` events; used for measuring fake factors with FF(QCD) 
* /eos/cms/store/group/phys_tau/rasp/HighPT/$ERA/munu : pre-selected muon+MET events; they are used to monitor control plots and construct templates in the `W*->mu+v` measurement region.

Apart from executable macros (which are described below), code includes also auxiliarly scripts:
* [src/HighPT/Tau/python/stylesHighPT.py](https://github.com/raspereza/HighPT/blob/main/Tau/python/stylesHighPT.py) defines of drawing ROOT styles,
* [src/HighPT/Tau/python/utilsHighPT.py](https://github.com/raspereza/HighPT/blob/main/Tau/python/utilsHighPT.py) defines configuration and helper classes : name of the root directory with pico tuples, data and MC samples used in the analysis, selectors, fake factor reader, helper methods to handle histograms, etc. 

The name of the root directory with picotuples is specified in the configuration file [src/HighPT/Tau/python/utilsHighPT.py](https://github.com/raspereza/HighPT/blob/main/Tau/python/utilsHighPT.py) via the variable
* `picoFolder=/eos/cms/store/group/phys_tau/rasp/HighPT`.

In the same python file the analyst should also specify the folder where output of the analysis routine will be stored via string variable `baseFolder` and the folder where figures in the png format will be saved via string variable `figureFolder`. 

It should be mentioned at this point that the package is intended also for computation of the high pT single-tau trigger SF (inclusive for pT > threshold + 10 GeV). Three triggering strategies are considered: 
* taus pass HLT_LooseDeepTauPFTauHPS180_L2NN_eta2p1
* taus pass HLT_SinglePNetTauhPFJet130_Loose_L2NN_eta2p3
* taus pass HLT_LooseDeepTauPFTauHPS180_L2NN_eta2p1 OR HLT_SinglePNetTauhPFJet130_Loose_L2NN_eta2p3

For this reason FFs are computed for the sample of fake taus passing and failing trigger requirements.
This measurement is ouside the scope of the current documentation. Instructions for this kind of measurement will be added later.

## Analysis workflow

## Determination of FFs.

Nominal FF(QCD) and FF(EW) are computed in dependence of pT(tau) for the two bins of the ratio = pT(tau)/pT(AK4jet):
* ratio < 0.85,
* ratio > 0.85.

Alternative FF parameterizations:
* FF = FF(pT(AKjet),pT(tau)/pT(AK4jet)
* FF = FF(pT(tau),decayMode)
* FF = FF(pT(AKjet),decayMode)
* FF = FF(mass(tau),decayMode)
are also introduced. They were used in early studies aimed at optimization of the measurement. Currently they are not employed in the nominal measurements of the high pT tau ID SFs.

FF are determined using script [src/HighPT/Tau/scripts/FakeFactorHighPt.py](https://github.com/raspereza/HighPT/blob/main/Tau/scripts/FakeFactorHighPt.py)
```
./scripts/FakeFactorHighPt.py 
```
The script starts interactive menu offering to check and modify configuration settings:
```
Options to adjust arguments:
1. Change era
2. Change WPvsJet
3. Change WPvsMu
4. Change WPvsE
5. Trigger option
6. Tau Tagger
7. Confirm and proceed
Enter your choice (1-7):
```
Choose option 7 to verify default configuration:
```
Parsed arguments:
Era: 2024
WPvsJet: Medium
WPvsMu: Tight
WPvsE: VVLoose
Tau Tagger: pnet
Trigger option: comb
Are these arguments correct? (yes/no)
```

You can change configuration parameters interactively by typing `no` or proceed with measurement of fake factors by typing `yes`. Trigger option can be set to `comb` when measuring offline tau ID scale factors.

IMPORTANT NOTE: whereas FF(QCD) are measured with data, FF(EW) are measured both in data and with simulated W+jets samples. The measurement with simulated sample is necessary to perform closure test of jet->tau fake background model and infer uncertainties in background estimation.  

The measured FF will be stored as histograms in the RooT file.
`utils.baseFolder/$ERA/FF/ff_$WPvsJet_$WPvsMu_$WPvsE_$tagger_$option.root`
where `$tagger` is the name of the tagger and $option is the trigger option.
They will be used to construct background model with jets faking taus in the `W*->tau+v` measurement regions. The information on FFs that are used in the nominal measurements is encoded in the following histograms:
* $sample_$type_pttau_$ptratiobin_$trigger
where
* $sample = data or MC 
* $type = dijets or wjets (measurement sample: dijets->FF(QCD), wjets->FF(EW))
* $ptratiobin - ptratioLow (<0.85) or ptratioHigh (>0.85)
* $trigger = incl (inclusive FF), trig (FF for triggering tau fakes), nottrig (FF for non-triggering tau fakes)
The RooT file contains also another histograms encoding alternative FF parametrizations. They are not used in the nominal measurements. 

## Selection of W*->mu+v sample 

Selection of events in the W*->mu+v sideband region is performed with the script [src/HighPT/Tau/scripts/DatacardsWToMuNu.py](https://github.com/raspereza/HighPT/blob/main/Tau/scripts/DatacardsWToMuNu.py). 
```
scripts/DatacardsWToMuNu.py 
```
The script will construct templates of
1. observed data,
2. simulated W*->mu+v sample,
3. and remaining simulated samples.

Interactive menu offers analyst to choose era (2024, 2025) and variable to plot: 
```
Options to adjust arguments:
1. Change era
2. Change variable(s) to plot
3. Confirm and proceed
```

The following variables can be plotted :
* `mt_1`  : transverse mass of muon and missing transverse momentum;
* `pt_1`  : transverse momentum of muon;
* `met`   : missing transverse momentum;
* `eta_1` : pseudorapidity of muon;
* `phi_1` : azimuthal angle of muon;

Control plots are saved in the png files:  
```
utils.figureFolder/WMuNu/wmunu_$VAR_$ERA.png
```

If variable `mt_1` is specified
datacards and root file with shapes for statistical inference of tau ID scale factors are produced and placed in the folder `utils.baseFolder/$ERA/datacards_munu/`:

```
utils.baseFolder/$ERA/datacards_munu/munu_$ERA.txt
utils.baseFolder/$ERA/datacards_munu/munu_$ERA.root
```

## Selection of W*->tau+v sample

Selection of events in the measurement W*->tau+v regions is done with script [src/HighPT/Tau/scripts/DatacardsWTauNu.py](https://github.com/raspereza/HighPT/blob/main/Tau/scripts/DatacardsWTauNu.py). 

```
./scripts/DatacardsWTauNu.py
```
The scripts offers to configure the steering parameters by means of interactive menu 
```
Options to adjust arguments:
1. Change era
2. Change WPvsJet
3. Change WPvsMu
4. Change WPvsE
5. Change variable to plot
6. Change fake factors to use
7. Change measurement to perform
8. Change the fake factor parametrization
9. Changer the tau tagger
10. Confirm and proceed
Enter your choice (1-10):
```
Enter 10 to see the default arguments
```
Parsed arguments:
Era: 2024
WPvsJet: Medium
WPvsMu: Tight
WPvsE: VVLoose
Variable: mt_1
Fake factors: comb
Measurement: incl
Fake factors parametrization: pttau
Tau tagger: pnet
Are these arguments correct? (yes/no):
```

Below available options for the arguments of primary interest are listed:
* Measurement: incl, lowpt, mediumpt, highpt
  * incl: selection inclusively in tau pT: pT(tau) > 100 GeV; 
  * lowpt : selection is done for tau PT in the range [100,150] GeV, intended for pT binned measurement of SF;
  * mediumpt : selection is done for tau PT in the range [150,250] GeV, intended for pT binned measurement of SF;
  * highpt : selection is done for tau pT in the range [250,350] GeV, intended for pT binned measurement of SF;



It is suggested to use combination of FF(QCD) and FF(EW) in estimation of the jet->tau fake background and parameterization of FF as a function of pT(tau):
```
* Fake factors: comb, 
* Fake factors parametrization: pttau
```



Once arguments are adjusted script is 



* observed data,
* simulated W*->tau+v events,
* remaining simulated samples with genuine selected tau lepton,
* simulated samples with electron or muon faking tau,
* j->tau background model (obtained by applying fake factors in the application region)
By default distributions of the transverse mass of tau and pTmis are produced.

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
output/datacards/taunu_$WP_$prong_$ERA.root
```  

## Fits with combine tool
Fit to extract ID scale factor is run with the script [`HighPT/Tau/scripts/RunCombine.py`](https://github.com/raspereza/HighPT/blob/main/Tau/scripts/RunCombine.py)
```
./scripts/RunCombine.py --era $ERA --prong $prong --WP $WP
```
Make sure that necessary datacards and RooT files for specified $era, $WP and $prong are created and present in the folder
```
output/datacards
```
The script calls bash macro  [`HighPT/Tau/scripts/RunCombineTau.bash`](https://github.com/raspereza/HighPT/blob/main/Tau/scripts/RunCombineTau.bash), which combines datacards `munu_$ERA.txt` and `taunu_$WP_$prong_$ERA.txt` and runs the fit with the combine utility. The fit results are saved in the RooT file:
```
output/datacards/tauID_$WP_$prong_$ERA_fit.root
```

## Plotter

Plotting of prefit and posfit distributions of `mt_1` is implemented in the script [`HighPT/Tau/scripts/PlotTau.py`](https://github.com/raspereza/HighPT/blob/main/Tau/scripts/PlotTau.py)
```
./scripts/PlotTau.py --era $ERA --prong $prong --WP $WP --Type $type
```
where $type should be either `postfit` or `prefit`. The script take as an input RooT file with fit results `tauID_$WP_$prong_$ERA_fit.root` and outputs plot of `mt_1` distribution in file: 
```
output/figures/wtaunu_VVLoose_1prong_UL2018_postFit[preFit].png
```
The measured tau ID scale factor with uncertainty is reported as an output of the script, for example:

```
Measurement of id SF ---->
Era = UL2017  2prong  WP = VVLooseVsJet
id SF = 1.38 +/- 0.39

```

