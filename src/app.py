import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image
# Assuming manager is a local module
from manager import manager 

# --- Page Configuration ---
st.set_page_config(
    page_title="Smart Toll Booth Detection System",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom Styling for Padding & Alignment ---
st.markdown("""
    <style>
        /* 1. Reduce vertical gap between all elements */
        [data-testid="stVerticalBlock"] > div {
            gap: 0.1rem !important;
        }
        
        /* 2. Center the "of X" text vertically with the input box */
        .counter-text {
            display: flex;
            align-items: center;
            height: 38px;
            margin: 0;
            font-size: 1.1em;
            color: #FAFAFA;
        }

        /* 3. Tighten the caption area (Blue Area) */
        .file-caption {
            text-align: center; 
            color: #808495; 
            margin-top: 5px !important;
            margin-bottom: 5px !important; 
            font-size: 0.9em;
        }

        /* 4. Ensure images are centered */
        div[data-testid="stImage"] {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

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
    
    # Initialize session states
    if 'current_index' not in st.session_state: st.session_state.current_index = 0
    if 'image_results' not in st.session_state: st.session_state.image_results = {}
    if 'captured_frame' not in st.session_state: st.session_state.captured_frame = None
    if 'detected_plate_img' not in st.session_state: st.session_state.detected_plate_img = None
    if 'detected_text' not in st.session_state: st.session_state.detected_text = None
    if 'plate_aspect_ratio' not in st.session_state: st.session_state.plate_aspect_ratio = 3/1
    if 'uploader_key' not in st.session_state: st.session_state.uploader_key = 0

    def reset_index():
        st.session_state.current_index = 0
        if 'nav_jump' in st.session_state:
            st.session_state.nav_jump = 1

    uploaded_files = st.file_uploader("Upload Video/Images", type=["mp4", "avi", "jpg", "png"], 
                                      accept_multiple_files=True, on_change=reset_index, 
                                      key=f"uploader_{st.session_state.uploader_key}")
    
    col_proc, col_clear = st.columns([2, 1])
    with col_proc:
        process_btn = st.button("Process Media", type="primary", width='stretch')
    with col_clear:
        if st.button("🗑️ Remove All", width='stretch'):
            st.session_state.uploader_key += 1
            st.session_state.image_results = {}
            st.session_state.current_index = 0
            st.session_state.detected_plate_img = None
            st.session_state.detected_text = None
            if 'nav_jump' in st.session_state:
                st.session_state.nav_jump = 1
            st.rerun()

    live_feed = st.checkbox("Enable Camera", key='live_feed_toggle')

    # Process Logic
    if process_btn:
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
                                'detected_plate_img': None, 'detected_text': "No Plate Detected", 'plate_aspect_ratio': 3/1
                            }
                st.rerun()

    # Video/Image Container
    video_container = st.container(border=True)
    with video_container:
        # 1. LIVE CAMERA
        if live_feed:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            frame_placeholder = st.empty()
            if st.button("Capture Photo"): st.session_state.live_feed_toggle = False
            
            while cap.isOpened() and st.session_state.get('live_feed_toggle', True):
                ret, frame = cap.read()
                if not ret: break
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, width='stretch')
                st.session_state.captured_frame = frame_rgb
            cap.release()

        # 2. UPLOADED FILE DISPLAY (Navigation + Logic)
        elif uploaded_files:
            # Navigation Bar (5-Column Layout to center the counter)
            if len(uploaded_files) > 1:
                def move_index(delta):
                    st.session_state.current_index = (st.session_state.current_index + delta) % len(uploaded_files)
                    st.session_state.nav_jump = st.session_state.current_index + 1

                n_c1, n_c2, n_c3, n_c4 = st.columns([0.7, 0.25, 0.25, 0.7], gap="small")
                
                with n_c1:
                    st.button("⬅️ Previous", width='stretch', on_click=move_index, args=(-1,))
                
                with n_c2:
                    def sync_index(): st.session_state.current_index = st.session_state.nav_jump - 1
                    st.number_input("Idx", 1, len(uploaded_files), value=int(st.session_state.current_index + 1), 
                                    key="nav_jump", on_change=sync_index, label_visibility="collapsed")
                
                with n_c3:
                    st.markdown(f"<div class='counter-text'>of {len(uploaded_files)}</div>", unsafe_allow_html=True)
                
                with n_c4:
                    st.button("Next ➡️", width='stretch', on_click=move_index, args=(1,))

            current_file = uploaded_files[st.session_state.current_index]
            st.markdown(f"<p class='file-caption'>Uploaded Image: {current_file.name}</p>", unsafe_allow_html=True)

            if current_file.type.startswith('image'):
                img = Image.open(current_file)
                st.image(img, width='stretch')
                
                # Update Detection Results for this specific image
                if current_file.name in st.session_state.image_results:
                    res = st.session_state.image_results[current_file.name]
                    st.session_state.detected_plate_img = res['detected_plate_img']
                    st.session_state.detected_text = res['detected_text']
                    st.session_state.plate_aspect_ratio = res['plate_aspect_ratio']
                else:
                    st.session_state.detected_plate_img = None

        elif st.session_state.captured_frame is not None:
            st.image(st.session_state.captured_frame, caption="Captured Frame")
            if st.button("Clear Capture"):
                st.session_state.captured_frame = None
                st.rerun()
        else:
            st.markdown("<div style='padding:100px; text-align:center; color:gray;'>Awaiting media...</div>", unsafe_allow_html=True)

# ==========================================
# RIGHT COLUMN: DATABASE & RESULTS
# ==========================================
with right_col:
    st.subheader("Database Records (Toll Info)")
    c1, c2 = st.columns([1, 2])
    with c1: st.button("Switch Table", width='stretch')
    with c2: search = st.text_input("Search", placeholder="🔍 Search Plate...", label_visibility="collapsed")
    
    filtered_df = df[df["License Plate"].str.contains(search.upper())] if search else df
    st.dataframe(filtered_df, width='stretch', hide_index=True)

    if st.session_state.detected_plate_img is not None:
        st.markdown("---")
        st.subheader("Detection Result")
        res_col1, res_col2 = st.columns([1, 1], gap="medium")
        with res_col1:
            st.image(st.session_state.detected_plate_img, caption="Cropped Plate", width='stretch')
        with res_col2:
            st.markdown(f"""
                <div style="background:#0e1117; width:100%; aspect-ratio:{st.session_state.plate_aspect_ratio}; 
                border-radius:12px; border:2px solid #31333f; display:flex; justify-content:center; align-items:center;">
                    <h1 style="color:white; font-size:2.5vw; font-family:monospace; letter-spacing:0.5vw; direction:rtl;">
                        {st.session_state.detected_text}
                    </h1>
                </div>
                <p style="text-align:center; color:#808495; font-size:14px; margin-top:5px;">Detected Characters</p>
            """, unsafe_allow_html=True)