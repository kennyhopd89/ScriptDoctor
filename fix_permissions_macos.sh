#!/bin/bash

# Script Doctor Pro - macOS Permission Fixer
# Run this if you get "Permission denied" errors

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Script Doctor Pro - Permission Fixer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "This script will make all launcher scripts executable."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Working directory: $SCRIPT_DIR"
echo ""

# Make scripts executable
echo "Setting permissions..."

if [ -f "install_macos.sh" ]; then
    chmod +x install_macos.sh
    echo "✓ install_macos.sh is now executable"
fi

if [ -f "run_app_macos.command" ]; then
    chmod +x run_app_macos.command
    echo "✓ run_app_macos.command is now executable"
fi

if [ -f "run_app.sh" ]; then
    chmod +x run_app.sh
    echo "✓ run_app.sh is now executable"
fi

if [ -f "fix_permissions_macos.sh" ]; then
    chmod +x fix_permissions_macos.sh
    echo "✓ fix_permissions_macos.sh is now executable"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✓ Done! All scripts are now executable."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "You can now:"
echo "  • Double-click install_macos.sh to set up the app"
echo "  • Double-click run_app_macos.command to start the app"
echo ""
