import os
import tempfile
from typing import Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(
    title="Financial Document Analyzer",
    description="AI-powered financial document analysis using Google Gemini",
    version="1.0.0"
)

class FinancialAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name
            
            # Extract text using pypdf
            reader = PdfReader(tmp_file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            return text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error extracting PDF text: {str(e)}")
    
    def analyze_financial_document(self, text: str) -> Dict[str, Any]:
        """Analyze financial document using Google Gemini"""
        try:
            prompt = f"""
            As a financial expert, analyze this financial document and provide insights:

            Document Text:
            {text[:4000]}  # Limit text to avoid token limits

            Please provide analysis in the following areas:
            1. Document Type and Purpose
            2. Key Financial Metrics
            3. Revenue Analysis
            4. Risk Assessment
            5. Investment Recommendations
            6. Summary and Conclusions

            Format your response as a structured analysis.
            """
            
            response = self.model.generate_content(prompt)
            
            return {
                "analysis": response.text,
                "document_type": "Financial Document",
                "status": "completed",
                "confidence": "high"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")

# Initialize analyzer
analyzer = FinancialAnalyzer()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Financial Document Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze - POST endpoint for document analysis",
            "health": "/health - Health check endpoint",
            "docs": "/docs - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Financial Document Analyzer"}

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """
    Analyze a financial document (PDF format)
    
    Returns comprehensive financial analysis including:
    - Document type identification
    - Key financial metrics
    - Risk assessment
    - Investment recommendations
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Extract text from PDF
        text = analyzer.extract_text_from_pdf(file_content)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
        
        # Analyze the document
        analysis_result = analyzer.analyze_financial_document(text)
        
        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "file_size": len(file_content),
            "text_length": len(text),
            "analysis": analysis_result
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Check if API key is configured
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  WARNING: GOOGLE_API_KEY not found in environment variables")
        print("Please add your Google API key to the .env file")
        exit(1)
    
    print("🚀 Starting Financial Document Analyzer API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Test endpoint: http://localhost:8000/analyze")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
