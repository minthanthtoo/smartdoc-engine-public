FROM python:3.11-slim

# Accept build-time argument for service-specific installs
ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app

# Install always-needed tools
RUN apt-get update && \
    apt-get install -y \
    ghostscript \
    curl \
    software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# Conditional installs for OCR and Convert services
RUN if [ "$SERVICE_NAME" = "convert" ]; then \
      apt-get update && \
      apt-get install -y libreoffice pandoc && \
      rm -rf /var/lib/apt/lists/*; \
    elif [ "$SERVICE_NAME" = "ocr" ]; then \
      apt-get update && \
      apt-get install -y tesseract-ocr && \
      rm -rf /var/lib/apt/lists/*; \
    fi

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint always runs your multi-service runner script
ENTRYPOINT ["bash", "run.sh"]

# Default command (overridden by CMD or passed args)
CMD []