#!/bin/sh
echo "Starting API server on port $PORT"
uvicorn api.main:app --host 0.0.0.0 --port ${PORT}