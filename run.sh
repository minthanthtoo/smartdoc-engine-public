#!/bin/bash

#SERVICE=${1:-api_core}
SERVICE=${1:-${SERVICE_NAME:-all}}

# === 🌐 Load ENV
ENV_FILE=".env.local"
[[ "$ENV" == "production" ]] && ENV_FILE=".env.prod"
export $(grep -v '^#' "$ENV_FILE" | xargs)

# === 🧠 Determine Mode & Host
if [[ "$ENV" == "production" ]]; then
    MODE="prod"
    HOST=${HOST:-"0.0.0.0"}
else
    MODE="dev"
    HOST="127.0.0.1"
fi

# === 🧪 Helper: extract port from URL
extract_port() {
    local url=$1
    echo "$url" | sed -nE 's@.*:(//)?[^:/]+:([0-9]+).*@\2@p'
}

# === 🔢 Assign Ports Based on Mode
if [[ "$MODE" == "prod" ]]; then
    PORT_CONVERT=$PORT
    PORT_COMPRESS=$PORT
    PORT_OCR=$PORT
    PORT_API=$PORT
    PORT_FILE_SERVER=$PORT
else
    PORT_CONVERT=$(extract_port "$CONVERT_API_URL")
    PORT_COMPRESS=$(extract_port "$COMPRESS_API_URL")
    PORT_OCR=$(extract_port "$OCR_API_URL")
    PORT_API=7860
    PORT_FILE_SERVER=8080
fi

# === 🎨 Color helpers
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
echo -e "${MODE}, ${HOST}; ${PORT}; conv:${PORT_CONVERT}; com:${PORT_COMPRESS}; ocr:${PORT_OCR}; api:${PORT_API}; file:${PORT_FILE_SERVER}"
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
            streamlit run web/streamlit_ui.py --server.port=$PORT_API --server.address=$HOST
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
        *)
            echo -e "${RED}❌ Unknown service: '$SERVICE'${NC}"
            echo "Usage: bash run.sh [compress|ocr|convert|api_core|telegram|streamlit|cli|all]"
            exit 1
            ;;
    esac
}

start_service "$SERVICE"