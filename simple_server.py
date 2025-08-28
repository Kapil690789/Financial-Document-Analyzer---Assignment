#!/usr/bin/env python3
import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import tempfile
import traceback

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    import PyPDF2
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Please install: pip install google-generativeai python-dotenv PyPDF2")
    sys.exit(1)

# Load environment variables
load_dotenv()

class FinancialAnalyzer:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"
    
    def analyze_document(self, text):
        """Analyze financial document using Gemini AI"""
        prompt = f"""
        As a financial analyst, analyze this document and provide:
        
        1. DOCUMENT TYPE: Identify what type of financial document this is
        2. KEY METRICS: Extract important financial figures and ratios
        3. FINANCIAL HEALTH: Assess the financial health based on the data
        4. RISKS: Identify potential financial risks
        5. RECOMMENDATIONS: Provide actionable investment recommendations
        
        Document text:
        {text[:4000]}  # Limit text to avoid token limits
        
        Provide a structured analysis in JSON format.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {
                "status": "success",
                "analysis": response.text,
                "document_length": len(text)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "document_length": len(text)
            }

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.analyzer = FinancialAnalyzer()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Financial Document Analyzer</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .container { background: #f5f5f5; padding: 20px; border-radius: 8px; }
                    .result { background: white; padding: 15px; margin-top: 20px; border-radius: 5px; }
                    button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
                    button:hover { background: #0056b3; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Financial Document Analyzer</h1>
                    <p>Upload a PDF financial document for AI-powered analysis</p>
                    
                    <form action="/analyze" method="post" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".pdf" required>
                        <br><br>
                        <button type="submit">Analyze Document</button>
                    </form>
                    
                    <div class="result">
                        <h3>API Status: ✅ Ready</h3>
                        <p>System is configured and ready to analyze financial documents.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "service": "Financial Document Analyzer"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        if self.path == '/analyze':
            try:
                # Parse multipart form data (simplified)
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                    # Extract PDF data from multipart (simplified approach)
                    boundary = self.headers['Content-Type'].split('boundary=')[1]
                    parts = post_data.split(f'--{boundary}'.encode())
                    
                    for part in parts:
                        if b'Content-Type: application/pdf' in part:
                            pdf_data = part.split(b'\r\n\r\n', 1)[1].rstrip(b'\r\n')
                            temp_file.write(pdf_data)
                            break
                    
                    temp_file_path = temp_file.name
                
                # Extract text and analyze
                text = self.analyzer.extract_text_from_pdf(temp_file_path)
                result = self.analyzer.analyze_document(text)
                
                # Clean up
                os.unlink(temp_file_path)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result, indent=2).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {
                    "status": "error",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
                self.wfile.write(json.dumps(error_response).encode())

def main():
    try:
        # Test configuration
        analyzer = FinancialAnalyzer()
        print("✅ Configuration successful!")
        print("✅ Google Gemini AI connected")
        
        # Start server
        server = HTTPServer(('localhost', 8000), RequestHandler)
        print("\n🚀 Financial Document Analyzer Server Started!")
        print("📍 Open: http://localhost:8000")
        print("📍 API Health: http://localhost:8000/health")
        print("⏹️  Press Ctrl+C to stop\n")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure your .env file contains: GOOGLE_API_KEY=your_api_key")

if __name__ == "__main__":
    main()
