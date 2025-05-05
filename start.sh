#!/bin/sh
echo "Starting API server on port 8080"
uvicorn api.main:app --host 0.0.0.0 --port 8080