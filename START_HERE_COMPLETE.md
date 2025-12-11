# 🚀 RGB CAMERA DETECTION SYSTEM - START HERE

## Quick Overview

This system monitors **Camera 3** (RTSP stream) and sends **email alerts** when persons/objects are detected.

- **Camera**: Camera 3 (rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101)
- **Alert Email**: karivaradhan7@gmail.com
- **Detection Types**: Persons, Animals, Vehicles
- **Real-time**: Live dashboard with WebSocket streaming

## ⚡ 5-Minute Quick Start

### Step 1: Setup Environment (3 minutes)

```bash
cd /workspaces/RGB
python3 setup_quick.py
```

**What it does:**
- Creates Python virtual environment
- Installs all dependencies (YOLO, OpenCV, FastAPI, etc.)
- Creates `.env` configuration file
- Installs frontend packages

### Step 2: Configure Gmail (2 minutes)

Edit `.env` file in the project root:

```bash
SENDER_EMAIL=karivaradhan7@gmail.com
SENDER_PASSWORD=xxxx-xxxx-xxxx-xxxx  # 16-char App Password
RTSP_URL=rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101
ALERT_RECIPIENTS=karivaradhan7@gmail.com
```

**How to get Gmail App Password:**
1. Go to [Google Account](https://myaccount.google.com/security)
2. Click "2-Step Verification" and enable it
3. Then click "App Passwords"
4. Select "Mail" and "Windows Computer"
5. Copy the 16-character password
6. Paste in `.env` as `SENDER_PASSWORD`

### Step 3: Start Backend

```bash
source venv/bin/activate
cd backend
python main.py
```

**Expected output:**
```
============================================================
RGB CAMERA DETECTION SYSTEM
============================================================
Camera: rtsp://admin:Mahesh@2025@103.59.107.2:554/...
Alert Email: karivaradhan7@gmail.com
Recipients: karivaradhan7@gmail.com
Mode: With Email
============================================================

INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Start Frontend (in new terminal)

```bash
source venv/bin/activate
cd frontend
npm run dev
```

Open: **http://localhost:5173**

## 🎯 How It Works

```
RTSP Camera Stream
        ↓
   OpenCV (read frames)
        ↓
   YOLOv8 (detect objects)
        ↓
   Tracker (track across frames)
        ↓
   Rules Engine
        ├→ Email Alert → Gmail SMTP → karivaradhan7@gmail.com
        ├→ WebSocket → Frontend
        └→ Database → Supabase (optional)
```

## 📊 Live Dashboard

After starting, go to **http://localhost:5173**

**You'll see:**
- ✅ Live video stream from camera
- ✅ Real-time detection counts (persons, animals, vehicles)
- ✅ Detection boxes on video
- ✅ Recent alerts history
- ✅ Rule configuration

## 🔧 Creating Detection Rules

### Via Web Dashboard

1. Go to **Rule Creation** tab
2. Enter rule name: "Person Detection"
3. Select object type: "person"
4. Set threshold: 1 (alert when 1+ persons detected)
5. Click Save

### Via API

```bash
curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Person Detection",
    "object_type": "person",
    "threshold": 1
  }'
```

## 📧 Testing Email Alerts

### Via API

```bash
curl -X POST http://localhost:8000/send_test_email \
  -H "Content-Type: application/json" \
  -d '["karivaradhan7@gmail.com"]'
```

Check your email inbox for test alert!

### What Alert Email Looks Like

```
Subject: 🚨 INTRUDER ALERT: Person Detection

⚠️ SECURITY ALERT

Rule: Person Detection
Detection Type: PERSON
Count Detected: 2
Time: 2025-12-11 14:30:45
Camera: Camera 3 (RTSP)
```

## 🎛️ Backend API Documentation

All endpoints run on **http://localhost:8000**

### Stream Control
```bash
POST /start_stream           # Start processing camera
POST /stop_stream            # Stop processing
GET /get_detections          # Get current counts
GET /health                  # Check system status
```

### Rules Management
```bash
POST /create_rule            # Create detection rule
GET /get_rules               # Get all rules
DELETE /delete_rule/{id}     # Delete rule
```

### Alerts
```bash
GET /get_alerts              # Get alert history
POST /configure_alerts       # Set email recipients
POST /send_test_email        # Send test email
```

### Configuration
```bash
POST /configure_camera       # Set camera source
POST /test_connection        # Test camera connection
```

### Live Stream
```
WebSocket ws://localhost:8000/ws/stream
```

## 🚨 Troubleshooting

### Issue: Camera won't connect

**Solution:**
```bash
# Test RTSP URL directly
ffmpeg -rtsp_transport tcp -i rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101 -t 5 -f null -

# Or check backend logs
```

### Issue: Emails not sending

**Check:**
1. `.env` has `SENDER_PASSWORD` set (not empty)
2. Gmail 2FA is enabled
3. Using App Password (not regular password)
4. Check backend console for errors

**Test:**
```bash
curl -X POST http://localhost:8000/send_test_email \
  -H "Content-Type: application/json" \
  -d '["karivaradhan7@gmail.com"]'
```

### Issue: Frontend won't load

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Issue: Port 8000 already in use

```bash
# Kill existing process
lsof -i :8000
kill -9 <PID>

# Then restart
python main.py
```

## 📁 Project Structure

```
RGB/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── tracker.py           # Object tracking
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── screens/         # Dashboard pages
│   │   ├── api.js
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── .env                     # Configuration (create this!)
├── setup_quick.py           # Automated setup
└── README.md
```

## 📋 Checklist

- [ ] Ran `python3 setup_quick.py`
- [ ] Created `.env` with Gmail App Password
- [ ] Started backend (`python main.py`)
- [ ] Started frontend (`npm run dev`)
- [ ] Opened http://localhost:5173
- [ ] Created a detection rule
- [ ] Sent test email
- [ ] See live camera stream

## 🎓 Learning Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [OpenCV Documentation](https://docs.opencv.org/)

## 💡 Tips

1. **Lower detection threshold** for more sensitive alerts
2. **Adjust frame processing** speed for better performance
3. **Use webcam** for testing instead of RTSP
4. **Check logs** - Backend prints debug info to console
5. **Restart backend** after changing `.env`

## 🆘 Need Help?

1. Check backend console for error messages
2. Test RTSP camera connection separately
3. Verify Gmail 2FA and App Password
4. Check `.env` file has all required values
5. Look at full [README.md](README.md) for advanced setup

## 🎉 You're All Set!

Your system is now ready to:
- ✅ Monitor Camera 3 in real-time
- ✅ Detect persons, animals, vehicles
- ✅ Send email alerts instantly
- ✅ View live dashboard
- ✅ Track detections over time

**Next**: Go to **http://localhost:5173** and start monitoring!

---

**Camera**: rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101  
**Alert Email**: karivaradhan7@gmail.com  
**Status**: Ready to deploy 🚀
