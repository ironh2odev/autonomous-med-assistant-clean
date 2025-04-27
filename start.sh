#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")"

# Activate the virtual environment
source .venv/bin/activate

# Open backend in new Terminal tab
osascript <<EOF
tell application "Terminal"
    do script "cd $(pwd); source .venv/bin/activate; uvicorn api.main:app --reload"
end tell
EOF

# Wait a second to let backend start
sleep 2

# Open frontend (Streamlit) in current Terminal
streamlit run ui/app.py
