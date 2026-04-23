import os
import cv2
import shutil
from ultralytics import YOLO

def test_character_model():
    # Paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    model_path = os.path.join(project_root, 'src', 'model', 'outputs', 'character_model.pt')
    data_yaml_path = os.path.join(project_root, 'src', 'data', 'processed_plates', 'data.yaml')
    test_images_dir = os.path.join(project_root, 'src', 'data', 'processed_plates', 'test', 'images')
    output_dir = os.path.join(project_root, 'src', 'test', 'output', 'character_model_results')
    metrics_output_dir = os.path.join(output_dir, 'metrics_analysis')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        return
    
    # Load model
    print(f"Loading character model from {model_path}...")
    model = YOLO(model_path)
    
    # 1. Detailed Metrics Analysis
    print("\n--- Starting Detailed Metrics Analysis ---")
    # Setting split='test' ensures it uses the test set from data.yaml, verbose=False reduces noise
    results = model.val(data=data_yaml_path, split='test', project=output_dir, name='metrics_analysis', exist_ok=True, verbose=False)
    
    print("\nResults for Character Model (Test Set):")
    print(f"mAP50: {results.results_dict['metrics/mAP50(B)'] * 100:.2f}%")
    print(f"mAP50-95: {results.results_dict['metrics/mAP50-95(B)'] * 100:.2f}%")
    print(f"Precision: {results.results_dict['metrics/precision(B)'] * 100:.2f}%")
    print(f"Recall: {results.results_dict['metrics/recall(B)'] * 100:.2f}%")
    
    # 2. Individual Image Inference and Visualization
    print("\n--- Starting Individual Image Inference (Silent) ---")
    visual_results_dir = os.path.join(output_dir, 'visual_results')
    if not os.path.exists(visual_results_dir):
        os.makedirs(visual_results_dir)

    # Get all images from test folder
    images = [f for f in os.listdir(test_images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Processing {len(images)} images...")
    
    for img_name in images:
        img_path = os.path.join(test_images_dir, img_name)
        # Run inference with verbose=False
        results_inf = model(img_path, verbose=False)
        res = results_inf[0]
        
        # Save visualized result
        res_plotted = res.plot()
        save_path = os.path.join(visual_results_dir, f"res_{img_name}")
        cv2.imwrite(save_path, res_plotted)
        
    print(f"\nAll character model visual results saved to {visual_results_dir}")
    print(f"Detailed metrics analysis artifacts (confusion matrix, curves, etc.) saved to {metrics_output_dir}")

if __name__ == "__main__":
    test_character_model()
