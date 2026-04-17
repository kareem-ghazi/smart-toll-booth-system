import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image

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
    
    # 1. Initialize session state to store the captured image
    if 'captured_frame' not in st.session_state:
        st.session_state.captured_frame = None

    # Upload & Live Feed Controls
    uploaded_file = st.file_uploader("Upload Video/Image", type=["mp4", "avi", "jpg", "png"])
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
        elif uploaded_file is not None:
            file_type = uploaded_file.type.split('/')[0]
            if file_type == 'image':
                img = Image.open(uploaded_file)
                st.image(img, caption="Uploaded Image", width='stretch')
            elif file_type == 'video':
                st.video(uploaded_file)

        # 3. CAPTURED IMAGE DISPLAY
        elif st.session_state.captured_frame is not None:
            st.image(st.session_state.captured_frame, caption="Captured Frame", width='stretch')
            if st.button("Clear Capture"):
                st.session_state.captured_frame = None
                st.rerun()

        # 4. EMPTY STATE
        else:
            st.markdown("""
                <div style='padding: 120px 20px; text-align: center; color: gray;'>
                    <i>Awaiting video feed or file upload...</i>
                </div>
            """, unsafe_allow_html=True)
    
    # Process Button
    st.button("Process Media", type="primary", width='stretch')

# ==========================================
# RIGHT COLUMN: DATABASE RECORDS
# ==========================================
with right_col:
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