#!/bin/bash

# Define arrays for the different parameters
#years=("2018" "2017" "2016_pre" "2016_post")
years=("2016")
regions=("BE")
bins=("OneB")

# Loop over each combination of year, region, and bin
for year in "${years[@]}"; do
  for region in "${regions[@]}"; do
    for bin in "${bins[@]}"; do
      
      # Construct the .txt file name based on the combination
      #dataCard="dataCards_mumu_2LB_exp_testing_singleBin/dimuon_${year}_${region}_${bin}_6_negLL.txt"
      dataCard="dataCards_mumu_2LB_exp_testing_singleBin/dimuon_${year}_10_negLL_shape.txt"
      
      # Check if the file exists before running the combine command
      if [[ -f "$dataCard" ]]; then
        echo "Running combine for ${year}, ${region}, ${bin}..."
        
        # Run the combine command
        combine -M MarkovChainMC "$dataCard" -n te2016 -m 10 -i 3000000 --tries 2 --prior flat --rMax 40 -v1
        
      else
        echo "File not found: $dataCard"
      fi
      
    done
  done
done

