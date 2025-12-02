#!/bin/bash

# Script Doctor Pro - Setup & Launch Script (Mac/Linux)

echo "====================================================="
echo "       SCRIPT DOCTOR PRO - AI ASSISTANT"
echo "====================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

echo "[1/4] Python version:"
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "[2/4] Creating virtual environment..."
    python3 -m venv .venv
else
    echo "[2/4] Virtual environment already exists."
fi

# Activate virtual environment
echo "[3/4] Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade dependencies
echo "[4/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "---------------------------------------------------"
echo "  Starting Script Doctor Pro..."
echo "  Press Ctrl+C to stop the application"
echo "---------------------------------------------------"
echo ""

# Run the application
streamlit run app.py

# Deactivate virtual environment on exit
deactivate
