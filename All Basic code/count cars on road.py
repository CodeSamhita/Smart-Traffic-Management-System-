# ----------------------------------------------------
# Safe imports with auto-install (self-healing)
# ----------------------------------------------------
import sys
import subprocess

def safe_import(module_name, pip_name=None):
    try:
        return __import__(module_name)
    except ImportError:
        pkg = pip_name if pip_name else module_name
        print(f"[INFO] '{module_name}' not found. Installing '{pkg}'...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg],
                stdout=subprocess.DEVNULL
            )
            return __import__(module_name)
        except Exception as e:
            raise RuntimeError(f"Failed to install {pkg}: {e}")

# Core dependencies
cv2 = safe_import("cv2", "opencv-python")
os = safe_import("os")
ultralytics = safe_import("ultralytics")
YOLO = ultralytics.YOLO

# ----------------------------------------------------
# Load YOLO26-X model safely
# ----------------------------------------------------
try:
    model = YOLO("yolo26x.pt")
except Exception as e:
    raise RuntimeError(f"Failed to load YOLO model: {e}")

# ----------------------------------------------------
# Resolve image path safely
# ----------------------------------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(BASE_DIR, "images", "road6.jpg")
except NameError:
    raise RuntimeError(
        "__file__ is not defined. Run this script from a .py file, not a notebook."
    )

# ----------------------------------------------------
# Load input image safely
# ----------------------------------------------------
try:
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        raise FileNotFoundError
except FileNotFoundError:
    raise FileNotFoundError(f"Image not found or unreadable at: {IMAGE_PATH}")

# ----------------------------------------------------
# Run high-accuracy inference safely
# ----------------------------------------------------
try:
    results = model.predict(
        source=image,
        conf=0.1,
        iou=0.55,
        imgsz=1280,
        device=0,        # change to "cpu" if CUDA is unavailable
        verbose=False
    )
except Exception as e:
    raise RuntimeError(f"YOLO inference failed: {e}")

# ----------------------------------------------------
# COCO vehicle class IDs (Indian traffic mapping)
# ----------------------------------------------------
VEHICLE_CLASSES = {
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

# ----------------------------------------------------
# Initialize counters
# ----------------------------------------------------
vehicle_stats = {
    "bicycle": 0,
    "car": 0,
    "motorcycle": 0,
    "bus": 0,
    "truck": 0
}
vehicle_count = 0

# ----------------------------------------------------
# Process detection results safely
# ----------------------------------------------------
try:
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            if cls_id in VEHICLE_CLASSES:
                vehicle_type = VEHICLE_CLASSES[cls_id]
                vehicle_stats[vehicle_type] += 1
                vehicle_count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"{vehicle_type} {conf:.2f}"

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    image, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 2
                )
except Exception as e:
    raise RuntimeError(f"Error while processing detections: {e}")

# ----------------------------------------------------
# Overlay statistics
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
# Display output safely
# ----------------------------------------------------
try:
    cv2.imshow("YOLO26-X Vehicle Detection (Classified Count)", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except cv2.error:
    print("[WARN] OpenCV GUI not supported. Saving output image instead.")
    output_path = os.path.join(BASE_DIR, "output_detected.jpg")
    cv2.imwrite(output_path, image)
    print(f"[INFO] Output saved to: {output_path}")
