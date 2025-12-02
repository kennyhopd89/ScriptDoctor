#!/bin/bash

# Script Doctor Pro - macOS Launcher
# Double-click this file to start the app

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Clear terminal and show header
clear
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "       🎬 Script Doctor Pro - AI Assistant"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}✗ Virtual environment not found!${NC}"
    echo ""
    echo "Please run the installation script first:"
    echo "  Double-click: install_macos.sh"
    echo "  OR run: ./install_macos.sh"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}[1/4] Activating virtual environment...${NC}"
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to activate virtual environment${NC}"
    read -p "Press Enter to exit..."
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Load environment variables from .env file
echo -e "${BLUE}[2/4] Loading configuration...${NC}"

if [ -f ".env" ]; then
    # Export variables from .env file
    export $(grep -v '^#' .env | xargs)
    echo -e "${GREEN}✓ Configuration loaded${NC}"
else
    echo -e "${BLUE}ℹ No .env file found (you can add API key in the app)${NC}"
fi

# Check if API key is configured
if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  ℹ API Key Setup${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "No Gemini API key found in configuration."
    echo ""
    echo "You have two options:"
    echo "  1. Enter it in the app's sidebar after launch (recommended for first-time)"
    echo "  2. Configure it now in the .env file"
    echo ""
    read -p "Would you like to configure it now? [y/N]: " config_now
    
    if [ "$config_now" = "y" ] || [ "$config_now" = "Y" ]; then
        echo ""
        echo "Get your API key from: https://ai.google.dev/"
        echo ""
        read -p "Enter your Gemini API Key: " api_key
        
        if [ ! -z "$api_key" ]; then
            echo "GEMINI_API_KEY=$api_key" >> .env
            export GEMINI_API_KEY=$api_key
            echo -e "${GREEN}✓ API key saved${NC}"
        fi
    else
        echo -e "${BLUE}ℹ You can add the API key in the app's sidebar${NC}"
    fi
    echo ""
fi

echo ""

# Check if Streamlit is installed
echo -e "${BLUE}[3/4] Checking dependencies...${NC}"

if ! python -c "import streamlit" 2>/dev/null; then
    echo -e "${RED}✗ Streamlit is not installed${NC}"
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt --quiet
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies installed${NC}"
    else
        echo -e "${RED}✗ Failed to install dependencies${NC}"
        echo "Please run install_macos.sh again"
        read -p "Press Enter to exit..."
        exit 1
    fi
else
    echo -e "${GREEN}✓ All dependencies are ready${NC}"
fi

echo ""

# Start the app
echo -e "${BLUE}[4/4] Starting Script Doctor Pro...${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  The app will open in your browser automatically"
echo "  To stop the app, press Ctrl+C in this window"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run Streamlit
streamlit run app.py

# Cleanup on exit
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  App stopped${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Thank you for using Script Doctor Pro!"
echo ""
read -p "Press Enter to close this window..."
