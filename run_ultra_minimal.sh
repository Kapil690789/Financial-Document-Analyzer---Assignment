#!/bin/bash

echo "🔧 Installing ultra minimal dependencies..."
pip install -r requirements_ultra_minimal.txt

echo "🚀 Starting Financial Document Analyzer..."
python main_ultra_minimal.py
