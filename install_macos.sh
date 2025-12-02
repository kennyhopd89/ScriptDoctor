#!/bin/bash

# Script Doctor Pro - macOS Installation Script
# This script sets up the complete environment for non-technical users

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Clear screen and show welcome message
clear
print_header "Script Doctor Pro - macOS Installation"
echo "This installer will set up everything you need to run the app."
echo "The process will take about 5-10 minutes."
echo ""
read -p "Press Enter to continue..."

# Step 1: Check macOS version
print_header "Step 1/6: Checking macOS Version"
MACOS_VERSION=$(sw_vers -productVersion)
print_info "Detected macOS version: $MACOS_VERSION"

# Check if version is compatible (macOS 10.15+)
MAJOR_VERSION=$(echo $MACOS_VERSION | cut -d. -f1)
MINOR_VERSION=$(echo $MACOS_VERSION | cut -d. -f2)

if [ "$MAJOR_VERSION" -lt 10 ] || ([ "$MAJOR_VERSION" -eq 10 ] && [ "$MINOR_VERSION" -lt 15 ]); then
    print_error "This app requires macOS 10.15 (Catalina) or later."
    exit 1
fi

print_success "macOS version is compatible"

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    print_info "Detected Apple Silicon (M1/M2/M3) Mac"
    BREW_PATH="/opt/homebrew/bin/brew"
else
    print_info "Detected Intel Mac"
    BREW_PATH="/usr/local/bin/brew"
fi

# Step 2: Check and install Homebrew
print_header "Step 2/6: Checking Homebrew"

if command -v brew &> /dev/null; then
    print_success "Homebrew is already installed"
    BREW_CMD="brew"
elif [ -f "$BREW_PATH" ]; then
    print_success "Homebrew found at $BREW_PATH"
    BREW_CMD="$BREW_PATH"
else
    print_warning "Homebrew is not installed"
    echo ""
    echo "Homebrew is required to install Python and other dependencies."
    echo "Would you like to install it now? (This is safe and recommended)"
    echo ""
    read -p "Install Homebrew? [Y/n]: " install_brew
    
    if [ -z "$install_brew" ] || [ "$install_brew" = "y" ] || [ "$install_brew" = "Y" ]; then
        print_info "Installing Homebrew... (this may take 5-10 minutes)"
        echo ""
        
        # Install Homebrew
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for this session
        if [ "$ARCH" = "arm64" ]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
            BREW_CMD="/opt/homebrew/bin/brew"
        else
            eval "$(/usr/local/bin/brew shellenv)"
            BREW_CMD="/usr/local/bin/brew"
        fi
        
        print_success "Homebrew installed successfully"
    else
        print_error "Installation cancelled. Please install Homebrew manually from:"
        echo "https://brew.sh"
        exit 1
    fi
fi

# Step 3: Check and install Python
print_header "Step 3/6: Checking Python"

REQUIRED_PYTHON_VERSION="3.10"

# Check if Python 3.10+ is available
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        print_success "Python $PYTHON_VERSION is installed and compatible"
        PYTHON_CMD="python3"
    else
        print_warning "Python $PYTHON_VERSION found, but version 3.10+ is required"
        INSTALL_PYTHON=true
    fi
else
    print_warning "Python 3 is not installed"
    INSTALL_PYTHON=true
fi

if [ "$INSTALL_PYTHON" = true ]; then
    print_info "Installing Python 3.11 via Homebrew..."
    $BREW_CMD install python@3.11
    
    # Add Python to PATH
    if [ "$ARCH" = "arm64" ]; then
        export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"
    else
        export PATH="/usr/local/opt/python@3.11/bin:$PATH"
    fi
    
    PYTHON_CMD="python3.11"
    print_success "Python 3.11 installed successfully"
fi

# Verify Python installation
if ! command -v $PYTHON_CMD &> /dev/null; then
    print_error "Python installation failed. Please install Python 3.10+ manually."
    exit 1
fi

# Step 4: Create virtual environment
print_header "Step 4/6: Creating Virtual Environment"

if [ -d ".venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? [y/N]: " recreate_venv
    
    if [ "$recreate_venv" = "y" ] || [ "$recreate_venv" = "Y" ]; then
        print_info "Removing old virtual environment..."
        rm -rf .venv
    else
        print_info "Using existing virtual environment"
    fi
fi

if [ ! -d ".venv" ]; then
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
python -m pip install --upgrade pip --quiet

print_success "Virtual environment is ready"

# Step 5: Install Python dependencies
print_header "Step 5/6: Installing Dependencies"

if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found!"
    exit 1
fi

print_info "Installing Python packages (this may take 2-3 minutes)..."
echo ""

pip install -r requirements.txt

print_success "All dependencies installed successfully"

# Step 6: Configure API Key
print_header "Step 6/6: Configuring Gemini API Key"

echo "To use this app, you need a Google Gemini API Key."
echo ""
echo "If you don't have one yet:"
echo "  1. Visit: https://ai.google.dev/"
echo "  2. Click 'Get API Key in Google AI Studio'"
echo "  3. Sign in with your Google account"
echo "  4. Create an API key and copy it"
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    if grep -q "GEMINI_API_KEY=" .env; then
        print_info "API key configuration already exists in .env file"
        read -p "Do you want to update it? [y/N]: " update_key
        
        if [ "$update_key" != "y" ] && [ "$update_key" != "Y" ]; then
            print_info "Keeping existing API key"
            API_CONFIGURED=true
        fi
    fi
fi

if [ "$API_CONFIGURED" != true ]; then
    echo ""
    read -p "Do you have your Gemini API Key ready? [Y/n]: " has_key
    
    if [ -z "$has_key" ] || [ "$has_key" = "y" ] || [ "$has_key" = "Y" ]; then
        echo ""
        read -p "Enter your Gemini API Key: " api_key
        
        if [ -z "$api_key" ]; then
            print_warning "No API key entered. You can configure it later in the .env file"
        else
            # Create or update .env file
            if grep -q "GEMINI_API_KEY=" .env 2>/dev/null; then
                # Update existing key
                if [ "$(uname)" = "Darwin" ]; then
                    sed -i '' "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$api_key/" .env
                else
                    sed -i "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$api_key/" .env
                fi
            else
                # Add new key
                echo "GEMINI_API_KEY=$api_key" >> .env
            fi
            
            print_success "API key saved to .env file"
        fi
    else
        print_info "You can add your API key later by:"
        echo "  1. Opening the .env file in a text editor"
        echo "  2. Adding this line: GEMINI_API_KEY=your_key_here"
        echo "  OR entering it in the app's sidebar after launch"
    fi
fi

# Make the launcher executable
print_info "Setting up launcher script..."
if [ -f "run_app_macos.command" ]; then
    chmod +x run_app_macos.command
    print_success "Launcher script is ready"
fi

# Installation complete
print_header "✓ Installation Complete!"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Setup completed successfully!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "To start using Script Doctor Pro:"
echo ""
echo "  Option 1 (Recommended):"
echo "    Double-click: run_app_macos.command"
echo ""
echo "  Option 2 (Terminal):"
echo "    Run: ./run_app_macos.command"
echo ""
echo "The app will open in your default web browser automatically."
echo ""
print_info "For detailed instructions, see README_MACOS.md"
echo ""
read -p "Would you like to start the app now? [Y/n]: " start_now

if [ -z "$start_now" ] || [ "$start_now" = "y" ] || [ "$start_now" = "Y" ]; then
    print_info "Starting Script Doctor Pro..."
    echo ""
    ./run_app_macos.command
else
    print_info "You can start the app anytime by double-clicking run_app_macos.command"
fi
