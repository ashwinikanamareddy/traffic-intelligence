🚦 Urban Traffic Intelligence System
AI-Powered Traffic Queue Analysis & Violation Detection

A computer vision–based system that analyzes traffic videos to automatically detect traffic congestion, queue length, red-light violations, and rash driving behavior, and presents the insights through a clean, multi-page dashboard.

📌 Problem Statement

Urban intersections across India suffer from:

Severe traffic congestion

Frequent red-light violations

Rash and unsafe driving

Manual monitoring and static signal timing

Traditional traffic systems lack real-time awareness and automated analytics, leading to inefficient traffic flow and increased accident risk.

💡 Our Solution

We propose an AI-powered traffic intelligence system that processes traffic camera footage and extracts actionable insights using computer vision and tracking algorithms.

The system:

Detects and tracks vehicles across frames

Estimates queue length and congestion levels

Identifies red-light violations

Detects rash driving using motion analysis

Visualizes insights via an interactive dashboard

🚀 Key Features

🚗 Vehicle Detection using YOLOv8

🔄 Multi-Object Tracking using DeepSORT

🚧 Queue Length Estimation using region-based analytics

🚨 Red-Light Violation Detection via stop-line crossing logic

⚠ Rash Driving Detection using speed heuristics

📊 Dashboard with Live & Historical Analytics

🗂 Run History Storage for previous analyses

⚡ Performance Optimized using frame skipping and resizing

🧠 System Architecture (High Level)
Input Traffic Video
        ↓
Frame Sampling & Resizing
        ↓
YOLOv8 Vehicle Detection
        ↓
DeepSORT Multi-Object Tracking
        ↓
Analytics Engine
 (Queue | Violations | Speed)
        ↓
CSV & Summary Storage
        ↓
Streamlit Dashboard
 (Home | Live | History | About)

🛠 Tech Stack

Programming & Frameworks

Python 3.9

Streamlit

Computer Vision & AI

OpenCV

YOLOv8 (Ultralytics)

DeepSORT

Data & Visualization

Pandas

Matplotlib

📂 Project Structure
urban-traffic-intelligence/
│
├── backend/
│   └── process_video.py
│
├── pages/
│   ├── Home.py
│   ├── Live.py
│   ├── History.py
│   └── About.py
│
├── dashboard.py
├── requirements.txt
├── README.md
└── .gitignore

▶ How to Run Locally
conda create -n netrik python=3.9
conda activate netrik
pip install -r requirements.txt
streamlit run dashboard.py


Upload a traffic video (30–60 seconds recommended) through the dashboard to start analysis.

⚡ Performance Optimizations

To ensure fast processing:

Frame skipping (process every Nth frame)

Resolution downscaling

Lightweight YOLOv8n model

Single-pass analytics logging

This enables near real-time performance for traffic analysis.

📊 Outputs Generated

For every run:

traffic_log.csv → frame-wise analytics

summary.json → run-level insights

Annotated live preview frames

Example insights:

Total vehicles detected

Average queue length

Peak congestion period

Number of violations

📦 Deployment Note (Important)

This application performs real-time computer vision inference using OpenCV and YOLOv8, which requires a Python runtime and native dependencies.

Therefore:

❌ Cannot run on static platforms like GitHub Pages

✅ GitHub is used for code review and reproducibility

✅ Live execution is demonstrated via local/VM deployment and demo video

This is an intentional and correct engineering decision.

🎥 Demo & Submission

📹 Demo Video: (attached in hackathon submission)

💻 Source Code: GitHub Repository

📝 Proposal & Explanation: PDF / README

🏁 Final Note

This project emphasizes design clarity, correctness, explainability, and real-world relevance over heavy model tuning.
The goal is to demonstrate system-level thinking in solving traffic challenges using AI
Built for NETRIK National Hack 2026
Turning traffic data into actionable intelligence.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/174c2389-7eee-49d9-97f6-11369c5ffa07" />
<img width="1920" height="1080" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/30ed7a7d-28fd-40b0-bf52-eaccc5630b23" />
<img width="1920" height="1080" alt="Screenshot (4)" src="https://github.com/user-attachments/assets/64ac57c8-1e29-40a2-9a67-6068040d2fae" />
<img width="1920" height="1080" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/45c21487-15d7-4543-abef-1d7099596f9b" />
<img width="1920" height="1080" alt="Screenshot (6)" src="https://github.com/user-attachments/assets/78a288ab-644c-4c26-9a01-3ed0f1267639" />

![Uploading image.png…]()

