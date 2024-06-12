#!/usr/bin/env python3
import os
import HighPT.Tau.utilsHighPT as utils
# Define the two sets of scripts
scripts = [
    'FakeFactorHighPt.py',
    'DatacardsWToMuNu.py',
    'DatacardsWToTauNu.py',
    '../combine/RunFitHighPT.py'
]

# Execute the selected scripts
for script in scripts:
    print(f"Running {script}...")
    user_input = input(f"Do you want to execute {script}? (y/n): ").lower()
    if user_input == 'n':
        print(f"Skipping {script}...")
        continue
    
    with open(script) as f:
        code = f.read()
        exec(code)
    
    print(f"Finished running {script}\n")
