import os
from celery import Celery
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor, llm
from task import analyze_financial_document, investment_analysis, risk_assessment, verification
from tools import financial_document_tool

load_dotenv()

celery_app = Celery(
    'tasks',
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client.financial_analyzer_db
results_collection = db.analysis_results

def run_financial_crew(query: str, file_path: str):
    """Initializes and runs the financial analysis crew."""
    try:
        financial_crew = Crew(
            agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
            tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
            process=Process.sequential,
            memory=True,  # This is the correct way to enable context sharing
            verbose=True,
            manager_llm=llm
        )

        # The line "verification.shared = True" has been removed as it is no longer supported.

        result = financial_crew.kickoff({'query': query, 'file_path': file_path})
        return result
    except Exception as e:
        print(f"Error running financial crew: {e}")
        return {"error": str(e)}

@celery_app.task
def process_document_task(query: str, file_path: str, original_filename: str):
    """
    Celery task to process a document, run the AI crew, and save to MongoDB.
    """
    print(f"Starting analysis for: {original_filename}")
    
    financial_document_tool.file_path = file_path
    
    analysis_result = run_financial_crew(query=query, file_path=file_path)
    
    db_entry = {
        "filename": original_filename,
        "query": query,
        "analysis_output": str(analysis_result),
        "status": "completed",
        "created_at": datetime.now(timezone.utc)
    }
    
    try:
        results_collection.insert_one(db_entry)
        print(f"Successfully saved analysis for {original_filename} to MongoDB.")
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleaned up temporary file: {file_path}")
            
    return str(analysis_result)