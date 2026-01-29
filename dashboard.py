import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

from backend.process_video import process_video
IS_CLOUD = os.getenv("STREAMLIT_CLOUD") is not None

# ==============================
# SESSION STATE
# ==============================
if "processed" not in st.session_state:
    st.session_state.processed = False

if "df" not in st.session_state:
    st.session_state.df = None

if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "total_vehicles": 0,
        "queue_count": 0,
        "red_light_violations": 0,
        "rash_driving": 0
    }

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Urban Traffic Intelligence – Home",
    layout="wide"
)

# ==============================
# GLOBAL STYLING (POLISHED)
# ==============================
st.markdown("""
<style>
body { background:#020617; }

.section {
    background:#020617;
    padding:24px;
    border-radius:16px;
    border:1px solid #334155;
    margin-bottom:24px;
}

.metric-box {
    background:#111827;
    padding:22px;
    border-radius:16px;
    border:1px solid #334155;
    text-align:center;
}

.metric-value {
    font-size:38px;
    font-weight:700;
    color:white;
}

.metric-label {
    color:#94a3b8;
    font-size:14px;
}

.sidebar-box {
    background:#020617;
    padding:16px;
    border-radius:12px;
    border:1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER (PROFESSIONAL)
# ==============================
st.markdown("""
<div class="section">
<h1>🚦 Urban Traffic Intelligence Console</h1>
<p style="color:#94a3b8;">
AI-Powered Traffic Queue & Violation Detection System<br>
NH-44 × RTC Junction · Kurnool · Smart City Analytics
</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown("## 🎛 Control Panel")
    st.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)

    uploaded_video = st.file_uploader(
        "Upload Traffic Video",
        type=["mp4", "avi", "mov"]
    )

    process_btn = st.button("▶ Process Video", use_container_width=True)

    st.markdown("---")
    st.markdown("**AI Stack Used**")
    st.caption("• YOLOv8 Object Detection")
    st.caption("• DeepSORT Tracking")
    st.caption("• Rule-based Traffic Analytics")

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# PROCESS VIDEO
# ==============================
if uploaded_video and process_btn and not st.session_state.processed:

    os.makedirs("uploads", exist_ok=True)
    video_path = f"uploads/{uploaded_video.name}"

    with open(video_path, "wb") as f:
        f.write(uploaded_video.getbuffer())

    if IS_CLOUD:
        st.warning(
            "🚫 Live video processing is disabled on Streamlit Cloud.\n\n"
            "👉 Please run the app locally to see real-time AI video analysis."
        )
    else:
        with st.spinner("Processing video… please wait"):
            run_dir = process_video(video_path)


    csv_path = os.path.join(run_dir, "traffic_log.csv")
    df = pd.read_csv(csv_path)

    st.session_state.df = df

    last = df.iloc[-1]
    st.session_state.metrics = {
        "total_vehicles": int(last["total_vehicles"]),
        "queue_count": int(last["queue_count"]),
        "red_light_violations": int(last["red_light_violations"]),
        "rash_driving": int(last["rash_driving"])
    }

    st.session_state.processed = True
    st.success("✅ Video processed successfully")

# ==============================
# METRICS DASHBOARD
# ==============================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("### 📊 Traffic Summary")

c1, c2, c3, c4 = st.columns(4)

def metric(col, value, label, color):
    with col:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color:{color};">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

m = st.session_state.metrics

metric(c1, m["total_vehicles"], "🚗 Total Vehicles", "#38bdf8")
metric(c2, m["queue_count"], "🚦 Queue Length", "#facc15")
metric(c3, m["red_light_violations"], "⛔ Violations", "#f87171")
metric(c4, m["rash_driving"], "⚠️ Rash Driving", "#fb7185")

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# TRAFFIC TREND
# ==============================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("### 📈 Traffic Behaviour Over Time")

if st.session_state.processed:
    df = st.session_state.df

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["frame"], df["queue_count"], label="Queue", linewidth=2)
    ax.plot(df["frame"], df["red_light_violations"], label="Violations", linewidth=2)
    ax.plot(df["frame"], df["rash_driving"], label="Rash Driving", linewidth=2)

    ax.set_facecolor("#020617")
    fig.patch.set_facecolor("#020617")
    ax.tick_params(colors="white")
    ax.legend(labelcolor="white")
    ax.grid(color="#334155")

    st.pyplot(fig)
else:
    st.info("Upload and process a video to view analytics")

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.caption(
    f"Urban Traffic Intelligence System | Generated {datetime.now().strftime('%d %b %Y · %I:%M %p')}"
)
