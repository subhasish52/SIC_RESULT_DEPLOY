#!/usr/bin/env bash

# Exit immediately on error
set -e

# Create directory for binaries
mkdir -p bin
cd bin

# Download headless Chromium (Render compatible)
curl -O https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1158166/chrome-linux.zip
unzip chrome-linux.zip

# Download matching ChromeDriver
curl -O https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1158166/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

cd ..

# Export paths for reference
echo "Chromium and Chromedriver downloaded and unzipped in /bin"
