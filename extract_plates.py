import os

# Character mapping from src/data/processed_plates/data.yaml
chars = [
    "أ", "ب", "ج", "د", "ر", "س", "ص", "ط", "ع", "ف", "ق", "ل", "م", "ن", "ھ", "و", "ى",
    "٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"
]

experimental_dir = "experimental/"
labels_dir = "_archive/EALPR-master/EALPR- LP characters dataset/Characters Labeling/"

files = [f for f in os.listdir(experimental_dir) if f.endswith(".jpg")]
files.sort()

results = []

for f in files:
    base_name = f.replace(".jpg", "")
    label_file = os.path.join(labels_dir, f"{base_name}_license_plate_1.txt")
    
    if os.path.exists(label_file):
        with open(label_file, "r") as lf:
            lines = lf.readlines()
            
        data = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                class_id = int(parts[0])
                x_center = float(parts[1])
                data.append((x_center, chars[class_id]))
        
        # Sort by x_center to get the correct order (Arabic is RTL, but YOLO x is LTR)
        # Sorting by x_center gives the characters from left to right as they appear in the image.
        data.sort(key=lambda x: x[0])
        plate = "".join([d[1] for d in data])
        results.append((f, plate))

for f, plate in results:
    print(f"{f}: {plate}")
