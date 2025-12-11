#!/usr/bin/env python3
"""
RGB Camera Detection System with Real-time Tracking and Email Alerts
Features:
- RTSP stream processing with YOLO v8
- Deep-Sort tracking
- Email alerts on detection
- WebSocket streaming to frontend
- Supabase integration (optional)
"""

from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime, timedelta
import json
import base64
from io import BytesIO
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time

load_dotenv()

# ============================================
# Configuration
# ============================================

RTSP_URL = os.getenv("RTSP_URL", "rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "karivaradhan7@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
ALERT_RECIPIENTS = os.getenv("ALERT_RECIPIENTS", "karivaradhan7@gmail.com").split(',')

# Supabase (optional)
supabase = None
try:
    from supabase import create_client, Client
    supabase_url = os.getenv("VITE_SUPABASE_URL")
    supabase_key = os.getenv("VITE_SUPABASE_SUPABASE_ANON_KEY")
    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)
        print("[✓] Supabase configured")
    else:
        print("[!] Supabase not configured - running in demo mode")
except:
    print("[!] Supabase not available - running in demo mode")

# ============================================
# FastAPI App Setup
# ============================================

app = FastAPI(title="RGB Detection System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Data Models
# ============================================

class CameraConfig(BaseModel):
    source_type: str
    rtsp_url: Optional[str] = None
    video_file: Optional[str] = None

class Rule(BaseModel):
    rule_id: Optional[str] = None
    name: str
    object_type: str
    threshold: int

class AlertSettings(BaseModel):
    emails: List[str]

class Alert(BaseModel):
    timestamp: str
    rule_name: str
    object_type: str
    count: int
    message: str

# ============================================
# Global State
# ============================================

camera_config = CameraConfig(source_type="rtsp", rtsp_url=RTSP_URL)
is_streaming = False
current_detections = {
    "person": 0,
    "animal": 0,
    "vehicle": 0,
    "timestamp": None
}
connected_clients = []
last_alert_time = {}  # Track last alert time per rule to avoid spam
ALERT_COOLDOWN = 5  # seconds between alerts for same rule

# ============================================
# Detection Model
# ============================================

print("[*] Loading YOLO model...")
model = YOLO("yolov8n.pt")
print("[✓] Model loaded")

def map_yolo_to_category(class_name):
    """Map YOLO class names to detection categories"""
    class_name = class_name.lower()
    if "person" in class_name or "human" in class_name:
        return "person"
    elif "dog" in class_name or "cat" in class_name or "animal" in class_name or "bird" in class_name or "horse" in class_name or "sheep" in class_name or "cow" in class_name:
        return "animal"
    elif "car" in class_name or "truck" in class_name or "bus" in class_name or "motorcycle" in class_name or "vehicle" in class_name or "bicycle" in class_name:
        return "vehicle"
    return None

def run_detection(frame):
    """Run YOLO detection on frame"""
    results = model(frame, verbose=False, conf=0.5)
    detections = {"person": 0, "animal": 0, "vehicle": 0}
    boxes = []
    
    for result in results:
        for box in result.boxes:
            class_name = model.names[int(box.cls[0])]
            category = map_yolo_to_category(class_name)
            if category:
                detections[category] += 1
                x1, y1, x2, y2 = box.xyxy[0]
                boxes.append({
                    "category": category,
                    "coords": [int(x1), int(y1), int(x2), int(y2)],
                    "confidence": float(box.conf[0])
                })
    
    return detections, boxes

def draw_boxes(frame, boxes):
    """Draw detection boxes on frame"""
    colors = {"person": (0, 255, 0), "animal": (255, 0, 0), "vehicle": (0, 0, 255)}
    
    for box in boxes:
        x1, y1, x2, y2 = box["coords"]
        color = colors.get(box["category"], (255, 255, 255))
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{box['category']} ({box['confidence']:.2f})"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    # Add timestamp
    cv2.putText(frame, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return frame

def encode_frame(frame):
    """Encode frame to base64 JPEG"""
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

async def send_alert_email(rule_name, object_type, count, emails=None):
    """Send alert email using SMTP with HTML formatting"""
    if emails is None:
        emails = ALERT_RECIPIENTS
    
    if not SENDER_PASSWORD:
        print(f"[!] Email disabled - SENDER_PASSWORD not configured")
        print(f"[*] Alert would be sent: {rule_name} - {object_type} count: {count}")
        return False
    
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        subject = f"🚨 INTRUDER ALERT: {rule_name}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="background-color: #ff4444; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                    <h2 style="margin: 0;">⚠️ SECURITY ALERT</h2>
                </div>
                
                <div style="background-color: white; padding: 20px; border-radius: 5px;">
                    <p><strong>Rule:</strong> {rule_name}</p>
                    <p><strong>Detection Type:</strong> {object_type.upper()}</p>
                    <p><strong>Count Detected:</strong> {count}</p>
                    <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Camera:</strong> Camera 3 (RTSP)</p>
                    <hr>
                    <p style="color: #666;">
                        A detection event has been triggered. Please check your system immediately.
                    </p>
                </div>
                
                <div style="margin-top: 20px; font-size: 12px; color: #999;">
                    <p>Camera Monitoring System - Automated Alert</p>
                </div>
            </body>
        </html>
        """
        
        def send_email_thread():
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                
                for email in emails:
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = subject
                    msg['From'] = SENDER_EMAIL
                    msg['To'] = email
                    msg.attach(MIMEText(html_body, 'html'))
                    
                    server.send_message(msg)
                    print(f"[✓] EMAIL SENT to {email} | {rule_name} | {object_type}×{count} | {datetime.now().strftime('%H:%M:%S')}")
                
                server.quit()
                return True
            except Exception as e:
                print(f"[✗] EMAIL ERROR: {str(e)}")
                return False
        
        thread = threading.Thread(target=send_email_thread, daemon=True)
        thread.start()
        return True
        
    except Exception as e:
        print(f"[✗] EMAIL ERROR: {str(e)}")
        return False

async def check_rules():
    """Check detection rules and send alerts"""
    global current_detections, last_alert_time

    if not supabase:
        return

    try:
        response = supabase.table("detection_rules").select("*").eq("is_active", True).execute()
        rules = response.data

        response = supabase.table("alert_settings").select("email").eq("is_active", True).execute()
        emails = [item["email"] for item in response.data]

        for rule in rules:
            count = current_detections.get(rule["object_type"], 0)
            rule_id = rule["id"]
            
            # Check cooldown
            last_time = last_alert_time.get(rule_id, datetime.min)
            if datetime.now() - last_time < timedelta(seconds=ALERT_COOLDOWN):
                continue
            
            if count > rule["threshold"]:
                alert_data = {
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "object_type": rule["object_type"],
                    "count": count,
                    "message": f"Alert: {rule['name']} - {rule['object_type']} count ({count}) exceeded threshold ({rule['threshold']})"
                }

                supabase.table("alerts").insert(alert_data).execute()
                last_alert_time[rule_id] = datetime.now()

                if emails:
                    await send_alert_email(rule["name"], rule["object_type"], count, emails)

                alert_data["timestamp"] = datetime.now().isoformat()
                await broadcast_alert(alert_data)
    except Exception as e:
        print(f"[!] Error checking rules: {e}")

async def broadcast_alert(alert):
    """Broadcast alert to all connected WebSocket clients"""
    for client in connected_clients:
        try:
            await client.send_json({"type": "alert", "data": alert})
        except:
            pass

async def process_stream(cap):
    """Main stream processing loop"""
    global is_streaming, current_detections

    frame_count = 0
    print("[*] Starting stream processing...")
    
    while is_streaming:
        try:
            ret, frame = cap.read()
            if not ret:
                print("[!] Stream ended or disconnected")
                break

            frame = cv2.resize(frame, (640, 480))
            detections, boxes = run_detection(frame)
            frame = draw_boxes(frame, boxes)

            current_detections = {
                "person": detections["person"],
                "animal": detections["animal"],
                "vehicle": detections["vehicle"],
                "timestamp": datetime.now().isoformat()
            }

            await check_rules()

            # Log detections periodically
            if frame_count % 30 == 0 and detections["person"] > 0:
                print(f"[*] Frame {frame_count}: {detections}")
                if supabase:
                    try:
                        supabase.table("detection_logs").insert({
                            "person_count": detections["person"],
                            "animal_count": detections["animal"],
                            "vehicle_count": detections["vehicle"]
                        }).execute()
                    except:
                        pass

            # Send frame to WebSocket clients
            if frame_count % 3 == 0:
                try:
                    encoded_frame = encode_frame(frame)
                    for client in connected_clients:
                        try:
                            await client.send_json({
                                "type": "frame",
                                "data": encoded_frame,
                                "detections": current_detections
                            })
                        except:
                            pass
                except:
                    pass

            frame_count += 1
            await asyncio.sleep(0.01)
            
        except Exception as e:
            print(f"[!] Stream processing error: {e}")
            await asyncio.sleep(1)

@app.post("/configure_camera")
async def configure_camera_endpoint(config: CameraConfig):
    """Configure camera source"""
    global camera_config
    camera_config = config
    
    try:
        if supabase:
            supabase.table("camera_configs").update({"is_active": False}).neq("id", "00000000-0000-0000-0000-000000000000").execute()
            supabase.table("camera_configs").insert({
                "source_type": config.source_type,
                "rtsp_url": config.rtsp_url,
                "video_file": config.video_file,
                "is_active": True
            }).execute()
    except Exception as e:
        print(f"[!] Error saving camera config: {e}")

    return {"status": "success", "message": "Camera configured"}

@app.post("/start_stream")
async def start_stream():
    """Start processing video stream"""
    global is_streaming, camera_config

    if is_streaming:
        return {"status": "error", "message": "Stream already running"}

    if not camera_config:
        return {"status": "error", "message": "Camera not configured"}

    print(f"[*] Starting stream from: {camera_config.source_type}")
    
    is_streaming = True

    try:
        if camera_config.source_type == "webcam":
            cap = cv2.VideoCapture(0)
        elif camera_config.source_type == "rtsp":
            print(f"[*] Connecting to RTSP: {camera_config.rtsp_url}")
            cap = cv2.VideoCapture(camera_config.rtsp_url)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer for lower latency
        elif camera_config.source_type == "upload":
            cap = cv2.VideoCapture(camera_config.video_file)
        else:
            return {"status": "error", "message": "Invalid source type"}

        # Test connection
        ret, _ = cap.read()
        if not ret:
            is_streaming = False
            return {"status": "error", "message": "Failed to connect to camera"}

        asyncio.create_task(process_stream(cap))
        return {"status": "success", "message": "Stream started"}
    except Exception as e:
        is_streaming = False
        return {"status": "error", "message": str(e)}

@app.post("/stop_stream")
async def stop_stream():
    """Stop processing video stream"""
    global is_streaming
    is_streaming = False
    print("[*] Stream stopped")
    return {"status": "success", "message": "Stream stopped"}

@app.get("/get_detections")
async def get_detections():
    """Get current detection counts"""
    return current_detections

@app.post("/create_rule")
async def create_rule_endpoint(rule: Rule):
    """Create a new detection rule"""
    if not supabase:
        return {"status": "error", "message": "Database not configured"}
    
    try:
        response = supabase.table("detection_rules").insert({
            "name": rule.name,
            "object_type": rule.object_type,
            "threshold": rule.threshold,
            "is_active": True
        }).execute()

        return {"status": "success", "rule_id": response.data[0]["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_rules")
async def get_rules():
    """Get all active detection rules"""
    if not supabase:
        return []
    
    try:
        response = supabase.table("detection_rules").select("*").eq("is_active", True).order("created_at", desc=True).execute()
        rules_data = []
        for rule in response.data:
            rules_data.append({
                "rule_id": rule["id"],
                "name": rule["name"],
                "object_type": rule["object_type"],
                "threshold": rule["threshold"]
            })
        return rules_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete_rule/{rule_id}")
async def delete_rule(rule_id: str):
    """Delete a detection rule"""
    if not supabase:
        return {"status": "error", "message": "Database not configured"}
    
    try:
        supabase.table("detection_rules").update({"is_active": False}).eq("id", rule_id).execute()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/configure_alerts")
async def configure_alerts(settings: AlertSettings):
    """Configure alert email settings"""
    if not supabase:
        return {"status": "error", "message": "Database not configured"}
    
    try:
        for email in settings.emails:
            try:
                supabase.table("alert_settings").insert({
                    "email": email,
                    "is_active": True
                }).execute()
            except:
                pass
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send_test_email")
async def send_test_email(emails: List[str]):
    """Send test email to configured addresses"""
    try:
        for email in emails:
            await send_alert_email("TEST ALERT", "person", 1, [email])
        return {"status": "success", "message": "Test emails sent"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/get_alerts")
async def get_alerts(limit: int = 20):
    """Get recent alerts"""
    if not supabase:
        return []
    
    try:
        response = supabase.table("alerts").select("*").order("created_at", desc=True).limit(limit).execute()
        alerts_data = []
        for alert in response.data:
            alerts_data.append({
                "timestamp": alert["created_at"],
                "rule_name": alert["rule_name"],
                "object_type": alert["object_type"],
                "count": alert["count"],
                "message": alert["message"]
            })
        return alerts_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test_connection")
async def test_connection(config: CameraConfig):
    """Test connection to camera source"""
    try:
        if config.source_type == "webcam":
            cap = cv2.VideoCapture(0)
        elif config.source_type == "rtsp":
            cap = cv2.VideoCapture(config.rtsp_url)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        elif config.source_type == "upload":
            cap = cv2.VideoCapture(config.video_file)

        ret, _ = cap.read()
        cap.release()

        if ret:
            return {"status": "success", "message": "Connection successful"}
        else:
            return {"status": "error", "message": "Failed to read from source"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket endpoint for live stream"""
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"[+] WebSocket client connected. Total clients: {len(connected_clients)}")

    try:
        while True:
            await websocket.receive_text()
    except:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"[-] WebSocket client disconnected. Total clients: {len(connected_clients)}")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "streaming": is_streaming,
        "detections": current_detections,
        "connected_clients": len(connected_clients)
    }

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "RGB Camera Detection System",
        "version": "1.0.0",
        "camera": RTSP_URL,
        "alert_email": SENDER_EMAIL,
        "streaming": is_streaming
    }

# ============================================
# Startup
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("RGB CAMERA DETECTION SYSTEM")
    print("="*60)
    print(f"Camera: {RTSP_URL}")
    print(f"Alert Email: {SENDER_EMAIL}")
    print(f"Recipients: {', '.join(ALERT_RECIPIENTS)}")
    print(f"Mode: {'With Email' if SENDER_PASSWORD else 'Demo (No Email)'}")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
