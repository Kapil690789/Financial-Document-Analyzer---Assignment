# Simplified main.py without heavy dependencies
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Financial Document Analyzer", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running!"}

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """Simple document analysis endpoint"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Simple analysis (placeholder)
        analysis_result = {
            "filename": file.filename,
            "status": "analyzed",
            "summary": "Document processed successfully",
            "key_metrics": {
                "revenue": "Analysis pending - install full dependencies",
                "expenses": "Analysis pending - install full dependencies", 
                "profit_margin": "Analysis pending - install full dependencies"
            },
            "recommendations": [
                "Install full dependencies for complete analysis",
                "Ensure GOOGLE_API_KEY is set in .env file"
            ]
        }
        
        # Clean up temp file
        os.unlink(tmp_file_path)
        
        return JSONResponse(content=analysis_result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
