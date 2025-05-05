# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install system packages needed for torch/dgl
RUN apt-get update && apt-get install -y build-essential python3-dev git \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean

# Copy app code
COPY . .

# Expose the dynamic port
EXPOSE 8080

# ✅ Use shell command so $PORT expands
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port $PORT"]
