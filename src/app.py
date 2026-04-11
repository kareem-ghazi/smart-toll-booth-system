import streamlit as st
import pandas as pd

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
    
    # Upload & Live Feed Controls
    uploaded_file = st.file_uploader("Upload Video/Image", type=["mp4", "avi", "jpg", "png"])
    live_feed = st.checkbox("Enable Live Feed")
    
    # Simulated Video Frame / AI Detection Window
    video_container = st.container(border=True)
    with video_container:
        if live_feed or uploaded_file:
            # Simulate the "Scanning..." and "Plate Detected" overlay
            # Removed the inner background-color to fix the nested box issue
            st.markdown("""
                <div style='padding: 100px 20px; text-align: center;'>
                    <span style='background-color: rgba(0,0,0,0.7); color: white; padding: 5px 10px; border-radius: 4px; position: absolute; top: 10px; right: 10px; font-size: 0.8em;'>Scanning...</span>
                    <div style='border: 2px solid #00FF00; display: inline-block; padding: 20px; position: relative;'>
                        <span style='background-color: #00FF00; color: black; padding: 2px 8px; font-size: 0.8em; font-weight: bold; position: absolute; top: -25px; left: -2px;'>Plate Detected: ABC-123 (Confidence: 98%)</span>
                        <h2 style='margin: 0; color: white;'>ABC-123</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Removed the inner background-color so it uses the container's native boundary seamlessly
            st.markdown("""
                <div style='padding: 120px 20px; text-align: center; color: gray;'>
                    <i>Awaiting video feed or file upload...</i>
                </div>
            """, unsafe_allow_html=True)
    
    st.write("") # Spacer
    
    # Progress Bar & Process Button
    st.progress(45)
    st.button("Process Media", type="primary", use_container_width=True)

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
        use_container_width=True,
        hide_index=True
        # Removed `height=400` here so the table fits the data exactly without blank rows
    )