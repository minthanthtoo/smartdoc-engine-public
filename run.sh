#!/bin/bash

# === 🚦 Detect or set service
SERVICE=${1:-${SERVICE_NAME:-all}}

# === 🌐 Load ENV file
ENV=${ENV:-local}
ENV_FILE=".env.${ENV}"
[[ ! -f "$ENV_FILE" && -f ".env" ]] && ENV_FILE=".env"
if [[ ! -f "$ENV_FILE" ]]; then
    echo "❌ ENV file '$ENV_FILE' not found."
    exit 1
fi
export $(grep -v '^#' "$ENV_FILE" | xargs)

# === 🧠 Host & Mode
HOST=${HOST:-127.0.0.1}
MODE="multi"
[[ "$ENV" == "monolith" ]] && MODE="monolith"
[[ "$ENV" == "production" ]] && HOST="0.0.0.0"

# === 🔧 Port fallback
PORT_API=${PORT_API:-7860}
PORT_CONVERT=${PORT_CONVERT:-8003}
PORT_COMPRESS=${PORT_COMPRESS:-8001}
PORT_OCR=${PORT_OCR:-8002}
PORT_FILE_SERVER=${PORT_FILE_SERVER:-8080}

# === 🛡️ Expose unified PORT for PaaS (e.g., RENDER/REPLIT)
export PORT=${PORT:-$PORT_API}

# === 🎨 Color helpers
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}ENV: $ENV | MODE: $MODE | HOST: $HOST${NC}"
echo -e "${GREEN}▶️ $SERVICE | Ports: OCR=$PORT_OCR | Compress=$PORT_COMPRESS | Convert=$PORT_CONVERT | API=$PORT_API${NC}"
echo -e "${SERVICE};${MODE}//${HOST}:${PORT}; conv:${PORT_CONVERT}; com:${PORT_COMPRESS}; ocr:${PORT_OCR}; api:${PORT_API}; file:${PORT_FILE_SERVER}"

# === 🚀 Start Selected Service
function start_service() {
    case "$1" in
        compress)
            echo -e "${GREEN}▶ Starting Compress API service...${NC}"
            uvicorn services.compress_service.main:router --host $HOST --port $PORT_COMPRESS
            ;;
        ocr)
            echo -e "${GREEN}▶ Starting OCR API service...${NC}"
            uvicorn services.ocr_service.main:router --host $HOST --port $PORT_OCR
            ;;
        convert)
            echo -e "${GREEN}▶ Starting Convert API service...${NC}"
            uvicorn services.convert_service.main:router --host $HOST --port $PORT_CONVERT
            ;;
        api_core)
            echo -e "${GREEN}▶ Starting Full API Core (all routes)...${NC}"
            uvicorn app:app --host $HOST --port $PORT_API
            ;;
        telegram)
            echo -e "${GREEN}▶ Starting Telegram Bot...${NC}"
            python services/telegram_bot/bot.py 
            ;;
        file_server)
            echo -e "${GREEN}▶ Starting File Server (FastAPI)...${NC}"
            export FILE_SERVER_ROOT=./tmp
            mkdir -p ./tmp
            uvicorn services.telegram_bot.file_server:app --host $HOST --port $PORT_FILE_SERVER
            ;;
        streamlit)
            echo -e "${GREEN}▶ Starting Streamlit UI (port 8501)...${NC}"
            PYTHONPATH=. streamlit run web/streamlit_ui.py --server.port=$PORT_API --server.address=$HOST
            ;;
        cli)
            echo -e "${GREEN}▶ Running CLI help (dev)...${NC}"
            python cli/smartdoc_cli.py --help
            ;;
        all)
            echo -e "${GREEN}▶ Starting ALL SmartDoc Services...${NC}"

            uvicorn services.compress_service.main:router --host $HOST --port $PORT_COMPRESS &
            echo -e "${GREEN}🧱 Compress API started on port $PORT_COMPRESS${NC}"

            uvicorn services.ocr_service.main:router --host $HOST --port $PORT_OCR &
            echo -e "${GREEN}🔤 OCR API started on port $PORT_OCR${NC}"

            uvicorn services.convert_service.main:router --host $HOST --port $PORT_CONVERT &
            echo -e "${GREEN}🔄 Convert API started on port $PORT_CONVERT${NC}"

            uvicorn services.telegram_bot.file_server:app --host $HOST --port $PORT_FILE_SERVER &
            echo -e "${GREEN}🗂️ File Server started on port $PORT_FILE_SERVER${NC}"

            uvicorn app:app --host $HOST --port $PORT_API &
            echo -e "${GREEN}🧠 Core API started on port $PORT_API${NC}"

            python services/telegram_bot/bot.py &
            echo -e "${GREEN}🤖 Telegram Bot started${NC}"

            wait
            ;;
        monolith)
            echo -e "${GREEN}▶ Starting monolith app with mounted routers...${NC}"
            uvicorn app:app --host $HOST --port $PORT_API
            ;;
        *)
            echo -e "${RED}❌ Unknown service: '$SERVICE'${NC}"
            echo "Usage: bash run.sh [compress|ocr|convert|api_core|telegram|streamlit|cli|all]"
            exit 1
            ;;
    esac
}

# === 🔁 Auto-switch to monolith if ENV=monolith or RENDER/REPLIT
if [[ "$ENV" == "monolith" || "$SERVICE" == "monolith" ]]; then
    start_service monolith
else
    start_service "$SERVICE"
fi