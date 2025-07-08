#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Downloading similarity.pkl..."
curl -L -o similarity.pkl "https://drive.google.com/uc?export=download&id=1eaRn28XCyrjwzAhWfB_C8yNHtRSNK3Mi"
