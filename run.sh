#!/bin/bash

SERVICE=${1:-api_core}

# Global Settings
PORT_API=${PORT:-7860}
HOST="0.0.0.0"

# Color helpers
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

function start_service() {
    case "$1" in
        compress)
            echo -e "${GREEN}▶ Starting Compress API service...${NC}"
            uvicorn services.compress_service.main:router --host $HOST --port 8001
            ;;
        ocr)
            echo -e "${GREEN}▶ Starting OCR API service...${NC}"
            uvicorn services.ocr_service.main:router --host $HOST --port 8002
            ;;
        convert)
            echo -e "${GREEN}▶ Starting Convert API service...${NC}"
            uvicorn services.convert_service.main:router --host $HOST --port 8003
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
            uvicorn services.telegram_bot.file_server:app --host $HOST --port 8888
            ;;
        streamlit)
            echo -e "${GREEN}▶ Starting Streamlit UI (port 8501)...${NC}"
            streamlit run web/streamlit_ui.py --server.port $PORT_API --server.address $HOST
            ;;
        cli)
            echo -e "${GREEN}▶ Running CLI help (dev)...${NC}"
            python cli/smartdoc_cli.py --help
            ;;
        all)
            echo -e "${GREEN}▶ Starting All Services (api_core + telegram)...${NC}"
            uvicorn app:app --host $HOST --port $PORT_API &
            python services/telegram_bot/bot.py &
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
