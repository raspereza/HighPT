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
check_file_existence "taunu_${name}_lowpt_${era}.txt"
check_file_existence "taunu_${name}_highpt_${era}.txt"

combineCards.py munu_${era}.txt taunu_${name}_lowpt_${era}.txt taunu_${name}_highpt_${era}.txt > tauID_${name}_ptbinned.txt

combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/*_highpt_${era}:r_highpt[1,0,2]"' --PO '"map=^.*/*_lowpt_${era}:r_lowpt[1,0,2]"' -o tauID_${name}_ptbinned.root -i tauID_${name}_ptbinned.txt 

combineTool.py -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL --redefineSignalPOIs r_lowpt,r_highpt --robustFit 1 -m 200 -d tauID_${name}_ptbinned.root --cminDefaultMinimizerTolerance 0.1 --cminDefaultMinimizerStrategy 1 -v 2

mv fitDiagnostics.Test.root tauID_${name}_ptbinned_fit.root
rm higgsCombine*

cd -
