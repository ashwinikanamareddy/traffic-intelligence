import streamlit as st

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="About – Urban Traffic Intelligence",
    layout="wide"
)

# ==============================
# STYLING
# ==============================
st.markdown("""
<style>
.section {
    background:#020617;
    padding:28px;
    border-radius:16px;
    border:1px solid #334155;
    margin-bottom:24px;
}
h2, h3 {
    color:#f8fafc;
}
p {
    color:#cbd5f5;
    font-size:16px;
    line-height:1.7;
}
.highlight {
    background:#111827;
    padding:16px;
    border-radius:12px;
    border-left:5px solid #22c55e;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("""
<div class="section">
<h2>🚦 About Urban Traffic Intelligence System</h2>
<p>
An AI-powered platform for real-time traffic monitoring, violation detection,
and congestion analysis using computer vision.
</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# PROBLEM STATEMENT
# ==============================
st.markdown("""
<div class="section">
<h3>❌ Problem Statement</h3>
<p>
Urban intersections suffer from heavy congestion, frequent red-light violations,
and unsafe driving behavior. Most traffic signals operate on fixed timers and rely
on manual monitoring, making them ineffective in real-time scenarios.
</p>
<p>
As a result:
</p>
<ul style="color:#cbd5f5">
<li>Traffic queues grow uncontrollably</li>
<li>Violations increase without enforcement</li>
<li>Emergency response is delayed</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ==============================
# EXISTING SYSTEM LIMITATIONS
# ==============================
st.markdown("""
<div class="section">
<h3>⚠ Limitations of Existing Systems</h3>
<ul style="color:#cbd5f5">
<li>Static signal timing (no real-time awareness)</li>
<li>Manual traffic police monitoring</li>
<li>No historical traffic intelligence</li>
<li>No automated violation analytics</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ==============================
# OUR SOLUTION
# ==============================
st.markdown("""
<div class="section">
<h3>✅ Our Solution</h3>
<p>
We propose an <b>AI-based Urban Traffic Intelligence System</b> that uses
video analytics to automatically detect vehicles, track movement,
analyze queues, and identify violations — all in near real-time.
</p>

<div class="highlight">
<b>Key Idea:</b><br>
Instead of fixed timers and human monitoring, traffic decisions are driven by
live video data and intelligent analytics.
</div>
</div>
""", unsafe_allow_html=True)

# ==============================
# SYSTEM WORKING
# ==============================
st.markdown("""
<div class="section">
<h3>🧠 How the System Works</h3>
<ol style="color:#cbd5f5">
<li>Traffic video is captured from junction cameras</li>
<li>YOLOv8 detects vehicles in each frame</li>
<li>DeepSORT assigns unique IDs and tracks vehicles</li>
<li>Queue region and stop-line rules are applied</li>
<li>Violations and driving behavior are logged</li>
<li>Live and historical analytics are generated</li>
</ol>
</div>
""", unsafe_allow_html=True)

# ==============================
# FEATURES
# ==============================
st.markdown("""
<div class="section">
<h3>🌟 Key Features</h3>
<ul style="color:#cbd5f5">
<li>🚗 Automatic vehicle detection & tracking</li>
<li>🚦 Queue length estimation</li>
<li>🚨 Red-light violation detection</li>
<li>⚠ Rash driving detection</li>
<li>📹 Live annotated video monitoring</li>
<li>📊 Historical traffic analytics</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ==============================
# HACKATHON IMPACT
# ==============================
st.markdown("""
<div class="section">
<h3>🏆 Why This Solution Stands Out</h3>
<ul style="color:#cbd5f5">
<li>End-to-end system (not just ML model)</li>
<li>Real-time + historical intelligence</li>
<li>Scalable to smart cities</li>
<li>Low-cost (camera-based, no sensors)</li>
<li>Ready for real-world deployment</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.caption(
    "Urban Traffic Intelligence System | Hackathon Project"
)
