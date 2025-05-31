#!/usr/bin/env bash
set -e
mkdir -p ../models
echo "Downloading XTTS v2 weights..."
# Placeholder URL - replace with official mirror
curl -L -o ../models/xtts-v2.zip https://huggingface.co/path/to/xtts-v2/resolve/main/xtts-v2.zip
echo "Downloading Bark weights..."
curl -L -o ../models/bark.zip https://huggingface.co/path/to/bark/resolve/main/bark.zip
echo "Done. Unzip in models/ directory."
