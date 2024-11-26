#!/bin/bash


# List all directories matching the pattern
directories=$(ls -d submission/crab_projects/crab_limits_m1000_negRL_3M_exp_singleBin_combB*)

# Loop through each directory and run crab status -d
for dir in $directories; do
    echo "Running crab status -d on directory: $dir"
    crab status -d "$dir"
done

