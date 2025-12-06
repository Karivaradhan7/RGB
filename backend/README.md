# Intruder Detection System - Backend

FastAPI backend for real-time object detection using YOLOv8.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`

## Features

- YOLOv8 object detection (Person/Animal/Vehicle)
- Multiple camera sources (Webcam/RTSP/Upload)
- Real-time detection results via WebSocket
- Custom detection rules with thresholds
- Email alert notifications
- REST API for all operations

## Configuration

Optional `.env` file for email:
```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```
