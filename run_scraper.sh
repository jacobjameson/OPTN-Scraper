#!/bin/bash

# This script sets up a Python virtual environment and runs the scraper

# Define the path of the virtual environment
VENV_DIR="venv"

echo "Checking if virtual environment exists..."
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found, creating one..."
    # Create virtual environment
    python3 -m venv $VENV_DIR
fi

echo "Activating the virtual environment..."
# Activate the virtual environment
source $VENV_DIR/bin/activate

echo "Installing dependencies..."
# Install dependencies
pip install -r requirements.txt

echo "Running the scraper..."
# Run the scraper script
python3 src/scraper.py

echo "Deactivating the virtual environment..."
# Deactivate the virtual environment
deactivate

echo "Scraper has finished running."
