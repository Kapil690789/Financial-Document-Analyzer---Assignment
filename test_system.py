#!/usr/bin/env python3
"""
Test script to validate the Financial Document Analyzer system
"""

import os
import sys
import asyncio
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test core imports
        from crewai import Agent, Task, Crew, Process
        print("✓ CrewAI imports successful")
        
        from fastapi import FastAPI, File, UploadFile, Form
        print("✓ FastAPI imports successful")
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✓ LangChain Google GenAI imports successful")
        
        from langchain_community.document_loaders import PyPDFLoader
        print("✓ PDF processing imports successful")
        
        # Test our modules
        from tools import search_tool, financial_document_tool, investment_analysis_tool, risk_assessment_tool
        print("✓ Tools module imports successful")
        
        from agents import financial_analyst, verifier, investment_advisor, risk_assessor
        print("✓ Agents module imports successful")
        
        from task import analyze_financial_document, investment_analysis, risk_assessment, verification
        print("✓ Task module imports successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during imports: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\nTesting environment...")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        return False
    print("✓ .env file exists")
    
    # Check for Google API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("✗ GOOGLE_API_KEY not found in environment")
        return False
    elif api_key.startswith('AIzaSy') and len(api_key) > 20:
        print("✓ GOOGLE_API_KEY appears to be valid format")
    else:
        print("⚠ GOOGLE_API_KEY format may be incorrect")
    
    return True

def test_tools():
    """Test that tools can be instantiated and basic functionality works"""
    print("\nTesting tools...")
    
    try:
        from tools import financial_document_tool, investment_analysis_tool, risk_assessment_tool
        
        # Test tool instantiation
        print("✓ Tools instantiated successfully")
        
        # Test basic tool functionality with dummy data
        test_data = "Sample financial data for testing"
        
        # Test investment analysis tool
        result = investment_analysis_tool._run(test_data)
        if result and "error" not in result.lower():
            print("✓ Investment analysis tool working")
        else:
            print(f"⚠ Investment analysis tool returned: {result}")
        
        # Test risk assessment tool
        result = risk_assessment_tool._run(test_data)
        if result and "error" not in result.lower():
            print("✓ Risk assessment tool working")
        else:
            print(f"⚠ Risk assessment tool returned: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ Tool testing error: {e}")
        return False

def test_agents():
    """Test that agents can be instantiated"""
    print("\nTesting agents...")
    
    try:
        from agents import financial_analyst, verifier, investment_advisor, risk_assessor
        
        # Check agent properties
        agents = [
            ("Financial Analyst", financial_analyst),
            ("Verifier", verifier),
            ("Investment Advisor", investment_advisor),
            ("Risk Assessor", risk_assessor)
        ]
        
        for name, agent in agents:
            if hasattr(agent, 'role') and hasattr(agent, 'goal'):
                print(f"✓ {name} agent configured properly")
            else:
                print(f"✗ {name} agent missing required attributes")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Agent testing error: {e}")
        return False

def test_tasks():
    """Test that tasks can be instantiated"""
    print("\nTesting tasks...")
    
    try:
        from task import analyze_financial_document, investment_analysis, risk_assessment, verification
        
        # Check task properties
        tasks = [
            ("Analyze Financial Document", analyze_financial_document),
            ("Investment Analysis", investment_analysis),
            ("Risk Assessment", risk_assessment),
            ("Verification", verification)
        ]
        
        for name, task in tasks:
            if hasattr(task, 'description') and hasattr(task, 'expected_output'):
                print(f"✓ {name} task configured properly")
            else:
                print(f"✗ {name} task missing required attributes")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Task testing error: {e}")
        return False

def test_fastapi_app():
    """Test that FastAPI app can be instantiated"""
    print("\nTesting FastAPI application...")
    
    try:
        from main import app
        
        if hasattr(app, 'routes') and len(app.routes) > 0:
            print("✓ FastAPI app instantiated with routes")
            
            # Check for required endpoints
            route_paths = [route.path for route in app.routes if hasattr(route, 'path')]
            required_paths = ['/', '/analyze', '/health']
            
            for path in required_paths:
                if path in route_paths:
                    print(f"✓ Endpoint {path} exists")
                else:
                    print(f"✗ Endpoint {path} missing")
                    return False
        else:
            print("✗ FastAPI app not properly configured")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ FastAPI testing error: {e}")
        return False

def test_data_directory():
    """Test that data directory exists or can be created"""
    print("\nTesting data directory...")
    
    try:
        data_dir = Path("data")
        if not data_dir.exists():
            data_dir.mkdir(exist_ok=True)
            print("✓ Data directory created")
        else:
            print("✓ Data directory exists")
        
        # Test write permissions
        test_file = data_dir / "test_write.txt"
        test_file.write_text("test")
        test_file.unlink()
        print("✓ Data directory is writable")
        
        return True
        
    except Exception as e:
        print(f"✗ Data directory error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Financial Document Analyzer - System Validation")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_environment,
        test_data_directory,
        test_tools,
        test_agents,
        test_tasks,
        test_fastapi_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nTo start the system:")
        print("1. Ensure your GOOGLE_API_KEY is set in .env")
        print("2. Run: python main.py")
        print("3. Access API docs at: http://localhost:8000/docs")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
