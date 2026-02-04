from ultralytics import YOLO
import cv2

# Target resolution: 480p
TARGET_WIDTH = 854
TARGET_HEIGHT = 480

# Load YOLOv8 model
model = YOLO("yolo26x.pt")

# Relevant classes for Indian traffic
VALID_CLASSES = ["motorcycle", "car", "bus", "truck", "person"]

def detect_vehicles(video_path):
    cap = cv2.VideoCapture(video_path)
    detections_per_frame = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to 480p
        frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))

        results = model(frame, conf=0.4, verbose=False)
        frame_data = []

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]

            if cls_name in VALID_CLASSES:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                frame_data.append({
                    "class": cls_name,
                    "bbox": (x1, y1, x2, y2),
                    "center": (cx, cy),
                    "frame_height": frame.shape[0]
                })

        detections_per_frame.append(frame_data)

        # Visualization
        annotated = results[0].plot()
        cv2.imshow("Traffic Detection (480p)", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return detections_per_frame
