#!/usr/bin/env python3
import os

# Definisci i due set di script
scripts = [
    'FakeFactorHighPt.py',
    'DatacardsWToMuNu.py',
    'DatacardsWToTauNu.py',
    '/afs/cern.ch/user/j/jmalvaso/HighPT_EPRs/CMSSW_12_4_8/src/HighPT/Tau/combine/RunCombineHighPT.py'
]

scripts_pt_binned = [
    'FakeFactorHighPt.py',
    'DatacardsWToMuNu.py',
    'DatacardsWToTauNu.py',
    '/afs/cern.ch/user/j/jmalvaso/HighPT_EPRs/CMSSW_12_4_8/src/HighPT/Tau/combine/RunCombineMultiDim.py'
]

# Chiedi all'utente quale set di script vuole utilizzare
user_choice = input("Which set of scripts do you want to use? Enter 1 for scripts or 2 for scripts_pt_binned: ")

# Seleziona il set di script in base alla scelta dell'utente
if user_choice == "1":
    selected_scripts = scripts
elif user_choice == "2":
    selected_scripts = scripts_pt_binned
else:
    print("Invalid choice. Exiting.")
    exit()

# Esegui gli script selezionati
for script in selected_scripts:
    print(f"Running {script}...")
    user_input = input(f"Do you want to execute {script}? (y/n): ").lower()
    if user_input == 'n':
        print(f"Skipping {script}...")
        continue
    
    with open(script) as f:
        code = f.read()
        exec(code)
    
    print(f"Finished running {script}\n")

