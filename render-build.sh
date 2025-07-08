#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Downloading similarity.pkl for the app..."
python app.py --download-only
