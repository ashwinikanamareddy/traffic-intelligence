import streamlit as st
import pandas as pd
import os
import time
from PIL import Image

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Live Traffic Monitoring",
    layout="wide"
)

# ==============================
# STYLING
# ==============================
st.markdown("""
<style>
.section {
    background:#020617;
    padding:24px;
    border-radius:16px;
    border:1px solid #334155;
    margin-bottom:20px;
}
.stat-box {
    background:#111827;
    padding:18px;
    border-radius:14px;
    border:1px solid #334155;
    text-align:center;
}
.stat-value {
    font-size:34px;
    font-weight:700;
    color:white;
}
.stat-label {
    color:#94a3b8;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("""
<div class="section">
<h2>🔴 Live Traffic Monitoring</h2>
<p style="color:#94a3b8;">
Near real-time annotated feed with live analytics
</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# TOP STATUS BAR
# ==============================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🚦 Traffic Signal")
    st.markdown("**Signal Status:** 🔴 **RED**")

with col2:
    auto_refresh = st.toggle("🔁 Auto Refresh (1 sec)", value=True)

# ==============================
# MAIN LIVE VIEW
# ==============================
left, right = st.columns([2.2, 1])

# ------------------------------
# LIVE VIDEO FEED
# ------------------------------
with left:
    st.markdown("### 📹 Live Annotated Feed")

    frame_path = "latest_frame.jpg"

    if os.path.exists(frame_path):
        img = Image.open(frame_path)
        st.image(img, caption="Live Traffic Feed", use_container_width=True)
    else:
        st.warning("Waiting for live feed...")

    st.caption("Live view updates every 1 second (near real-time)")

# ------------------------------
# LIVE STATS
# ------------------------------
with right:
    st.markdown("### 📊 Live Stats")

    # Default values
    vehicles = queue = violations = rash = 0

    # Try reading latest history
    if os.path.exists("history"):
        runs = sorted(os.listdir("history"), reverse=True)
        if runs:
            latest_run = os.path.join("history", runs[0], "traffic_log.csv")
            if os.path.exists(latest_run):
                df = pd.read_csv(latest_run)
                last = df.iloc[-1]
                vehicles = int(last["total_vehicles"])
                queue = int(last["queue_count"])
                violations = int(last["red_light_violations"])
                rash = int(last["rash_driving"])

    def stat(label, value, emoji):
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{emoji} {label}</div>
        </div>
        """, unsafe_allow_html=True)

    stat("Vehicles", vehicles, "🚗")
    stat("Queue", queue, "🚧")
    stat("Red-Light", violations, "🚨")
    stat("Rash Driving", rash, "⚠️")

# ==============================
# AUTO REFRESH
# ==============================
if auto_refresh:
    time.sleep(1)
    st.rerun()
