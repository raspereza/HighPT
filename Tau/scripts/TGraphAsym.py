#!/usr/bin/env python3
import ROOT
import os
from argparse import ArgumentParser
import numpy as np

def convert_TH1_to_TGraphAsymmErrors(root_file_path, histogram_name, era):
    # Open the ROOT file in update mode
    root_file = ROOT.TFile.Open(root_file_path, "UPDATE")
    if not root_file or root_file.IsZombie():
        raise Exception(f"Cannot open file {root_file_path}")

    # Retrieve the histogram
    hist = root_file.Get(histogram_name)
    if not hist:
        raise Exception(f"Cannot find histogram {histogram_name} in {root_file_path}")
    if not isinstance(hist, (ROOT.TH1F, ROOT.TH1D)):
        raise Exception(f"Object {histogram_name} is not a TH1F or TH1D histogram")

    # Construct the new name using the era
    new_name = "{}_statandsyst_{}".format(histogram_name, era)

    # Check if the TGraphAsymmErrors object already exists
    existing_graph = root_file.Get(new_name)
    if existing_graph:
        print(f"TGraphAsymmErrors {new_name} already exists in {root_file_path}. Skipping creation.")
    else:
        # Create a TGraphAsymmErrors from the histogram
        graph = ROOT.TGraphAsymmErrors(hist)
        graph.SetName(new_name)
        graph.Write()
        print(f"TGraphAsymmErrors saved as {new_name} in {root_file_path}")

    root_file.Close()

def confirm_arguments(parsed_args):
    print("Parsed arguments:")
    print("Era:", parsed_args.era)
    print("WPvsJet:", parsed_args.WPvsJet)
    print("WPvsMu:", parsed_args.WPvsMu)
    print("WPvsE:", parsed_args.WPvsE)
    
    confirmation = input("Are these arguments correct? (yes/no): ").strip().lower()
    return confirmation == "yes"

def adjust_arguments(args):
    print("Options to adjust arguments:")
    print("1. Change era")
    print("2. Change WPvsJet")
    print("3. Change WPvsMu")
    print("4. Change WPvsE")
    print("5. Confirm and proceed")

    while True:
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            args.era = input("Enter the era (UL2016, UL2017, UL2018, 2022, 2023): ").strip()
        elif choice == "2":
            args.WPvsJet = input("Enter the WPvsJet (Loose, Medium, Tight, VTight, VVTight): ").strip()
        elif choice == "3":
            args.WPvsMu = input("Enter the WPvsMu (VLoose, Tight): ").strip()
        elif choice == "4":
            args.WPvsE = input("Enter the WPvsE (VVLoose, Tight): ").strip()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

    return args

# Command-line argument parsing
if __name__ == "__main__":
    parser = ArgumentParser(description="Convert TH1 histograms to TGraphAsymmErrors and save them with a new name.")
    parser.add_argument('-e', '--era', dest='era', nargs='+', default=['2022', '2023'], choices=['UL2016', 'UL2017', 'UL2018', '2022', '2023'])
    parser.add_argument('-wpVsJet', '--WPvsJet', dest='WPvsJet', nargs='+', default=['Loose', 'Medium', 'Tight', 'VTight', 'VVTight'], choices=['Loose', 'Medium', 'Tight', 'VTight', 'VVTight'])
    parser.add_argument('-wpVsMu', '--WPvsMu', dest='WPvsMu', nargs='+', default=['Tight'], choices=['VLoose', 'Tight'])
    parser.add_argument('-wpVsE', '--WPvsE', dest='WPvsE', nargs='+', default=['VVLoose', 'Tight'], choices=['VVLoose', 'Tight'])
    
    args = parser.parse_args()
    
    while True:
        if confirm_arguments(args):
            break
        else:
            args = adjust_arguments(args)

    release_date = "May24"
    for era in args.era:
        for wp_jet in args.WPvsJet:
            for wp_mu in args.WPvsMu:
                for wp_e in args.WPvsE:
                    # Define the histogram name and ROOT file path
                    root_file_path = "TauID_SF_Highpt_DeepTau2018v2p5VSjet_VSjet{}_VSele{}_{}.root".format(wp_jet, wp_e, release_date)  # Replace with your input ROOT file path
                    histogram_name = "DMinclusive_{}".format(era)  # Replace with your histogram name
                    # Call the function to convert the histogram
                    convert_TH1_to_TGraphAsymmErrors(root_file_path, histogram_name, era)
