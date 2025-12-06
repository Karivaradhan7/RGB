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
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from io import BytesIO

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================== MODELS ========================
class CameraConfig(BaseModel):
    source_type: str  # "webcam", "rtsp", "upload"
    rtsp_url: Optional[str] = None
    video_file: Optional[str] = None

class Rule(BaseModel):
    rule_id: Optional[str] = None
    name: str
    object_type: str  # "person", "animal", "vehicle"
    threshold: int

class AlertSettings(BaseModel):
    emails: List[str]

class Alert(BaseModel):
    timestamp: str
    rule_name: str
    object_type: str
    count: int
    message: str

# ======================== GLOBAL STATE ========================
camera_config = None
is_streaming = False
current_detections = {
    "person": 0,
    "animal": 0,
    "vehicle": 0,
    "timestamp": None
}
rules = []
alerts = []
alert_settings = {"emails": []}
connected_clients = []

# Load YOLO model
model = YOLO("yolov8n.pt")

# ======================== HELPER FUNCTIONS ========================
def map_yolo_to_category(class_name):
    """Map YOLO class names to our categories"""
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
    results = model(frame, verbose=False)
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
    """Draw bounding boxes on frame"""
    colors = {"person": (0, 255, 0), "animal": (255, 0, 0), "vehicle": (0, 0, 255)}
    for box in boxes:
        x1, y1, x2, y2 = box["coords"]
        color = colors.get(box["category"], (255, 255, 255))
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{box['category']} ({box['confidence']:.2f})"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame

def encode_frame(frame):
    """Encode frame to base64"""
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def send_alert_email(rule_name, object_type, count, emails):
    """Send alert email"""
    try:
        sender_email = os.getenv("SENDER_EMAIL", "test@example.com")
        sender_password = os.getenv("SENDER_PASSWORD", "password")
        
        subject = f"🚨 Intruder Alert: {rule_name}"
        body = f"""
        Alert Triggered!
        
        Rule: {rule_name}
        Object Type: {object_type}
        Count: {count}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Please check your system immediately.
        """
        
        # For demo, we'll just log it
        print(f"[EMAIL] Would send to {emails}: {subject}")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def check_rules():
    """Check if any rules are triggered"""
    global alerts, current_detections
    
    for rule in rules:
        count = current_detections.get(rule["object_type"], 0)
        if count > rule["threshold"]:
            alert = {
                "timestamp": datetime.now().isoformat(),
                "rule_name": rule["name"],
                "object_type": rule["object_type"],
                "count": count,
                "message": f"Alert: {rule['name']} - {rule['object_type']} count ({count}) exceeded threshold ({rule['threshold']})"
            }
            alerts.append(alert)
            alerts = alerts[-50:]  # Keep last 50 alerts
            
            if alert_settings["emails"]:
                send_alert_email(rule["name"], rule["object_type"], count, alert_settings["emails"])
            
            # Notify connected websocket clients
            asyncio.create_task(broadcast_alert(alert))

async def broadcast_alert(alert):
    """Broadcast alert to all connected websocket clients"""
    for client in connected_clients:
        try:
            await client.send_json({"type": "alert", "data": alert})
        except:
            pass

async def process_stream(cap):
    """Process video stream"""
    global is_streaming, current_detections
    
    frame_count = 0
    while is_streaming:
        ret, frame = cap.read()
        if not ret:
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
        
        check_rules()
        
        # Broadcast frame to websockets every 3 frames
        if frame_count % 3 == 0:
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
        
        frame_count += 1
        await asyncio.sleep(0.01)

# ======================== API ENDPOINTS ========================

@app.post("/configure_camera")
async def configure_camera(config: CameraConfig):
    """Configure camera source"""
    global camera_config
    camera_config = config
    return {"status": "success", "message": "Camera configured"}

@app.post("/start_stream")
async def start_stream():
    """Start video stream"""
    global is_streaming, camera_config, connected_clients
    
    if is_streaming:
        return {"status": "error", "message": "Stream already running"}
    
    if not camera_config:
        return {"status": "error", "message": "Camera not configured"}
    
    is_streaming = True
    
    if camera_config.source_type == "webcam":
        cap = cv2.VideoCapture(0)
    elif camera_config.source_type == "rtsp":
        cap = cv2.VideoCapture(camera_config.rtsp_url)
    elif camera_config.source_type == "upload":
        cap = cv2.VideoCapture(camera_config.video_file)
    
    asyncio.create_task(process_stream(cap))
    return {"status": "success", "message": "Stream started"}

@app.post("/stop_stream")
async def stop_stream():
    """Stop video stream"""
    global is_streaming
    is_streaming = False
    return {"status": "success", "message": "Stream stopped"}

@app.get("/get_detections")
async def get_detections():
    """Get current detections"""
    return current_detections

@app.post("/create_rule")
async def create_rule(rule: Rule):
    """Create detection rule"""
    if not rule.rule_id:
        rule.rule_id = f"rule_{len(rules) + 1}"
    
    rules.append(rule.model_dump())
    return {"status": "success", "rule_id": rule.rule_id}

@app.get("/get_rules")
async def get_rules():
    """Get all rules"""
    return rules

@app.delete("/delete_rule/{rule_id}")
async def delete_rule(rule_id: str):
    """Delete a rule"""
    global rules
    rules = [r for r in rules if r.get("rule_id") != rule_id]
    return {"status": "success"}

@app.post("/configure_alerts")
async def configure_alerts(settings: AlertSettings):
    """Configure alert email settings"""
    global alert_settings
    alert_settings = {"emails": settings.emails}
    return {"status": "success"}

@app.post("/send_test_email")
async def send_test_email(emails: List[str]):
    """Send test email"""
    try:
        for email in emails:
            print(f"[TEST EMAIL] Sending to {email}")
        return {"status": "success", "message": "Test emails sent"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/get_alerts")
async def get_alerts(limit: int = 20):
    """Get recent alerts"""
    return alerts[-limit:]

@app.post("/test_connection")
async def test_connection(config: CameraConfig):
    """Test camera connection"""
    try:
        if config.source_type == "webcam":
            cap = cv2.VideoCapture(0)
        elif config.source_type == "rtsp":
            cap = cv2.VideoCapture(config.rtsp_url)
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
    
    try:
        while True:
            await websocket.receive_text()
    except:
        connected_clients.remove(websocket)

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
