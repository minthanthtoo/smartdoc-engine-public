FROM python:3.11-slim

# Accept build-time argument for service-specific installs
ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

# Set working dir
WORKDIR /app

# Copy everything
COPY . /app

# Always needed tools
RUN apt-get update && \
    apt-get install -y ghostscript curl software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# Conditional install for convert tools
RUN if [ "$SERVICE_NAME" = "convert" ]; then \
      apt-get update && \
      apt-get install -y libreoffice pandoc && \
      rm -rf /var/lib/apt/lists/*; \
    fi

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint always runs script
ENTRYPOINT ["bash", "run.sh"]

# Default command (can be overridden by CMD or in Render)
CMD ["all"]