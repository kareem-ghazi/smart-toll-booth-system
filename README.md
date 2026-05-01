# Smart Toll Booth Detection System 🛣️

An automated toll booth system that utilizes deep learning (YOLO) to detect vehicles and recognize license plates for seamless toll collection.

## 🌟 Overview

The Smart Toll Booth Detection System is designed to automate the process of vehicle identification and toll management. It leverages custom-trained YOLO models to:
1.  **Detect Vehicles:** Identify vehicles as they approach the toll booth.
2.  **Locate License Plates:** Precisely crop license plate regions from vehicle images.
3.  **Recognize Characters:** Perform Optical Character Recognition (OCR) on the license plates to extract the plate number.
4.  **Manage Records:** Track toll transactions in a database with a user-friendly dashboard.

## 🛠️ Tech Stack & Libraries

The following libraries are used in this project (as listed in `requirements.txt`):

*   **`streamlit`**: Used to build the interactive web-based dashboard and user interface.
*   **`ultralytics`**: Provides the YOLOv8 implementation for vehicle detection, license plate localization, and character recognition.
*   **`opencv-python`**: Used for real-time image processing, video stream handling, and image transformations.
*   **`pandas`**: Facilitates data manipulation and structured display of database records within the UI.
*   **`numpy`**: Handles large, multi-dimensional arrays and matrices for image data processing.
*   **`pillow` (PIL)**: Used for opening, manipulating, and saving many different image file formats.
*   **`PyYAML`**: Used for parsing and managing configuration files (like `data.yaml`) for YOLO training.
*   **`pyodbc`**: Used to establish connections to an **MS SQL Server** database to store and retrieve persistent toll booth records.

## 🗄️ Database Architecture

We use **MS SQL Server** as our primary relational database management system. This ensures robust data storage for vehicle logs, owner information, and transaction history.

### Visual Assets & Diagrams

| Asset | Preview |
| :--- | :---: |
| **Application Dashboard** | ![Application Interface](assets/Application%20(1).png) |
| **Database Relationship** | ![Database Overview](assets/Database%20(2).png) |

| Diagram | Preview |
| :--- | :---: |
| **Entity Relationship Diagram (ERD)** | ![Database ERD](assets/Database%20ERD.png) |
| **Schema Diagram** | ![Database Schema Diagram](assets/Database%20Schema%20Diagram.png) |

## 📁 Project Structure

```text
smart-toll-booth-system/
├── src/
│   ├── app.py              # Streamlit web application
│   ├── database.py         # Database management (MS SQL Server via pyodbc)
│   ├── manager.py          # System orchestration logic
│   ├── model/
│   │   ├── lp_model.py     # Vehicle & License Plate detection trainer
│   │   ├── character_model.py # License Plate character recognition trainer
│   │   └── outputs/        # Trained .pt model files
│   ├── data/
│   │   ├── processed_plates/  # Dataset for character detection & recognition
│   │   └── processed_vehicles/ # Dataset for vehicle detection
│   └── utils/
│       ├── create_db.sql    # SQL script to initialize MS SQL tables
│       ├── clean_db.sql     # SQL script to drop/reset tables
│       └── dataset_splitter.py # Utility to split raw data
├── assets/                 # Project diagrams and screenshots
├── LICENSE.txt             # Project license
└── README.md               # You are here!
```

## 🚀 Getting Started

### Prerequisites

*   Python 3.10+
*   MS SQL Server (configured and accessible)

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

## ⚙️ Features

*   **Live Camera Feed:** Real-time capture and processing from a webcam.
*   **Media Upload:** Support for processing static images and recorded videos.
*   **Searchable Database:** A clean UI to view, search, and manage toll records stored in MS SQL Server.
*   **Dual YOLO Pipeline:** Separated models for high-accuracy detection and recognition.

## 📊 Dataset

This project utilizes the EALPR (Egyptian Automated License Plate Recognition) dataset. We would like to credit the authors for providing this benchmark dataset:

**Citation:**
> Youssef, Ahmed Ramadan and Sayed, Fawzya Ramadan and Ali, Abdelmgeid Ameen, "A New Benchmark Dataset for Egyptian License Plate Detection and Recognition," 2022 7th Asia-Pacific Conference on Intelligent Robot Systems (ACIRS), 2022, pp. 106-111, doi: 10.1109/ACIRS55390.2022.9845514.

## 📄 License

This project is licensed under the terms of the `LICENSE.txt` file included in this repository.
