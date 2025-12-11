# QUICK START - YOUR CAMERA MONITORING

## Your Configuration

Camera RTSP URL: `rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101`
Alert Email: `karivaradhan7@gmail.com`

## FASTEST WAY TO START (2 Minutes)

### Terminal 1 - Backend

```bash
cd /tmp/cc-agent/61354207/project/backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Wait for: `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2 - Frontend

```bash
cd /tmp/cc-agent/61354207/project/frontend
npm install
npm run dev
```

Wait for: `Local: http://localhost:5173/`

### Browser Setup (1 Minute)

1. Open: http://localhost:5173
2. Click "Camera Setup" tab
3. Select "RTSP Stream"
4. Enter URL: `rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101`
5. Click "Test Connection"
6. Click "Start Stream"

### Configure Alerts (30 Seconds)

1. Click "Alert Settings" tab
2. Enter email: `karivaradhan7@gmail.com`
3. Click "Add"
4. Click "Send Test Email"

### Create Detection Rule (30 Seconds)

1. Click "Detection Rules" tab
2. Rule Name: "Camera 3 Monitoring"
3. Object Type: "Person"
4. Threshold: 1 (alert if any person detected)
5. Click "Create Rule"

### Watch Live Detection

1. Click "Live Dashboard" tab
2. See real-time video from your camera
3. Detection boxes will appear on persons/animals/vehicles
4. Email alerts will be sent when rules trigger

## What Gets Detected

- Persons (human detection)
- Animals (dogs, cats, birds, etc.)
- Vehicles (cars, trucks, motorcycles, bicycles)

## How Alerts Work

- When person count exceeds threshold = 1
- Email sent to karivaradhan7@gmail.com
- Alert appears in Live Dashboard
- Alert stored in database

## Troubleshooting

### Camera Connection Failed

Check if camera is reachable:
```bash
ffmpeg -i "rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101" -frames:v 1 test.jpg
```

Or use VLC player to test the RTSP stream.

### Backend Port Already in Use

Change port:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

Then update frontend to use port 8001 in `frontend/src/api.js`

### Email Not Sending

For now, emails are logged to console. To enable real SMTP:

Create `backend/.env` file:
```
SENDER_EMAIL=your-gmail@gmail.com
SENDER_PASSWORD=your-app-password
```

Get Gmail app password: https://support.google.com/accounts/answer/185833

## System is Running When You See:

- Backend console: "Uvicorn running on http://0.0.0.0:8000"
- Frontend console: "Local: http://localhost:5173/"
- Browser: Live video feed with detection boxes
- Detection counters updating in real-time

## READY TO GO!

Your camera monitoring system is fully configured for Camera 3.
Just follow the steps above and you'll be tracking intruders in 3 minutes.
