# Installation Guide

## Prerequisites

- **Python 3.8+** - Download from https://www.python.org/
- **Node.js 16+** - Download from https://nodejs.org/
- **npm** - Comes with Node.js
- **pip** - Python package manager (comes with Python)

Verify installation:
```bash
python --version
node --version
npm --version
```

## Automated Setup (Recommended)

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

This will automatically install all dependencies.

---

## Manual Setup

### Step 1: Backend Installation

```bash
# Navigate to backend
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi uvicorn opencv-python ultralytics numpy ...
```

### Step 2: Frontend Installation

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

**Expected output:**
```
added XXX packages in X.XXs
```

---

## Running the Application

### Terminal 1 - Start Backend:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2 - Start Frontend:
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

### Open in Browser:
Navigate to: **http://localhost:5173**

---

## First Time Setup Tips

1. **Backend will download YOLOv8 model** on first run (~130MB)
   - This happens automatically when you start the backend
   - Takes 1-2 minutes for first download

2. **Frontend hot-reload enabled** 
   - Changes to React files auto-refresh in browser

3. **API Documentation** available at:
   - http://localhost:8000/docs (interactive)
   - http://localhost:8000/redoc (detailed docs)

---

## Troubleshooting Installation

### Python version issue:
```bash
# If python command not found, try:
python3 --version
python3 -m pip install -r requirements.txt
```

### Permission denied on Linux/Mac:
```bash
# Make setup script executable
chmod +x setup.sh
```

### Module not found errors:
```bash
# Clear cache and reinstall
pip cache purge
pip install --upgrade -r requirements.txt
```

### npm install fails:
```bash
# Try clearing npm cache
npm cache clean --force
npm install
```

### Port already in use:
```bash
# Backend on different port:
uvicorn main:app --port 8001

# Frontend on different port:
npm run dev -- --port 5174
```

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 2GB | 8GB+ |
| CPU | 2 cores | 4+ cores |
| Storage | 500MB | 2GB+ |
| Browser | Chrome 60+ | Chrome/Firefox latest |

---

## Next Steps

After successful installation:

1. Go to **Camera Setup** tab
2. Select "Webcam" and click "Start Stream"
3. Go to **Detection Rules** and create a test rule
4. View live detections in **Live Dashboard**
5. Configure emails in **Alert Settings**

For detailed usage, see the main README.md
