import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import math
import csv
import os

# ------------------------------
# Load YOLO model
# ------------------------------
model = YOLO("yolov8n.pt")

# ------------------------------
# Initialize DeepSORT tracker
# ------------------------------
tracker = DeepSort(max_age=30, n_init=3, max_iou_distance=0.7)

# ------------------------------
# Video input
# ------------------------------
video_path = "data/sample_video.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video")
    exit()

# ------------------------------
# Queue Region (ROI)
# ------------------------------
QUEUE_X1, QUEUE_Y1 = 100, 200
QUEUE_X2, QUEUE_Y2 = 500, 450

# ------------------------------
# Stop Line (Red Light)
# ------------------------------
STOP_LINE_Y = 300

# ------------------------------
# Tracking helpers
# ------------------------------
seen_vehicle_ids = set()
previous_positions = {}
previous_centers = {}
violated_ids = set()
rash_ids = set()

SPEED_THRESHOLD = 30

# ------------------------------
# Logging setup
# ------------------------------
os.makedirs("outputs", exist_ok=True)

log_file = open("outputs/traffic_log.csv", mode="w", newline="")
log_writer = csv.writer(log_file)

log_writer.writerow([
    "frame",
    "queue_count",
    "total_vehicles",
    "red_light_violations",
    "rash_driving"
])

frame_number = 0

print("Traffic Analysis running... Press 'q' to quit.")

# ------------------------------
# Main loop
# ------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break

    frame_number += 1

    results = model(frame, verbose=False)
    detections = []

    # --------------------------
    # YOLO detections
    # --------------------------
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        if class_name in ["car", "truck", "bus", "motorcycle"]:
            detections.append(
                ([x1, y1, x2 - x1, y2 - y1], confidence, class_name)
            )

    # --------------------------
    # Update tracker
    # --------------------------
    tracks = tracker.update_tracks(detections, frame=frame)

    queue_count = 0

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, w, h = map(int, track.to_ltrb())
        cx = l + w // 2
        cy = t + h // 2

        seen_vehicle_ids.add(track_id)

        # ----------------------
        # Red-light violation logic
        # ----------------------
        prev_y = previous_positions.get(track_id)
        previous_positions[track_id] = cy

        if prev_y is not None and prev_y < STOP_LINE_Y <= cy:
            violated_ids.add(track_id)

        # ----------------------
        # Rash driving detection
        # ----------------------
        prev_center = previous_centers.get(track_id)
        previous_centers[track_id] = (cx, cy)

        if prev_center is not None:
            px, py = prev_center
            distance = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
            if distance > SPEED_THRESHOLD:
                rash_ids.add(track_id)

        # ----------------------
        # Queue detection
        # ----------------------
        in_queue = QUEUE_X1 <= cx <= QUEUE_X2 and QUEUE_Y1 <= cy <= QUEUE_Y2
        if in_queue:
            queue_count += 1

        # ----------------------
        # Coloring priority
        # ----------------------
        if track_id in violated_ids:
            color = (0, 0, 255)
            label = f"ID {track_id} RED"
        elif track_id in rash_ids:
            color = (0, 165, 255)
            label = f"ID {track_id} RASH"
        elif in_queue:
            color = (0, 255, 255)
            label = f"ID {track_id}"
        else:
            color = (255, 0, 0)
            label = f"ID {track_id}"

        cv2.rectangle(frame, (l, t), (l + w, t + h), color, 2)
        cv2.putText(frame, label, (l, t - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # --------------------------
    # Draw queue region
    # --------------------------
    cv2.rectangle(frame, (QUEUE_X1, QUEUE_Y1),
                  (QUEUE_X2, QUEUE_Y2), (0, 255, 255), 2)
    cv2.putText(frame, "Queue Region",
                (QUEUE_X1, QUEUE_Y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # --------------------------
    # Draw stop line
    # --------------------------
    cv2.line(frame, (0, STOP_LINE_Y),
             (frame.shape[1], STOP_LINE_Y), (0, 0, 255), 2)
    cv2.putText(frame, "STOP LINE",
                (10, STOP_LINE_Y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # --------------------------
    # Display stats
    # --------------------------
    cv2.putText(frame, f"Queue Count: {queue_count}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.putText(frame, f"Total Vehicles: {len(seen_vehicle_ids)}", (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.putText(frame, f"Red-Light Violations: {len(violated_ids)}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(frame, f"Rash Driving: {len(rash_ids)}", (20, 135),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

    # --------------------------
    # Write CSV log
    # --------------------------
    log_writer.writerow([
        frame_number,
        queue_count,
        len(seen_vehicle_ids),
        len(violated_ids),
        len(rash_ids)
    ])

    cv2.imshow("Traffic Analysis System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Stopped by user")
        break

cap.release()
cv2.destroyAllWindows()
log_file.close()

print("Logs saved to outputs/traffic_log.csv")
