#!/bin/bash
# Start Flask server for Explosive Girlfriend AI

cd "$(dirname "$0")"

if lsof -ti:8888 > /dev/null 2>&1; then
    echo "Port 8888 in use, killing existing process..."
    lsof -ti:8888 | xargs kill -9
    sleep 1
fi

if [ ! -f .env ]; then
    echo "Warning: .env file not found. Make sure GEMINI_API_KEY is set."
fi

echo "Starting Flask server on 0.0.0.0:8888"
echo "Public URL: http://18.143.187.4:8888"

source venv/bin/activate
python server.py