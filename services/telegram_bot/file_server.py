import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# === 📁 File Storage Root
FILE_DIR = os.getenv("FILE_SERVER_ROOT", "/tmp")

# === 🚀 FastAPI App Initialization
app = FastAPI(title="SmartDoc File Server")

# === 🌐 Enable CORS (for cross-origin access, e.g., Telegram bot / web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with a specific frontend domain
    allow_methods=["GET"],
    allow_headers=["*"],
)

# === 📎 Serve Files by Name
@app.get("/files/{filename}")
async def get_file(filename: str):
    # ✅ Avoid path traversal (e.g., '../../etc/passwd')
    safe_filename = os.path.basename(filename)
    path = os.path.join(FILE_DIR, safe_filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path, filename=safe_filename)