import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image
from manager import manager

# --- Page Configuration ---
st.set_page_config(
    page_title="Smart Toll Booth Detection System",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Dummy Data for Database ---
@st.cache_data
def load_dummy_data():
    return pd.DataFrame({
        "License Plate": ["ABC-123", "ABC-123", "ABC-123", "ABC-123", "ABC-127", "ABC-126", "ABC-134", "ABC-124"],
        "Car Type": ["Sedan", "Sedan", "Sedan", "Sedan", "Sedan", "Medium", "Sedan", "Sedan"],
        "Toll Fee ($)": ["$5.00", "$5.00", "$5.00", "$5.00", "$5.00", "$5.00", "$4.00", "$5.00"],
        "Timestamp": [
            "2024-05-15 10:32:01", "2024-05-15 10:32:01", "2024-05-15 10:32:01", 
            "2024-05-15 10:32:01", "2024-05-15 10:32:09", "2024-05-15 10:32:08", 
            "2024-05-15 10:32:01", "2024-05-15 10:32:03"
        ]
    })

df = load_dummy_data()

# --- Main Title ---
st.title("Smart Toll Booth Detection System")
st.markdown("---")

# --- Two-Column Layout ---
left_col, right_col = st.columns([1.2, 1.5], gap="large")

# ==========================================
# LEFT COLUMN: CAMERA / UPLOAD FEED
# ==========================================
with left_col:
    st.subheader("Camera / Upload Feed")
    
    # 1. Initialize session state to store the captured image and results
    if 'captured_frame' not in st.session_state:
        st.session_state.captured_frame = None
    if 'image_results' not in st.session_state:
        st.session_state.image_results = {}
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'detected_plate_img' not in st.session_state:
        st.session_state.detected_plate_img = None
    if 'detected_text' not in st.session_state:
        st.session_state.detected_text = None
    if 'plate_aspect_ratio' not in st.session_state:
        st.session_state.plate_aspect_ratio = 3/1

    def reset_index():
        st.session_state.current_index = 0

    # Upload & Live Feed Controls
    uploaded_files = st.file_uploader("Upload Video/Images", type=["mp4", "avi", "jpg", "png"], accept_multiple_files=True, on_change=reset_index)
    live_feed = st.checkbox("Enable Camera", key='live_feed')

    # Simulated Video Frame / AI Detection Window
    video_container = st.container(border=True)

    # 1. Define a function to turn off the camera
    def stop_camera():
        st.session_state['live_feed'] = False

    with video_container:
        # 1. LIVE CAMERA FEED
        if live_feed:
            camera_index = 0
            cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            frame_placeholder = st.empty()
            st.button("Capture Photo", on_click=stop_camera)
            
            try:
                while cap.isOpened() and st.session_state.get('live_feed', True):
                    ret, frame = cap.read()
                    if not ret: break
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_placeholder.image(frame_rgb, channels="RGB", width='stretch')
                    
                    # Constantly update state so we have the "last seen" frame
                    st.session_state.captured_frame = frame_rgb
            finally:
                cap.release()

        # 2. UPLOADED FILE DISPLAY (Priority over static captures)
        elif uploaded_files:
            if st.session_state.current_index >= len(uploaded_files):
                st.session_state.current_index = 0
            
            current_file = uploaded_files[st.session_state.current_index]
            file_type = current_file.type.split('/')[0]
            
            if file_type == 'image':
                img = Image.open(current_file)
                st.image(img, caption=f"Uploaded Image: {current_file.name}", width='stretch')
                # Convert PIL to numpy for processing
                st.session_state.current_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            elif file_type == 'video':
                st.video(current_file)
                st.session_state.current_image = None

            # Navigation Arrows
            if len(uploaded_files) > 1:
                nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
                with nav_col1:
                    if st.button("⬅️ Previous", width='stretch'):
                        st.session_state.current_index = (st.session_state.current_index - 1) % len(uploaded_files)
                        st.rerun()
                with nav_col2:
                    st.markdown(f"<p style='text-align: center; line-height: 2.5;'>{st.session_state.current_index + 1} of {len(uploaded_files)}</p>", unsafe_allow_html=True)
                with nav_col3:
                    if st.button("Next ➡️", width='stretch'):
                        st.session_state.current_index = (st.session_state.current_index + 1) % len(uploaded_files)
                        st.rerun()

            # Update detection results from cache for the current file
            if current_file.name in st.session_state.image_results:
                res = st.session_state.image_results[current_file.name]
                st.session_state.detected_plate_img = res.get('detected_plate_img')
                st.session_state.detected_text = res.get('detected_text')
                st.session_state.plate_aspect_ratio = res.get('plate_aspect_ratio', 3/1)
                if st.session_state.detected_plate_img is None:
                    st.warning("No license plate detected in this image.")
            else:
                st.session_state.detected_plate_img = None
                st.session_state.detected_text = None

        # 3. CAPTURED IMAGE DISPLAY
        elif st.session_state.captured_frame is not None:
            st.image(st.session_state.captured_frame, caption="Captured Frame", width='stretch')
            # Convert RGB (from session state) to BGR for processing
            st.session_state.current_image = cv2.cvtColor(st.session_state.captured_frame, cv2.COLOR_RGB2BGR)
            if st.button("Clear Capture"):
                st.session_state.captured_frame = None
                st.session_state.detected_plate_img = None
                st.session_state.detected_text = None
                st.session_state.image_results = {}
                st.rerun()

        # 4. EMPTY STATE
        else:
            st.markdown("""
                <div style='padding: 120px 20px; text-align: center; color: gray;'>
                    <i>Awaiting video feed or file upload...</i>
                </div>
            """, unsafe_allow_html=True)
    
    # Process Button
    if st.button("Process Media", type="primary", width='stretch'):
        if uploaded_files:
            with st.spinner(f"Processing {len(uploaded_files)} files..."):
                for f in uploaded_files:
                    if f.type.startswith('image/'):
                        img = Image.open(f)
                        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                        cropped_plate, _ = manager.detect_and_crop_plate(img_bgr)
                        if cropped_plate is not None:
                            h, w = cropped_plate.shape[:2]
                            st.session_state.image_results[f.name] = {
                                'detected_plate_img': cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2RGB),
                                'plate_aspect_ratio': w / h,
                                'detected_text': manager.extract_text_from_plate(cropped_plate)
                            }
                        else:
                            st.session_state.image_results[f.name] = {
                                'detected_plate_img': None,
                                'detected_text': "No Plate Detected",
                                'plate_aspect_ratio': 3/1
                            }
                st.rerun()
        elif st.session_state.captured_frame is not None:
            with st.spinner("Processing Capture..."):
                img_bgr = cv2.cvtColor(st.session_state.captured_frame, cv2.COLOR_RGB2BGR)
                cropped_plate, _ = manager.detect_and_crop_plate(img_bgr)
                
                if cropped_plate is not None:
                    st.session_state.detected_plate_img = cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2RGB)
                    h, w = cropped_plate.shape[:2]
                    st.session_state.plate_aspect_ratio = w / h
                    st.session_state.detected_text = manager.extract_text_from_plate(cropped_plate)
                else:
                    st.error("No license plate detected.")
                    st.session_state.detected_plate_img = None
                    st.session_state.detected_text = None

# ==========================================
# RIGHT COLUMN: DATABASE RECORDS
# ==========================================
with right_col:
    # --- Detection Results Area ---
    if st.session_state.detected_plate_img is not None:
        st.subheader("Detection Result")
        res_col1, res_col2 = st.columns([1, 1], gap="medium", vertical_alignment="top")
        with res_col1:
            # We use a container to help with alignment if needed, but st.image is usually fine
            st.image(st.session_state.detected_plate_img, caption="Cropped License Plate", width='stretch')
        with res_col2:
            # Using dynamic aspect-ratio to match the actual cropped image size
            aspect_ratio = st.session_state.get('plate_aspect_ratio', 3/1)
            st.markdown(
                f"""
                <div style="
                    background-color: #0e1117; 
                    width: 100%; 
                    aspect-ratio: {aspect_ratio}; 
                    border-radius: 12px; 
                    border: 2px solid #31333f; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    margin-bottom: 8px;
                ">
                    <h1 style="
                        color: white; 
                        margin: 0; 
                        font-size: 2.5vw; 
                        font-family: 'Courier New', Courier, monospace; 
                        letter-spacing: 0.5vw;
                        text-align: center;
                        direction: rtl;
                    ">{st.session_state.detected_text}</h1>
                </div>
                <p style="text-align: center; color: #808495; font-size: 14px; margin-top: 0px; margin-bottom: 25px;">Detected Characters</p>
                """,
                unsafe_allow_html=True
            )
        st.markdown("---")

    st.subheader("Database Records (Toll Info)")
    
    # Controls row: Button and Search Bar
    control_col1, control_col2 = st.columns([1, 2])
    
    with control_col1:
        st.button("Switch Database Table")
        
    with control_col2:
        search_query = st.text_input("Search", placeholder="🔍 Search License Plate...", label_visibility="collapsed")
    
    # Filter data based on search
    if search_query:
        filtered_df = df[df["License Plate"].str.contains(search_query.upper())]
    else:
        filtered_df = df
        
    # Data Table Display
    st.dataframe(
        filtered_df,
        width='stretch',
        hide_index=True
    )