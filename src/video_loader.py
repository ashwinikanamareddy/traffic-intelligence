import cv2

video_path = "data/sample_video.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video file")
    exit()

print("Playing video... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break

    cv2.imshow("Video Playback", frame)

    # waitKey(25) controls playback speed (25 ms ~ 40 FPS)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("Stopped by user")
        break

cap.release()
cv2.destroyAllWindows()
