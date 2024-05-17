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
    print("7. Add another set of WPs")
    print("8. Confirm and proceed")

    while True:
        choice = input("Enter your choice (1-8): ").strip()
        if choice == "1":
            args.era = input("Enter the era (UL2016, UL2017, UL2018, 2022, 2023): ").strip()
        elif choice == "2":
            args.WPvsJet.append(input("Enter the WPvsJet (Loose, Medium, Tight, VTight, VVTight): ").strip())
        elif choice == "3":
            args.WPvsMu.append(input("Enter the WPvsMu (VLoose, Tight): ").strip())
        elif choice == "4":
            args.WPvsE.append(input("Enter the WPvsE (VVLoose, Tight): ").strip())
        elif choice == "5":
            args.ff = input("Enter the fake_factors (comb, wjets, dijets): ").strip()
        elif choice == "6":
            args.ff_par = input("Enter the fake factor parametrization to use (pttau, ptjet): ").strip()
        elif choice == "7":
            args.WPvsJet.append(input("Enter the WPvsJet (Loose, Medium, Tight, VTight, VVTight): ").strip())
            args.WPvsMu.append(input("Enter the WPvsMu (VLoose, Tight): ").strip())
            args.WPvsE.append(input("Enter the WPvsE (VVLoose, Tight): ").strip())
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

    return args

def init_histos(args, name):
    h_dict = {}
    bins = [100, 200, 1000]

    h_dict[name] = ROOT.TH1F(name, name, len(bins) - 1, np.array(bins, dtype=np.float64))
    h_dict[name].SetTitle(name)
    h_dict[name].GetXaxis().SetTitle("#tau_{pt}")
    h_dict[name].GetYaxis().SetTitle("SF")

    return h_dict

def fill_hists(h_dict, args, full_filename, name):
    the_file = ROOT.TFile(full_filename, "READ")
    print(full_filename)

    fitResult = the_file.Get('fit_s')
    pars = fitResult.floatParsFinal()
    tauId_central_lowpt, tauId_error_lowpt = None, None
    tauId_central_highpt, tauId_error_highpt = None, None
    for par in pars:
        parname = par.GetName()
        if parname == 'r_lowpt':
            tauId_central_lowpt = par.getVal()
            tauId_error_lowpt = par.getError()
        elif parname == 'r_highpt':
            tauId_central_highpt = par.getVal()
            tauId_error_highpt = par.getError()

    if tauId_central_lowpt is not None and tauId_central_highpt is not None:
        h_dict[name].SetBinContent(1, tauId_central_lowpt)
        h_dict[name].SetBinError(1, tauId_error_lowpt)
        h_dict[name].SetBinContent(2, tauId_central_highpt)
        h_dict[name].SetBinError(2, tauId_error_highpt)
    else:
        print("Error: r_lowpt or r_highpt values not found in file.")

    return h_dict

def main(args, name, full_filename):
    h_dict = init_histos(args, name)
    h_dict = fill_hists(h_dict, args, full_filename, name)

    outfile = ROOT.TFile(args.out_root_file[0], "UPDATE")
    for hist in h_dict.values():
        hist.Write(hist.GetName(), ROOT.TObject.kOverwrite)
    outfile.Close()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-e', '--era', dest='era', default='2022', choices=['UL2016', 'UL2017', 'UL2018', '2022', '2023'])
    parser.add_argument('-wpVsJet', '--WPvsJet', dest='WPvsJet', action='append', default=['Loose', 'Medium', 'Tight', 'VTight', 'VVTight'], choices=['Loose', 'Medium', 'Tight', 'VTight', 'VVTight'])
    parser.add_argument('-wpVsMu', '--WPvsMu', dest='WPvsMu', action='append', default=['Tight'], choices=['VLoose', 'Tight'])
    parser.add_argument('-wpVsE', '--WPvsE', dest='WPvsE', action='append', default=['VVLoose', 'Tight'], choices=['VVLoose', 'Tight'])
    parser.add_argument('-ff', '--fake_factors', dest='ff', default='comb', choices=['comb', 'wjets', 'dijets'])
    parser.add_argument('-ff_par', '--ff_par', dest='ff_par', default='pttau', choices=['pttau', 'ptjet'])
    parser.add_argument('--out_root', dest='out_root_file', type=str, nargs='*', default=['tauID_HighPT_2022.root'], help="path to store results in the form of root histograms")
    
    args = parser.parse_args()

    while True:
        args = adjust_arguments(args)
        if confirm_arguments(args):
            break

    for wp_jet in args.WPvsJet:
        for wp_mu in args.WPvsMu:
            for wp_e in args.WPvsE:
                name = "{}_{}_{}_{}".format(args.ff, wp_jet, wp_mu, wp_e)
                folder_taunu = "/eos/user/j/jmalvaso/HighPt/{}/datacards_{}".format(args.era, name)
                full_filename = folder_taunu + "/tauID_{}_{}_ptbinned_fit.root".format(args.ff_par, name)
                main(args, name, full_filename)
