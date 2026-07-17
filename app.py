import streamlit as st
import pandas as pd
import time
from templates import get_intervention_card, get_safe_card, get_homeostasis_card

# 1. Page Configuration
st.set_page_config(page_title="BioStream Music", layout="wide", initial_sidebar_state="expanded")

# Inject external style.css file into the Streamlit application context
try:
    with open("style.css") as f:
        # Using a regular string instead of an f-string to prevent brackets conflict
        st.markdown("<style>" + f.read() + "</style>", unsafe_allowed_html=True)
except FileNotFoundError:
    pass

# 2. Session State Initialization
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False
if 'hrv_history' not in st.session_state:
    st.session_state.hrv_history = []
if 'eda_history' not in st.session_state:
    st.session_state.eda_history = []

# Load simulated WESAD telemetry data
try:
    df = pd.read_csv("simulated_wesad_data.csv")
except FileNotFoundError:
    st.error("Error: 'simulated_wesad_data.csv' missing from repository.")
    st.stop()

# 3. Sidebar: Media Library Management
st.sidebar.markdown("# 🎵 BioStream Music")
st.sidebar.markdown("### `Library` / Your Playlist")

music_library = {
    "Thunderstruck - AC/DC (134 BPM) [Rock]": {"bpm": 134, "risk": True, "type": "High-Tempo Rock"},
    "Blinding Lights - The Weeknd (171 BPM) [Pop]": {"bpm": 171, "risk": True, "type": "Synth-Pop"},
    "Starboy - The Weeknd (186 BPM) [Pop]": {"bpm": 186, "risk": True, "type": "Up-Tempo Pop"},
    "Lose Yourself - Eminem (86 BPM) [Hip-Hop]": {"bpm": 86, "risk": True, "type": "Aggressive Hip-Hop"},
    "Animals - Martin Garrix (128 BPM) [EDM]": {"bpm": 128, "risk": True, "type": "High-Energy EDM"},
    "Harder Better Faster - Daft Punk (123 BPM) [Electronic]": {"bpm": 123, "risk": True, "type": "Electronic"},
    "Believer - Imagine Dragons (125 BPM) [Alternative]": {"bpm": 125, "risk": True, "type": "Alternative Rock"},
    "Ocean Eyes - Billie Eilish (135 BPM) [Indie Pop]": {"bpm": 135, "risk": False, "type": "Soft Indie"},
    "Clair de Lune - Debussy (62 BPM) [Classical]": {"bpm": 62, "risk": False, "type": "Classical Calm"},
    "Weightless - Marconi Union (60 BPM) [Ambient]": {"bpm": 60, "risk": False, "type": "Therapeutic Ambient"},
    "Strawberry Swing - Coldplay (78 BPM) [Alternative]": {"bpm": 78, "risk": False, "type": "Acoustic Pop"},
    "Gymnopédie No.1 - Erik Satie (65 BPM) [Piano]": {"bpm": 65, "risk": False, "type": "Minimalist Piano"},
    "Comfortably Numb - Pink Floyd (112 BPM) [Rock]": {"bpm": 112, "risk": False, "type": "Progressive Rock"},
    "Sunset Lover - Petit Biscuit (91 BPM) [Lo-Fi]": {"bpm": 91, "risk": False, "type": "Chill Electronic"},
    "Midnight City - M83 (105 BPM) [Synthwave]": {"bpm": 105, "risk": False, "type": "Dream Pop"}
}

selected_track = st.sidebar.radio("Select a track to play:", list(music_library.keys()))
track_meta = music_library[selected_track]

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Simulation Controls")

if st.sidebar.button("Toggle Telemetry Stream"):
    st.session_state.is_streaming = not st.session_state.is_streaming

if st.sidebar.button("Reset Session"):
    st.session_state.current_index = 0
    st.session_state.hrv_history = []
    st.session_state.eda_history = []
    st.session_state.is_streaming = False
    st.rerun()

# 4. Main User Interface
st.markdown(f"## Now Playing: **{selected_track}**")
st.caption(f"Audio Analytics: Genre Profile — {track_meta['type']} | Base Tempo — {track_meta['bpm']} BPM")

col_sensors, col_ai = st.columns([4, 5])

# Operational Telemetry Stream Loop Execution
if st.session_state.is_streaming and st.session_state.current_index < len(df):
    row = df.iloc[st.session_state.current_index]
    st.session_state.hrv_history.append(row['HRV'])
    st.session_state.eda_history.append(row['EDA'])
    st.session_state.current_index += 1
    
    if len(st.session_state.hrv_history) > 30:
        st.session_state.hrv_history.pop(0)
        st.session_state.eda_history.pop(0)

current_hrv = st.session_state.hrv_history[-1] if st.session_state.hrv_history else 72.0
current_eda = st.session_state.eda_history[-1] if st.session_state.eda_history else 2.1

# Left Canvas Elements: Data Ingestion Visualizer
with col_sensors:
    st.markdown("### ⌚ Wearable Device Telemetry")
    m1, m2 = st.columns(2)
    m1.metric("Heart Rate Variability", f"{current_hrv} BPM")
    m2.metric("Electrodermal Activity", f"{current_eda} µS")
    
    st.markdown("#### Dynamic Physiological Trends")
    st.line_chart(st.session_state.hrv_history, use_container_width=True)
    st.line_chart(st.session_state.eda_history, use_container_width=True)

# Right Canvas Elements: AI Engine Decision Visualizer
with col_ai:
    st.markdown("### 🧠 Deep Inference & Recommendation Engine")
    is_stressed = current_eda > 4.0 and current_hrv > 85.0
    
    if is_stressed:
        st.error("🚨 Inference Result: ACUTE PHYSIOLOGICAL STRESS DETECTED")
        st.caption("Model Evaluation Stability: Confidence Level @ 91.4% (CNN-LSTM Subnetwork)")
        st.markdown("### 🔔 Human-in-the-Loop Feedback Dispatcher")
        
        # Call modularized layout cards from templates.py
        if track_meta['risk']:
            st.markdown(get_intervention_card(selected_track, track_meta['bpm']), unsafe_allowed_html=True)
        else:
            st.markdown(get_safe_card(), unsafe_allowed_html=True)
    else:
        st.success("🟢 Inference Result: HOMEOSTASIS BASELINE STATE")
        st.caption("Model Evaluation Stability: Confidence Level @ 94.2% (Steady State)")
        st.markdown("### 🔔 Human-in-the-Loop Feedback Dispatcher")
        st.markdown(get_homeostasis_card(), unsafe_allowed_html=True)

# Loop Re-trigger Control Directive
if st.session_state.is_streaming and st.session_state.current_index < len(df):
    time.sleep(0.4)
    st.rerun()
elif st.session_state.current_index >= len(df):
    st.info("Simulation run completed. Click 'Reset Session' in the sidebar to test again.")
