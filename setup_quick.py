#!/usr/bin/env python3
"""
Quick Start Script for RGB Camera Detection System
Automatically sets up environment and starts the system
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional

# Configuration
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
ENV_FILE = PROJECT_ROOT / ".env"
VENV_DIR = PROJECT_ROOT / "venv"

# Default values
DEFAULT_CONFIG = {
    "RTSP_URL": "rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101",
    "SENDER_EMAIL": "karivaradhan7@gmail.com",
    "ALERT_RECIPIENTS": "karivaradhan7@gmail.com"
}

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def print_warning(text):
    """Print warning message"""
    print(f"⚠️  {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def create_venv():
    """Create Python virtual environment"""
    print_info("Creating virtual environment...")
    
    if VENV_DIR.exists():
        print_success(f"Virtual environment already exists at {VENV_DIR}")
        return
    
    try:
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
        print_success("Virtual environment created")
    except Exception as e:
        print_error(f"Failed to create virtual environment: {e}")
        sys.exit(1)

def get_python_executable():
    """Get the path to python in venv"""
    if os.name == 'nt':  # Windows
        return VENV_DIR / "Scripts" / "python.exe"
    else:  # Unix-like
        return VENV_DIR / "bin" / "python"

def install_dependencies():
    """Install Python dependencies"""
    print_info("Installing Python dependencies...")
    
    python_exe = get_python_executable()
    requirements_file = BACKEND_DIR / "requirements.txt"
    
    if not requirements_file.exists():
        print_error(f"Requirements file not found: {requirements_file}")
        sys.exit(1)
    
    try:
        # Upgrade pip
        subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)], check=True)
        print_success("Dependencies installed")
    except Exception as e:
        print_error(f"Failed to install dependencies: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file with default configuration"""
    if ENV_FILE.exists():
        print_success(".env file already exists")
        return
    
    print_info("Creating .env file...")
    
    env_content = f"""# RGB Camera Detection System Configuration
# Created: {Path(__file__).name}

# ============================================
# Supabase Configuration (Optional)
# ============================================
VITE_SUPABASE_URL=
VITE_SUPABASE_SUPABASE_ANON_KEY=

# ============================================
# Email Configuration for Alerts
# ============================================
SENDER_EMAIL={DEFAULT_CONFIG['SENDER_EMAIL']}
SENDER_PASSWORD=your-gmail-app-password

# ============================================
# Camera Configuration (RTSP URL for Camera 3)
# ============================================
RTSP_URL={DEFAULT_CONFIG['RTSP_URL']}

# ============================================
# Alert Recipients
# ============================================
ALERT_RECIPIENTS={DEFAULT_CONFIG['ALERT_RECIPIENTS']}

# ============================================
# Email Configuration Help
# ============================================
# For Gmail:
# 1. Enable 2-Factor Authentication
# 2. Generate an App Password at https://myaccount.google.com/apppasswords
# 3. Copy the 16-character password and paste above
"""
    
    try:
        with open(ENV_FILE, 'w') as f:
            f.write(env_content)
        print_success(f".env file created at {ENV_FILE}")
        print_warning(f"⚠️  Please edit {ENV_FILE} and set SENDER_PASSWORD")
    except Exception as e:
        print_error(f"Failed to create .env file: {e}")
        sys.exit(1)

def install_frontend_deps():
    """Install frontend dependencies"""
    print_info("Installing frontend dependencies...")
    
    try:
        os.chdir(FRONTEND_DIR)
        subprocess.run(["npm", "install", "--legacy-peer-deps"], check=True)
        print_success("Frontend dependencies installed")
    except subprocess.CalledProcessError:
        # Try without legacy-peer-deps
        try:
            subprocess.run(["npm", "install"], check=True)
            print_success("Frontend dependencies installed")
        except Exception as e:
            print_warning(f"npm install failed: {e}")
    except Exception as e:
        print_warning(f"npm not found or not installed: {e}")

def check_dependencies():
    """Check if all required tools are available"""
    print_info("Checking system dependencies...")
    
    required = ['python3', 'npm']
    missing = []
    
    for tool in required:
        result = subprocess.run(['which', tool], capture_output=True)
        if result.returncode != 0 and tool != 'npm':
            missing.append(tool)
    
    if missing:
        print_error(f"Missing dependencies: {', '.join(missing)}")
        return False
    
    print_success("All required dependencies found")
    return True

def show_startup_instructions():
    """Show instructions for starting the system"""
    print_header("✅ SETUP COMPLETE - NEXT STEPS")
    
    print("1. Edit your .env file with Gmail App Password:")
    print(f"   nano {ENV_FILE}")
    print()
    
    print("2. Activate virtual environment and start backend:")
    if os.name == 'nt':  # Windows
        print(f"   .\\venv\\Scripts\\activate")
        print(f"   cd backend && python main.py")
    else:  # Unix-like
        print(f"   source venv/bin/activate")
        print(f"   cd backend && python main.py")
    print()
    
    print("3. In another terminal, start the frontend:")
    if os.name == 'nt':  # Windows
        print(f"   .\\venv\\Scripts\\activate")
        print(f"   cd frontend && npm run dev")
    else:  # Unix-like
        print(f"   source venv/bin/activate")
        print(f"   cd frontend && npm run dev")
    print()
    
    print("📷 Camera Configuration:")
    print(f"   RTSP URL: {DEFAULT_CONFIG['RTSP_URL']}")
    print(f"   Alert Email: {DEFAULT_CONFIG['SENDER_EMAIL']}")
    print()
    
    print("🌐 Web Interface:")
    print("   Frontend: http://localhost:5173")
    print("   Backend API: http://localhost:8000")
    print()

def main():
    """Main setup routine"""
    print_header("🚀 RGB CAMERA DETECTION SYSTEM - QUICK START")
    
    # Check dependencies
    if not check_dependencies():
        print_error("Please install missing dependencies and try again")
        sys.exit(1)
    
    # Create virtual environment
    create_venv()
    
    # Install Python dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Try to install frontend dependencies
    try:
        install_frontend_deps()
    except KeyboardInterrupt:
        print_warning("Skipped frontend installation")
    
    # Show instructions
    show_startup_instructions()
    
    print("="*60)
    print("For detailed documentation, see:")
    print("  - README.md - Project overview")
    print("  - QUICK_RUN.sh - Quick start script")
    print("  - backend/README.md - Backend documentation")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        sys.exit(1)
