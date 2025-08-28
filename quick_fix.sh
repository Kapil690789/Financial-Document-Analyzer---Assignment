#!/bin/bash

echo "🔧 Quick Fix for Import Issues"
echo "=============================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected"
    echo "Creating new virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install minimal requirements
echo "📦 Installing minimal requirements..."
pip install -r requirements_backup.txt

# Test imports
echo "🧪 Testing imports..."
python test_imports.py

# Run server if tests pass
if [ $? -eq 0 ]; then
    echo "🚀 Starting server..."
    python simple_server.py
else
    echo "❌ Import tests failed. Check error messages above."
fi
