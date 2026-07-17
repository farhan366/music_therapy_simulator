import streamlit as st
import pandas as pd
import time

# Configure page layout and title
st.set_page_config(page_title="Bio-Music Simulator", layout="wide")
st.title("AI-Driven Closed-Loop Music Therapy Simulation Engine")
st.markdown("### Technical Framework: Human-in-the-Loop Therapeutic Recommendation via Biosignal Ingestion")
st.markdown("---")

# Load the simulated WESAD baseline dataset
try:
    df = pd.read_csv("simulated_wesad_data.csv")
except FileNotFoundError:
    st.error("Error: 'simulated_wesad_data.csv' not found. Please ensure it is uploaded to the repository.")
    st.stop()

# User initialization - Simulating starting a manual track
st.sidebar.markdown("## 🎵 User Music Selection")
user_track = st.sidebar.selectbox(
    "Select a song to start listening:",
    ["Rock Anthem - Heavy Distortions (130 BPM)", "Pop Synth Beats - High Energy (115 BPM)", "Lo-Fi Chills - Soft Acoustics (75 BPM)"]
)

# Rule Engine to evaluate if the current song is good or bad for stress
is_track_heavy = "Rock" in user_track or "Pop" in user_track

# Initialize structured dashboard columns for visual interface
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⌚ Wearable Telemetry Ingestion (Sensor Streams)")
    hrv_metric = st.empty()
    eda_metric = st.empty()
    hrv_chart = st.empty()
    eda_chart = st.empty()

with col2:
    st.markdown("### 🧠 Deep Sequential Inference Engine (AI Classifier)")
    status_indicator = st.empty()
    confidence_metrics = st.empty()
    st.markdown("---")
    st.markdown("### 🔔 Human-in-the-Loop Recommendation Actuator")
    current_audio_status = st.empty()
    recommendation_alert = st.empty()

# Streamlit session execution simulation logic
st.sidebar.markdown("## Simulation Controls")
if st.sidebar.button("Start Live Telemetry Streaming"):
    st.sidebar.success("Streaming Active...")
    
    # Pre-allocate tracking buffers for dynamic historical chart rendering
    hrv_buffer = []
    eda_buffer = []
    
    for idx, row in df.iterrows():
        time.sleep(0.5) # Dynamic stream replication latency
        
        # Extract operational signal scalars
        current_hrv = row['HRV']
        current_eda = row['EDA']
        
        # Append to visual plotting buffers
        hrv_buffer.append(current_hrv)
        eda_buffer.append(current_eda)
        
        # Update dashboard biometric monitoring widgets
        hrv_metric.metric(label="Heart Rate Variability (HRV)", value=f"{current_hrv} BPM")
        eda_metric.metric(label="Electrodermal Activity (EDA)", value=f"{current_eda} µS")
        
        # Render historical line trends
        hrv_chart.line_chart(hrv_buffer[-30:], use_container_width=True)
        eda_chart.line_chart(eda_buffer[-30:], use_container_width=True)
        
        # Show what the user is currently playing
        current_audio_status.info(f"🎧 Currently Listening to: {user_track}")
        
        # Real-Time Inference formulation (Emulating CNN-LSTM & Audio Analyzer)
        if current_eda > 4.0 and current_hrv > 85.0:
            status_indicator.error("🚨 Classification: ACUTE STRESS STATE DETECTED")
            confidence_metrics.caption("Inference Parameters: Model Stability @ 91.4% Accuracy")
            
            # If the user is listening to a bad song for stress (High BPM Rock/Pop)
            if is_track_heavy:
                recommendation_alert.warning(
                    "⚠️ **AI Recommendation Triggered:** Your biometric indicators show rising stress levels. "
                    "The current high-tempo track may aggravate anxiety. We recommend switching to: **'Binaural Ambient Waves (60 BPM)'**."
                )
            else:
                recommendation_alert.info("ℹ️ **AI Analysis:** Stress detected, but your current low-tempo song choice is helping to mitigate it. Keep listening.")
        else:
            status_indicator.success("🟢 Classification: HOMEOSTASIS / BASELINE RELAXED STATE")
            confidence_metrics.caption("Inference Parameters: Model Stability @ 94.2% Accuracy")
            recommendation_alert.success("✅ **System Status:** Physiological signals are optimal. No intervention needed.")
else:
    st.info("Select a song in the sidebar and click 'Start Live Telemetry Streaming' to initialize the simulation.")
