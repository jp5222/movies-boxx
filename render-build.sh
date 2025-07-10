#!/bin/bash

echo "Installing gdown..."
pip install gdown

echo "Downloading similarity.pkl from Google Drive..."
gdown --id 1eaRn28XCyrjwzAhWfB_C8yNHtRSNK3Mi -O similarity.pkl