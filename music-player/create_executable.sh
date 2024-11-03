#!/bin/bash

# Set the script name and paths
SCRIPT_NAME="music_player.py"  # Replace with your script name
VENV_DIR="venv"
DIST_DIR="dist"
EXE_NAME="music_player"  # Replace with desired executable name

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install pygame pyinstaller

# Check if the script exists
if [[ ! -f $SCRIPT_NAME ]]; then
    echo "Error: Script $SCRIPT_NAME not found!"
    exit 1
fi

# Build the executable with PyInstaller
echo "Creating executable..."
pyinstaller --onefile --name $EXE_NAME $SCRIPT_NAME

# Check if the build was successful
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to create executable."
    deactivate
    exit 1
fi

# Deactivate the virtual environment
deactivate

# Move the executable to a specific location if needed
echo "Moving executable to $DIST_DIR..."
mv $DIST_DIR/$EXE_NAME ./

# Clean up build files
echo "Cleaning up build files..."
rm -rf build $DIST_DIR $SCRIPT_NAME.spec $VENV_DIR

echo "Executable created successfully: ./$EXE_NAME"