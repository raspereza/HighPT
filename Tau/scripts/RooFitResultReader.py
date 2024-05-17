#!/usr/bin/env python3
import ROOT
import os
import subprocess
from argparse import ArgumentParser
import numpy as np

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
    print("7. Confirm and proceed")

    while True:
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            args.era = input("Enter the era (UL2016, UL2017, UL2018, 2022, 2023): ").strip()
        elif choice == "2":
            args.WPvsJet = input("Enter the WPvsJet (Loose, Medium, Tight, VTight, VVTight): ").strip()
        elif choice == "3":
            args.WPvsMu = input("Enter the WPvsMu (VLoose, Tight): ").strip()
        elif choice == "4":
            args.WPvsE = input("Enter the WPvsE (VVLoose, Tight): ").strip()
        elif choice == "5":
            args.ff = input("Enter the fake_factors (comb, wjets, dijets): ").strip()
        elif choice == "6":
            args.ff_par = input("Enter the fake factor parametrizatin to use (pttau, ptjet): ").strip()  
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

    return args

def init_histos(args,name):
  
  h_dict = {}
  bins = [100,200,1000]

  h_dict[name] = ROOT.TH1F(name, name, len(bins)-1, np.array(bins))
  h_dict[name].SetTitle(wp)
  h_dict[name].GetXaxis().SetTitle("#tau_{pt}")
  h_dict[name].GetYaxis().SetTitle("SF")
  
  return h_dict

def fill_hists(h_dict, args, full_filename):
    
    the_file = ROOT.TFile(full_filename,"R")
    print(full_filename)
    
    fitResult = the_file.Get('fit_s')
    pars = fitResult.floatParsFinal()
    tauId = {}
    tauId_central = 1.0
    tauId_error = 0.2
    print(name)
    for par in pars:
        parname =  par.GetName()
        if parname=='r_lowpt':
            tauId_central = par.getVal()
            tauId_error = par.getError()
            print(parname, tauId_central, tauId_error)
            h_dict[name].SetBinContent(1, tauId_central)
            h_dict[name].SetBinError(1, tauId_error)           
        elif parname=='r_highpt':
            tauId_central = par.getVal()
            tauId_error = par.getError()
            print(parname, tauId_central, tauId_error)
            h_dict[name].SetBinContent(2, tauId_central)
            h_dict[name].SetBinError(2, tauId_error)

    return h_dict

def main(args,name,full_filename):
  h_dict = init_histos(args,name)
  h_dict = fill_hists(h_dict, args, full_filename)
  outfile = ROOT.TFile.Open(str(args.out_root_file[0]), "RECREATE")
  for (h_name, hist) in h_dict.items():
    print(hist)
    outfile.WriteObject(hist, h_name)
  outfile.Close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2022', choices=['UL2016', 'UL2017', 'UL2018', '2022', '2023'])
    parser.add_argument('-wpVsJet', '--WPvsJet', dest='WPvsJet', default='Medium', choices=['Loose', 'Medium', 'Tight', 'VTight', 'VVTight'])
    parser.add_argument('-wpVsMu', '--WPvsMu', dest='WPvsMu', default='Tight', choices=['VLoose', 'Tight'])
    parser.add_argument('-wpVsE', '--WPvsE', dest='WPvsE', default='VVLoose', choices=['VVLoose', 'Tight'])
    parser.add_argument('-ff','--fake_factors',dest='ff',default='comb',choices=['comb','wjets','dijets'])
    parser.add_argument('-ff_par','--ff_par',dest='ff_par',default='pttau',choices=['pttau','ptjet'])
    parser.add_argument('--out_root',  dest='out_root_file', type=str, nargs='*',default=['HighPT_out.root'], help="path to store resutls in a form of root histograms")
    
    args = parser.parse_args()

    while True:
        args = adjust_arguments(args)
        if confirm_arguments(args):
            break

    name = "{}_{}_{}_{}".format(args.ff, args.WPvsJet, args.WPvsMu, args.WPvsE)
    
    # Check existence of required files
    folder_taunu = "/eos/user/j/jmalvaso/HighPt/{}/datacards_{}".format(args.era, name)


    full_filename = folder_taunu +"/tauID_{}_{}_ptbinned_fit.root".format(args.ff_par,name)
    
    main(args, name, full_filename)
    
    
    
    
    
    # the_file = ROOT.TFile(full_filename,"R")
    # # print(full_filename)
    # # fit = the_file.Get('fit_s')
    # # r_lowpt = fit.floatParsFinal().find('r_lowpt')
    # # r_highpt = fit.floatParsFinal().find('r_highpt')
    # # print(r_lowpt,r_highpt)
    
    # fitResult = the_file.Get('fit_s')
    # pars = fitResult.floatParsFinal()
    # tauId = {}
    # tauId_central = 1.0
    # tauId_error = 0.2
    # print(name)
    # for par in pars:
    #     parname =  par.GetName()
    #     if parname=='r_lowpt':
    #         tauId_central = par.getVal()
    #         tauId_error = par.getError()
    #         print(parname, tauId_central, tauId_error)
    #     elif parname=='r_highpt':
    #         tauId_central = par.getVal()
    #         tauId_error = par.getError()
    #         print(parname, tauId_central, tauId_error)