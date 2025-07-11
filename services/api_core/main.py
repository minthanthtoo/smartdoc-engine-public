import os
import secrets
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from services.compress_service.main import router as compress_router
from services.ocr_service.main import router as ocr_router
from services.convert_service.main import router as convert_router

# === 🔧 Load environment variables
ENV = os.getenv("ENV", "local").lower()
ENV_FILE = f".env.{ENV}"

load_dotenv(".env")
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE, override=True)

api_key = os.getenv("API_KEY")

def save_to_env(key: str, value: str):
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()
    key_found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            key_found = True
            break
    if not key_found:
        lines.append(f"{key}={value}\n")
    with open(ENV_FILE, "w") as f:
        f.writelines(lines)

# === 🔐 API Key Setup
if not api_key:
    if ENV == "production":
        api_key = secrets.token_urlsafe(32)
        print("🔐 [PROD] No API_KEY found, generated new one:")
    else:
        api_key = "secret123"
        print("⚠️ [DEV] No API_KEY found, using fallback 'secret123'")
    print(f"👉 {api_key}\n")
    save_to_env("API_KEY", api_key)
else:
    print(f"🔐 [{ENV.upper()}] Loaded API_KEY from environment: {api_key}")

# === 🚀 FastAPI App
app = FastAPI(title="SmartDoc Engine")

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path.startswith("/api"):
        token = request.headers.get("x-api-key")
        if token != api_key:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid or missing API key"}
            )
    return await call_next(request)

# === ✅ Optional health check
@app.get("/health")
async def health():
    return {"status": "ok", "env": ENV}

# === 📦 Mount APIs
app.include_router(compress_router, prefix="/api/v1")
app.include_router(ocr_router, prefix="/api/v1")
app.include_router(convert_router, prefix="/api/v1")