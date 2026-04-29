# Smart Toll Booth Detection System 🛣️

An automated toll booth system that utilizes deep learning (YOLO) to detect vehicles and recognize license plates for seamless toll collection.

## 🌟 Overview

The Smart Toll Booth Detection System is designed to automate the process of vehicle identification and toll management. It leverages custom-trained YOLO models to:
1.  **Detect Vehicles:** Identify vehicles as they approach the toll booth.
2.  **Locate License Plates:** Precisely crop license plate regions from vehicle images.
3.  **Recognize Characters:** Perform Optical Character Recognition (OCR) on the license plates to extract the plate number.
4.  **Manage Records:** Track toll transactions in a database with a user-friendly dashboard.

## 🛠️ Tech Stack

*   **UI/Dashboard:** [Streamlit](https://streamlit.io/)
*   **Computer Vision:** [OpenCV](https://opencv.org/), [PIL](https://python-pillow.org/)
*   **Deep Learning:** [Ultralytics YOLO](https://docs.ultralytics.com/)
*   **Data Processing:** [NumPy](https://numpy.org/), [Pandas](https://pandas.pydata.org/)
*   **Language:** Python 3.x

## 📁 Project Structure

```text
smart-toll-booth-system/
├── src/
│   ├── app.py              # Streamlit web application
│   ├── database.py         # Database management (SQLite/Dummy)
│   ├── manager.py          # System orchestration logic
│   ├── model/
│   │   ├── lp_model.py     # Vehicle & License Plate detection trainer
│   │   ├── character_model.py # License Plate character recognition trainer
│   │   └── outputs/        # Trained .pt model files
│   ├── data/
│   │   ├── processed_plates/  # Dataset for character detection & recognition (labels/images)
│   │   └── processed_vehicles/ # Dataset for vehicle detection
│   └── utils/
│       └── dataset_splitter.py # Utility to split raw data
├── LICENSE.txt             # Project license
└── README.md               # You are here!
```

## 🚀 Getting Started

### Prerequisites

*   Python 3.10+

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/smart-toll-booth-system.git
    cd smart-toll-booth-system
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To launch the interactive dashboard:
```bash
streamlit run src/app.py
```

### Training Models

If you wish to retrain the models with your own data:

*   **License Plate Detection:** `python src/model/lp_model.py`
*   **Character Recognition:** `python src/model/character_model.py`

*Ensure your `data.yaml` files in `src/data/` are correctly configured.*

## ⚙️ Features

*   **Live Camera Feed:** Real-time capture and processing from a webcam.
*   **Media Upload:** Support for processing static images and recorded videos.
*   **Searchable Database:** A clean UI to view, search, and manage toll records.
*   **Dual YOLO Pipeline:** Separated models for high-accuracy detection and recognition.

## 📊 Dataset

This project utilizes the EALPR (Egyptian Automated License Plate Recognition) dataset. We would like to credit the authors for providing this benchmark dataset:

**Citation:**
> Youssef, Ahmed Ramadan and Sayed, Fawzya Ramadan and Ali, Abdelmgeid Ameen, "A New Benchmark Dataset for Egyptian License Plate Detection and Recognition," 2022 7th Asia-Pacific Conference on Intelligent Robot Systems (ACIRS), 2022, pp. 106-111, doi: 10.1109/ACIRS55390.2022.9845514.

**BibTeX:**
```bibtex
@INPROCEEDINGS{9845514,
  author={Youssef, Ahmed Ramadan and Sayed, Fawzya Ramadan and Ali, Abdelmgeid Ameen},
  booktitle={2022 7th Asia-Pacific Conference on Intelligent Robot Systems (ACIRS)}, 
  title={A New Benchmark Dataset for Egyptian License Plate Detection and Recognition}, 
  year={2022},
  volume={},
  number={},
  pages={106-111},
  doi={10.1109/ACIRS55390.2022.9845514}}
```

## 📄 License

This project is licensed under the terms of the `LICENSE.txt` file included in this repository.
