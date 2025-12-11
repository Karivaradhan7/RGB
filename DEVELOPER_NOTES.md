# 👨‍💻 Developer Notes - RGB System

## Architecture Overview

### What This System Does

```
Real-time RTSP stream → YOLOv8 Detection → Object Tracking → Email Alert
                              ↓
                        Web Dashboard (Live View)
                              ↓
                        Rule Engine → Conditional Alerts
```

## Key Implementation Details

### 1. Email Alerting System

**Location**: `backend/main.py` → `send_alert_email()`

**Design Decision**: Threaded SMTP
- Why: Prevents blocking the frame processing loop
- How: Each alert spawns a background thread
- Result: Non-blocking email sending

```python
def send_email_thread():
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    # Send email...
    server.quit()

thread = threading.Thread(target=send_email_thread, daemon=True)
thread.start()
```

### 2. RTSP Stream Handling

**Location**: `backend/main.py` → `start_stream()`

**Key Settings**:
```python
cap = cv2.VideoCapture(rtsp_url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Low latency
```

**Why Buffer Size = 1?**
- Default buffer causes lag in monitoring
- Size 1 = only keep latest frame
- Trade-off: Lower CPU but potential frame loss

### 3. Object Tracking Strategy

**Location**: `backend/tracker.py` → `SimpleTracker`

**Algorithm**: Centroid-based tracking
1. Calculate centroid of each detected box
2. Match to previous frame using distance
3. Assign object IDs
4. Track object history

**Why Simple Tracker?**
- Fast (no deep neural network overhead)
- Extensible (can upgrade to deep-sort)
- Sufficient for alert triggers
- Uses existing YOLOv8 detections

**Future Upgrade**: Replace with `deep-sort-realtime`
```python
# Already in requirements.txt
# Just need to integrate into main.py
from deepsort_realtime.deepsort import DeepSort
```

### 4. Rule Engine Design

**Location**: `backend/main.py` → `check_rules()`

**Flow**:
```
Detections Arrive
    ↓
Load Rules from Database
    ↓
For Each Rule:
    Check Count > Threshold
    ↓
    Check Alert Cooldown
    ↓
    If Both True:
        - Insert Alert Record
        - Send Email
        - Broadcast WebSocket
        - Log to Console
```

**Alert Cooldown**: Prevents spam
```python
ALERT_COOLDOWN = 5  # seconds
last_alert_time[rule_id] = datetime.now()
# Skip if within cooldown period
```

## Performance Considerations

### Frame Processing Loop
**Location**: `backend/main.py` → `process_stream()`

```
Read Frame (30ms)
    ↓
Resize to 640x480 (1ms)
    ↓
YOLOv8 Inference (50-100ms on CPU)
    ↓
Draw Boxes (5ms)
    ↓
Rule Check (5ms)
    ↓
WebSocket Send (2ms)
    ↓
Total: ~100-150ms per frame (~7-10 FPS on CPU)
```

### Optimization Tips

1. **Lower YOLOv8 Confidence**
```python
results = model(frame, verbose=False, conf=0.3)  # 0.5 default
```

2. **Skip Frames for Processing**
```python
if frame_count % 3 == 0:  # Process every 3rd frame
    detections, boxes = run_detection(frame)
```

3. **Use GPU if Available**
```python
# CUDA compatible GPU
# YOLOv8 auto-detects
# Will be 10x faster
```

4. **Reduce Stream Resolution**
- Set camera to lower resolution
- RTSP stream quality setting

## Database Integration (Optional Supabase)

### Tables Used

1. **detection_rules**
```sql
id, name, object_type, threshold, is_active, created_at
```

2. **alert_settings**
```sql
id, email, is_active, created_at
```

3. **alerts**
```sql
id, rule_id, rule_name, object_type, count, message, created_at
```

4. **detection_logs**
```sql
id, person_count, animal_count, vehicle_count, created_at
```

5. **camera_configs**
```sql
id, source_type, rtsp_url, video_file, is_active, created_at
```

### Graceful Degradation

System works WITHOUT Supabase:
- Rules stored in-memory only
- Alerts logged to console
- No email (if credentials set, emails still work)
- Demo mode enabled

## Configuration Management

### Environment Variables
All configuration via `.env` file:

```bash
# Required for Email
SENDER_EMAIL=karivaradhan7@gmail.com
SENDER_PASSWORD=xxxx-xxxx-xxxx-xxxx

# Camera
RTSP_URL=rtsp://admin:...

# Alerts
ALERT_RECIPIENTS=email@example.com,other@example.com

# Optional
VITE_SUPABASE_URL=
VITE_SUPABASE_SUPABASE_ANON_KEY=
```

### Why .env?
- Credentials not in code
- Different configs per environment
- Easy to change without redeploying
- Git ignored (won't commit secrets)

## WebSocket Implementation

**Location**: `backend/main.py` → `/ws/stream` endpoint

**Protocol**:
```python
{
    "type": "frame",
    "data": "base64_encoded_jpg",
    "detections": {
        "person": 2,
        "animal": 0,
        "vehicle": 1,
        "timestamp": "2025-12-11T14:30:45"
    }
}
```

**Client Connection** (Frontend):
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/stream');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'frame') {
        // Display frame
        // Update detection counts
    }
};
```

## Testing Endpoints

### Test Camera Connection
```bash
curl -X POST http://localhost:8000/test_connection \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "rtsp",
    "rtsp_url": "rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101"
  }'
```

### Test Email
```bash
curl -X POST http://localhost:8000/send_test_email \
  -H "Content-Type: application/json" \
  -d '["karivaradhan7@gmail.com"]'
```

### Check System Health
```bash
curl http://localhost:8000/health
```

Response:
```json
{
    "status": "ok",
    "streaming": true,
    "detections": {
        "person": 2,
        "animal": 0,
        "vehicle": 1,
        "timestamp": "2025-12-11T14:30:45"
    },
    "connected_clients": 1
}
```

## Common Issues & Solutions

### Issue: RTSP connection timeout
**Solution**: Check credentials and network
```bash
# Test with ffmpeg
ffmpeg -rtsp_transport tcp -i rtsp://admin:... -t 5 -f null -
```

### Issue: High CPU usage
**Solution**: Lower detection frequency
```python
# In process_stream()
if frame_count % 5 == 0:  # Process every 5th frame instead of 3
    detections, boxes = run_detection(frame)
```

### Issue: Emails delay in being sent
**Solution**: Already handled! Threaded background sending
- Doesn't block frame processing
- Use browser console to verify WebSocket still streaming

### Issue: Memory leak
**Solution**: Monitor with `top` or `htop`
- Check for frame buffer accumulation
- Ensure WebSocket clients disconnect properly
- Database queries have timeouts

## Code Quality

### Type Hints
```python
async def process_stream(cap) -> None:
def run_detection(frame) -> Tuple[Dict, List]:
```

### Error Handling
```python
try:
    # Operation
except Exception as e:
    print(f"[!] Error: {e}")
    # Graceful fallback
```

### Logging Prefix Convention
```
[*] - Info/processing
[✓] - Success
[!] - Warning
[✗] - Error
[+] - Addition
[-] - Removal
```

## Future Enhancements

1. **Deep-SORT Tracking**
   - Import module: Already in requirements.txt
   - Implement: Better tracking accuracy
   - Cost: ~2x more CPU time

2. **GPU Support**
   - YOLOv8 auto-detects CUDA
   - No code changes needed
   - Performance: 10x faster

3. **Persistent Rules**
   - Without Supabase: File-based JSON
   - With Supabase: Already integrated

4. **Analytics Dashboard**
   - Detection patterns
   - Peak hours
   - Alert statistics

5. **Multiple Cameras**
   - Parallel processing
   - Per-camera rules
   - Aggregated alerts

6. **Advanced Filtering**
   - Motion detection (skip static frames)
   - Zone-based detection (regions of interest)
   - Human pose estimation (HumanPose)

## File Organization Philosophy

```
backend/
├── main.py          # Core application (no imports of tracker)
├── tracker.py       # Tracking module (can be replaced)
└── requirements.txt # All dependencies

frontend/
├── src/
│   ├── api.js       # API communication
│   ├── App.jsx      # Main app
│   └── screens/     # Page components
└── package.json
```

**Why?**: Separation of concerns, easy to swap/upgrade modules

## Deployment Checklist

- [ ] Set SENDER_PASSWORD in .env
- [ ] Test email with `/send_test_email`
- [ ] Verify RTSP connection with `/test_connection`
- [ ] Create at least one detection rule
- [ ] Test rule by triggering detection
- [ ] Monitor logs for errors
- [ ] Check frontend WebSocket connection
- [ ] Verify email alerts arrive
- [ ] Document any custom rules
- [ ] Set up monitoring/logging

---

**Last Updated**: December 2025  
**Maintainer**: Dev Team  
**Status**: Production Ready ✅
