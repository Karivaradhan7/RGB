# Intruder Detection System 🚨

A complete web-based intruder detection system with real-time object detection using YOLOv8.

## Features

✅ **Real-time Detection** - Live video stream processing with YOLOv8
✅ **Multiple Camera Sources** - Webcam, RTSP streams, or uploaded videos
✅ **Smart Rules Engine** - Create custom detection rules with thresholds
✅ **Alert System** - Email notifications when rules are triggered
✅ **Live Dashboard** - Real-time object counting and alert monitoring
✅ **Beautiful UI** - Modern React + Tailwind design
✅ **WebSocket Support** - Live frame streaming to frontend

## Architecture

```
RGB/
├── backend/
│   ├── main.py           # FastAPI application with all endpoints
│   └── requirements.txt   # Python dependencies
└── frontend/
    ├── src/
    │   ├── App.jsx               # Main app component with navigation
    │   ├── api.js                # API client and WebSocket connection
    │   ├── index.css             # Tailwind imports
    │   ├── main.jsx              # React entry point
    │   └── screens/
    │       ├── CameraConfiguration.jsx    # Screen 1: Camera setup
    │       ├── RuleCreation.jsx          # Screen 2: Create rules
    │       ├── LiveDetectionDashboard.jsx # Screen 3: Live dashboard
    │       └── AlertSettings.jsx         # Screen 4: Email alerts
    ├── package.json      # Node dependencies
    ├── vite.config.js    # Vite configuration
    ├── tailwind.config.js
    ├── postcss.config.js
    └── index.html        # HTML entry point
```

## Installation & Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a Python virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs:
   - FastAPI & Uvicorn
   - OpenCV for video processing
   - YOLOv8 for object detection
   - WebSocket support

4. **(Optional) Setup email notifications:**
   Create a `.env` file in the backend directory:
   ```bash
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   ```

5. **Start the backend server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Backend will be running at: `http://localhost:8000`
   API Docs available at: `http://localhost:8000/docs`

### Frontend Setup

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   
   Frontend will be running at: `http://localhost:5173`

## Usage Guide

### Screen 1: Camera Configuration
- Select camera source: Webcam, RTSP Stream, or Upload Video
- For RTSP: Enter the camera URL (e.g., `rtsp://192.168.1.100:554/stream`)
- Click "Test Connection" to verify
- Click "Start Stream" to begin processing

### Screen 2: Detection Rules
- Create rules to trigger alerts
- Set rule name, object type (Person/Animal/Vehicle), and threshold
- Example: Alert when more than 5 persons are detected
- View and delete existing rules

### Screen 3: Live Dashboard
- Watch real-time video with bounding boxes
- See live detection counts for persons, animals, vehicles
- Monitor recent alerts with timestamps
- Data updates every 1 second

### Screen 4: Alert Settings
- Add multiple email addresses
- Configure which emails receive alerts
- Click "Send Test Email" to verify configuration
- Alerts are sent immediately when rules are triggered

## API Endpoints

**POST /configure_camera**
- Configure camera source
- Body: `{source_type: "webcam"|"rtsp"|"upload", rtsp_url?: string}`

**POST /start_stream**
- Start video processing

**POST /stop_stream**
- Stop video processing

**GET /get_detections**
- Get current detection counts
- Returns: `{person: int, animal: int, vehicle: int, timestamp: string}`

**POST /create_rule**
- Create detection rule
- Body: `{name: string, object_type: string, threshold: int}`

**GET /get_rules**
- Get all active rules

**DELETE /delete_rule/{rule_id}**
- Delete a rule

**POST /configure_alerts**
- Set alert email addresses
- Body: `{emails: [string]}`

**POST /send_test_email**
- Send test emails
- Body: `[string]`

**GET /get_alerts**
- Get recent alerts
- Query: `limit=20`

**POST /test_connection**
- Test camera connection before streaming

**WS /ws/stream**
- WebSocket for live frame streaming
- Receives: `{type: "frame"|"alert", data: ...}`

**GET /health**
- Health check endpoint

## Object Detection

YOLOv8 automatically detects and classifies:
- **Persons**: People in the video
- **Animals**: Dogs, cats, birds, horses, etc.
- **Vehicles**: Cars, trucks, motorcycles, bicycles, etc.

Detection happens on every frame with confidence scores displayed.

## Performance Tips

1. **RTSP Streams**: Use standard resolution (720p or lower) for better performance
2. **Video Files**: Smaller files process faster
3. **Rules**: Keep threshold counts reasonable (e.g., 1-5 for sensitive areas)
4. **Browser**: Use Chrome/Firefox for best WebSocket performance

## Troubleshooting

**Backend won't start:**
```bash
# Make sure Python 3.8+ is installed
python --version

# Clear cache and reinstall
pip install --upgrade -r requirements.txt
```

**Frontend connection failed:**
- Check if backend is running on `http://localhost:8000`
- Look at browser console (F12) for errors
- Verify CORS is enabled in FastAPI

**Camera not working:**
- Webcam: Check browser permissions
- RTSP: Verify URL format and camera is reachable
- Upload: Use MP4 or AVI format files

**Slow performance:**
- Reduce video resolution
- Skip some frames in processing
- Use GPU acceleration (CUDA) for YOLO if available

## Building for Production

**Backend:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

**Frontend:**
```bash
npm run build
# Deploy dist/ folder to web server
```

## Dependencies

**Backend:**
- FastAPI 0.104.1
- OpenCV 4.8.1.78
- YOLOv8 (Ultralytics)
- Uvicorn 0.24.0

**Frontend:**
- React 18.2.0
- Tailwind CSS 3.3.5
- Vite 5.0.8
- Lucide React (Icons)

## License

This project is open source and available for personal and educational use.

## Support

For issues or questions, check the following:
1. Ensure all dependencies are installed
2. Backend and frontend are running on correct ports
3. Camera/RTSP source is accessible
4. Browser console shows no CORS errors

---

**Made with ❤️ for security monitoring**
