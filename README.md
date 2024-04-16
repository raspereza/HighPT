# High pT tau ID SF measurements

## Installation

The measurement will require [Higgs combination package](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git) and [python analysis code](https://github.com/raspereza/HighPT.git) 

Login to lxplus7 machine and execute the following commands
```
export SCRAM_ARCH=CMSSW_12_4_8
cmsrel CMSSW_12_4_8
cd CMSSW_12_4_8/src
cmsenv
https://github.com/raspereza/TauFW TauFW
scramv1 b -j 4
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
cd ../..
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scramv1 b clean 
scramv1 b
git clone https://github.com/raspereza/HighPT.git HighPT
scramv1 b -j 4
```

After installation is complete change to the directory [`$CMSSW_BASE/src/HighPT/Tau`](https://github.com/raspereza/HighPT/tree/main/Tau).

```
cd $CMSSW_BASE/src/HighPT/Tau
```

Create main directory and subfolder where output of the code will be stored:
```
mkdir /afs/cern.ch/work/u/username/HighPT
```

NB : several subfolders should be created manually. Automated script is being developed for that.

All scripts at every step of the measurement will be run from the directory [`$CMSSW_BASE/src/HighPT/Tau`](https://github.com/raspereza/HighPT/tree/main/Tau)


## Measurement strategy

The data/simulation scale factors for high pT tau identification are extracted from two selected samples: 

1. measurement sample `W*->tau+v`
2. sideband sample `W*->mu+v`

The measurement is done by performing simultaneous fit in two regions. The fitted distributions are

1. transverse mass of muon and missing pT in the `W*->mu+v` sideband, and
2. transverse mass of tau and missing pT in the `W*->tau+v` region.

The tuples for these samples are created with [PicoProducers]().

The fit is performed with two unconstrained rate parameters. One of them accounts for cross section
of highly virtual W production. The analysis probes specific phase space with mass of W* greater than about 200 GeV.
This rate parameter scales both W*->mu+v and W*->tau+v simulated templates. Second parameter is the measured thin-jet ID scale factor. It is apllied to W*->tau+v template and all other smulated processes with genuine selected tau lepton. The measurement is performed individually for 1-prong, 2-prong and 3-prong type of thin-jets.


