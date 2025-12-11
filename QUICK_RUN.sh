#!/bin/bash

echo "=========================================="
echo "  INTRUDER DETECTION - QUICK START"
echo "=========================================="
echo ""

RTSP_URL="rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101"
ALERT_EMAIL="karivaradhan7@gmail.com"

echo "Camera: $RTSP_URL"
echo "Alert Email: $ALERT_EMAIL"
echo ""

cd /tmp/cc-agent/61354207/project/backend

echo "1/3 Installing backend dependencies..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Trying without --quiet..."
    pip install -r requirements.txt
fi

echo ""
echo "2/3 Starting backend server..."
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:5173"
echo ""
echo "NEXT STEPS:"
echo "1. Keep this terminal running"
echo "2. Open a NEW terminal and run:"
echo "   cd /tmp/cc-agent/61354207/project/frontend && npm install && npm run dev"
echo "3. Open browser: http://localhost:5173"
echo "4. Click 'Camera Setup' tab"
echo "5. Select 'RTSP Stream'"
echo "6. URL is already configured: $RTSP_URL"
echo "7. Click 'Start Stream'"
echo ""
echo "=========================================="
echo ""

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
