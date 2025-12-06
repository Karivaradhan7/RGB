#!/bin/bash

# Intruder Detection System - Run Guide
# This script provides all the information needed to run the system

cat << 'EOF'

╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   🚨 INTRUDER DETECTION SYSTEM - RUN INSTRUCTIONS 🚨          ║
║                                                                ║
║   A Complete Real-time Object Detection System                ║
║   with YOLOv8, FastAPI, and React                             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

📁 PROJECT STRUCTURE
═══════════════════════════════════════════════════════════════

RGB/
├── backend/
│   ├── main.py           (600+ lines) FastAPI backend
│   ├── requirements.txt   Python dependencies
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── App.jsx       Main React component
│   │   ├── api.js        API integration
│   │   └── screens/      4 Screen components
│   ├── package.json      Node dependencies
│   └── README.md
├── README.md             Main documentation
├── QUICKSTART.md         5-minute start guide
├── INSTALLATION.md       Detailed setup
├── FEATURES.md           Complete feature list
├── PROJECT_SUMMARY.md    Architecture overview
└── setup.sh/.bat         Automated setup


✅ FEATURES INCLUDED
═══════════════════════════════════════════════════════════════

✓ Real-time YOLOv8 object detection
✓ Person/Animal/Vehicle detection
✓ Multiple camera sources (Webcam/RTSP/Upload)
✓ Custom detection rules with thresholds
✓ Email alert notifications
✓ Live WebSocket streaming
✓ Beautiful dark theme UI
✓ 4 dedicated screens
✓ REST API with 11+ endpoints
✓ Production-ready code


🚀 QUICK START (Choose One)
═══════════════════════════════════════════════════════════════

OPTION 1: Automated Setup (Recommended)
────────────────────────────────────────
Linux/macOS:
    bash setup.sh

Windows:
    setup.bat

Then follow on-screen instructions.


OPTION 2: Manual Setup (5 minutes)
──────────────────────────────────

Terminal 1 - Backend:
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload

Terminal 2 - Frontend:
    cd frontend
    npm install
    npm run dev

Then open: http://localhost:5173


⚙️ PREREQUISITES
═══════════════════════════════════════════════════════════════

Required:
  • Python 3.8+         (check: python --version)
  • Node.js 16+         (check: node --version)
  • npm 8+              (check: npm --version)
  • ~500MB disk space

Optional:
  • GPU (NVIDIA/CUDA) for faster detection
  • IP camera for RTSP streams


📋 FIRST TIME USAGE
═══════════════════════════════════════════════════════════════

Step 1: Start Both Servers (see above)

Step 2: Open http://localhost:5173 in browser

Step 3: Configure Camera
    Screens → Camera Setup
    • Select "Webcam"
    • Click "Test Connection"
    • Click "Start Stream"

Step 4: Create Detection Rule
    Screens → Detection Rules
    • Rule Name: "Main Entry"
    • Object Type: "Person"
    • Threshold: 1
    • Click "Create Rule"

Step 5: View Live Dashboard
    Screens → Live Dashboard
    • Watch real-time video
    • See detection counts
    • Monitor alerts

Step 6: Setup Email Alerts
    Screens → Alert Settings
    • Add your email
    • Click "Send Test Email"
    • Verify configuration


🎯 WHAT EACH SCREEN DOES
═══════════════════════════════════════════════════════════════

Screen 1: Camera Setup
├── Configure video source (Webcam/RTSP/Upload)
├── Test camera connection
├── Start/stop video streaming
└── View stream status

Screen 2: Detection Rules
├── Create detection rules
├── Set alert thresholds
├── View active rules
└── Delete rules

Screen 3: Live Dashboard
├── Watch real-time video feed
├── See live detection counts
├── Monitor recent alerts
└── Check connection status

Screen 4: Alert Settings
├── Add email addresses for alerts
├── Manage alert recipients
├── Send test emails
└── View email configuration


🔧 BACKEND ENDPOINTS (11 Total)
═══════════════════════════════════════════════════════════════

Camera Operations:
  POST   /configure_camera     Configure video source
  POST   /start_stream         Begin detection
  POST   /stop_stream          Stop detection
  POST   /test_connection      Verify camera

Detection & Rules:
  GET    /get_detections       Current counts
  POST   /create_rule          Add detection rule
  GET    /get_rules            List all rules
  DELETE /delete_rule/{id}     Remove rule

Alerts & Notifications:
  POST   /configure_alerts     Set email recipients
  POST   /send_test_email      Test email
  GET    /get_alerts           Alert history

System:
  WS     /ws/stream            Live frame streaming
  GET    /health               System health check


📊 API DOCUMENTATION
═══════════════════════════════════════════════════════════════

Interactive Docs:    http://localhost:8000/docs
Alternative Format:  http://localhost:8000/redoc

Try endpoints directly in the browser!


🎨 UI COMPONENTS
═══════════════════════════════════════════════════════════════

Technologies Used:
  • React 18 - UI framework
  • Vite 5 - Build tool
  • Tailwind CSS - Styling
  • Lucide React - Icons
  • Axios - HTTP client
  • WebSocket API - Real-time streaming

Features:
  • Dark theme interface
  • Responsive design
  • Real-time updates
  • Status indicators
  • Smooth animations
  • Professional styling


🔐 OBJECT DETECTION
═══════════════════════════════════════════════════════════════

Model: YOLOv8 (Ultralytics)

Detectable Objects:
  👤 Persons      - Human detection
  🐾 Animals      - Dogs, cats, birds, etc.
  🚗 Vehicles     - Cars, trucks, motorcycles, etc.

Processing:
  • Real-time frame analysis
  • Bounding box visualization
  • Confidence scoring
  • JSON output format


⚡ PERFORMANCE
═══════════════════════════════════════════════════════════════

Typical Performance (On Average Hardware):
  • Frame Processing: 50-100ms per frame
  • Detection FPS: 5-15 FPS at 640x480
  • WebSocket Latency: ~30ms
  • Memory Usage: 200-300MB
  • CPU Usage: 20-40%

Optimization Tips:
  • Use RTSP at 720p or lower
  • Reduce frame processing rate
  • Use GPU if available (CUDA)
  • Monitor browser console


❌ TROUBLESHOOTING
═══════════════════════════════════════════════════════════════

Backend Won't Start:
  ✓ Check: python --version (needs 3.8+)
  ✓ Reinstall: pip install --upgrade -r requirements.txt
  ✓ Port in use: uvicorn main:app --port 8001

Frontend Won't Start:
  ✓ Clear cache: rm -rf node_modules && npm install
  ✓ Check Node: node --version (needs 16+)
  ✓ Port in use: npm run dev -- --port 5174

Connection Failed:
  ✓ Backend must run on port 8000
  ✓ Frontend must run on port 5173
  ✓ Check: curl http://localhost:8000/health

Camera Not Working:
  ✓ Webcam: Check browser permissions
  ✓ RTSP: Verify URL and camera is reachable
  ✓ Upload: Use MP4 or AVI format


📁 FILE LOCATIONS REFERENCE
═══════════════════════════════════════════════════════════════

Backend Entry Point:      backend/main.py
Frontend Entry Point:     frontend/src/main.jsx
Main React Component:     frontend/src/App.jsx
API Integration:          frontend/src/api.js
Screen Components:        frontend/src/screens/

Config Files:
  • vite.config.js
  • tailwind.config.js
  • postcss.config.js
  • package.json
  • requirements.txt


📚 DOCUMENTATION FILES
═══════════════════════════════════════════════════════════════

README.md             - Main documentation
QUICKSTART.md         - 5-minute start guide
INSTALLATION.md       - Detailed setup instructions
FEATURES.md           - Complete feature list
PROJECT_SUMMARY.md    - Architecture & overview


💾 DEPENDENCIES
═══════════════════════════════════════════════════════════════

Backend (Python):
  • fastapi            Web framework
  • uvicorn            ASGI server
  • opencv-python      Video processing
  • ultralytics        YOLOv8 detection
  • websockets         Real-time streaming
  • pydantic           Data validation

Frontend (Node):
  • react              UI framework
  • vite               Build tool
  • tailwindcss        Styling
  • axios              HTTP client
  • lucide-react       Icon library


🌐 NETWORK PORTS
═══════════════════════════════════════════════════════════════

Default Configuration:
  Frontend:     http://localhost:5173
  Backend:      http://localhost:8000
  API Docs:     http://localhost:8000/docs
  WebSocket:    ws://localhost:8000/ws/stream

Change Ports:
  Backend: uvicorn main:app --port 8001
  Frontend: npm run dev -- --port 5174


🎓 LEARNING RESOURCES
═══════════════════════════════════════════════════════════════

FastAPI:        https://fastapi.tiangolo.com/
YOLOv8:         https://docs.ultralytics.com/
OpenCV:         https://docs.opencv.org/
React:          https://react.dev/
Tailwind CSS:   https://tailwindcss.com/
Vite:           https://vitejs.dev/


🚀 DEPLOYMENT
═══════════════════════════════════════════════════════════════

Production Backend:
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:8000 main:app

Production Frontend:
  npm run build
  # Deploy dist/ folder to your web server


✨ WHAT YOU CAN DO
═══════════════════════════════════════════════════════════════

✓ Real-time video monitoring
✓ Automatic threat detection
✓ Custom alert rules
✓ Email notifications
✓ Alert history tracking
✓ System performance monitoring
✓ Multi-camera support (architecture ready)


🎯 NEXT STEPS
═══════════════════════════════════════════════════════════════

1. Read QUICKSTART.md for fast setup
2. Read README.md for full documentation
3. Read FEATURES.md for all capabilities
4. Try different camera sources
5. Create multiple detection rules
6. Configure email alerts
7. Monitor live detections
8. Deploy to production


💡 PRO TIPS
═══════════════════════════════════════════════════════════════

• Create rules BEFORE starting stream for testing
• Use "Send Test Email" to verify setup
• Check browser console (F12) for debugging
• Monitor API docs at /docs for all endpoints
• Test connection before starting stream
• Use RTSP at 720p for best performance


📞 SUPPORT
═══════════════════════════════════════════════════════════════

Installation Issues?  → See INSTALLATION.md
Feature Questions?   → See FEATURES.md
Usage Help?          → See README.md
Architecture Info?   → See PROJECT_SUMMARY.md
Quick Start?         → See QUICKSTART.md


🎉 YOU'RE ALL SET!
═══════════════════════════════════════════════════════════════

Your complete Intruder Detection System is ready!

1. Run: bash setup.sh (or setup.bat on Windows)
2. Start backend and frontend (see above)
3. Open: http://localhost:5173
4. Start detecting threats!


═══════════════════════════════════════════════════════════════

        Ready to Build Your Security System? 🚨
        
═══════════════════════════════════════════════════════════════

EOF
