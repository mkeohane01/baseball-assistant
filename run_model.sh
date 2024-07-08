#!/bin/bash

# Function to check if a file exists and download it if it does not
download_if_not_exists() {
    local url=$1
    local output=$2
    if [ ! -f "$output" ]; then
        mkdir llamafiles/
        echo "Downloading $output..."
        curl -L -o "$output" "$url"
    else
        echo "$output already exists, skipping download."
    fi
}

# Download the llamafile executable if it does not exist
download_if_not_exists "https://github.com/Mozilla-Ocho/llamafile/releases/download/0.6/llamafile-0.6" "llamafiles/llamafile.exe"

# Download the GGUF file if it does not exist
download_if_not_exists "https://huggingface.co/TheBloke/NexusRaven-V2-13B-GGUF/resolve/main/nexusraven-v2-13b.Q4_K_M.gguf" "llamafiles/nexusraven-v2-13b.gguf"

# Make the executable file executable
chmod +x llamafile.exe

# Run the model
./llamafile.exe -m llamafiles/nexusraven-v2-13b.gguf
