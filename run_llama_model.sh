#!/bin/bash

# Function to check if a file exists and download it if it does not
download_if_not_exists() {
    local url=$1
    local output=$2
    if [ ! -f "$output" ]; then
        mkdir -p "$(dirname "$output")"
        echo "Downloading $output..."
        curl -L -o "$output" "$url"
    else
        echo "$output already exists, skipping download."
    fi
}

# Download the Meta-Llama-3-8B-Instruct.llamafile if it does not exist
download_if_not_exists "https://huggingface.co/Mozilla/Meta-Llama-3-8B-Instruct-llamafile/resolve/main/Meta-Llama-3-8B-Instruct.Q3_K_S.llamafile" "llamafiles/Meta-Llama-3-8B-Instruct.Q3_K_S.llamafile"

# Make the Meta-Llama-3-8B-Instruct.llamafile executable
chmod +x llamafiles/Meta-Llama-3-8B-Instruct.Q3_K_S.llamafile

# Run the model
./llamafiles/Meta-Llama-3-8B-Instruct.Q3_K_S.llamafile
