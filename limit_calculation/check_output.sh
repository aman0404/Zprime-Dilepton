#!/bin/bash

# List of ROOT files
files=(
    "higgsCombinemumu_2LB_negRL_fixed_3M_obs_singleBin_combB_negRL.MarkovChainMC.mH4.root"
    "higgsCombinemumu_2LB_negRL_fixed_3M_obs_singleBin_combB_negRL.MarkovChainMC.mH6.root"
    "higgsCombinemumu_2LB_negRL_fixed_3M_obs_singleBin_combB_negRL.MarkovChainMC.mH8.root"
    "higgsCombinemumu_2LB_negRL_fixed_3M_obs_singleBin_combB_negRL.MarkovChainMC.mH10.root"
    "higgsCombinemumu_2LB_negRL_fixed_3M_obs_singleBin_combB_negRL.MarkovChainMC.mH14.root"
    "higgsCombinemumu_2LB_negRL_fixed_3M_obs_singleBin_combB_negRL.MarkovChainMC.mH18.root"
)

# Loop through each file and execute ROOT commands
for file in "${files[@]}"
do
    echo "Processing $file"
    root -l results_mumu_2LB_negRL_fixed_3M_obs_singleBin_combB/20240918_1256/$file << EOF
limit->Scan()
.q
EOF
done

