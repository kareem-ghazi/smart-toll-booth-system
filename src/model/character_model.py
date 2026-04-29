import os
from ultralytics import YOLO
import cv2

def finetune_character_model(data_yaml_path, model_variant='yolo26n.pt', epochs=10, imgsz=640):
    """
    Finetunes a YOLO model for character detection.
    """
    print(f"Loading model {model_variant}...")
    model = YOLO(model_variant)
    
    print(f"Starting character finetuning with {data_yaml_path} for {epochs} epochs...")
    results = model.train(
        data=data_yaml_path,
        epochs=epochs,
        imgsz=imgsz,
        plots=True,
        batch=32,              # 'Batch size'
        degrees=10.0,          # Handles tilted plates
        shear=2.0,             # Handles perspective distortion
        perspective=0.0001,    # Subtle perspective shifts
        flipud=0.0,            # Never flip Arabic text upside down!
        fliplr=0.0,            # Never flip Arabic text left-to-right!
        mosaic=1.0,            # Mixes images to help with context
        mixup=0.1,             # Helps the model distinguish similar characters
    )
    
    # Save the model
    save_path = os.path.join(os.path.dirname(__file__), 'character_model.pt')
    model.save(save_path)
    print(f"Model saved to {save_path}")
    
    return model, results

def detect_and_extract_text(model, image_path, output_path):
    """
    Detects characters, extracts text, and saves the visualized result.
    """
    print(f"Running character inference on {image_path}...")
    results = model(image_path)
    res = results[0]
    
    # Get class names
    names = res.names
    
    # Extract boxes, classes and scores
    boxes = res.boxes
    detected_chars = []
    
    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x_min = float(box.xyxy[0][0])
        char = names[cls_id]
        detected_chars.append({
            'char': char,
            'x_min': x_min,
            'conf': conf
        })
    
    # Sort characters by x_min to read from left to right (or right to left for Arabic)
    # Note: For Arabic, usually it is right to left, but depending on how the bounding boxes 
    # are ordered in the labels, we might need to reverse.
    # We will sort by x_min ascending for now.
    detected_chars.sort(key=lambda x: x['x_min'])
    
    plate_text = "".join([d['char'] for d in detected_chars])
    print(f"Extracted Text: {plate_text}")
    
    # Save visualized result
    res_plotted = res.plot()
    cv2.imwrite(output_path, res_plotted)
    print(f"Result saved to {output_path}")
    
    return plate_text

if __name__ == "__main__":
    # Paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_yaml = os.path.join(project_root, 'src', 'data', 'processed_plates', 'data.yaml')
    test_image = os.path.join(project_root, 'src', 'data', 'processed_plates', 'test', 'images', '0002_license_plate_1.png')
    output_image = os.path.join(project_root, 'src', 'data', 'character_detection_result.jpg')
    
    # Finetune for 150 epochs
    model, _ = finetune_character_model(data_yaml, epochs=150)
    
    # Test
    if os.path.exists(test_image):
        text = detect_and_extract_text(model, test_image, output_image)
    else:
        print(f"Test image not found at {test_image}")
