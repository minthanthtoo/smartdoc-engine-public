FROM python:3.11-slim

# Accept build-time argument for service-specific installs
ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app

# Always-needed tools + libmagic for python-magic
RUN apt-get update && \
    apt-get install -y \
    ghostscript \
    curl \
    file \
    libmagic1 libmagic-dev \
    software-properties-common \
    fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

# Conditional installs for Convert and OCR services
RUN if [ "$SERVICE_NAME" = "convert" ] || [ "$SERVICE_NAME" = "streamlit" ]; then \
      echo "Installing convert tools for $SERVICE_NAME"; \
      apt-get update && \
      apt-get install -y libreoffice pandoc && \
      rm -rf /var/lib/apt/lists/*; \
    fi && \
    if [ "$SERVICE_NAME" = "ocr" ] || [ "$SERVICE_NAME" = "streamlit" ]; then \
      echo "Installing OCR tools for $SERVICE_NAME"; \
      apt-get update && \
      apt-get install -y tesseract-ocr tesseract-ocr-eng && \
      tesseract --version && \
      rm -rf /var/lib/apt/lists/*; \
    fi

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint always runs your multi-service runner script
ENTRYPOINT ["bash", "run.sh"]

# Default command (overridden by CMD or passed args)
CMD []