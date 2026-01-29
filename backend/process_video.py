import cv2
import csv
import math
import os
import json
from datetime import datetime

from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# ======================================================
# LOAD MODEL ONCE (CRITICAL PERFORMANCE OPTIMIZATION)
# ======================================================
MODEL = YOLO("yolov8n.pt")
TRACKER = DeepSort(max_age=30)

# ======================================================
# MAIN FUNCTION
# ======================================================
def process_video(video_path):
    # ================= CONFIG (OPTIMIZED) =================
    FRAME_SKIP = 4                      # faster than 3
    RESIZE_WIDTH, RESIZE_HEIGHT = 512, 288
    SPEED_THRESHOLD = 30

    QUEUE_X1, QUEUE_Y1 = 100, 200
    QUEUE_X2, QUEUE_Y2 = 500, 450
    STOP_LINE_Y = 300

    # ================= HISTORY =================
    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    run_dir = os.path.join("history", run_id)
    os.makedirs(run_dir, exist_ok=True)

    output_csv = os.path.join(run_dir, "traffic_log.csv")
    summary_path = os.path.join(run_dir, "summary.json")
    live_frame_path = "latest_frame.jpg"

    cap = cv2.VideoCapture(video_path)

    raw_frame_id = 0
    processed_frame_id = 0

    seen = set()
    violated = set()
    rash = set()
    prev_pos = {}
    prev_center = {}

    # ================= CSV SETUP =================
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "frame",
            "queue_count",
            "red_light_violations",
            "rash_driving",
            "total_vehicles"
        ])

        # ================= MAIN LOOP =================
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            raw_frame_id += 1
            if raw_frame_id % FRAME_SKIP != 0:
                continue

            processed_frame_id += 1

            frame = cv2.resize(frame, (RESIZE_WIDTH, RESIZE_HEIGHT))

            results = MODEL(frame, verbose=False)
            detections = []

            # -------- YOLO DETECTIONS --------
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                name = MODEL.names[cls]
                conf = float(box.conf[0])

                if name in ["car", "bus", "truck", "motorcycle"]:
                    detections.append(([x1, y1, x2 - x1, y2 - y1], conf, name))

            tracks = TRACKER.update_tracks(detections, frame=frame)
            queue_count = 0

            for t in tracks:
                if not t.is_confirmed():
                    continue

                tid = t.track_id
                l, t_, w, h = map(int, t.to_ltrb())
                cx, cy = l + w // 2, t_ + h // 2

                seen.add(tid)

                # -------- RED-LIGHT VIOLATION --------
                py = prev_pos.get(tid)
                prev_pos[tid] = cy
                if py is not None and py < STOP_LINE_Y <= cy:
                    violated.add(tid)

                # -------- RASH DRIVING --------
                pc = prev_center.get(tid)
                prev_center[tid] = (cx, cy)
                if pc and math.dist(pc, (cx, cy)) > SPEED_THRESHOLD:
                    rash.add(tid)

                # -------- QUEUE COUNT --------
                if QUEUE_X1 <= cx <= QUEUE_X2 and QUEUE_Y1 <= cy <= QUEUE_Y2:
                    queue_count += 1

                # -------- DRAW (LIVE PREVIEW) --------
                cv2.rectangle(frame, (l, t_), (l + w, t_ + h), (0, 255, 0), 2)

            # Save live preview frame
            if processed_frame_id % 10 == 0:
                cv2.imwrite(live_frame_path, frame)

            # -------- CSV LOG --------
            writer.writerow([
                processed_frame_id,
                queue_count,
                len(violated),
                len(rash),
                len(seen)
            ])

    cap.release()

    # ================= SUMMARY =================
    summary = {
        "run_id": run_id,
        "processed_at": datetime.now().isoformat(),
        "total_vehicles": len(seen),
        "red_light_violations": len(violated),
        "rash_driving": len(rash),
        "frames_processed": processed_frame_id
    }

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)

    return run_dir
