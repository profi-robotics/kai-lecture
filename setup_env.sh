#!/bin/bash

# This script sets up and activates a virtual environment for the lecture
# It also installs the necessary dependencies and registers the environment as a Jupyter kernel

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install ipykernel to allow the virtual environment to be used in Jupyter
echo "Setting up Jupyter kernel..."
pip install ipykernel

# Register the virtual environment as a Jupyter kernel
python -m ipykernel install --user --name=robotics_vision --display-name="Python (Robotics Vision)"

echo ""
echo "Setup complete! Virtual environment is now active and registered with Jupyter."
echo ""
echo "To use this environment in Jupyter notebooks:"
echo "1. Launch Jupyter: jupyter notebook"
echo "2. Open your notebook"
echo "3. Select Kernel > Change kernel > Python (Robotics Vision)"
echo ""
echo "To use this environment in terminal:"
echo "source venv/bin/activate  # On macOS/Linux"
echo "venv\\Scripts\\activate    # On Windows"
echo ""

# Create a template .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating template .env file for API keys..."
    echo "# Environment variables for the Robotics Vision project" > .env
    echo "# Replace the placeholder with your actual API key" >> .env
    echo "ROBOFLOW_API_KEY=your_api_key_here" >> .env
    echo "" >> .env
    echo ".env file created. Edit this file to add your actual API keys."
    echo "IMPORTANT: Never commit this file to version control!"
fi
