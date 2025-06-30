#!/usr/bin/env bash

# Download Chrome version 123
echo "📥 Downloading Chrome 123..."
mkdir -p chrome
curl -sSL https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.105/linux64/chrome-linux64.zip -o chrome.zip
unzip chrome.zip -d chrome

# Download matching ChromeDriver 123
echo "📥 Downloading ChromeDriver 123..."
mkdir -p chromedriver
curl -sSL https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.105/linux64/chromedriver-linux64.zip -o chromedriver.zip
unzip chromedriver.zip -d chromedriver

echo "✅ Chrome and ChromeDriver 123 setup complete"
