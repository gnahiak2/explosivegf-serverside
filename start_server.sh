#!/bin/bash
# Start Flask server for Explosive Girlfriend AI

cd "$(dirname "$0")"

# Check if port 8888 is already in use
if lsof -ti:8888 > /dev/null 2>&1; then
    echo "Port 8888 is already in use. Killing existing processes..."
    lsof -ti:8888 | xargs kill -9 2>/dev/null
    sleep 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Make sure GEMINI_API_KEY is set."
    echo "You can create .env file with: echo 'GEMINI_API_KEY=your_key_here' > .env"
fi

# Start the server
echo "Starting Flask server on http://localhost:8888"
source venv/bin/activate && python server.py

