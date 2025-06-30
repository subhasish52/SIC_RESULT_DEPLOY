#!/usr/bin/env bash

# Update the package list
apt-get update

# Install Chromium and ChromeDriver
apt-get install -y chromium chromium-driver

# Optional: Verify installation
chromium --version
chromedriver --version
