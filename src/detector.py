import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

video_path = "data/sample_video.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video")
    exit()

print("Running YOLO on video... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break

    # Run detection on the frame
    results = model(frame, verbose=False)

    # Draw boxes
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = model.names[class_id]

        label = f"{class_name} {confidence:.2f}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    cv2.imshow("YOLO Video Detection", frame)

    # Press 'q' to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Stopped by user")
        break

cap.release()
cv2.destroyAllWindows()
