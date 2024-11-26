#!/bin/bash

# Prompt for configuration name
read -p "Enter configuration name (e.g., mumu_2LB): " config_name

# Prompt for channel name
read -p "Enter channel name (e.g., numInt_final_posLL_mumu_exp_combB_crab): " channel_name

# Fetch list of timestamps from remote directory
remote_base_dir="davs://eos.cms.rcac.purdue.edu:9000/store/user/amkaur/limits/${config_name}/${channel_name}/test/"
timestamps=$(gfal-ls "$remote_base_dir")

# Create single local base directory
local_base_dir="results_${config_name}_${channel_name}"
mkdir -p "$local_base_dir"

# Get current timestamp
current_timestamp=$(date +"%y%m%d_%H%M%S")

# Create local directory with current timestamp
local_timestamp_dir="${local_base_dir}/${current_timestamp}/"
mkdir -p "$local_timestamp_dir"

# Loop through each timestamp and copy files
for timestamp in $timestamps; do
    remote_dir="${remote_base_dir}/${timestamp}/0000/"

    # List files in remote directory
    files=$(gfal-ls "$remote_dir")

    # Copy each file individually
    for file in $files; do
        remote_file="${remote_dir}/${file}"
        local_file="${local_timestamp_dir}/${file}"

        echo "Copying file $remote_file to $local_file ..."
        gfal-copy "$remote_file" "$local_file"

        echo "File copied successfully."
    done

    echo "Files copied successfully for timestamp: $timestamp"
done

echo "All files copied successfully into $local_timestamp_dir."

