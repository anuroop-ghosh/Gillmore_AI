import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi import Request
import uvicorn
from ingest import ingest_file  # This connects to your existing logic!
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into your system memory

app = FastAPI(title="Gillmore AI Webhook Receiver")

# Create the data directory if it doesn't exist
if not os.path.exists("./data"):
    os.makedirs("./data")

@app.post("/api/ingest")
async def receive_document(request: Request):
    # n8n sends the filename in a header called 'x-file-name' or we can hardcode it
    filename = request.headers.get("x-file-name", "uploaded_file.pdf")
    print(f"📥 Received raw binary from n8n: {filename}")
    
    # Read the raw bytes directly from the request body
    binary_data = await request.body()
    
    # 1. Save the file
    file_path = os.path.join("./data", filename)
    with open(file_path, "wb") as f:
        f.write(binary_data)
        
    # 2. Trigger your existing embedding logic
    try:
        print("🧠 Starting vectorization...")
        ingest_file(file_path) 
        return {"status": "success", "message": f"{filename} processed!"}
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # This runs the API on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
