# services/api_core/main.py
import os
import secrets
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from services.compress_service.main import router as compress_router
from services.ocr_service.main import router as ocr_router
from services.convert_service.main import router as convert_router

# Step 1: Load base .env always
load_dotenv(".env")

# Step 2: Load override if ENV is set
ENV = os.getenv("ENV", "local").lower()
env_override = f".env.{ENV}"
if os.path.exists(env_override):
    load_dotenv(env_override, override=True)

# Now re-read after loading full env
api_key = os.getenv("API_KEY")
ENV_FILE = env_file

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

# Check environment and API_KEY presence
if ENV == "production":
    if not api_key:
        api_key = secrets.token_urlsafe(32)
        print("🔐 [PROD] No API_KEY found, generated new one:")
        print(f"👉 {api_key}\n")
        save_to_env("API_KEY", api_key)
else:
    if not api_key:
        api_key = "secret123"
        print("⚠️ [DEV] No API_KEY found, using fallback 'secret123'")
        save_to_env("API_KEY", api_key)
    else:
        print("🔐 [DEV] Loaded API_KEY from environment")
    print(f"👉 {api_key}\n")

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

app.include_router(compress_router, prefix="/api/v1")
app.include_router(ocr_router, prefix="/api/v1")
app.include_router(convert_router, prefix="/api/v1")