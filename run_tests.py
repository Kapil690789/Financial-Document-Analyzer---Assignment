#!/usr/bin/env python3
"""
Simple test runner script
"""

import subprocess
import sys
import os

def run_system_tests():
    """Run the system validation tests"""
    print("Running Financial Document Analyzer System Tests...")
    print("-" * 60)
    
    try:
        # Run the test script
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def check_requirements():
    """Check if requirements are installed"""
    print("Checking requirements...")
    
    try:
        import crewai
        import fastapi
        import langchain_google_genai
        import langchain_community
        import dotenv
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    print("Financial Document Analyzer - Test Runner")
    print("=" * 60)
    
    # Check requirements first
    if not check_requirements():
        return False
    
    # Run system tests
    return run_system_tests()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n❌ Tests failed. Please check the output above.")
    sys.exit(0 if success else 1)
