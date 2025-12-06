# ⚡ Quick Start Guide

## 🎯 Get Running in 5 Minutes

### Prerequisites Check
```bash
python --version   # Should be 3.8+
node --version     # Should be 16+
npm --version      # Should be 8+
```

---

## Option A: Automated Setup (Easiest)

### Linux/macOS:
```bash
cd RGB
bash setup.sh
```

### Windows:
```bash
cd RGB
setup.bat
```

This script will:
✅ Install all Python dependencies
✅ Install all Node.js packages
✅ Display next steps

---

## Option B: Manual Setup (5 minutes)

### Terminal 1: Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Wait for message: `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2: Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Wait for message: `Local: http://localhost:5173/`

---

## 🌐 Open in Browser

Go to: **http://localhost:5173**

You'll see the Intruder Detection System UI!

---

## 📋 First Time User Flow

### 1. Camera Setup (1 minute)
```
Screens → Camera Setup
├── Select "Webcam"
├── Click "Test Connection"
└── Click "Start Stream"
```

### 2. Create Rule (1 minute)
```
Screens → Detection Rules
├── Rule Name: "Main Entry"
├── Object Type: "Person"
├── Threshold: 1
└── Click "Create Rule"
```

### 3. View Dashboard (1 minute)
```
Screens → Live Dashboard
├── See live video feed
├── Watch detection counts
└── Monitor alerts (if any)
```

### 4. Setup Alerts (1 minute)
```
Screens → Alert Settings
├── Add your email: user@example.com
├── Click "Send Test Email"
└── Check inbox (demo: check console)
```

---

## 🎬 Demo Walkthrough

### Without Webcam (Simulation):
1. Create rule with threshold 100
2. Detections won't exceed threshold
3. No alerts will trigger
4. But system is fully functional!

### With Webcam:
1. Create rule with threshold 1 (Person)
2. Stand in front of camera
3. Live detection counts update
4. If rule triggers, alert appears
5. Email would be sent

---

## 🛠️ Common Commands

### Start Backend Only:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Only:
```bash
cd frontend
npm run dev
```

### Run Frontend on Different Port:
```bash
cd frontend
npm run dev -- --port 5174
```

### Run Backend on Different Port:
```bash
cd backend
uvicorn main:app --port 8001
```

### View Backend API Docs:
```
Open: http://localhost:8000/docs
```

### Build Frontend for Production:
```bash
cd frontend
npm run build
```

---

## 📝 Accessing Different Screens

### From Navigation Bar:
- **Camera Setup** - Configure video source
- **Detection Rules** - Create alert rules
- **Live Dashboard** - Watch detections
- **Alert Settings** - Configure emails

---

## 🔌 Testing APIs Directly

### Test Backend Health:
```bash
curl http://localhost:8000/health
```

### Get Current Detections:
```bash
curl http://localhost:8000/get_detections
```

### View API Documentation:
```
http://localhost:8000/docs
```

---

## ❌ Troubleshooting

### Backend won't start:
```bash
# Make sure Python is installed
python3 -m pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend won't start:
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### CORS errors in browser:
- Backend must be running on `http://localhost:8000`
- Frontend must be on `http://localhost:5173`
- Check browser console for details

### "Port already in use":
- Change the port: `uvicorn main:app --port 8001`
- Or kill existing process on that port

---

## 🎓 Next Steps

### Learn the System:
1. Read `README.md` - Full documentation
2. Read `FEATURES.md` - All features explained
3. Read `PROJECT_SUMMARY.md` - Architecture overview

### Deploy to Production:
See `INSTALLATION.md` → "Building for Production"

### Customize:
- Add your own detection logic
- Modify email notifications
- Extend with database
- Add authentication

---

## 📊 Project Structure

```
RGB/
├── backend/main.py         # 600+ lines, all endpoints
├── frontend/src/App.jsx    # Main React component
├── frontend/src/screens/   # 4 screen components
└── Documentation/          # 5 guide files
```

---

## ✨ Key Features

✅ Real-time YOLOv8 detection
✅ Custom rule creation
✅ Email alert notifications
✅ Live WebSocket streaming
✅ Beautiful React UI
✅ Full REST API
✅ Production-ready code

---

## 🚀 System Status

After starting both servers:

- ✅ Backend: `http://localhost:8000`
- ✅ Frontend: `http://localhost:5173`
- ✅ API Docs: `http://localhost:8000/docs`
- ✅ WebSocket: `ws://localhost:8000/ws/stream`

---

## 💡 Pro Tips

1. **Create rules before streaming** for quick testing
2. **Use "Send Test Email"** to verify settings
3. **Check browser console** (F12) for debugging
4. **Monitor detection counts** in live dashboard
5. **Test connection** before starting stream

---

## 🎯 What You Can Do Now

✅ Monitor real-time video
✅ Create custom detection rules
✅ Get email alerts on detections
✅ View detection history
✅ Test the complete system
✅ Understand modern web architecture
✅ Deploy to production

---

## 📞 Need Help?

| Issue | Solution |
|-------|----------|
| Won't start | Check `INSTALLATION.md` |
| Feature question | Check `FEATURES.md` |
| How to use | Check `README.md` |
| Architecture | Check `PROJECT_SUMMARY.md` |
| Setup issues | Run `setup.sh` or `setup.bat` |

---

## 🎉 You're All Set!

**Enjoy your Intruder Detection System!**

```
🚨 Real-time threat detection at your fingertips
```

---

*For full documentation, see the other .md files in the project root*
