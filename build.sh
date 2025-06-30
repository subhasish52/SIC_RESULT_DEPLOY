#!/usr/bin/env bash

# Install real headless Chrome (not chromium)
echo "Installing Chrome for headless mode..."
apt-get update
apt-get install -y wget unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

echo "✅ Chrome installed successfully"
