import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image
import random
from manager import manager
from database import db_manager

# --- Page Configuration ---
st.set_page_config(
    page_title="Smart Toll Booth Detection System",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Session State Initialization ---
if 'view_table' not in st.session_state:
    st.session_state.view_table = "Logs"
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

# --- Constants for Randomization ---
FEES = [10.0, 15.0, 20.0, 25.0]
CAR_TYPES = ["Sedan", "Off-road", "Hatchback", "Pickup", "Van", "Sport", "SUV"]

# --- Database Loading Logic ---
def load_data():
    try:
        if st.session_state.view_table == "Logs":
            df = db_manager.get_recent_logs()
            if not df.empty:
                df.columns = ["License Plate", "Car Type", "Fee ($)", "Timestamp"]
            return df
        elif st.session_state.view_table == "Cars":
            df = db_manager.get_all_cars()
            if not df.empty:
                df.columns = ["License Plate", "Type", "Passes", "Total Fees ($)"]
            return df
        elif st.session_state.view_table == "Drivers":
            df = db_manager.get_all_drivers()
            if not df.empty:
                df.columns = ["NID", "Full Name", "Phone", "Plate", "Last Update"]
            return df
    except Exception as e:
        st.error(f"Table Error: {e}")
    return pd.DataFrame()

df = load_data()

# --- Main Title ---
st.title("Smart Toll Booth Detection System")
st.markdown("---")

left_col, right_col = st.columns([1.2, 1.5], gap="large")

with left_col:
    st.subheader("Camera / Upload Feed")
    
    uploaded_files = st.file_uploader("Upload Video/Images", type=["mp4", "avi", "jpg", "png"], accept_multiple_files=True)
    live_feed = st.checkbox("Enable Camera", key='live_feed')

    video_container = st.container(border=True)

    with video_container:
        if live_feed:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            frame_placeholder = st.empty()
            if st.button("Capture Photo"):
                st.session_state['live_feed'] = False
            try:
                while cap.isOpened() and st.session_state.get('live_feed', True):
                    ret, frame = cap.read()
                    if not ret: break
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
                    st.session_state.captured_frame = frame_rgb
            finally:
                cap.release()
        elif uploaded_files:
            if st.session_state.current_index >= len(uploaded_files):
                st.session_state.current_index = 0
            current_file = uploaded_files[st.session_state.current_index]
            if current_file.type.startswith('image'):
                img = Image.open(current_file)
                st.image(img, caption=f"Uploaded Image: {current_file.name}", use_container_width=True)
            elif current_file.type.startswith('video'):
                st.video(current_file)

            if len(uploaded_files) > 1:
                nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
                with nav_col1:
                    if st.button("⬅️ Previous", use_container_width=True):
                        st.session_state.current_index = (st.session_state.current_index - 1) % len(uploaded_files)
                        st.rerun()
                with nav_col2:
                    st.markdown(f"<p style='text-align: center;'>{st.session_state.current_index + 1} of {len(uploaded_files)}</p>", unsafe_allow_html=True)
                with nav_col3:
                    if st.button("Next ➡️", use_container_width=True):
                        st.session_state.current_index = (st.session_state.current_index + 1) % len(uploaded_files)
                        st.rerun()
        elif st.session_state.captured_frame is not None:
            st.image(st.session_state.captured_frame, caption="Captured Frame", use_container_width=True)
            if st.button("Clear Capture"):
                st.session_state.captured_frame = None
                st.session_state.detected_plate_img = None
                st.session_state.detected_text = None
                st.session_state.image_results = {}
                st.rerun()
        else:
            st.markdown("<div style='padding: 120px 20px; text-align: center; color: gray;'><i>Awaiting feed...</i></div>", unsafe_allow_html=True)
    
    if st.button("Process Media", type="primary", use_container_width=True):
        if uploaded_files:
            with st.spinner("Processing..."):
                for f in uploaded_files:
                    if f.type.startswith('image/'):
                        img = Image.open(f)
                        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                        cropped_plate, _ = manager.detect_and_crop_plate(img_bgr)
                        if cropped_plate is not None:
                            text = manager.extract_text_from_plate(cropped_plate)
                            h, w = cropped_plate.shape[:2]
                            st.session_state.image_results[f.name] = {
                                'detected_plate_img': cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2RGB),
                                'plate_aspect_ratio': w / h,
                                'detected_text': text
                            }
                            if text:
                                db_manager.record_passage(text, random.choice(CAR_TYPES), random.choice(FEES))
                st.rerun()
        elif st.session_state.captured_frame is not None:
            with st.spinner("Processing..."):
                img_bgr = cv2.cvtColor(st.session_state.captured_frame, cv2.COLOR_RGB2BGR)
                cropped_plate, _ = manager.detect_and_crop_plate(img_bgr)
                if cropped_plate is not None:
                    text = manager.extract_text_from_plate(cropped_plate)
                    st.session_state.detected_plate_img = cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2RGB)
                    h, w = cropped_plate.shape[:2]
                    st.session_state.plate_aspect_ratio = w / h
                    st.session_state.detected_text = text
                    if text:
                        db_manager.record_passage(text, random.choice(CAR_TYPES), random.choice(FEES))
                        st.rerun()

with right_col:
    st.subheader(f"Database View: {st.session_state.view_table}")
    control_col1, control_col2 = st.columns([1, 1.5])
    with control_col1:
        tables = ["Logs", "Cars", "Drivers"]
        current_idx = tables.index(st.session_state.view_table)
        if st.button(f"🔄 Switch to {tables[(current_idx + 1) % 3]}", use_container_width=True):
            st.session_state.view_table = tables[(current_idx + 1) % 3]
            st.rerun()
    with control_col2:
        search_query = st.text_input("Search", placeholder="🔍 Search Plate / Name...", label_visibility="collapsed")
    
    if not df.empty and search_query:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        display_df = df[mask]
    else: display_df = df
        
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    if st.session_state.detected_plate_img is not None:
        st.markdown("---")
        st.subheader("Detection Result")
        res_col1, res_col2 = st.columns([1, 1], gap="medium")
        with res_col1:
            st.image(st.session_state.detected_plate_img, caption="Cropped Plate", use_container_width=True)
        with res_col2:
            aspect = st.session_state.get('plate_aspect_ratio', 3/1)
            st.markdown(f"""
                <div style="background-color: #0e1117; aspect-ratio: {aspect}; border-radius: 12px; border: 2px solid #31333f; display: flex; justify-content: center; align-items: center;">
                    <h1 style="color: white; font-size: 2.5vw; font-family: 'Courier New'; letter-spacing: 0.5vw; direction: rtl;">{st.session_state.detected_text}</h1>
                </div>
                <p style="text-align: center; color: #808495; font-size: 14px; margin-top: 5px;">Detected Characters</p>
                """, unsafe_allow_html=True)
