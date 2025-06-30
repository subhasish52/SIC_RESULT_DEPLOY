#!/usr/bin/env bash
set -e

mkdir -p bin
cd bin

# Download Chromium
curl -fsSL https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1278065/chrome-linux.zip -o chrome-linux.zip

# Download matching ChromeDriver (latest for this build)
curl -fsSL https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1278065/chromedriver_linux64.zip -o chromedriver_linux64.zip

unzip chrome-linux.zip
unzip chromedriver_linux64.zip

cd ..
echo "✅ Chromium and Chromedriver installed"
