import cv2
import os
from ultralytics import YOLO

# ----------------------------------------------------
# Load YOLO26-X model (extra-large, accuracy-first)
# ----------------------------------------------------
model = YOLO("yolo26x.pt")

# ----------------------------------------------------
# Resolve image path safely (independent of run folder)
# ----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "images", "road6.jpg")

# Load input image
image = cv2.imread(IMAGE_PATH)
if image is None:
    raise FileNotFoundError(f"Image not found at: {IMAGE_PATH}")

# ----------------------------------------------------
# Run high-accuracy inference
# NOTE:
# - conf is kept low to avoid missing vehicles
# - imgsz is high to improve small-object detection
# - device is CPU because CUDA is not available
# ----------------------------------------------------
results = model.predict(
    source=image,
    conf=0.1,          # lower confidence → fewer missed vehicles
    iou=0.55,          # IoU threshold for box filtering
    imgsz=1280,        # higher resolution → better accuracy
    #device="cpu",      # CPU-only system
    device=0,         # use this ONLY if CUDA GPU is available
    verbose=False
)

# ----------------------------------------------------
# COCO vehicle class IDs (mapped to Indian traffic)
# ----------------------------------------------------
VEHICLE_CLASSES = {
    1: "bicycle",        # cycles
    2: "car",            # cars, vans
    3: "motorcycle",     # bikes, scooters
    5: "bus",            # buses, school buses
    7: "truck"           # trucks, tempos, tractors
}

# ----------------------------------------------------
# Initialize class-wise vehicle counters
# ----------------------------------------------------
vehicle_stats = {
    "bicycle": 0,
    "car": 0,
    "motorcycle": 0,
    "bus": 0,
    "truck": 0
}

# Total vehicle counter
vehicle_count = 0

# ----------------------------------------------------
# Process detection results
# ----------------------------------------------------
for r in results:
    for box in r.boxes:
        cls_id = int(box.cls[0])     # detected class ID
        conf = float(box.conf[0])    # confidence score

        # Check if detected object is a vehicle
        if cls_id in VEHICLE_CLASSES:
            vehicle_type = VEHICLE_CLASSES[cls_id]

            # Update counts
            vehicle_stats[vehicle_type] += 1
            vehicle_count += 1

            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw bounding box and label
            label = f"{vehicle_type} {conf:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                image,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

# ----------------------------------------------------
# Display total vehicle count
# ----------------------------------------------------
cv2.putText(
    image,
    f"Total Vehicles: {vehicle_count}",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 0, 255),
    2
)

# ----------------------------------------------------
# Display class-wise vehicle counts
# ----------------------------------------------------
y_offset = 80
for v_type, count in vehicle_stats.items():
    cv2.putText(
        image,
        f"{v_type.capitalize()}: {count}",
        (20, y_offset),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2
    )
    y_offset += 30

# ----------------------------------------------------
# Show final output
# ----------------------------------------------------
cv2.imshow("YOLO26-X Vehicle Detection (Classified Count)", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
