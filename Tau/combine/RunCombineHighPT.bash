#!/bin/bash

usage() {
    echo "Usage: $0 [--era <era>] [--WPvsJet <WPvsJet>] [--WPvsMu <WPvsMu>] [--WPvsE <WPvsE>]"
    echo "Options:"
    echo "  --era <era>      Specify the era ('UL2016','UL2017','UL2018','2022','2023')"
    echo "  --WPvsJet <WPvsJet> Specify the WPvsJet ('Loose','Medium','Tight','VTight','VVTight')"
    echo "  --WPvsMu <WPvsMu> Specify the WPvsMu ('VLoose','Tight')"
    echo "  --WPvsE <WPvsE>  Specify the WPvsE ('VVLoose','Tight')"
    exit 1
}

check_file_existence() {
    filename="$1"
    if [ -f "$filename" ]; then
        echo "$filename found!"
    else
        echo "Error: File $filename does not exist."
        similar_files=$(ls -1 | grep "$(basename "$filename" | cut -d'_' -f1)")
        if [ ! -z "$similar_files" ]; then
            echo "Similar options available in the directory:"
            echo "$similar_files"
        fi
        exit 1
    fi
}

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --era)
            era="$2"
            shift
            shift
            ;;
        --WPvsJet)
            WPvsJet="$2"
            shift
            shift
            ;;
        --WPvsMu)
            WPvsMu="$2"
            shift
            shift
            ;;
        --WPvsE)
            WPvsE="$2"
            shift
            shift
            ;;
        *)
            usage
            ;;
    esac
done

# Check if all arguments have been provided
if [ -z "$era" ] || [ -z "$WPvsJet" ] || [ -z "$WPvsMu" ] || [ -z "$WPvsE" ]; then
    echo "Error: Make sure to specify all arguments."
    usage
fi
name="${WPvsJet}_${WPvsMu}_${WPvsE}"
folder="/eos/user/j/jmalvaso/HighPt/${era}/datacards_${name}"


cd "${folder}" || exit

# Check existence of required files
check_file_existence "munu_${era}.txt"
check_file_existence "taunu_${name}_${era}.txt"

# Combine W*->mu+v and W*->tau+v cards
combineCards.py "munu_${era}.txt" "taunu_${name}_${era}.txt" > "tauID_${name}.txt"
# Creating workspace
combineTool.py -M T2W -o "tauID_${name}.root" -i "tauID_${name}.txt"
# Doing fit
combineTool.py -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --robustFit 1 --rMin 0 --rMax 3 -m 200 -d "tauID_${name}.root" --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1 -v 2
# Renaming output
mv "fitDiagnostics.Test.root" "tauID_${name}_fit.root"
# Running impacts
# combineTool.py -M Impacts -d "tauID_${name}.root" --robustFit 1 --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 --doInitialFit -m 200
# combineTool.py -M Impacts -d "tauID_${name}.root" --robustFit 1 --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 --doFits -m 200 
# Plotting impacts
# combineTool.py -M Impacts -d "tauID_${name}.root" -o "impacts_${name}.json" -m 200
# plotImpacts.py -i "impacts_${name}.json" -o "impacts_${name}"
echo "Leaving folder ${folder}"
cd - || exit
