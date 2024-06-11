#!/usr/bin/env python3
import os

scripts = [
    'FakeFactorHighPt.py',
    'DatacardsWToMuNu.py',
    'DatacardsWToTauNu.py',
    '/afs/cern.ch/user/j/jmalvaso/HighPT_EPRs/CMSSW_12_4_8/src/HighPT/Tau/combine/RunCombineMultiDim.py'
    
]

for script in scripts:
    print(f"Running {script}...")
    with open(script) as f:
        code = f.read()
        exec(code)
    print(f"Finished running {script}\n")

