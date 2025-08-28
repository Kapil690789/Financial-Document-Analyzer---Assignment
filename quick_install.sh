#!/bin/bash
# Quick installation script for macOS ARM

echo "Installing system dependencies..."
# Install numpy via conda (more reliable on ARM Mac)
pip install --upgrade pip

# Try installing with no-deps first, then dependencies
pip install --no-deps crewai==0.28.8
pip install --no-deps langchain-google-genai==1.0.10

# Install core dependencies
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
pip install pypdf==3.17.1
pip install pydantic==2.5.0

# Try numpy with different approach
pip install --only-binary=all numpy || pip install --pre --only-binary=all numpy

echo "Installation complete!"
