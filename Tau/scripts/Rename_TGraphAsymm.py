#!/usr/bin/env python3
import ROOT
def rename_and_remove_TGraphAsymmErrors(root_file_path, old_name, new_name):
    # Open the ROOT file in update mode
    root_file = ROOT.TFile.Open(root_file_path, "UPDATE")
    if not root_file or root_file.IsZombie():
        raise Exception(f"Cannot open file {root_file_path}")

    # Retrieve the TGraphAsymmErrors object
    graph = root_file.Get(old_name)
    if not graph:
        raise Exception(f"Cannot find TGraphAsymmErrors {old_name} in {root_file_path}")
    if not isinstance(graph, ROOT.TGraphAsymmErrors):
        raise Exception(f"Object {old_name} is not a TGraphAsymmErrors")

    # Change the name of the TGraphAsymmErrors object
    graph.SetName(new_name)

    # Write the object with the new name to the file
    graph.Write(new_name)

    # Delete the original object from the file
    root_file.Delete(old_name + ";*")

    root_file.Close()

    print(f"TGraphAsymmErrors {old_name} renamed to {new_name} and old object removed from {root_file_path}")

# Example usage:
if __name__ == "__main__":
    root_file_path = "TauID_SF_Highpt_DeepTau2018v2p5VSjet_VSjetLoose_VSeleTight_May24.root"  # Replace with your ROOT file path
    old_name = "DMinclusive_2023_statandsyst_2022"        # Replace with the current name of the TGraphAsymmErrors
    new_name = "DMinclusive_2023_statandsyst_2023"        # Replace with the new name for the TGraphAsymmErrors
    rename_and_remove_TGraphAsymmErrors(root_file_path, old_name, new_name)
