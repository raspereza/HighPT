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

After installation is complete change to the directory `HighPT/ThinJet` and run the script:

```
cd HighPT/ThinJet
./setup.sh
```

This will create in the cuurent directory several folders where outputs of the code will be stored:
1. `output/figures` - plots (png files) of data and simulated distributions used in the measurement;
2. `output/figures/FF` - plots of measured fake factors  
3. `output/FF` - root files with fake factors for building fake background model
4. `output/datacards` - datacards used to measure thin jet ID scale factors with [Higgs combination package](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git) 


## Measurement strategy

Analysis uses tau leptons as proxy for thin-jets. The data/simulation scale factors for thin-jet identification 
are extracted from two selected samples: 

1. measurement sample `W*->tau+v`
2. sideband sample `W*->mu+v`

The measurement is done by performing simultaneous fit in two regions. The fitted distributions are

1. transverse mass of muon and missing pT in the `W*->mu+v` sideband
2. transverse mass of thin-jet(tau) and missing pT in the `W*->tau+v` region

The fit is performed with two unconstrained rate parameters. One of them accounts for cross section
of highly virtual W production. The analysis probes specific phase space with mass of W* greater than about 300 GeV.
This rate parameter scales both W*->mu+v and W*->tau+v simulated templates. Second parameter is the measured
thin-jet ID scale factor. It is apllied to W*->tau+v template and all other smulated processes with genuine 
selected tau lepton. The measurement is performed individually for 1-prong, 2-prong and 3-prong type of thin-jets.

We recommend to identify thin-jets as taus passing either VVLoose or VLoose WP agains jets.

Selection the sideband `W*->mu+v` region:
* exactly one mediumID 
* muon kinematics : pT>140 GeV and |eta|<2.4
* missing ET > 150 GeV
* transverse mass of muon and missing pT > 300 GeV 
* additional leptons and jets are vetoed

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

For the `W*->tau+v` region four templates are saved in datacards for statistical inference:
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

The whole analysis is performed using PicoTuples located on lxplus machine in the folder 
`/eos/user/r/rasp/output/HighPT_thinjet`

## Determination of fake factors

Fake factors are measured in dependence of number of prongs (1-prong, 2-prong or 3-prong) and in dependence of 
HPS jet pT. Measurement is performed using script [HighPT/ThinJet/scripts/FakeFactorThinJet.py](https://github.com/raspereza/HighPT/blob/main/ThinJet/scripts/FakeFactorThinJet.py)
```
./scripts/FakeFactorThinJet.py --era $Era --WP $WP
```
where 
* `$WP` is WP against jet (VVLoose or VLoose)
* `$ERA` is era (UL2016, UL2017, UL2018)



## Selection of W*->mu+v sample



## Selection of W*->tau+v sample