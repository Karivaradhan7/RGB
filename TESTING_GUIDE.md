# 🧪 RGB CAMERA DETECTION SYSTEM - TESTING & VERIFICATION GUIDE

## Pre-Flight Checklist

```bash
# 1. Verify Python version (3.8+)
python3 --version

# 2. Verify Node version (16+)
node --version && npm --version

# 3. Check RTSP accessibility (requires ffmpeg)
ffmpeg -rtsp_transport tcp -i "rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101" -t 5 -f null - && echo "✓ RTSP accessible" || echo "✗ RTSP unreachable"

# 4. Verify workspace structure
ls -la /workspaces/RGB/
```

---

## Step-by-Step Setup & Testing

### Phase 1: Environment Setup (5 minutes)

```bash
# Navigate to project
cd /workspaces/RGB

# 1. Create virtual environment
python3 -m venv venv
echo "✓ Virtual environment created"

# 2. Activate venv
source venv/bin/activate
echo "✓ Activated: $(which python)"

# 3. Install backend dependencies
pip install -r backend/requirements.txt -q
echo "✓ Backend dependencies installed"

# 4. Verify critical packages
python3 -c "
import cv2, ultralytics, fastapi
print('✓ OpenCV:', cv2.__version__)
print('✓ YOLOv8:', ultralytics.__version__)
print('✓ FastAPI: OK')
"

# 5. Download YOLO model (first time only, ~30MB)
python3 -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
echo "✓ YOLO model ready"
```

**Expected Output**:
```
✓ Virtual environment created
✓ Activated: /workspaces/RGB/venv/bin/python
✓ Backend dependencies installed
✓ OpenCV: 4.12.0
✓ YOLOv8: 8.3.235
✓ FastAPI: OK
✓ YOLO model ready
```

---

### Phase 2: Configuration (2 minutes)

```bash
# 1. Create .env file with credentials
cat > /workspaces/RGB/.env << 'EOF'
RTSP_URL=rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101
SENDER_EMAIL=karivaradhan7@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx
ALERT_RECIPIENTS=karivaradhan7@gmail.com
EOF

echo "✓ Configuration file created"

# 2. Verify .env is readable
cat /workspaces/RGB/.env && echo "✓ .env configured"
```

**Gmail App Password Setup**:
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification (if not done)
3. Create App Password:
   - Select "Mail" and "Windows Computer"
   - Google generates 16-character password
   - Copy it: `xxxx xxxx xxxx xxxx`
4. Paste into SENDER_PASSWORD field in .env

---

### Phase 3: Backend Testing (5 minutes)

```bash
# Terminal 1: Start backend server
cd /workspaces/RGB
source venv/bin/activate
cd backend
python main.py
```

**Expected Output**:
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
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Check Health Status**:
```bash
# Terminal 3 (new tab)
curl -s http://localhost:8000/ | jq .
```

**Expected Response**:
```json
{
  "message": "RGB Camera Detection System API",
  "version": "1.0.0",
  "endpoints": {
    "stream": "/start_stream, /stop_stream",
    "detections": "/get_detections",
    "alerts": "/get_alerts",
    "rules": "/create_rule",
    "email": "/send_test_email",
    "websocket": "/ws/stream"
  }
}
```

---

### Phase 4: Test Email System (2 minutes)

```bash
# Send test email
curl -X POST http://localhost:8000/send_test_email \
  -H "Content-Type: application/json" \
  -d '["karivaradhan7@gmail.com"]'
```

**Expected Response**:
```json
{
  "status": "success",
  "message": "Test email sent to 1 recipient(s)",
  "recipients": ["karivaradhan7@gmail.com"]
}
```

**Backend Console Output**:
```
[✓] EMAIL SENT to karivaradhan7@gmail.com | Test Email | 14:23:45
```

**Verify Email Received**:
- Check inbox at gmail.com
- Look for subject: "🧪 TEST EMAIL - RGB System"
- Content should show detection info and timestamp

---

### Phase 5: Start Stream Processing (2 minutes)

```bash
# Start the RTSP stream
curl -X POST http://localhost:8000/start_stream
```

**Expected Response**:
```json
{
  "status": "success",
  "message": "Stream started successfully"
}
```

**Backend Console Output**:
```
[POST /start_stream]
[*] Starting stream from: rtsp
[*] Connecting to RTSP: rtsp://admin:Mahesh@2025@...
[*] Connected successfully
[*] Starting stream processing...
[*] Frame 0: {'person': 0, 'animal': 0, 'vehicle': 0}
[*] Frame 30: {'person': 1, 'animal': 0, 'vehicle': 0}
[*] Frame 60: {'person': 2, 'animal': 0, 'vehicle': 0}
[✓] EMAIL SENT to karivaradhan7@gmail.com | Person Detection | person×2 | 14:24:15
[*] Frame 90: {'person': 2, 'animal': 0, 'vehicle': 1}
...
```

---

### Phase 6: Verify Detections (1 minute)

```bash
# Check current detections
curl -s http://localhost:8000/get_detections | jq .
```

**Expected Response**:
```json
{
  "person": 2,
  "animal": 0,
  "vehicle": 1,
  "timestamp": "2025-12-11T14:24:30.123456"
}
```

**Check Alert History**:
```bash
curl -s http://localhost:8000/get_alerts?limit=5 | jq .
```

**Expected Response**:
```json
[
  {
    "timestamp": "2025-12-11T14:24:15",
    "rule_name": "Person Detection",
    "object_type": "person",
    "count": 2,
    "threshold": 1,
    "message": "Alert: Person Detection - person count (2) exceeded threshold (1)"
  }
]
```

---

### Phase 7: Create Detection Rules (2 minutes)

```bash
# Create a person detection rule
curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Person Alert",
    "object_type": "person",
    "threshold": 1
  }'
```

**Expected Response**:
```json
{
  "status": "success",
  "message": "Rule created successfully"
}
```

**Create more rules**:
```bash
# Vehicle detection rule
curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vehicle Alert",
    "object_type": "vehicle",
    "threshold": 1
  }'

# Animal detection rule
curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Animal Alert",
    "object_type": "animal",
    "threshold": 0
  }'
```

---

### Phase 8: Frontend Setup (3 minutes)

```bash
# Terminal 2: Install and run frontend
cd /workspaces/RGB/frontend
npm install
npm run dev
```

**Expected Output**:
```
  VITE v4.5.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

---

### Phase 9: Dashboard Access (1 minute)

**Open Browser**:
```
http://localhost:5173
```

**Expected to see**:
1. Live video stream from RTSP camera
2. Real-time detection counts
3. Detection bounding boxes overlaid on video
4. Alert history panel
5. Rule creation form
6. Camera configuration section

---

## Complete Testing Sequence

```bash
# Terminal 1: Backend
cd /workspaces/RGB
source venv/bin/activate
cd backend
python main.py

# Wait for: "Uvicorn running on http://0.0.0.0:8000"
```

```bash
# Terminal 2: Frontend
cd /workspaces/RGB/frontend
npm install
npm run dev

# Wait for: "Local: http://localhost:5173/"
```

```bash
# Terminal 3: API Testing
cd /workspaces/RGB

# 1. Send test email
echo "1. Testing email..."
curl -X POST http://localhost:8000/send_test_email \
  -H "Content-Type: application/json" \
  -d '["karivaradhan7@gmail.com"]'
sleep 2

# 2. Check API health
echo "2. Checking health..."
curl -s http://localhost:8000/ | jq '.endpoints'

# 3. Start stream
echo "3. Starting stream..."
curl -X POST http://localhost:8000/start_stream

# 4. Create rules
echo "4. Creating rules..."
curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d '{"name":"Person Alert","object_type":"person","threshold":1}'

# 5. Monitor detections
echo "5. Monitoring detections (10 samples)..."
for i in {1..10}; do
    echo "Sample $i:"
    curl -s http://localhost:8000/get_detections | jq '.'; 
    sleep 3
done

# 6. Check alerts
echo "6. Alert history..."
curl -s http://localhost:8000/get_alerts?limit=10 | jq '.[] | {timestamp, rule_name, count}'
```

---

## Real-Time Monitoring Script

```bash
#!/bin/bash
# save as: monitor.sh
# run: bash monitor.sh

echo "🎥 RGB Camera Detection System - Live Monitor"
echo "=============================================="
echo "Refreshing every 2 seconds... (Ctrl+C to stop)"
echo ""

while true; do
    clear
    echo "📊 Detection Monitor - $(date '+%H:%M:%S')"
    echo "=============================================="
    
    # Get current detections
    detections=$(curl -s http://localhost:8000/get_detections 2>/dev/null)
    person=$(echo $detections | grep -o '"person":[0-9]*' | grep -o '[0-9]*')
    animal=$(echo $detections | grep -o '"animal":[0-9]*' | grep -o '[0-9]*')
    vehicle=$(echo $detections | grep -o '"vehicle":[0-9]*' | grep -o '[0-9]*')
    
    # Display
    echo ""
    echo "Current Detections:"
    echo "  🟩 Person:  $person"
    echo "  🟦 Animal:  $animal"
    echo "  🟥 Vehicle: $vehicle"
    
    # Get alerts
    echo ""
    echo "Recent Alerts (last 5):"
    curl -s http://localhost:8000/get_alerts?limit=5 2>/dev/null | \
    jq -r '.[] | "  ⏰ \(.timestamp) | \(.rule_name) | Count: \(.count)"' || echo "  No alerts yet"
    
    echo ""
    echo "Backend Status: $(curl -s http://localhost:8000/ 2>/dev/null | jq -r '.message')"
    
    sleep 2
done
```

Run the monitor:
```bash
bash monitor.sh
```

---

## Troubleshooting Tests

### Test 1: Check Backend is Running
```bash
curl http://localhost:8000 2>&1 | head -20
```
Should return API info, not "Connection refused"

### Test 2: Check Frontend is Running
```bash
curl http://localhost:5173 2>&1 | grep -i vite
```
Should return Vite HTML, not "Connection refused"

### Test 3: Check WebSocket Connection
```bash
# Install wscat if needed: npm install -g wscat
wscat -c ws://localhost:8000/ws/stream
# Should connect and show frame data streaming
```

### Test 4: Check RTSP Connection
```bash
timeout 5 ffmpeg -rtsp_transport tcp -i "rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101" -f null - 2>&1 | grep -i "stream"
```
Should show stream info, not authentication errors

### Test 5: Check Email Configuration
```bash
python3 << 'PYTHON'
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = "karivaradhan7@gmail.com"
password = input("Enter Gmail App Password: ")
recipient = "karivaradhan7@gmail.com"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "Test Email"
    msg.attach(MIMEText("This is a test email", "plain"))
    
    server.send_message(msg)
    server.quit()
    print("✓ Email configuration working!")
except Exception as e:
    print(f"✗ Email error: {e}")
PYTHON
```

### Test 6: Check Port Availability
```bash
# Check if ports are in use
lsof -i :8000   # Backend port
lsof -i :5173   # Frontend port
lsof -i :25     # SMTP port (should be free)

# If ports in use, kill them:
kill -9 $(lsof -t -i :8000)
kill -9 $(lsof -t -i :5173)
```

---

## Performance Verification

```bash
# Monitor CPU/Memory usage during streaming
watch -n 1 'ps aux | grep -E "python|node" | grep -v grep'

# Or use top
top -p $(pgrep -f "python main.py")

# Monitor network usage
iftop -n  # Shows real-time network

# Check GPU (if available)
nvidia-smi

# Check RTSP stream bitrate
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=s=x:p=0 \
  rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101
```

---

## Success Criteria Checklist

- [ ] Backend starts without errors (Uvicorn running)
- [ ] Frontend loads (http://localhost:5173 accessible)
- [ ] API responds to health check (curl localhost:8000)
- [ ] Test email arrives in inbox (check gmail)
- [ ] RTSP stream connects (no "Connection refused")
- [ ] Detections showing (person/animal/vehicle counts > 0)
- [ ] Alerts being generated (rule engine triggering)
- [ ] Dashboard displays live video
- [ ] WebSocket connected (real-time updates)
- [ ] Email alerts sent on detection (cooldown working)

---

## End-to-End Test Report Template

```markdown
## RGB Camera Detection System - Test Report
Date: YYYY-MM-DD
Tester: [Your Name]

### Environment
- OS: Ubuntu 24.04
- Python: 3.10
- Node: 18.x
- RTSP Camera: Camera 3

### Test Results

| Component | Status | Notes |
|-----------|--------|-------|
| Backend (8000) | ✓ Pass | Uvicorn started |
| Frontend (5173) | ✓ Pass | Vite development server |
| RTSP Connection | ✓ Pass | Connected to camera |
| YOLO Detection | ✓ Pass | Detecting persons/animals |
| Email Alert | ✓ Pass | Received at karivaradhan7@gmail.com |
| WebSocket | ✓ Pass | Real-time data flowing |
| Dashboard | ✓ Pass | Video and detections visible |
| Alert Cooldown | ✓ Pass | 5-second cooldown working |

### Performance Metrics
- Avg FPS: 8-10 (CPU processing)
- Memory: 250MB (backend streaming)
- CPU Load: 45-60%
- Email Latency: ~2-3 seconds

### Issues Found
- None

### Recommendations
- Monitor: System stable under normal load
- Next: Deploy to production

### Sign-off
✓ Ready for Production
```

---

## Quick Reference Commands

```bash
# View logs
tail -f /tmp/rgb_detection.log

# View active detections in real-time
watch -n 1 'curl -s http://localhost:8000/get_detections | jq .'

# Test email delivery (10 times)
for i in {1..10}; do curl -X POST http://localhost:8000/send_test_email \
  -H "Content-Type: application/json" \
  -d '["karivaradhan7@gmail.com"]'; sleep 5; done

# Stream statistics
curl -s http://localhost:8000/get_detections && curl -s http://localhost:8000/get_alerts?limit=1

# Create multiple test rules
for obj in person animal vehicle; do
  curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"${obj} Alert\",\"object_type\":\"${obj}\",\"threshold\":1}"
done

# Stop streaming
curl -X POST http://localhost:8000/stop_stream

# Kill all processes
pkill -f "python main.py"
pkill -f "npm run dev"
```

---

## Support

**Common Issues & Solutions**:

1. **"Connection refused" on localhost:8000**
   - Solution: Run `python main.py` in backend directory
   
2. **"RTSP connection timeout"**
   - Solution: Verify camera URL and network connectivity
   
3. **"Gmail authentication failed"**
   - Solution: Verify Gmail App Password (not regular password)
   
4. **"No detections appearing"**
   - Solution: Check if camera is pointing at objects
   
5. **"Port already in use"**
   - Solution: Run `kill -9 $(lsof -t -i :8000)` or change port

**System Status**: ✅ Production Ready

---

**Next Steps**: Open dashboard → monitor camera → receive alerts!
