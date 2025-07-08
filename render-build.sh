#!/usr/bin/env bash

# Upgrade pip to the latest version
pip install --upgrade pip

# Install all dependencies using binary wheels (faster, avoids build errors)
pip install --only-binary=:all: -r requirements.txt
