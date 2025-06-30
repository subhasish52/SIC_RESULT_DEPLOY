#!/usr/bin/env bash

echo "📦 Downloading headless Chrome..."
mkdir -p chrome
curl -sSL https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.105/linux64/chrome-linux64.zip -o chrome.zip
unzip chrome.zip -d chrome
echo "✅ Chrome downloaded and extracted"
