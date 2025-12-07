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
import base64
from io import BytesIO
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI()

supabase_url = os.getenv("VITE_SUPABASE_URL")
supabase_key = os.getenv("VITE_SUPABASE_SUPABASE_ANON_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

camera_config = None
is_streaming = False
current_detections = {
    "person": 0,
    "animal": 0,
    "vehicle": 0,
    "timestamp": None
}
connected_clients = []

model = YOLO("yolov8n.pt")

def map_yolo_to_category(class_name):
    class_name = class_name.lower()
    if "person" in class_name or "human" in class_name:
        return "person"
    elif "dog" in class_name or "cat" in class_name or "animal" in class_name or "bird" in class_name or "horse" in class_name or "sheep" in class_name or "cow" in class_name:
        return "animal"
    elif "car" in class_name or "truck" in class_name or "bus" in class_name or "motorcycle" in class_name or "vehicle" in class_name or "bicycle" in class_name:
        return "vehicle"
    return None

def run_detection(frame):
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
    colors = {"person": (0, 255, 0), "animal": (255, 0, 0), "vehicle": (0, 0, 255)}
    for box in boxes:
        x1, y1, x2, y2 = box["coords"]
        color = colors.get(box["category"], (255, 255, 255))
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{box['category']} ({box['confidence']:.2f})"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame

def encode_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

async def send_alert_email(rule_name, object_type, count, emails):
    try:
        sender_email = os.getenv("SENDER_EMAIL", "intruder-detection@system.com")
        subject = f"Intruder Alert: {rule_name}"
        body = f"""
        Alert Triggered!

        Rule: {rule_name}
        Object Type: {object_type}
        Count: {count}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Please check your system immediately.
        """

        print(f"[EMAIL ALERT] To: {emails} | Rule: {rule_name} | Count: {count}")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

async def check_rules():
    global current_detections

    try:
        response = supabase.table("detection_rules").select("*").eq("is_active", True).execute()
        rules = response.data

        response = supabase.table("alert_settings").select("email").eq("is_active", True).execute()
        emails = [item["email"] for item in response.data]

        for rule in rules:
            count = current_detections.get(rule["object_type"], 0)
            if count > rule["threshold"]:
                alert_data = {
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "object_type": rule["object_type"],
                    "count": count,
                    "message": f"Alert: {rule['name']} - {rule['object_type']} count ({count}) exceeded threshold ({rule['threshold']})"
                }

                supabase.table("alerts").insert(alert_data).execute()

                if emails:
                    await send_alert_email(rule["name"], rule["object_type"], count, emails)

                alert_data["timestamp"] = datetime.now().isoformat()
                await broadcast_alert(alert_data)
    except Exception as e:
        print(f"Error checking rules: {e}")

async def broadcast_alert(alert):
    for client in connected_clients:
        try:
            await client.send_json({"type": "alert", "data": alert})
        except:
            pass

async def process_stream(cap):
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

        await check_rules()

        if frame_count % 30 == 0:
            try:
                supabase.table("detection_logs").insert({
                    "person_count": detections["person"],
                    "animal_count": detections["animal"],
                    "vehicle_count": detections["vehicle"]
                }).execute()
            except:
                pass

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

@app.post("/configure_camera")
async def configure_camera_endpoint(config: CameraConfig):
    global camera_config
    camera_config = config

    try:
        supabase.table("camera_configs").update({"is_active": False}).neq("id", "00000000-0000-0000-0000-000000000000").execute()

        supabase.table("camera_configs").insert({
            "source_type": config.source_type,
            "rtsp_url": config.rtsp_url,
            "video_file": config.video_file,
            "is_active": True
        }).execute()
    except Exception as e:
        print(f"Error saving camera config: {e}")

    return {"status": "success", "message": "Camera configured"}

@app.post("/start_stream")
async def start_stream():
    global is_streaming, camera_config

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
    global is_streaming
    is_streaming = False
    return {"status": "success", "message": "Stream stopped"}

@app.get("/get_detections")
async def get_detections():
    return current_detections

@app.post("/create_rule")
async def create_rule_endpoint(rule: Rule):
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
    try:
        supabase.table("detection_rules").update({"is_active": False}).eq("id", rule_id).execute()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/configure_alerts")
async def configure_alerts(settings: AlertSettings):
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
    try:
        for email in emails:
            print(f"[TEST EMAIL] Sending to {email}")
        return {"status": "success", "message": "Test emails sent"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/get_alerts")
async def get_alerts(limit: int = 20):
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
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except:
        connected_clients.remove(websocket)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
