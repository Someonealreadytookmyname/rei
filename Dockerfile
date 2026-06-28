# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV HOSTED=true

# Set working directory
WORKDIR /app

# Install system dependencies (needed to compile ChromaDB dependency hnswlib if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker build cache
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create directories for default/local persistent storage
RUN mkdir -p /app/storage /app/chroma_db

# Expose port
EXPOSE 8000

# Command to run the application using the PORT env variable provided by Render/Railway
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}
