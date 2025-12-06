# 🚨 INTRUDER DETECTION SYSTEM - COMPLETE SETUP & RUN GUIDE

## 📋 TABLE OF CONTENTS
1. Prerequisites
2. Automated Setup
3. Manual Setup
4. Running the Application
5. First Time Usage
6. API Testing
7. Troubleshooting

---

## ✅ PREREQUISITES

Make sure you have installed:
- **Python 3.8+** → Check: `python --version`
- **Node.js 16+** → Check: `node --version`
- **npm 8+** → Check: `npm --version`

---

## 🚀 OPTION 1: AUTOMATED SETUP (RECOMMENDED)

### For Linux/macOS:
```bash
bash setup.sh
```

### For Windows:
```bash
setup.bat
```

This will automatically install all dependencies. Then jump to "Running the Application" section.

---

## 🔧 OPTION 2: MANUAL SETUP

### Step 1: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**This installs:**
- FastAPI (web framework)
- Uvicorn (ASGI server)
- OpenCV (video processing)
- YOLOv8 (object detection)
- WebSockets (real-time streaming)
- And more...

### Step 2: Install Frontend Dependencies
```bash
cd frontend
npm install
```

**This installs:**
- React 18
- Vite
- Tailwind CSS
- Axios
- Lucide Icons
- And more...

---

## ▶️ RUNNING THE APPLICATION

You need **TWO TERMINALS** - one for backend, one for frontend.

### 📺 TERMINAL 1: START BACKEND

Copy and paste this command:

```bash
cd /workspaces/RGB/backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Or if using virtual environment:**

```bash
cd /workspaces/RGB/backend && /workspaces/RGB/.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
INFO:     Started reloader process
```

✅ **Backend is ready at:** http://localhost:8000

---

### 🌐 TERMINAL 2: START FRONTEND

Open a **NEW TERMINAL** and copy-paste:

```bash
cd /workspaces/RGB/frontend && npm run dev
```

**Expected Output:**
```
VITE v5.4.21 ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ **Frontend is ready at:** http://localhost:5173

---

## 🌍 ACCESSING THE APPLICATION

Once both servers are running:

**Open in your browser:** http://localhost:5173

You should see:
- Dark-themed UI
- 4 navigation tabs
- Camera configuration screen

---

## 📖 FIRST TIME USAGE FLOW

### Step 1: Configure Camera (2 minutes)
```
1. Click "Camera Setup" tab
2. Select "Webcam"
3. Click "Test Connection" button
4. Click "Start Stream" button
→ Video stream begins
```

### Step 2: Create Detection Rule (1 minute)
```
1. Click "Detection Rules" tab
2. Enter Rule Name: "Main Entry"
3. Select Object Type: "Person"
4. Set Threshold: "1"
5. Click "Create Rule" button
→ Rule is created and active
```

### Step 3: View Live Dashboard (1 minute)
```
1. Click "Live Dashboard" tab
2. See real-time video with bounding boxes
3. Check detection counts (Persons/Animals/Vehicles)
4. Monitor recent alerts
→ Live detection working!
```

### Step 4: Setup Email Alerts (1 minute)
```
1. Click "Alert Settings" tab
2. Enter your email: user@example.com
3. Click "Add" button
4. Click "Send Test Email" button
→ Alert system configured
```

---

## 🔌 API ENDPOINTS (FOR TESTING)

### View Interactive API Documentation:
```
http://localhost:8000/docs
```

### Test Endpoints with curl:

**Check Backend Health:**
```bash
curl http://localhost:8000/health
```

**Get Current Detections:**
```bash
curl http://localhost:8000/get_detections
```

**Get Active Rules:**
```bash
curl http://localhost:8000/get_rules
```

**Get Recent Alerts:**
```bash
curl http://localhost:8000/get_alerts
```

---

## 📱 4 MAIN SCREENS

### Screen 1: Camera Configuration
- Select video source (Webcam/RTSP/Upload)
- Enter RTSP URL for IP cameras
- Test camera connection
- Start/stop stream

### Screen 2: Detection Rules
- Create custom detection rules
- Set object type (Person/Animal/Vehicle)
- Configure threshold (1-50)
- View and delete existing rules

### Screen 3: Live Dashboard
- Real-time video feed
- Live detection counters
- Recent alerts display
- Connection status

### Screen 4: Alert Settings
- Add multiple email addresses
- Send test emails
- Verify alert configuration

---

## 🛠️ CHANGING PORTS (If default ports are in use)

### Change Backend Port:
```bash
cd /workspaces/RGB/backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```
Then update frontend API URL in `/frontend/src/api.js` from `8000` to `8001`

### Change Frontend Port:
```bash
cd /workspaces/RGB/frontend && npm run dev -- --port 5174
```

---

## 🐛 TROUBLESHOOTING

### Backend Won't Start: "Python not found"
```bash
python3 --version
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload
```

### Frontend Won't Start: "npm not found"
```bash
node --version
npm install
npm run dev
```

### Port Already in Use (8000 or 5173)
```bash
# Find and kill process on port 8000:
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Find and kill process on port 5173:
lsof -i :5173 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Connection Refused Error
- Make sure backend is running on port 8000
- Make sure frontend is running on port 5173
- Check firewall settings
- Look at browser console (F12) for errors

### Camera Not Working
- **Webcam:** Check browser permissions for camera
- **RTSP:** Verify URL format and camera is reachable
- **Upload:** Use MP4 or AVI video files

### Slow Performance
- Reduce video resolution
- Use lower quality camera stream
- Close other applications
- Check CPU usage

---

## 🔍 MONITORING LOGS

### Backend Console Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
INFO:     GET /health 200 OK
INFO:     POST /start_stream 200 OK
```

### Frontend Console Output:
```
VITE v5.4.21 ready in XXX ms
[vite] connected
```

### Browser Console (F12):
- WebSocket connection messages
- API request/response logs
- Any JavaScript errors

---

## 📊 COMPLETE COMMAND REFERENCE

| Task | Command |
|------|---------|
| Install backend deps | `cd backend && pip install -r requirements.txt` |
| Install frontend deps | `cd frontend && npm install` |
| Start backend | `cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000` |
| Start frontend | `cd frontend && npm run dev` |
| View API docs | Open http://localhost:8000/docs |
| View application | Open http://localhost:5173 |
| Test backend health | `curl http://localhost:8000/health` |
| Build frontend | `cd frontend && npm run build` |
| Clean install | `rm -rf backend/__pycache__ frontend/node_modules && pip install -r backend/requirements.txt && cd frontend && npm install` |

---

## 🎯 QUICK COPY-PASTE COMMANDS

### Setup Everything (First Time):
```bash
# Terminal 1
cd /workspaces/RGB/backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 (in new terminal)
cd /workspaces/RGB/frontend
npm install
npm run dev

# Browser
# Open: http://localhost:5173
```

### Just Run (After First Setup):
```bash
# Terminal 1
cd /workspaces/RGB/backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2
cd /workspaces/RGB/frontend && npm run dev

# Browser
# Open: http://localhost:5173
```

---

## 📚 ADDITIONAL RESOURCES

**Documentation Files:**
- `README.md` - Main documentation
- `QUICKSTART.md` - 5-minute setup
- `INSTALLATION.md` - Detailed setup guide
- `FEATURES.md` - Complete feature list
- `PROJECT_SUMMARY.md` - Architecture details

**GitHub Repository:**
https://github.com/Karivaradhan7/RGB

**Backend API:**
http://localhost:8000/docs (Interactive Swagger UI)

**Frontend Application:**
http://localhost:5173

---

## ✨ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────┐
│           INTRUDER DETECTION SYSTEM                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Frontend (React + Tailwind)    Backend (FastAPI)  │
│  http://localhost:5173           http://localhost:8000
│  ┌──────────────────────┐       ┌──────────────────┐
│  │ • Camera Config      │       │ • YOLOv8 Model   │
│  │ • Detection Rules    │       │ • OpenCV         │
│  │ • Live Dashboard     │◄─────►│ • WebSocket      │
│  │ • Alert Settings     │       │ • REST API       │
│  │                      │       │ • Email Service  │
│  └──────────────────────┘       └──────────────────┘
│         WebSocket & REST API Connection            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎉 YOU'RE ALL SET!

Your complete Intruder Detection System is ready to use!

**Start with:**
1. Terminal 1: Run backend command
2. Terminal 2: Run frontend command
3. Browser: Visit http://localhost:5173
4. Start detecting threats!

---

**Made with ❤️ for security monitoring**
