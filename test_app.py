import requests
import time
import os

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"
FILE_PATH = os.path.join("data", "TSLA-Q2-2025-Update.pdf")
QUERY = "Provide a comprehensive financial analysis of this document, including key metrics, an investment recommendation, and a risk assessment."

def run_test():
    """
    Runs a full test of the financial analyzer API.
    """
    print("--- Starting Financial Analyzer Test ---")

    # --- Step 1: Upload the document and start the analysis ---
    try:
        print(f"\n[1] Uploading document: {FILE_PATH}")
        with open(FILE_PATH, "rb") as f:
            files = {'file': (os.path.basename(FILE_PATH), f, 'application/pdf')}
            data = {'query': QUERY}
            response = requests.post(f"{BASE_URL}/analyze", files=files, data=data)

        if response.status_code == 202:
            task_id = response.json().get("task_id")
            print(f"✅ Analysis started successfully! Task ID: {task_id}")
        else:
            print(f"❌ Error starting analysis: {response.status_code} - {response.text}")
            return

    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED to connect to the server at {BASE_URL}. Is it running?")
        print(f"   Error: {e}")
        return
    except FileNotFoundError:
        print(f"❌ FAILED to find the test file at {FILE_PATH}. Make sure it exists.")
        return

    # --- Step 2: Poll for the result ---
    print("\n[2] Waiting for result (checking every 5 seconds)...")
    start_time = time.time()
    while True:
        try:
            result_response = requests.get(f"{BASE_URL}/results/{task_id}")
            result_data = result_response.json()
            
            status = result_data.get("status")
            print(f"   Status: {status}")

            if status == "SUCCESS":
                end_time = time.time()
                print(f"\n✅ SUCCESS! Analysis completed in {end_time - start_time:.2f} seconds.")
                print("\n--- FINAL ANALYSIS REPORT ---")
                print(result_data.get("result"))
                break
            elif status == "FAILURE":
                end_time = time.time()
                print(f"\n❌ FAILED! Analysis failed after {end_time - start_time:.2f} seconds.")
                print(f"   Error details: {result_data.get('result')}")
                break
            
            time.sleep(5) # Wait 5 seconds before checking again

        except requests.exceptions.RequestException as e:
            print(f"❌ FAILED to poll for results. Error: {e}")
            break

if __name__ == "__main__":
    run_test()