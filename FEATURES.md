# Features & Capabilities

## Core Detection Features

### 🎥 Video Source Support
- **Webcam** - Real-time webcam input
- **RTSP Streams** - IP camera support via RTSP protocol
- **Video Upload** - Process pre-recorded video files
- **Connection Testing** - Verify camera access before streaming

### 🤖 Object Detection
- **YOLOv8 Model** - State-of-the-art object detection
- **Real-time Processing** - Frame-by-frame analysis
- **Bounding Boxes** - Visual object identification
- **Confidence Scores** - Detection reliability metrics

**Detectable Objects:**
- 👤 **Persons** - Human detection
- 🐾 **Animals** - Dogs, cats, birds, horses, and other animals
- 🚗 **Vehicles** - Cars, trucks, motorcycles, bicycles

### 📊 Detection Statistics
- **Live Counters** - Real-time object counts
- **Timestamp** - Detection timing information
- **History** - Historical detection data
- **JSON Format** - Machine-readable detection output

---

## Rule Engine Features

### 🛡️ Custom Rules
- **Rule Creation** - Define custom detection rules
- **Flexible Configuration** - Set thresholds per rule
- **Multiple Triggers** - Create rules for different object types
- **Easy Management** - Add/edit/delete rules

**Rule Parameters:**
- Rule Name - Descriptive identifier
- Object Type - Person/Animal/Vehicle
- Threshold Count - Alert trigger point

**Example Rules:**
```
Rule: "Unauthorized Entry"
- Object Type: Person
- Threshold: 1 (alert if 1+ person detected)

Rule: "Parking Violation"
- Object Type: Vehicle
- Threshold: 5 (alert if 5+ vehicles present)
```

---

## Alert & Notification Features

### 📧 Email Alerts
- **Multiple Recipients** - Configure multiple email addresses
- **Immediate Notification** - Instant email on rule trigger
- **Rich Content** - Includes rule details and timestamp
- **Test Email** - Verify email configuration

### 🔔 Alert Management
- **Real-time Alerts** - Live alert display
- **Alert History** - Recent alerts panel (last 50)
- **Timestamp** - Exact trigger time
- **Rule Information** - Which rule was triggered

**Alert Contents:**
- Rule Name
- Object Type Detected
- Detection Count
- Timestamp
- Custom Message

---

## Dashboard Features

### 📺 Live Monitoring
- **Real-time Video** - Live feed with processing
- **Bounding Boxes** - Visual object identification
- **FPS Indicator** - Stream quality indicator
- **LIVE Badge** - Stream status indicator

### 📈 Detection Display
- **Person Counter** - Current person count
- **Animal Counter** - Current animal count
- **Vehicle Counter** - Current vehicle count
- **Auto-refresh** - Updates every 1 second

### 🚨 Alert Panel
- **Recent Alerts** - Last 10 alerts displayed
- **Alert Timestamp** - When alert was triggered
- **Expandable** - Scroll through alert history
- **Color-coded** - Visual alert severity

---

## User Interface Features

### 🎨 Design
- **Modern UI** - Clean, professional appearance
- **Dark Theme** - Easy on the eyes
- **Responsive Design** - Works on desktop/tablet/mobile
- **Tailwind CSS** - Professional styling

### 🧭 Navigation
- **Tab-based Navigation** - Easy screen switching
- **Consistent Layout** - Familiar structure
- **Status Indicators** - Visual feedback
- **Loading States** - Clear operation status

### 📱 Screens

#### 1. Camera Configuration
- Source selection (Webcam/RTSP/Upload)
- URL input for RTSP
- Connection testing
- Stream control buttons

#### 2. Detection Rules
- Rule form with validation
- Threshold slider (1-50)
- Active rules display
- Delete rule functionality

#### 3. Live Dashboard
- Full-screen video preview
- Real-time detection counts
- Recent alerts panel
- Connection status

#### 4. Alert Settings
- Email input field
- Email list management
- Test email button
- Configuration info panel

---

## API Features

### REST Endpoints (11 total)

**Camera Control:**
- `POST /configure_camera` - Setup camera source
- `POST /start_stream` - Begin video processing
- `POST /stop_stream` - Stop video processing
- `POST /test_connection` - Verify camera access

**Detection & Rules:**
- `GET /get_detections` - Current detection counts
- `POST /create_rule` - Add new detection rule
- `GET /get_rules` - List all active rules
- `DELETE /delete_rule/{id}` - Remove a rule

**Alerts:**
- `POST /configure_alerts` - Set email addresses
- `POST /send_test_email` - Test email configuration
- `GET /get_alerts` - Retrieve alert history

**Monitoring:**
- `WS /ws/stream` - WebSocket for live frames
- `GET /health` - System health check

---

## WebSocket Features

### Real-time Streaming
- **Frame Streaming** - Live video frames
- **Low Latency** - ~30ms updates
- **Bidirectional** - Client-server communication
- **Auto-reconnect** - Handles disconnections

**WebSocket Messages:**
```json
{
  "type": "frame",
  "data": "base64-encoded-image",
  "detections": {
    "person": 3,
    "animal": 1,
    "vehicle": 0,
    "timestamp": "2024-01-15T10:30:45.123Z"
  }
}
```

---

## Performance Features

### Optimization
- **Frame Throttling** - Efficient frame processing
- **Async Processing** - Non-blocking operations
- **Memory Efficient** - Stream management
- **CPU Optimized** - Responsive detection

### Scalability
- **Multiple Streams** - Could handle multiple cameras
- **Concurrent Rules** - Process multiple rules
- **Alert Queuing** - Reliable alert delivery
- **Connection Pooling** - Efficient resource use

---

## Security Features

### Access Control
- **CORS Enabled** - Cross-origin requests allowed
- **Input Validation** - Secure data handling
- **Error Handling** - Graceful failure modes
- **Environment Variables** - Secure credential storage

### Data Handling
- **Base64 Encoding** - Safe image transmission
- **JSON Format** - Structured data
- **Timestamp Tracking** - Audit trail
- **Status Codes** - Clear error reporting

---

## Configuration Features

### Customization
- **Flexible Thresholds** - 1-50 range
- **Multiple Object Types** - Person/Animal/Vehicle
- **Email Management** - Add/remove recipients
- **Rule Names** - Custom descriptive labels

### Advanced Options
- **Environment Variables** - Email configuration
- **RTSP URL Support** - Various camera formats
- **Video File Support** - Multiple formats
- **Port Configuration** - Custom ports

---

## Logging & Debugging

### System Logging
- **API Endpoints** - All requests logged
- **Error Messages** - Detailed error info
- **Connection Status** - Stream status tracking
- **Alert Logging** - Alert trigger records

### Browser Console
- **WebSocket Events** - Connection tracking
- **API Errors** - Failed request details
- **Warning Messages** - Potential issues
- **Debug Info** - Development information

---

## Supported Formats

### Video Formats
- **Webcam:** Native browser access
- **RTSP:** Standard IP camera protocol
- **Files:** MP4, AVI, MOV, MKV

### Image Formats
- **JPEG:** For frame transmission
- **PNG:** Optional support
- **Base64:** Safe encoding for web

---

## Browser Compatibility

✅ **Fully Supported:**
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

⚠️ **Limited Support:**
- IE 11 (not recommended)
- Mobile browsers (basic support)

---

## System Limits

| Feature | Limit | Notes |
|---------|-------|-------|
| Active Rules | Unlimited | No practical limit |
| Email Recipients | Unlimited | Per rule configuration |
| Alert History | 50 most recent | Auto-purged |
| Frame Rate | 30 FPS | Depends on CPU |
| Stream Resolution | 640x480 | Configurable |

---

## Future Enhancement Ideas

- 🎥 Multi-camera support
- 🎞️ Video recording/playback
- 📊 Analytics dashboard
- 🔐 User authentication
- 💾 Database integration
- 📱 Mobile app
- 🤖 ML-based scheduling
- 🔗 Webhook integration
- 📺 MJPEG streaming
- 🧠 Advanced filtering

---

For setup instructions, see [INSTALLATION.md](INSTALLATION.md)
For usage guide, see [README.md](README.md)
