"""
Simple Tracker Module - Tracks detected objects across frames
Lightweight implementation without requiring deep-sort installation
Can be upgraded to deep-sort-realtime when needed
"""

import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class SimpleTracker:
    """
    Simple centroid-based tracker for object tracking
    """
    
    def __init__(self, max_disappeared=30):
        self.next_object_id = 0
        self.objects = {}  # Stores object IDs and their centroids
        self.disappeared = {}  # Track frames where object wasn't detected
        self.max_disappeared = max_disappeared
        self.object_history = {}  # Track object history
        self.alerts_sent = {}  # Track which objects have triggered alerts
        
    def register(self, centroid, object_data=None):
        """Register a new object"""
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.object_history[self.next_object_id] = [centroid]
        self.alerts_sent[self.next_object_id] = False
        self.next_object_id += 1
        
    def deregister(self, object_id):
        """Deregister an object"""
        del self.objects[object_id]
        del self.disappeared[object_id]
        if object_id in self.alerts_sent:
            del self.alerts_sent[object_id]
    
    def update(self, rects, category="person"):
        """
        Update tracker with new detections
        rects: list of bounding boxes [x1, y1, x2, y2]
        """
        if len(rects) == 0:
            # Mark all objects as disappeared
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects
        
        # Calculate centroids for new detections
        input_centroids = np.zeros((len(rects), 2))
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = (startX + endX) / 2.0
            cY = (startY + endY) / 2.0
            input_centroids[i] = (cX, cY)
        
        # If no objects yet, register all
        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i], category)
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            
            # Calculate distances between existing and new centroids
            D = np.zeros((len(object_centroids), len(input_centroids)))
            for i in range(len(object_centroids)):
                for j in range(len(input_centroids)):
                    diff = object_centroids[i] - input_centroids[j]
                    D[i][j] = np.linalg.norm(diff)
            
            # Find matches
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            
            used_rows = set()
            used_cols = set()
            
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                if D[row, col] > 50:  # Distance threshold
                    continue
                
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                self.object_history[object_id].append(input_centroids[col])
                
                used_rows.add(row)
                used_cols.add(col)
            
            # Register unmatched centroids
            unused_cols = set(range(0, len(input_centroids))) - used_cols
            for col in unused_cols:
                self.register(input_centroids[col], category)
            
            # Deregister disappeared objects
            unused_rows = set(range(0, len(object_centroids))) - used_rows
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
        
        return self.objects
    
    def get_tracked_objects(self):
        """Get all currently tracked objects"""
        return self.objects
    
    def get_object_count(self):
        """Get number of currently tracked objects"""
        return len(self.objects)


class MultiClassTracker:
    """
    Tracks multiple object classes independently
    """
    
    def __init__(self):
        self.trackers = {
            'person': SimpleTracker(),
            'animal': SimpleTracker(),
            'vehicle': SimpleTracker()
        }
        self.frame_count = 0
    
    def update(self, detections):
        """
        Update all trackers
        detections: dict with category -> list of bboxes
        """
        self.frame_count += 1
        results = {}
        
        for category, tracker in self.trackers.items():
            rects = detections.get(category, [])
            tracker.update(rects, category)
            results[category] = tracker.get_object_count()
        
        return results
    
    def get_stats(self):
        """Get tracking statistics"""
        return {
            'frame': self.frame_count,
            'person': self.trackers['person'].get_object_count(),
            'animal': self.trackers['animal'].get_object_count(),
            'vehicle': self.trackers['vehicle'].get_object_count(),
        }
