#!/bin/bash
WP=$1
folder=$2

./scripts/CombineCardsHighPT_Eras.bash ${WP} ${folder}
./scripts/CreateWorkspace.bash tauID_${WP} ${folder}
./scripts/RunCombineMultiDimGroupsEras.bash ${WP} ${folder}
