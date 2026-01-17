#!/bin/bash
cd "$(dirname "$0")"

if lsof -ti:8888 > /dev/null 2>&1; then
    echo "Port 8888 in use, killing existing process..."
    lsof -ti:8888 | xargs kill -9
    sleep 1
fi

source venv/bin/activate

echo "Starting Gunicorn on 0.0.0.0:8888"
echo "Public URL: http://18.143.187.4:8888"

gunicorn \
  --bind 0.0.0.0:8888 \
  --workers 2 \
  server:app
