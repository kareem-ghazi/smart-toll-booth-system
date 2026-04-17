import os
import cv2
import glob
import shutil
import random
import yaml

def get_dataset_paths(base_dir):
    """
    Returns a list of image paths and their corresponding label paths.
    
    Args:
        base_dir (str): Path to 'EALPR Vechicles dataset' directory.
        
    Returns:
        tuple: (image_paths, label_paths)
    """
    vehicles_dir = os.path.join(base_dir, 'Vehicles')
    labels_dir = os.path.join(base_dir, 'Vehicles Labeling')
    
    # Supported image extensions
    image_extensions = {'.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG'}
    
    all_files = os.listdir(vehicles_dir)
    image_paths = []
    
    for filename in all_files:
        if any(filename.lower().endswith(ext.lower()) for ext in image_extensions):
            image_paths.append(os.path.join(vehicles_dir, filename))
    
    # Sort for consistency
    image_paths.sort()
    
    valid_image_paths = []
    label_paths = []
    
    for img_path in image_paths:
        # Get filename without extension
        filename_no_ext = os.path.splitext(os.path.basename(img_path))[0]
        label_path = os.path.join(labels_dir, f"{filename_no_ext}.txt")
        
        if os.path.exists(label_path):
            valid_image_paths.append(img_path)
            label_paths.append(label_path)
            
    return valid_image_paths, label_paths

def parse_yolo_label(label_path):
    """
    Parses a YOLO format label file.
    
    Args:
        label_path (str): Path to the .txt label file.
        
    Returns:
        list: List of bounding boxes [class_id, x_center, y_center, width, height].
    """
    bboxes = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 5:
                    bboxes.append([int(parts[0])] + [float(x) for x in parts[1:]])
    return bboxes

def load_image(image_path):
    """
    Loads an image using OpenCV.
    
    Args:
        image_path (str): Path to the image file.
        
    Returns:
        numpy.ndarray: Loaded image in BGR format.
    """
    return cv2.imread(image_path)

def load_dataset(base_dir, num_samples=None):
    """
    Loads images and their corresponding labels.
    
    Args:
        base_dir (str): Path to 'EALPR Vechicles dataset' directory.
        num_samples (int, optional): Number of samples to load. Defaults to None (all).
        
    Returns:
        list: List of dictionaries containing 'image', 'bboxes', and 'image_path'.
    """
    img_paths, lbl_paths = get_dataset_paths(base_dir)
    
    if num_samples is not None:
        img_paths = img_paths[:num_samples]
        lbl_paths = lbl_paths[:num_samples]
        
    dataset = []
    for img_path, lbl_path in zip(img_paths, lbl_paths):
        img = load_image(img_path)
        if img is not None:
            bboxes = parse_yolo_label(lbl_path)
            dataset.append({
                'image': img,
                'bboxes': bboxes,
                'image_path': img_path
            })
            
    return dataset

def split_dataset(img_paths, lbl_paths, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    """
    Splits the dataset into train, val, and test sets.
    """
    data = list(zip(img_paths, lbl_paths))
    random.shuffle(data)
    
    total = len(data)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    train_data = data[:train_end]
    val_data = data[train_end:val_end]
    test_data = data[val_end:]
    
    return train_data, val_data, test_data

def prepare_yolo_dataset(output_base_dir, train_data, val_data, test_data):
    """
    Creates the YOLO directory structure and copies images and labels.
    """
    for split_name, split_data in [('train', train_data), ('val', val_data), ('test', test_data)]:
        img_dir = os.path.join(output_base_dir, split_name, 'images')
        lbl_dir = os.path.join(output_base_dir, split_name, 'labels')
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(lbl_dir, exist_ok=True)
        
        for img_path, lbl_path in split_data:
            shutil.copy(img_path, os.path.join(img_dir, os.path.basename(img_path)))
            shutil.copy(lbl_path, os.path.join(lbl_dir, os.path.basename(lbl_path)))

def create_yolo_yaml(output_base_dir, yaml_path, nc=1, names=['license_plate']):
    """
    Creates the data.yaml file for YOLO.
    """
    data = {
        'path': os.path.abspath(output_base_dir),
        'train': 'train/images',
        'val': 'val/images',
        'test': 'test/images',
        'nc': nc,
        'names': names
    }
    
    with open(yaml_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

def get_plate_dataset_paths(plates_dir, labels_dir):
    """
    Returns a list of plate image paths and their corresponding character label paths.
    """
    # Supported image extensions
    image_extensions = {'.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG'}
    
    if not os.path.exists(plates_dir):
        print(f"Directory not found: {plates_dir}")
        return [], []
        
    all_files = os.listdir(plates_dir)
    image_paths = []
    
    for filename in all_files:
        if any(filename.lower().endswith(ext.lower()) for ext in image_extensions):
            image_paths.append(os.path.join(plates_dir, filename))
    
    # Sort for consistency
    image_paths.sort()
    
    valid_image_paths = []
    label_paths = []
    
    for img_path in image_paths:
        # Get filename without extension
        filename_no_ext = os.path.splitext(os.path.basename(img_path))[0]
        label_path = os.path.join(labels_dir, f"{filename_no_ext}.txt")
        
        if os.path.exists(label_path):
            valid_image_paths.append(img_path)
            label_paths.append(label_path)
            
    return valid_image_paths, label_paths

if __name__ == "__main__":
    # --- EALPR Vehicles Dataset ---
    base_vehicles_path = 'src/data/EALPR-master/EALPR Vechicles dataset'
    output_vehicles_path = 'src/data/processed_vehicles'
    
    v_img_paths, v_lbl_paths = get_dataset_paths(base_vehicles_path)
    print(f"Total vehicle images found: {len(v_img_paths)}")
    
    if len(v_img_paths) > 0:
        v_train, v_val, v_test = split_dataset(v_img_paths, v_lbl_paths)
        print(f"Vehicle Split: Train={len(v_train)}, Val={len(v_val)}, Test={len(v_test)}")
        prepare_yolo_dataset(output_vehicles_path, v_train, v_val, v_test)
        create_yolo_yaml(output_vehicles_path, os.path.join(output_vehicles_path, 'data.yaml'))
        print(f"Created vehicle data.yaml")

    # --- EALPR Plates/Characters Dataset ---
    plates_dir = 'src/data/EALPR-master/EALPR- Plates dataset'
    char_labels_dir = 'src/data/EALPR-master/EALPR- LP characters dataset/Characters Labeling'
    output_plates_path = 'src/data/processed_plates'
    
    p_img_paths, p_lbl_paths = get_plate_dataset_paths(plates_dir, char_labels_dir)
    print(f"Total plate images found: {len(p_img_paths)}")
    
    if len(p_img_paths) > 0:
        p_train, p_val, p_test = split_dataset(p_img_paths, p_lbl_paths)
        print(f"Plate Split: Train={len(p_train)}, Val={len(p_val)}, Test={len(p_test)}")
        prepare_yolo_dataset(output_plates_path, p_train, p_val, p_test)
        
        # Read class names for plates
        classes_file = os.path.join(char_labels_dir, 'classes.txt')
        names = []
        if os.path.exists(classes_file):
            with open(classes_file, 'r', encoding='utf-8') as f:
                names = [line.strip() for line in f if line.strip()]
        
        create_yolo_yaml(output_plates_path, os.path.join(output_plates_path, 'data.yaml'), nc=len(names), names=names)
        print(f"Created plate data.yaml with {len(names)} classes")
