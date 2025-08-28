#!/usr/bin/env python3
"""Test script to verify all imports work correctly"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import google.generativeai as genai
        print("✅ google-generativeai imported successfully")
    except ImportError as e:
        print(f"❌ google-generativeai failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"❌ PyPDF2 failed: {e}")
        return False
    
    # Test environment
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print("✅ GOOGLE_API_KEY found in environment")
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            print("✅ Gemini AI configured successfully")
        except Exception as e:
            print(f"⚠️  Gemini AI configuration warning: {e}")
    else:
        print("⚠️  GOOGLE_API_KEY not found - add to .env file")
    
    return True

if __name__ == "__main__":
    if test_imports():
        print("\n🎉 All imports successful! You can run the server.")
        print("Run: python simple_server.py")
    else:
        print("\n❌ Some imports failed. Try:")
        print("pip install -r requirements_backup.txt")
