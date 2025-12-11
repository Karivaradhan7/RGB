# 🚨 RGB Camera Detection System

Real-time **RTSP camera monitoring** with **AI-powered object detection**, **tracking**, and **email alerts**.

## 🎯 Features

- ✅ **Real-time RTSP Stream Processing** - Monitor Camera 3 continuously
- ✅ **AI Detection** - YOLOv8 for persons, animals, and vehicles
- ✅ **Object Tracking** - Track objects across frames
- ✅ **Email Alerts** - Send instant notifications to `karivaradhan7@gmail.com`
- ✅ **WebSocket Live Stream** - Real-time video to frontend
- ✅ **Web Dashboard** - Live detection dashboard and alerts
- ✅ **Supabase Integration** - Optional database for rules and logs
- ✅ **Docker Ready** - Container deployment support

## 📷 Camera Configuration

- **Camera**: Camera 3
- **Stream**: `rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101`
- **Alert Email**: `karivaradhan7@gmail.com`

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
cd /workspaces/RGB
python3 setup_quick.py
```

This will:
1. Create a Python virtual environment
2. Install all dependencies
3. Create a `.env` configuration file
4. Install frontend dependencies

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r backend/requirements.txt
cd frontend && npm install
cd ..

# 3. Create .env file (see Configuration section)
```

## ⚙️ Configuration

### 1. Create `.env` file in project root:

```bash
# Gmail Configuration
SENDER_EMAIL=karivaradhan7@gmail.com
SENDER_PASSWORD=your-gmail-app-password

# Camera RTSP URL
RTSP_URL=rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101

# Alert Recipients
ALERT_RECIPIENTS=karivaradhan7@gmail.com

# Optional: Supabase for database features
VITE_SUPABASE_URL=
VITE_SUPABASE_SUPABASE_ANON_KEY=
```

### 2. Gmail App Password Setup

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Generate an **App Password** (select "Mail" and "Windows Computer")
4. Copy the 16-character password
5. Paste it in `.env` as `SENDER_PASSWORD`

## 🏃 Running the System

### Terminal 1: Backend (FastAPI Server)

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd backend
python main.py
```

Server will start on `http://localhost:8000`

**Output:**
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

### Terminal 2: Frontend (React UI)

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd frontend
npm run dev
```

Open browser: `http://localhost:5173`

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 RTSP Camera Stream                      │
│   rtsp://admin:Mahesh@2025@103.59.107.2:554/...        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│          Backend (FastAPI) - Port 8000                  │
├─────────────────────────────────────────────────────────┤
│ • OpenCV: Frame capture & processing                   │
│ • YOLOv8: Object detection (person, animal, vehicle)   │
│ • Tracker: Object tracking across frames               │
│ • Email: SMTP alerts to recipients                     │
│ • WebSocket: Real-time stream to frontend              │
│ • Database: Optional Supabase integration              │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    Frontend       Email Alerts    Supabase
    (React UI)     (Gmail SMTP)     (Optional)
    :5173           :notifications  :database
```

## 🔧 API Endpoints

### Video Stream Control

- `POST /start_stream` - Start processing RTSP stream
- `POST /stop_stream` - Stop processing
- `GET /get_detections` - Get current detection counts
- `WebSocket /ws/stream` - Live video stream

### Rules & Alerts

- `POST /create_rule` - Create detection rule
- `GET /get_rules` - Get all rules
- `DELETE /delete_rule/{id}` - Delete rule
- `POST /configure_alerts` - Set alert recipients
- `GET /get_alerts` - Get recent alerts

### Health & Testing

- `GET /health` - Health check
- `GET /` - API info
- `POST /test_connection` - Test camera connection
- `POST /send_test_email` - Send test email

## 📝 Detection Rules Example

Create a rule via API:

```bash
curl -X POST http://localhost:8000/create_rule \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Person Detection",
    "object_type": "person",
    "threshold": 1
  }'
```

This will alert when 1 or more persons are detected.

## 🎯 Detection Categories

- **person**: Humans (high confidence detection)
- **animal**: Dogs, cats, birds, etc.
- **vehicle**: Cars, trucks, motorcycles, etc.

## 📧 Email Alert Example

When a person is detected:

```
Subject: 🚨 INTRUDER ALERT: Person Detection

⚠️ SECURITY ALERT

Rule: Person Detection
Detection Type: PERSON
Count Detected: 2
Time: 2025-12-11 14:30:45
Camera: Camera 3 (RTSP)

A detection event has been triggered. Please check your system immediately.
```

## 🐳 Docker Deployment (Optional)

```bash
docker-compose up -d
```

See `docker-compose.yml` for configuration.

## 📚 Project Structure

```
RGB/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── tracker.py           # Object tracking module
│   ├── requirements.txt      # Python dependencies
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── screens/         # Dashboard components
│   │   └── api.js           # API client
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── supabase/
│   └── migrations/          # Database schema
│
├── .env                     # Configuration (GITIGNORED)
├── .env.example             # Example configuration
├── setup_quick.py           # Automated setup script
└── README.md                # This file
```

## 🔐 Security Notes

1. **Never commit `.env`** - It contains sensitive credentials
2. **Use Gmail App Passwords**, not your actual password
3. **Keep RTSP credentials secure** - Don't share camera URLs
4. **Enable 2FA on Gmail** - Required for App Passwords

## 🚨 Troubleshooting

### Camera Not Connecting

```bash
# Test RTSP connection
curl -v rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101
```

### Emails Not Sending

1. Check `.env` has valid `SENDER_PASSWORD`
2. Enable **2-Step Verification** on Gmail
3. Use **App Password** (not regular password)
4. Check backend logs for errors

### Frontend Not Loading

```bash
# Clear npm cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Port Already in Use

```bash
# Backend (8000)
lsof -i :8000
kill -9 <PID>

# Frontend (5173)
lsof -i :5173
kill -9 <PID>
```

## 📊 Dependencies

**Backend (Python 3.8+)**
- `fastapi>=0.104` - Web framework
- `ultralytics>=8.3` - YOLOv8 object detection
- `opencv-python>=4.12` - Video processing
- `supabase>=2.3` - Database (optional)

**Frontend (Node.js 16+)**
- `react>=18` - UI framework
- `vite>=4` - Build tool
- `lucide-react` - UI icons
- `tailwindcss` - Styling

## 📈 Performance Tips

1. **Reduce frame processing frequency** - Adjust in `main.py`
2. **Lower detection confidence** - Faster but less accurate
3. **Use GPU** - If CUDA/GPU available for YOLOv8
4. **Optimize RTSP stream quality** - Lower resolution = faster
5. **Database queries** - Cache rules in memory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues or questions:
1. Check `backend/README.md` and `frontend/README.md`
2. Review troubleshooting section above
3. Check system logs for error messages

## 📄 License

This project is provided as-is for security monitoring purposes.

---

**Last Updated**: December 2025  
**Camera**: Camera 3 (RTSP)  
**Alert Email**: karivaradhan7@gmail.com
