import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Traffic History",
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
.run-box {
    background:#111827;
    padding:14px;
    border-radius:12px;
    border:1px solid #334155;
    margin-bottom:10px;
}
.metric {
    font-size:14px;
    color:#cbd5f5;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("""
<div class="section">
<h2>🕘 Traffic Analysis History</h2>
<p style="color:#94a3b8">
Previously processed traffic videos and analytics
</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# LOAD RUNS
# ==============================
HISTORY_DIR = "history"

if not os.path.exists(HISTORY_DIR):
    st.warning("No history found yet. Process a video first.")
    st.stop()

runs = sorted(os.listdir(HISTORY_DIR), reverse=True)

if not runs:
    st.info("No processed runs available.")
    st.stop()

# ==============================
# SIDEBAR – SELECT RUN
# ==============================
with st.sidebar:
    st.header("📂 Select Run")

    selected_run = st.selectbox(
        "Available Runs",
        runs,
        format_func=lambda x: x.replace("run_", "").replace("_", " ")
    )

# ==============================
# LOAD SUMMARY
# ==============================
run_path = os.path.join(HISTORY_DIR, selected_run)
summary_path = os.path.join(run_path, "summary.json")
csv_path = os.path.join(run_path, "traffic_log.csv")

if not os.path.exists(summary_path) or not os.path.exists(csv_path):
    st.error("Run data incomplete.")
    st.stop()

with open(summary_path) as f:
    summary = json.load(f)

df = pd.read_csv(csv_path)

# ==============================
# SUMMARY CARDS
# ==============================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("### 📌 Run Summary")

c1, c2, c3, c4 = st.columns(4)

def card(col, title, value):
    with col:
        st.markdown(f"""
        <div class="run-box">
            <div class="metric">{title}</div>
            <h3>{value}</h3>
        </div>
        """, unsafe_allow_html=True)

card(c1, "Total Vehicles", summary["total_vehicles"])
card(c2, "Red-Light Violations", summary["red_light_violations"])
card(c3, "Rash Driving", summary["rash_driving"])
card(c4, "Frames Processed", summary["frames_processed"])

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# TREND GRAPH
# ==============================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("### 📈 Traffic Trends")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["frame"], df["queue_count"], label="Queue Length")
ax.plot(df["frame"], df["red_light_violations"], label="Red-Light Violations")
ax.plot(df["frame"], df["rash_driving"], label="Rash Driving")

ax.set_xlabel("Frame")
ax.set_ylabel("Count")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.caption(
    f"Run processed on {summary['processed_at']}"
)
