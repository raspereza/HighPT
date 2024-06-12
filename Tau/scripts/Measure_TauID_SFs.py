#!/usr/bin/env python3
import os

# Define the two sets of scripts
scripts = [
    'FakeFactorHighPt.py',
    'DatacardsWToMuNu.py',
    'DatacardsWToTauNu.py',
    '../combine/RunCombineHighPT.py'
]

scripts_pt_binned = [
    'FakeFactorHighPt.py',
    'DatacardsWToMuNu.py',
    'DatacardsWToTauNu.py',
    '../combine/RunCombineMultiDim.py'
]

# Ask the user which set of scripts they want to use
user_choice = input("Which set of scripts do you want to use? Enter 1 for scripts or 2 for scripts_pt_binned: ")

# Select the set of scripts based on the user's choice
if user_choice == "1":
    selected_scripts = scripts
elif user_choice == "2":
    selected_scripts = scripts_pt_binned
else:
    print("Invalid choice. Exiting.")
    exit()

# Execute the selected scripts
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
