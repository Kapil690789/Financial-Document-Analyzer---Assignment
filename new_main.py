import os
import uuid
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from celery_tasks import process_document_task

app = FastAPI(
    title="Financial Document Analyzer - Advanced",
    description="Analyzes financial documents using an AI crew with background processing.",
    version="3.0.0" # Final Version
)

os.makedirs("data", exist_ok=True)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Document Analyzer</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background-color: #f8f9fa; }
        .container { width: 100%; max-width: 600px; padding: 2rem; background-color: white; border-radius: 12px; box-shadow: 0 4px-12px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .form-group { margin-bottom: 1.5rem; }
        label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #555; }
        input[type="file"], input[type="text"] { width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 0.85rem; border: none; border-radius: 8px; background-color: #007bff; color: white; font-size: 1rem; cursor: pointer; transition: background-color 0.2s; }
        button:hover { background-color: #0056b3; }
        .result { margin-top: 1.5rem; padding: 1rem; border-radius: 8px; text-align: left; white-space: pre-wrap; word-wrap: break-word; }
        .success { background-color: #e0f8e9; color: #28a745; }
        .error { background-color: #f8d7da; color: #721c24; }
        .loading { background-color: #e2e3e5; color: #383d41; text-align: center; }
        .final-result { background-color: #f0f4f8; color: #333; border: 1px solid #d1d9e2; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Financial Document Analyzer</h1>
        <form id="uploadForm">
            <div class="form-group">
                <label for="fileInput">Upload Financial PDF</label>
                <input type="file" id="fileInput" name="file" accept=".pdf" required>
            </div>
            <div class="form-group">
                <label for="queryInput">What do you want to analyze?</label>
                <input type="text" id="queryInput" name="query" value="Provide a comprehensive financial analysis of this document.">
            </div>
            <button type="submit" id="submitButton">Analyze Document</button>
        </form>
        <div id="result" class="result" style="display: none;"></div>
    </div>
    <script>
        const form = document.getElementById('uploadForm');
        const resultDiv = document.getElementById('result');
        const submitButton = document.getElementById('submitButton');
        let intervalId;

        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            if (intervalId) clearInterval(intervalId); // Clear any previous timers

            const formData = new FormData(form);
            resultDiv.style.display = 'block';
            resultDiv.className = 'result loading';
            resultDiv.textContent = 'Uploading and starting analysis...';
            submitButton.disabled = true;

            try {
                const response = await fetch('/analyze', { method: 'POST', body: formData });
                const data = await response.json();
                
                if (response.ok) {
                    resultDiv.className = 'result loading';
                    resultDiv.textContent = '✅ Task started. Waiting for result...';
                    // Start polling for the result
                    intervalId = setInterval(() => checkResult(data.task_id), 3000);
                } else {
                    showError(data.detail || 'Unknown error');
                }
            } catch (error) {
                showError(`Network Error: ${error.message}`);
            }
        });

        async function checkResult(taskId) {
            try {
                const response = await fetch(`/results/${taskId}`);
                const data = await response.json();

                if (data.status === 'SUCCESS') {
                    clearInterval(intervalId);
                    resultDiv.className = 'result final-result';
                    // Display only the main part of the result
                    const output = data.result.analysis_output || data.result;
                    resultDiv.textContent = "--- Analysis Complete ---\\n\\n" + output;
                    submitButton.disabled = false;
                } else if (data.status === 'FAILURE') {
                    showError('Task failed. Check Celery logs for details.');
                }
                // If still pending, the interval will just continue
            } catch (error) {
                showError(`Error fetching result: ${error.message}`);
            }
        }
        
        function showError(message) {
            clearInterval(intervalId);
            resultDiv.className = 'result error';
            resultDiv.textContent = `❌ Error: ${message}`;
            submitButton.disabled = false;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def get_ui():
    """Serves the main HTML user interface."""
    return HTMLResponse(content=HTML_CONTENT)

@app.post("/analyze", status_code=202, tags=["Analysis"])
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join("data", f"financial_document_{file_id}.pdf")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        task = process_document_task.delay(
            query=query, 
            file_path=file_path, 
            original_filename=file.filename
        )
        return JSONResponse(content={"task_id": task.id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")

# --- NEW ENDPOINT TO GET RESULTS ---
@app.get("/results/{task_id}", tags=["Analysis"])
async def get_task_result(task_id: str):
    """Fetches the result of a background analysis task."""
    task_result = process_document_task.AsyncResult(task_id)
    if task_result.ready():
        if task_result.successful():
            return {"status": "SUCCESS", "result": task_result.get()}
        else:
            return {"status": "FAILURE", "result": str(task_result.info)}
    return {"status": "PENDING"}

@app.get("/run_test", response_class=HTMLResponse, tags=["Testing"])
async def run_test_endpoint():
    """
    Triggers a full, automated test of the application and returns the result.
    """
    log = ["<h1>--- Starting Financial Analyzer Test ---</h1>"]
    BASE_URL = "http://127.0.0.1:8000"
    FILE_PATH = os.path.join("data", "TSLA-Q2-2025-Update.pdf")
    QUERY = "Provide a comprehensive financial analysis of this document."

    # Step 1: Upload and start
    try:
        log.append(f"<p>[1] Uploading document: {FILE_PATH}</p>")
        with open(FILE_PATH, "rb") as f:
            files = {'file': (os.path.basename(FILE_PATH), f, 'application/pdf')}
            data = {'query': QUERY}
            response = requests.post(f"{BASE_URL}/analyze", files=files, data=data)

        if response.status_code == 202:
            task_id = response.json().get("task_id")
            log.append(f"<p>✅ Analysis started successfully! Task ID: {task_id}</p>")
        else:
            log.append(f"<p>❌ Error starting analysis: {response.status_code} - {response.text}</p>")
            return HTMLResponse(content="".join(log))
    except Exception as e:
        log.append(f"<p>❌ FAILED to run test. Is Celery running? Error: {e}</p>")
        return HTMLResponse(content="".join(log))

    # Step 2: Poll for result
    log.append("<p>[2] Waiting for result (checking every 5 seconds)...</p>")
    start_time = time.time()
    while True:
        await asyncio.sleep(5)
        result_response = requests.get(f"{BASE_URL}/results/{task_id}")
        result_data = result_response.json()
        status = result_data.get("status")
        log.append(f"<p>   Status: {status}</p>")
        if status == "SUCCESS":
            end_time = time.time()
            log.append(f"<p>✅ SUCCESS! Analysis completed in {end_time - start_time:.2f} seconds.</p>")
            log.append("<h2>--- FINAL ANALYSIS REPORT ---</h2>")
            log.append(f"<pre>{result_data.get('result')}</pre>")
            break
        elif status == "FAILURE":
            log.append(f"<p>❌ FAILED! Check Celery logs.</p>")
            log.append(f"<pre>Error details: {result_data.get('result')}</pre>")
            break
            
    return HTMLResponse(content="".join(log))
