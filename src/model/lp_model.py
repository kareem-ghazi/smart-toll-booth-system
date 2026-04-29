import os
from ultralytics import YOLO
import cv2

def finetune_yolo(data_yaml_path, model_variant='yolo26n.pt', epochs=10, imgsz=640):
    """
    Finetunes a YOLO model.
    """
    print(f"Loading model {model_variant}...")
    model = YOLO(model_variant)
    
    print(f"Starting finetuning with {data_yaml_path} for {epochs} epochs...")
    results = model.train(
        data=data_yaml_path,
        epochs=epochs,
        imgsz=imgsz,
        plots=True,
        batch=32,              # 'Batch size'
        degrees=10.0,          # Handles tilted plates
        shear=2.0,             # Handles perspective distortion
        perspective=0.0001,    # Subtle perspective shifts
        mosaic=1.0,            # Mixes images to help with context
    )
    
    # Save the model
    save_path = os.path.join(os.path.dirname(__file__), 'lp_model.pt')
    model.save(save_path)
    print(f"Model saved to {save_path}")
    
    return model, results

def test_and_save_result(model, image_path, output_path):
    """
    Runs inference on an image and saves the result with bounding boxes.
    """
    print(f"Running inference on {image_path}...")
    results = model(image_path)
    
    # results is a list, take the first one
    res = results[0]
    
    # Plot results on the image
    res_plotted = res.plot()
    
    # Save the image
    cv2.imwrite(output_path, res_plotted)
    print(f"Result saved to {output_path}")

if __name__ == "__main__":
    # Paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_yaml = os.path.join(project_root, 'src', 'data', 'processed_vehicles', 'data.yaml')
    test_image = os.path.join(project_root, 'src', 'data', 'processed_vehicles', 'test', 'images', '0002.jpg')
    output_image = os.path.join(project_root, 'src', 'data', 'detection_result.jpg')
    
    # Training on 100 epochs
    model, train_results = finetune_yolo(data_yaml, epochs=100)
    
    # Test
    if os.path.exists(test_image):
        test_and_save_result(model, test_image, output_image)
    else:
        print(f"Test image not found at {test_image}")
