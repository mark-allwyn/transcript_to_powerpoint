# Single-port Docker build for AI Document Processing Suite
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose single port
EXPOSE 8503

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8503/ || exit 1

# Start unified application
CMD ["streamlit", "run", "app.py", "--server.port", "8503", "--server.address", "0.0.0.0"]
