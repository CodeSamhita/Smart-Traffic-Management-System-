import os
import sys
import subprocess

# -------------------------------------------------
# Auto install helper
# -------------------------------------------------
def auto_install(pkg):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
    except Exception as e:
        print(f"❌ Auto-install failed for {pkg}: {e}")
        sys.exit(1)

# -------------------------------------------------
# Safe imports
# -------------------------------------------------
try:
    from ultralytics import YOLO
except ImportError:
    auto_install("ultralytics")
    from ultralytics import YOLO

try:
    import cv2
except ImportError:
    auto_install("opencv-python")
    import cv2


# -------------------------------------------------
# Paths (EDIT ONLY THESE IF NEEDED)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "YOLO26x-obb.pt")
IMAGE_PATH = os.path.join(BASE_DIR, "image.jpg")
OUTPUT_PATH = os.path.join(BASE_DIR, "output_with_boxes.jpg")


# -------------------------------------------------
# Validate files
# -------------------------------------------------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")


# -------------------------------------------------
# Load model
# -------------------------------------------------
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"❌ Model load failed: {e}")
    sys.exit(1)


# -------------------------------------------------
# Run inference
# -------------------------------------------------
try:
    results = model(IMAGE_PATH, conf=0.25)
except Exception as e:
    print(f"❌ Inference failed: {e}")
    sys.exit(1)


# -------------------------------------------------
# Draw SQUARE (axis-aligned) boxes + labels
# -------------------------------------------------
try:
    image = cv2.imread(IMAGE_PATH)

    for r in results:
        boxes = r.boxes  # axis-aligned boxes
        names = r.names

        if boxes is None:
            continue

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            label = f"{names[cls_id]} {conf:.2f}"

            # Draw rectangle
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label
            cv2.putText(
                image,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.imwrite(OUTPUT_PATH, image)
    print(f"✅ Output saved: {OUTPUT_PATH}")

except Exception as e:
    print(f"❌ Drawing/saving failed: {e}")
    sys.exit(1)
