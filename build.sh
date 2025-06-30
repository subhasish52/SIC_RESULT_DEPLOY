#!/usr/bin/env bash
set -e

# Create bin directory
mkdir -p bin
cd bin

# ✅ Download Chromium (stable from Playwright)
curl -Lo chrome-linux.zip https://github.com/macchrome/winchrome/releases/download/v114.0.5735.91-r1103743-Win64/chrome-win.zip

# This is a Windows zip, use this instead:
curl -LO https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1174245/chrome-linux.zip
curl -LO https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1174245/chromedriver_linux64.zip

# Unzip both archives
unzip chrome-linux.zip
unzip chromedriver_linux64.zip

cd ..
