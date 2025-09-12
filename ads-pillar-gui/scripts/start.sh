#!/bin/bash
# This script starts the ADS Pillar GUI application

# Navigate to the directory containing the application
cd "$(dirname "$0")/../.."

# Activate the virtual environment if needed
# source venv/bin/activate

# Run the GUI application
python3 Files/gui_app.py