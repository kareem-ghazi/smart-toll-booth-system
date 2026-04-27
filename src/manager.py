import cv2
import numpy as np
from ultralytics import YOLO
import os

class TollBoothManager:
    def __init__(self):
        # Resolve paths relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        lp_model_path = os.path.join(current_dir, "model", "outputs", "lp_model.pt")
        char_model_path = os.path.join(current_dir, "model", "outputs", "character_model.pt")
        
        # Load models
        self.lp_model = YOLO(lp_model_path)
        self.char_model = YOLO(char_model_path)

    def detect_and_crop_plate(self, image, padding=20):
        """
        Detects the license plate and returns the cropped image with padding.
        """
        results = self.lp_model(image)
        if not results or len(results[0].boxes) == 0:
            return None, None

        # Get the first detected box (highest confidence usually)
        box = results[0].boxes[0]
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        
        # Add padding
        h, w = image.shape[:2]
        x1 = max(0, int(x1 - padding))
        y1 = max(0, int(y1 - padding))
        x2 = min(w, int(x2 + padding))
        y2 = min(h, int(y2 + padding))
        
        cropped_plate = image[y1:y2, x1:x2]
        return cropped_plate, [x1, y1, x2, y2]

    def _filter_overlapping_boxes(self, boxes, iou_threshold=0.5):
        """
        Removes overlapping boxes, keeping the one with higher confidence.
        """
        if not boxes:
            return []

        # Sort by confidence descending
        sorted_boxes = sorted(boxes, key=lambda x: x['conf'], reverse=True)
        keep = []

        for box in sorted_boxes:
            overlap = False
            for kept_box in keep:
                # Calculate Intersection over Union (IoU)
                b1 = box['coords']
                b2 = kept_box['coords']
                
                xi1 = max(b1[0], b2[0])
                yi1 = max(b1[1], b2[1])
                xi2 = min(b1[2], b2[2])
                yi2 = min(b1[3], b2[3])
                
                inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
                
                b1_area = (b1[2] - b1[0]) * (b1[3] - b1[1])
                b2_area = (b2[2] - b2[0]) * (b2[3] - b2[1])
                union_area = b1_area + b2_area - inter_area
                
                iou = inter_area / union_area if union_area > 0 else 0
                
                if iou > iou_threshold:
                    overlap = True
                    break
            
            if not overlap:
                keep.append(box)
        
        return keep

    def extract_text_from_plate(self, cropped_plate):
        """
        Extracts characters from the cropped plate image and returns the text
        formatted for Egyptian plates: Letters (RTL) - Numbers (LTR).
        """
        results = self.char_model(cropped_plate)
        if not results or len(results[0].boxes) == 0:
            return ""

        res = results[0]
        names = res.names
        boxes = res.boxes
        
        detected_items = []
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            coords = box.xyxy[0].tolist()
            x_min = coords[0]
            char = names[cls_id]
            detected_items.append({
                'char': char, 
                'x_min': x_min, 
                'cls_id': cls_id, 
                'conf': conf, 
                'coords': coords
            })

        # Filter duplicates (overlapping boxes)
        filtered_items = self._filter_overlapping_boxes(detected_items)
        
        letters = []
        numbers = []
        
        for item in filtered_items:
            # Egyptian dataset classes: 0-16 are letters, 17-26 are numbers
            if item['cls_id'] <= 16:
                letters.append(item)
            else:
                numbers.append(item)

        # Sort letters by x_min descending (Right to Left)
        letters.sort(key=lambda x: x['x_min'], reverse=True)
        # Sort numbers by x_min ascending (Left to Right)
        numbers.sort(key=lambda x: x['x_min'])
        
        letters_part = "".join([l['char'] for l in letters])
        numbers_part = "".join([n['char'] for n in numbers])
        
        if letters_part and numbers_part:
            return f"{letters_part} - {numbers_part}"
        return letters_part + numbers_part

manager = TollBoothManager()
