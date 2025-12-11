#!/usr/bin/env python3
"""
Verify that all required packages are installed and importable
"""

import sys
from typing import List, Tuple

# Color output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def check_imports() -> Tuple[List[str], List[Tuple[str, str]]]:
    """Check all required imports"""
    
    packages = {
        'fastapi': 'FastAPI Web Framework',
        'uvicorn': 'ASGI Server',
        'cv2': 'OpenCV (Computer Vision)',
        'numpy': 'Numerical Computing',
        'ultralytics': 'YOLOv8 Object Detection',
        'pydantic': 'Data Validation',
        'dotenv': 'Environment Configuration',
        'supabase': 'Supabase Database (Optional)',
    }
    
    installed = []
    missing = []
    
    print(f"\n{Colors.BLUE}Checking Python Packages...{Colors.RESET}\n")
    
    for package, description in packages.items():
        try:
            __import__(package)
            installed.append(package)
            print(f"{Colors.GREEN}✓{Colors.RESET} {package:20} - {description}")
        except ImportError:
            missing.append((package, description))
            print(f"{Colors.RED}✗{Colors.RESET} {package:20} - {description} {Colors.YELLOW}(MISSING){Colors.RESET}")
    
    return installed, missing

def main():
    """Main verification routine"""
    
    print("\n" + "="*70)
    print("RGB CAMERA DETECTION SYSTEM - DEPENDENCY CHECK")
    print("="*70)
    
    print(f"Python Version: {sys.version}")
    print(f"Executable: {sys.executable}")
    
    installed, missing = check_imports()
    
    print("\n" + "="*70)
    print(f"Summary: {len(installed)} installed, {len(missing)} missing")
    print("="*70)
    
    if missing:
        print(f"\n{Colors.YELLOW}Missing Packages:{Colors.RESET}")
        for package, description in missing:
            print(f"  - {package}: {description}")
        
        print(f"\n{Colors.YELLOW}To install, run:{Colors.RESET}")
        print(f"  pip install -r backend/requirements.txt")
        return 1
    else:
        print(f"\n{Colors.GREEN}✓ All required packages are installed!{Colors.RESET}")
        print(f"\n{Colors.GREEN}Ready to start the system:{Colors.RESET}")
        print(f"  1. cd backend")
        print(f"  2. python main.py")
        return 0

if __name__ == "__main__":
    sys.exit(main())
