# 🚀 RGB CAMERA DETECTION SYSTEM - QUICK START & PREVIEW

## ⚡ One-Command Setup

Copy and paste this in your terminal:

```bash
cd /workspaces/RGB && python3 -m venv venv && source venv/bin/activate && pip install -r backend/requirements.txt -q && echo "✓ Backend setup complete" && cd frontend && npm install -q && echo "✓ Frontend setup complete" && cd ..
```

---

## 📋 Step-by-Step Setup

### Step 1: Create Virtual Environment
```bash
cd /workspaces/RGB
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Python Dependencies
```bash
pip install -r backend/requirements.txt
```
**Time**: ~2-3 minutes (first time, installs YOLOv8)

### Step 3: Create Configuration File
```bash
cat > .env << 'EOF'
SENDER_EMAIL=karivaradhan7@gmail.com
SENDER_PASSWORD=your-16-char-gmail-app-password
RTSP_URL=rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101
ALERT_RECIPIENTS=karivaradhan7@gmail.com
VITE_SUPABASE_URL=
VITE_SUPABASE_SUPABASE_ANON_KEY=
EOF
```

### Step 4: Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

---

## 🎯 Launch System (3 Terminals)

### Terminal 1: Start Backend Server
```bash
source venv/bin/activate
cd backend
python main.py
```

**Expected Output:**
```
============================================================
RGB CAMERA DETECTION SYSTEM
============================================================
Camera: rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101
Alert Email: karivaradhan7@gmail.com
Recipients: karivaradhan7@gmail.com
Mode: With Email
============================================================

[*] Loading YOLO model...
[✓] Model loaded
INFO:     Started server process [XXXXX]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2: Start Frontend Server
```bash
source venv/bin/activate
cd frontend
npm run dev
```

**Expected Output:**
```
  VITE v4.5.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

### Terminal 3: Test the System
```bash
# Check health
curl http://localhost:8000/health

# Start camera stream
curl -X POST http://localhost:8000/start_stream

# Test email alert
curl -X POST http://localhost:8000/send_test_email \
  -H "Content-Type: application/json" \
  -d '["karivaradhan7@gmail.com"]'

# Check detections
curl http://localhost:8000/get_detections
```

---

## 🌐 Dashboard Preview

**Open in Browser**: http://localhost:5173

### Dashboard Screens:

**1. Live Detection Dashboard**
```
┌─────────────────────────────────────────────┐
│  📹 Live Detection Dashboard                │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │                                     │   │
│  │   LIVE VIDEO STREAM                │   │
│  │   (RTSP Camera Feed)                │   │
│  │                                     │   │
│  │   🟩 Person: 2 detected            │   │
│  │   🟦 Animal: 0 detected            │   │
│  │   🟥 Vehicle: 1 detected           │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ⏸ Stop Stream │ 🔄 Refresh                │
└─────────────────────────────────────────────┘
```

**2. Alert Settings**
```
┌─────────────────────────────────────────────┐
│  ⚙️  Alert Settings                         │
├─────────────────────────────────────────────┤
│                                             │
│  Email Recipients:                          │
│  ☑ karivaradhan7@gmail.com                 │
│                                             │
│  [+ Add Email]  [Test Email]               │
│                                             │
│  Alert History:                             │
│  ─────────────────────────────────────────  │
│  ⏰ 14:30:45 | Person Detection | Count: 2 │
│  📧 Email sent to karivaradhan7@gmail.com  │
│                                             │
│  ⏰ 14:29:12 | Vehicle Detection | Count: 1│
│  📧 Email sent to karivaradhan7@gmail.com  │
│                                             │
└─────────────────────────────────────────────┘
```

**3. Rule Creation**
```
┌─────────────────────────────────────────────┐
│  📋 Rule Creation                           │
├─────────────────────────────────────────────┤
│                                             │
│  Rule Name: [Person Alert________]         │
│                                             │
│  Detection Type:                            │
│  ○ Person  ○ Animal  ○ Vehicle             │
│                                             │
│  Alert Threshold: [1▼]                     │
│  (Alert when count exceeds threshold)      │
│                                             │
│  [Create Rule]  [Cancel]                   │
│                                             │
│  Active Rules:                              │
│  ✓ Person Detection (threshold: 1)         │
│  ✓ Vehicle Detection (threshold: 2)        │
│  ✓ Animal Detection (threshold: 1)         │
│                                             │
│  [Delete] Person Detection                 │
│                                             │
└─────────────────────────────────────────────┘
```

**4. Camera Configuration**
```
┌─────────────────────────────────────────────┐
│  📷 Camera Configuration                    │
├─────────────────────────────────────────────┤
│                                             │
│  Source Type:                               │
│  ⦿ RTSP Stream  ○ Webcam  ○ Video File    │
│                                             │
│  RTSP URL:                                  │
│  [rtsp://admin:Mahesh@2025@103.59...] │
│                                             │
│  [Test Connection]  [Configure]            │
│                                             │
│  Connection Status: ✓ Connected            │
│  Resolution: 640×480                       │
│  FPS: 7-10 (CPU processing)                │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 📊 API Endpoints Preview

### Health Check
```bash
$ curl http://localhost:8000/health
```
**Response:**
```json
{
  "status": "ok",
  "streaming": true,
  "detections": {
    "person": 2,
    "animal": 0,
    "vehicle": 1,
    "timestamp": "2025-12-11T14:30:45.123456"
  },
  "connected_clients": 1
}
```

### Create Detection Rule
```bash
$ curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Person Alert",
    "object_type": "person",
    "threshold": 1
  }'
```
**Response:**
```json
{
  "status": "success",
  "rule_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Get Detections
```bash
$ curl http://localhost:8000/get_detections
```
**Response:**
```json
{
  "person": 2,
  "animal": 0,
  "vehicle": 1,
  "timestamp": "2025-12-11T14:30:45.123456"
}
```

### Get Alerts
```bash
$ curl http://localhost:8000/get_alerts?limit=10
```
**Response:**
```json
[
  {
    "timestamp": "2025-12-11T14:30:45",
    "rule_name": "Person Detection",
    "object_type": "person",
    "count": 2,
    "message": "Alert: Person Detection - person count (2) exceeded threshold (1)"
  },
  {
    "timestamp": "2025-12-11T14:29:12",
    "rule_name": "Vehicle Detection",
    "object_type": "vehicle",
    "count": 1,
    "message": "Alert: Vehicle Detection - vehicle count (1) exceeded threshold (0)"
  }
]
```

---

## 📧 Email Alert Preview

**Subject**: 🚨 INTRUDER ALERT: Person Detection

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ SECURITY ALERT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rule: Person Detection
Detection Type: PERSON
Count Detected: 2
Time: 2025-12-11 14:30:45
Camera: Camera 3 (RTSP)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A detection event has been triggered.
Please check your system immediately.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Camera Monitoring System - Automated Alert
```

---

## 🎥 Backend Console Output Preview

```
============================================================
RGB CAMERA DETECTION SYSTEM
============================================================
Camera: rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101
Alert Email: karivaradhan7@gmail.com
Recipients: karivaradhan7@gmail.com
Mode: With Email
============================================================

[*] Loading YOLO model...
[✓] Model loaded
INFO:     Started server process [12345]
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

[POST /start_stream] 
[*] Starting stream from: rtsp
[*] Connecting to RTSP: rtsp://admin:Mahesh@2025@...
[*] Starting stream processing...
[*] Frame 0: {'person': 0, 'animal': 0, 'vehicle': 0}
[*] Frame 30: {'person': 1, 'animal': 0, 'vehicle': 0}
[*] Frame 60: {'person': 2, 'animal': 0, 'vehicle': 0}
[*] Frame 90: {'person': 2, 'animal': 0, 'vehicle': 1}
[✓] EMAIL SENT to karivaradhan7@gmail.com | Person Detection | person×2 | 14:30:45
[+] WebSocket client connected. Total clients: 1
[*] Frame 120: {'person': 2, 'animal': 0, 'vehicle': 1}
[*] Frame 150: {'person': 1, 'animal': 0, 'vehicle': 1}
...
```

---

## ⌚ Real-Time Monitoring View

As the system runs, you'll see real-time updates:

**Terminal Output**:
```
[*] Frame 300: {'person': 2, 'animal': 0, 'vehicle': 0}
[✓] EMAIL SENT to karivaradhan7@gmail.com | Person Detection | person×2 | 14:32:15
[+] WebSocket broadcast: frame 300, detections updated
[*] Frame 330: {'person': 2, 'animal': 0, 'vehicle': 1}
[*] Frame 360: {'person': 1, 'animal': 0, 'vehicle': 1}
```

**Dashboard Updates** (Real-time):
- 🟩 Person count: 0 → 1 → 2
- 🟥 Vehicle count: 0 → 1
- 📧 Alert received and displayed
- ⏰ Timestamp updates every frame
- 🎬 Live video stream continuous

---

## 🧪 Testing Workflow

### 1. Verify Setup
```bash
curl http://localhost:8000/                    # API info
curl http://localhost:8000/health              # System health
```

### 2. Test Camera Connection
```bash
curl -X POST http://localhost:8000/test_connection \
  -H "Content-Type: application/json" \
  -d '{"source_type": "rtsp", "rtsp_url": "rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101"}'
```

### 3. Start Stream
```bash
curl -X POST http://localhost:8000/start_stream
```

### 4. Create Rules
```bash
curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d '{"name": "Person Alert", "object_type": "person", "threshold": 1}'
```

### 5. Test Email
```bash
curl -X POST http://localhost:8000/send_test_email \
  -H "Content-Type: application/json" \
  -d '["karivaradhan7@gmail.com"]'
```

### 6. Monitor Detections
```bash
# In a loop
watch -n 1 'curl -s http://localhost:8000/get_detections | jq .'
```

---

## 📱 Dashboard URL

**Open in Browser:**
```
http://localhost:5173
```

**Available Screens:**
- 📺 Live Detection Dashboard
- ⚙️ Camera Configuration
- 📋 Rule Creation
- 🔔 Alert Settings

---

## 🔧 Troubleshooting Quick Fixes

### Port 8000 already in use?
```bash
lsof -i :8000
kill -9 <PID>
```

### Port 5173 already in use?
```bash
lsof -i :5173
kill -9 <PID>
```

### Backend won't start?
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check dependencies
pip list | grep -E "fastapi|opencv|ultralytics"
```

### Frontend won't load?
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Camera won't connect?
```bash
# Test RTSP directly
ffmpeg -rtsp_transport tcp -i "rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101" -t 5 -f null -
```

---

## ✅ Success Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Dashboard loads and displays live video
- [ ] Detection counts show (0 initially)
- [ ] Can create detection rules
- [ ] Test email arrives in inbox
- [ ] Camera stream processes frames
- [ ] Alerts show on dashboard
- [ ] Terminal shows detection logs

---

## 🎉 System Ready!

Your **RGB Camera Detection System** is now set up and ready to:

✅ Monitor Camera 3 in real-time  
✅ Detect persons, animals, vehicles  
✅ Send email alerts  
✅ Display live dashboard  
✅ Track detections  

**Next Step**: Open http://localhost:5173 and start monitoring! 🚀

---

**Camera**: rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101  
**Alert Email**: karivaradhan7@gmail.com  
**Backend**: http://localhost:8000  
**Frontend**: http://localhost:5173  
**Status**: Ready to Deploy ✅
