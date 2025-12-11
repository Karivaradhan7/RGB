# 📺 SYSTEM PREVIEW - WHAT YOU'LL SEE WHEN RUNNING

## 🖥️ Backend Console Output (Terminal 1)

```
╔═════════════════════════════════════════════════════════════════╗
║         RGB CAMERA DETECTION SYSTEM - BACKEND STARTUP           ║
╚═════════════════════════════════════════════════════════════════╝

[*] Loading configuration from .env...
[✓] Configuration loaded
  • RTSP URL: rtsp://admin:Mahesh@2025@103.59.107.2:554/...
  • Alert Email: karivaradhan7@gmail.com
  • Recipients: karivaradhan7@gmail.com

[*] Loading YOLO model (yolov8n.pt)...
[✓] Model loaded (3.2M parameters)

[*] Initializing FastAPI application...
[✓] FastAPI initialized

INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
INFO:     Press CTRL+C to quit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Backend Ready!
   API: http://localhost:8000
   WebSocket: ws://localhost:8000/ws/stream
   Status: Waiting for requests...

```

---

## 🌐 Frontend Console Output (Terminal 2)

```
╔═════════════════════════════════════════════════════════════════╗
║           RGB CAMERA DETECTION - FRONTEND STARTUP               ║
╚═════════════════════════════════════════════════════════════════╝

  VITE v4.5.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help

➜  network:   use --host to expose

VITE v4.5.0 ready in 346 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose

[12:34:56] [vite] ✨ built in 1.5s
[12:34:57] [vite] ✨ page reload src/App.jsx

✅ Frontend Ready!
   Dashboard: http://localhost:5173
   Status: Connected to backend

```

---

## 📊 API Testing Output (Terminal 3)

### 1️⃣ Health Check Response

```bash
$ curl http://localhost:8000

{
  "message": "RGB Camera Detection System API",
  "version": "1.0.0",
  "status": "active",
  "endpoints": {
    "stream": "POST /start_stream, POST /stop_stream",
    "detections": "GET /get_detections",
    "alerts": "GET /get_alerts?limit=10",
    "rules": "POST /create_rule",
    "email": "POST /send_test_email",
    "websocket": "WS /ws/stream",
    "test": "GET /test_connection"
  }
}
```

### 2️⃣ Test Email Response

```bash
$ curl -X POST http://localhost:8000/send_test_email \
  -H "Content-Type: application/json" \
  -d '["karivaradhan7@gmail.com"]'

{
  "status": "success",
  "message": "Test email sent to 1 recipient(s)",
  "recipients": ["karivaradhan7@gmail.com"],
  "timestamp": "2025-12-11T14:23:45.123456Z"
}
```

**Backend Console** (same terminal):
```
[POST /send_test_email]
[✓] EMAIL SENT to karivaradhan7@gmail.com | Test Email | 14:23:45
[+] Response: 250 Message accepted
```

### 3️⃣ Start Stream Response

```bash
$ curl -X POST http://localhost:8000/start_stream

{
  "status": "success",
  "message": "Stream started successfully",
  "rtsp_url": "rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101",
  "timestamp": "2025-12-11T14:24:00.000000Z"
}
```

**Backend Console** (continuous output):
```
[POST /start_stream]
[*] Starting stream from: rtsp
[*] Creating VideoCapture object...
[*] Connecting to RTSP: rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101
[✓] Connected to RTSP camera
[*] Resolution: 1920×1080
[*] FPS: 30

[*] Starting frame processing loop...
[+] Frame processing started (10 FPS target)

[*] Frame 0: person=0 animal=0 vehicle=0
[*] Frame 30: person=1 animal=0 vehicle=0
[*] Frame 60: person=2 animal=0 vehicle=0

[*] Rule check: Person Detection (threshold: 1)
[!] Condition met: person count (2) >= threshold (1)
[✓] EMAIL SENT to karivaradhan7@gmail.com | Person Detection | person×2 | 14:24:15
[+] WebSocket broadcast: 2 clients connected

[*] Frame 90: person=2 animal=0 vehicle=1
[*] Frame 120: person=1 animal=0 vehicle=1
[*] Frame 150: person=0 animal=0 vehicle=1
[*] Frame 180: person=0 animal=0 vehicle=0
```

### 4️⃣ Create Rule Response

```bash
$ curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Person Alert",
    "object_type": "person",
    "threshold": 1
  }'

{
  "status": "success",
  "message": "Rule created successfully",
  "rule": {
    "rule_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Person Alert",
    "object_type": "person",
    "threshold": 1,
    "enabled": true,
    "created_at": "2025-12-11T14:25:30.123456Z"
  }
}
```

### 5️⃣ Get Detections Response

```bash
$ curl http://localhost:8000/get_detections

{
  "person": 2,
  "animal": 0,
  "vehicle": 1,
  "timestamp": "2025-12-11T14:24:30.456789Z",
  "frame_count": 150,
  "processing_time_ms": 18.5
}
```

### 6️⃣ Get Alerts Response

```bash
$ curl http://localhost:8000/get_alerts?limit=5

[
  {
    "alert_id": "abc-123-def",
    "timestamp": "2025-12-11T14:24:15.000000Z",
    "rule_id": "550e8400-e29b-41d4-a716-446655440000",
    "rule_name": "Person Detection",
    "object_type": "person",
    "count": 2,
    "threshold": 1,
    "message": "Alert: Person Detection - person count (2) exceeded threshold (1)",
    "status": "sent"
  },
  {
    "alert_id": "xyz-789-uvw",
    "timestamp": "2025-12-11T14:24:45.000000Z",
    "rule_id": "550e8400-e29b-41d4-a716-446655440001",
    "rule_name": "Vehicle Detection",
    "object_type": "vehicle",
    "count": 1,
    "threshold": 1,
    "message": "Alert: Vehicle Detection - vehicle count (1) exceeded threshold (1)",
    "status": "sent"
  }
]
```

---

## 🎬 Browser Dashboard Preview (http://localhost:5173)

### Live Detection Dashboard Screen

```
╔════════════════════════════════════════════════════════════════════════════╗
║  RGB Camera Detection System - Live Dashboard                        [⚙️]  ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─ Live Detection Feed ──────────────────────────────────────────────────────┐
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                                                                      │ │
│  │                                                                      │ │
│  │          ╔═══════════════════════════════════════════╗             │ │
│  │          ║  LIVE VIDEO STREAM (RTSP)                ║             │ │
│  │          ║  1920×1080 @ 30 FPS                       ║             │ │
│  │          ║                                            ║             │ │
│  │          ║  [Person with bounding box] ◻️             ║             │ │
│  │          ║  │                                        │ ║             │ │
│  │          ║  │  [Person] ID:1                         │ ║             │ │
│  │          ║  │  Conf: 0.94                           │ ║             │ │
│  │          ║  │                                        │ ║             │ │
│  │          ║           [Car] ◻️                         ║             │ │
│  │          ║           ID:2                            ║             │ │
│  │          ║           Conf: 0.87                      ║             │ │
│  │          ║                                            ║             │ │
│  │          ╚═══════════════════════════════════════════╝             │ │
│  │                                                                      │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ⏸ Stop Stream   🔄 Refresh   📹 Toggle View                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Real-time Detections ─────────────────────────────────────────────────────┐
│                                                                            │
│  🟩 Person:   2   [████████████ 66%]                                    │
│  🟥 Vehicle:  1   [███████ 33%]                                        │
│  🟦 Animal:   0   [░░░░░░░░░░░░░░░░░░░░ 0%]                           │
│                                                                            │
│  Last Updated: 14:24:30 (real-time)                                      │
│  Processing: 18.5ms per frame                                            │
│  WebSocket: ✓ Connected (2 clients)                                      │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Alert History ────────────────────────────────────────────────────────────┐
│                                                                            │
│  ⏰ 14:24:15  | Person Detection      | Count: 2 | ✓ Email Sent        │
│  ⏰ 14:24:45  | Vehicle Detection     | Count: 1 | ✓ Email Sent        │
│  ⏰ 14:25:30  | Person Detection      | Count: 2 | ✓ Email Sent        │
│                                                                            │
│  [Clear History]  [Export CSV]                                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Active Rules ─────────────────────────────────────────────────────────────┐
│                                                                            │
│  ✓ Person Detection        (Threshold: 1)    [Delete]                   │
│  ✓ Vehicle Detection       (Threshold: 1)    [Delete]                   │
│  ✓ Animal Detection        (Threshold: 0)    [Delete]                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Camera Configuration Screen

```
╔════════════════════════════════════════════════════════════════════════════╗
║  Camera Configuration                                                      ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─ Camera Source ────────────────────────────────────────────────────────────┐
│                                                                            │
│  Source Type:                                                              │
│  ⦿ RTSP Stream    ○ HTTP Webcam    ○ Local Webcam    ○ Video File       │
│                                                                            │
│  RTSP URL:                                                                 │
│  [rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101]    │
│                                                                            │
│  [Test Connection]  [Update Configuration]                               │
│                                                                            │
│  ✓ Status: Connected                                                      │
│  📊 Resolution: 1920×1080                                                 │
│  📹 FPS: 30                                                                │
│  ⏱️ Latency: 245ms                                                         │
│  💾 Bitrate: 4.5 Mbps                                                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Detection Settings ───────────────────────────────────────────────────────┐
│                                                                            │
│  YOLO Model:       yolov8n (Nano)                                         │
│  Confidence Threshold: 0.3 [════════░] 0.3                               │
│  IoU Threshold:    0.45 [═════════░░] 0.45                              │
│  Processing FPS:   8-10 FPS                                              │
│                                                                            │
│  [Reset to Defaults]                                                      │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Alert Settings Screen

```
╔════════════════════════════════════════════════════════════════════════════╗
║  Alert Settings                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─ Email Recipients ─────────────────────────────────────────────────────────┐
│                                                                            │
│  ☑ karivaradhan7@gmail.com        [Edit]  [Remove]                     │
│                                                                            │
│  [+ Add Email Address]                                                    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Alert Options ────────────────────────────────────────────────────────────┐
│                                                                            │
│  ☑ Email on detection                                                    │
│  ☑ Sound notification                                                    │
│  ☑ Browser notification                                                  │
│  ☑ Log to database (optional Supabase)                                   │
│                                                                            │
│  Cooldown period: 5 [━━━━] seconds (prevents email spam)                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Test Alert ───────────────────────────────────────────────────────────────┐
│                                                                            │
│  [Send Test Email]  [Test Notification]  [View Sample Alert]             │
│                                                                            │
│  ✓ Last test sent: 14:23:45                                              │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Alert History ────────────────────────────────────────────────────────────┐
│                                                                            │
│  Status    | Time          | Rule Name           | Count | Recipient     │
│  ────────────────────────────────────────────────────────────────────────  │
│  ✓ Sent    | 14:24:15      | Person Detection    | 2     | karivaradhan7 │
│  ✓ Sent    | 14:24:45      | Vehicle Detection   | 1     | karivaradhan7 │
│  ✓ Sent    | 14:25:30      | Person Detection    | 2     | karivaradhan7 │
│  ✓ Sent    | 14:26:00      | Animal Detection    | 1     | karivaradhan7 │
│  ⏳ Pending | 14:26:30      | Person Detection    | 3     | karivaradhan7 │
│                                                                            │
│  [Clear History]  [Export]                                                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Rule Creation Screen

```
╔════════════════════════════════════════════════════════════════════════════╗
║  Create Detection Rule                                                     ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─ New Rule ─────────────────────────────────────────────────────────────────┐
│                                                                            │
│  Rule Name:                                                                │
│  [Person Intrusion Alert________________________________________]         │
│                                                                            │
│  Detection Type:                                                           │
│  ○ Person    ○ Vehicle    ○ Animal    ○ Multiple                         │
│                                                                            │
│  Threshold:                                                                │
│  Alert when count reaches: [1] (0-10)                                   │
│                                                                            │
│  Enabled:                                                                  │
│  ☑ This rule is active                                                   │
│                                                                            │
│  [Create Rule]  [Clear Form]                                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Existing Rules ───────────────────────────────────────────────────────────┐
│                                                                            │
│  Rule Name                | Type      | Threshold | Enabled | Actions   │
│  ───────────────────────────────────────────────────────────────────────  │
│  Person Alert             | Person    | 1         | ✓ ON   | Edit Del  │
│  Vehicle Alert            | Vehicle   | 1         | ✓ ON   | Edit Del  │
│  Animal Alert             | Animal    | 0         | ✓ ON   | Edit Del  │
│  Multiple Objects Alert   | Mixed     | 3         | ✓ ON   | Edit Del  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 📧 Email Alert Preview

### Test Email (HTML)

```
Subject: 🧪 TEST EMAIL - RGB System

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    RGB CAMERA DETECTION SYSTEM
    Test Email

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is a test email to verify the alert system is working properly.

System Status: ✓ Operational
Sent at: 2025-12-11 14:23:45 UTC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[View Dashboard]

RGB Camera Detection System
Automated Monitoring
```

### Detection Alert Email (HTML)

```
Subject: 🚨 INTRUDER ALERT: Person Detection

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ⚠️ SECURITY ALERT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rule: Person Detection
Status: TRIGGERED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Detection Details:

Detection Type:    PERSON
Count Detected:    2
Threshold:         1
Alert Status:      TRIGGERED ⚠️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Camera Information:

Camera Source:     Camera 3 (RTSP)
URL:               rtsp://admin:Mahesh@2025@...
Resolution:        1920×1080
FPS:               30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ Timestamp:       2025-12-11 14:24:15 UTC
Rule ID:           550e8400-e29b-41d4-a716-446655440000
Alert ID:          abc-123-def

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please check your camera system immediately.

[View Live Dashboard] [Manage Rules]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RGB Camera Detection System
Automated Monitoring & Alerts
```

---

## 📱 Mobile View (Responsive Design)

```
╔═════════════════════════════╗
║ RGB Detection System        ║
║ [☰]                  [⚙️]   ║
╠═════════════════════════════╣
║                             ║
║  ┌─────────────────────────┐│
║  │   LIVE STREAM           ││
║  │                         ││
║  │   Person: 2             ││
║  │   Vehicle: 1            ││
║  │   Animal: 0             ││
║  │                         ││
║  └─────────────────────────┘│
║                             ║
║  ⏸ Stop  🔄 Refresh        ║
║                             ║
║  📊 Detections             ║
║  [████] Person    66%       ║
║  [████] Vehicle   33%       ║
║  [░░░░] Animal    0%        ║
║                             ║
║  ⏰ Recent Alerts           ║
║  ✓ Person - 14:24:15       ║
║  ✓ Vehicle - 14:24:45      ║
║  ✓ Person - 14:25:30       ║
║                             ║
║  [Rules] [Settings] [More]  ║
║                             ║
╚═════════════════════════════╝
```

---

## 🎯 Real-Time Streaming Data (WebSocket)

```json
{
  "type": "frame_update",
  "timestamp": "2025-12-11T14:24:30.456789Z",
  "frame_number": 150,
  "detections": {
    "person": 2,
    "animal": 0,
    "vehicle": 1
  },
  "bounding_boxes": [
    {
      "class": "person",
      "confidence": 0.94,
      "x": 450,
      "y": 300,
      "width": 120,
      "height": 200,
      "track_id": 1
    },
    {
      "class": "vehicle",
      "confidence": 0.87,
      "x": 800,
      "y": 200,
      "width": 250,
      "height": 150,
      "track_id": 2
    }
  ],
  "processing_time_ms": 18.5,
  "fps": 10.2,
  "connected_clients": 2
}
```

---

## ✅ System Status Indicators

### Backend Status (Green = Healthy)

```
┌─ Backend Status ─────────────────────────────────┐
│                                                  │
│  ✓ API Server:        Online (8000)            │
│  ✓ YOLO Model:        Loaded                   │
│  ✓ RTSP Connection:   Connected                │
│  ✓ Email Service:     Ready                    │
│  ✓ WebSocket:        Active (2 clients)        │
│  ✓ Database:          Ready (optional)         │
│                                                  │
│  Overall: ✅ SYSTEM OPERATIONAL               │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Performance Metrics

```
┌─ Performance ────────────────────────────────────┐
│                                                  │
│  Frame Rate:       8-10 FPS (CPU)              │
│  Inference Time:   12-15 ms per frame          │
│  Processing Lag:   <50 ms total                │
│  Memory Usage:     250 MB                      │
│  CPU Usage:        45-60%                      │
│  Network I/O:      1-2 Mbps (RTSP)            │
│                                                  │
│  Status: ✅ OPTIMAL                            │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 🎊 Success Confirmation

When everything is working correctly, you will see:

```
✅ Backend running on port 8000
✅ Frontend accessible on port 5173
✅ Dashboard loads with live video
✅ Detections updating in real-time
✅ Test email arrives in inbox within 3 seconds
✅ Rules can be created and managed
✅ WebSocket showing green "Connected" status
✅ Email alerts sent on detection with 5-sec cooldown
✅ No errors in browser console
✅ No errors in backend logs

SYSTEM STATUS: 🟢 FULLY OPERATIONAL ✨

Ready to monitor Camera 3 with real-time AI detection!
```

---

**Expected Timeline**:
- ⏱️ Setup: 5 minutes (venv + dependencies)
- ⏱️ Backend startup: 30 seconds
- ⏱️ Frontend startup: 20 seconds
- ⏱️ Dashboard load: 5 seconds
- ⏱️ Detection start: 10 seconds (frame processing)

**Total time to full system**: ~6 minutes from "python main.py" ✨
