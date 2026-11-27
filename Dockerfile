# syntax=docker/dockerfile:1

# Use a slim Python image
FROM python:3.11-slim

# Install system dependencies required by OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default command to run the voting script
CMD ["python", "smart vote.py"]
