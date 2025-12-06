@echo off
REM Intruder Detection System - Quick Start (Windows)

echo.
echo 🚀 Intruder Detection System - Quick Start
echo ==========================================
echo.

REM Check if running from project root
if not exist "README.md" (
    echo ❌ Please run this script from the project root directory
    exit /b 1
)

echo 📦 Setting up Backend...
echo.

REM Backend setup
cd backend

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed
    exit /b 1
)

echo ✅ Python found
echo 📥 Installing backend dependencies...

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    exit /b 1
)

echo ✅ Backend dependencies installed

cd ..

echo.
echo 📦 Setting up Frontend...
echo.

REM Check Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is required but not installed
    exit /b 1
)

echo ✅ Node.js found

cd frontend

echo 📥 Installing frontend dependencies...
npm install

if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    exit /b 1
)

echo ✅ Frontend dependencies installed

cd ..

echo.
echo 🎉 Setup Complete!
echo.
echo To run the application:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:5173
echo.
