import os
import sys
import subprocess

# =================================================
# AUTO-INSTALL HELPER
# =================================================
def auto_install(pkg):
    try:
        print(f"[INFO] Installing missing package: {pkg}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
    except Exception as e:
        print(f"[FATAL] Failed to install {pkg}: {e}")
        sys.exit(1)

# =================================================
# SAFE IMPORT
# =================================================
try:
    from ultralytics import YOLO
except ImportError:
    auto_install("ultralytics")
    from ultralytics import YOLO

# =================================================
# BASE DIRECTORY (SCRIPT LOCATION, NOT CWD)
# =================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_YAML = os.path.join(BASE_DIR, "data.yaml")
IMAGES_TRAIN = os.path.join(BASE_DIR, "images", "train")
IMAGES_VAL = os.path.join(BASE_DIR, "images", "val")
LABELS_TRAIN = os.path.join(BASE_DIR, "labels", "train")
LABELS_VAL = os.path.join(BASE_DIR, "labels", "val")

# =================================================
# VALIDATION CHECKS
# =================================================
def fatal(msg):
    print(f"[FATAL] {msg}")
    sys.exit(1)

if not os.path.isfile(DATA_YAML):
    fatal(f"data.yaml not found at: {DATA_YAML}")

for p in [IMAGES_TRAIN, IMAGES_VAL, LABELS_TRAIN, LABELS_VAL]:
    if not os.path.isdir(p):
        fatal(f"Required directory missing: {p}")

# Check at least one label has content
label_files = [
    os.path.join(LABELS_TRAIN, f)
    for f in os.listdir(LABELS_TRAIN)
    if f.endswith(".txt")
]

if not label_files:
    fatal("No label files found in labels/train")

non_empty = False
for lf in label_files:
    try:
        if os.path.getsize(lf) > 0:
            non_empty = True
            break
    except:
        pass

if not non_empty:
    fatal("All label files are empty. Bounding boxes not annotated.")

print("[OK] Dataset structure verified")

# =================================================
# TRAIN YOLO26
# =================================================
try:
    print("[INFO] Loading YOLO26 COCO-pretrained model")
    model = YOLO("yolo26s.pt")   # COCO pretrained

    print("[INFO] Starting training (Auto + Truck)")

    model.train(
        data=DATA_YAML,
        epochs=50,
        imgsz=640,
        batch=8,
        patience=10,
        device=0,                # set -1 for CPU
        workers=4,
        project=os.path.join(BASE_DIR, "runs_indian"),
        name="yolo26_auto_truck",
        pretrained=True
    )

    print("[SUCCESS] Training completed")

except Exception as e:
    print("[FATAL] Training failed")
    print(e)
    sys.exit(1)

# =================================================
# POST-TRAIN MESSAGE
# =================================================
print("\n=================================================")
print(" Training finished successfully")
print(" Model saved at:")
print(f" {os.path.join(BASE_DIR, 'runs_indian', 'yolo26_auto_truck', 'weights', 'best.pt')}")
print("=================================================\n")
