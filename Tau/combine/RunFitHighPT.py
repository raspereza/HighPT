#!/usr/bin/env python3

import os
import subprocess
from argparse import ArgumentParser
import HighPT.Tau.utilsHighPT as utils

def check_file_existence(filename):
    if os.path.isfile(filename):
        print(filename + " found!")
    else:
        print("Error: File " + filename + " does not exist.")
        similar_files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.basename(filename).split('_')[0] in f]
        if similar_files:
            print("Similar options available in the directory:")
            print("\n".join(similar_files))
        exit(1)    
        
def confirm_arguments(parsed_args):
    print("Parsed arguments:")
    print("Era:", parsed_args.era)
    print("WPvsJet:", parsed_args.WPvsJet)
    print("WPvsMu:", parsed_args.WPvsMu)
    print("WPvsE:", parsed_args.WPvsE)
    print("Fake_factors:", parsed_args.ff)
    print("Fake factors parametrization:", parsed_args.ff_par)
    print("Tau Tagger:",parsed_args.tagger)
    
    confirmation = input("Are these arguments correct? (yes/no): ").strip().lower()
    return confirmation == "yes"

def adjust_arguments(args):
    print("Options to adjust arguments:")
    print("1. Change era")
    print("2. Change WPvsJet")
    print("3. Change WPvsMu")
    print("4. Change WPvsE")
    print("5. Change fake_factors")
    print("6. Change fake factors parametrization")
    print("7. Tau Tagger")
    print("8. Confirm and proceed")

    while True:
        choice = input("Enter your choice (1-8): ").strip()
        if choice == "1":
            args.era = input("Enter the era (UL2016, UL2017, UL2018, 2022, 2023, 2024, 2025): ").strip()
        elif choice == "2":
            args.WPvsJet = input("Enter the WPvsJet (VLoose, Loose, Medium, Tight, VTight, VVTight): ").strip()
        elif choice == "3":
            args.WPvsMu = input("Enter the WPvsMu (VLoose, Tight): ").strip()
        elif choice == "4":
            args.WPvsE = input("Enter the WPvsE (VVLoose, Tight): ").strip()
        elif choice == "5":
            args.ff = input("Enter the fake_factors (comb, wjets, dijets): ").strip()
        elif choice == "6":
            args.ff_par = input("Enter the fake factor parametrizatin to use (pttau, ptjet): ").strip()  
        elif choice == "7":
            args.tagger = input("Enter the tau tagger to use (deeptau, pnet, upart): ").strip()  
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

    return args

# Ask the user which set of scripts they want to use
user_choice = input("Which measurement do you want to run? Enter 1 for pt_incl or 2 for pt_binned: ")

pt_binned = True
# Select the set of scripts based on the user's choice
if user_choice == "1":
    pt_binned = False
    print("Running pt_inclusive measurement...")
elif user_choice == "2":
    pt_binned = True
    print("Running pt_binned measurement...")
else:
    print("Invalid choice. Exiting.")
    exit()

if __name__ == "__main__":
    parser = ArgumentParser()
    if pt_binned == False:
        parser.add_argument('-e', '--era', dest='era', default='2024', choices=['UL2016', 'UL2017', 'UL2018', '2022', '2023','2024','2025'])
        parser.add_argument('-wpVsJet', '--WPvsJet', dest='WPvsJet', default='Medium', choices=['VLoose','Loose', 'Medium', 'Tight', 'VTight', 'VVTight','SuperTight','KiloTight','MegaTight'])
        parser.add_argument('-wpVsMu', '--WPvsMu', dest='WPvsMu', default='Tight', choices=['VLoose', 'Tight'])
        parser.add_argument('-wpVsE', '--WPvsE', dest='WPvsE', default='VVLoose', choices=['VVLoose', 'Tight'])
        parser.add_argument('-ff','--fake_factors',dest='ff',default='comb',choices=['comb','wjets','dijets'])
        parser.add_argument('-ff_par','--ff_par',dest='ff_par',default='pttau',choices=['pttau','ptjet'])
        parser.add_argument('-tagger','--tagger',dest='tagger',default='pnet',choices=['deeptau','pnet','upart'])
    elif pt_binned == True:
        parser.add_argument('-e', '--era', dest='era', default='2024', choices=['UL2016', 'UL2017', 'UL2018', '2022', '2023','2024','2025'])
        parser.add_argument('-wpVsJet', '--WPvsJet', dest='WPvsJet', default='Medium', choices=['VLoose','Loose', 'Medium', 'Tight', 'VTight', 'VVTight','SuperTight','KiloTight','MegaTight'])
        parser.add_argument('-wpVsMu', '--WPvsMu', dest='WPvsMu', default='Tight', choices=['VLoose', 'Tight'])
        parser.add_argument('-wpVsE', '--WPvsE', dest='WPvsE', default='VVLoose', choices=['VVLoose', 'Tight'])
        parser.add_argument('-ff','--fake_factors',dest='ff',default='comb',choices=['comb','wjets','dijets'])
        parser.add_argument('-ff_par','--ff_par',dest='ff_par',default='pttau',choices=['pttau','ptjet'])
        parser.add_argument('-tagger','--tagger',dest='tagger',default='pnet',choices=['deeptau','pnet','upart'])
    
    args = parser.parse_args()

    while True:
        args = adjust_arguments(args)
        if confirm_arguments(args):
            break

    name = "{}_{}_{}_{}_{}_incl_{}_{}".format(args.ff_par, args.ff, args.WPvsJet, args.WPvsMu, args.WPvsE, args.era, args.tagger)
    datacard_subfolder = "datacards_{}_{}_{}_{}".format(args.ff, args.WPvsJet, args.WPvsMu, args.WPvsE)
    
    # Check existence of required files
    
    folder_munu = utils.baseFolder+"/{}/datacards_munu".format(args.era)
    folder_taunu = utils.baseFolder+"/{}/{}".format(args.era, datacard_subfolder)
    
    os.chdir(folder_munu)
    check_file_existence("munu_{}.txt".format(args.era))

    folder = utils.baseFolder+"/{}/{}".format(args.era, datacard_subfolder)
    os.chdir(folder_taunu)    
    
    if pt_binned == False:
        check_file_existence("taunu_{}.txt".format(name))


        # Combine W*->mu+v and W*->tau+v cards
        subprocess.call(["combineCards.py", folder_munu+"/munu_{}.txt".format(args.era), "taunu_{}.txt".format(name)], stdout=open("tauID_{}.txt".format(name), 'w'))

        # Creating workspace
        subprocess.call(["combineTool.py", "-M", "T2W", "-o", "tauID_{}.root".format(name), "-i", "tauID_{}.txt".format(name)])

        # Doing fit
        subprocess.call(["combineTool.py", "-M", "FitDiagnostics", "--saveNormalizations", "--saveShapes", "--saveWithUncertainties", "--saveNLL", "--robustHesse", "1", "--rMin", "0", "--rMax", "3", "-m", "200", "-d", "tauID_{}.root".format(name), "--cminDefaultMinimizerTolerance", "0.1", "--cminDefaultMinimizerStrategy", "0", "-v", "2"])

        # Renaming output
        os.rename("fitDiagnostics.Test.root", "tauID_{}_fit.root".format(name))
   
    elif pt_binned == True:
        name = "{}_{}_{}_{}_{}".format(args.ff_par, args.ff, args.WPvsJet, args.WPvsMu, args.WPvsE)
        check_file_existence("taunu_{}_lowpt_{}_{}.txt".format(name,args.era,args.tagger))
        check_file_existence("taunu_{}_mediumpt_{}_{}.txt".format(name,args.era,args.tagger))
        check_file_existence("taunu_{}_highpt_{}_{}.txt".format(name,args.era,args.tagger))
        # Combine W*->mu+v and W*->tau+v cards
        subprocess.call(["combineCards.py", folder_munu+"/munu_{}.txt".format(args.era), "taunu_{}_lowpt_{}_{}.txt".format(name, args.era, args.tagger), "taunu_{}_mediumpt_{}_{}.txt".format(name, args.era, args.tagger), "taunu_{}_highpt_{}_{}.txt".format(name, args.era, args.tagger)], stdout=open("tauID_{}_{}_ptbinned.txt".format(name,args.tagger), 'w'))

        # Creating workspace
        subprocess.call(["combineTool.py", "-M", "T2W", "-P", "HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel", "--PO", '"map=^.*/*_highpt_{}:r_highpt[1,0,2]"'.format(args.era), "--PO", '"map=^.*/*_mediumpt_{}:r_mediumpt[1,0,2]"'.format(args.era), "--PO", '"map=^.*/*_lowpt_{}:r_lowpt[1,0,2]"'.format(args.era), "-o", "tauID_{}_{}_ptbinned.root".format(name, args.tagger), "-i", "tauID_{}_{}_ptbinned.txt".format(name, args.tagger)])

        # Doing fit
        subprocess.call(["combineTool.py", "-M", "FitDiagnostics", "--saveNormalizations", "--saveShapes", "--saveWithUncertainties", "--saveNLL", "--redefineSignalPOIs", "r_lowpt,r_mediumpt,r_highpt", "--robustHesse", "1", "-m", "200", "-d", "tauID_{}_{}_ptbinned.root".format(name, args.tagger), "--cminDefaultMinimizerTolerance", "0.1", "--cminDefaultMinimizerStrategy", "0", "-v", "2"])

        # Renaming output
        os.rename("fitDiagnostics.Test.root", "tauID_{}_{}_ptbinned_fit.root".format(name, args.tagger))

    # Remove intermediate files
    for f in os.listdir('.'):
        if f.startswith('higgsCombine'):
            os.remove(f)

    print("Leaving folder {}".format(folder_taunu))
