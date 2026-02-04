import os
import random
import shutil
import sys

# -------------------------------------------------
# ABSOLUTE BASE DIR (script location, not cwd)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUTO_DIR = os.path.join(BASE_DIR, "Auto")
TRUCK_DIR = os.path.join(BASE_DIR, "Truck")

TRAIN_SPLIT = 0.8
IMAGE_EXTS = (".jpg", ".jpeg", ".png")

CLASS_MAP = {
    "Auto": 0,
    "Truck": 1
}

# -------------------------------------------------
# SAFETY CHECK (IMPORTANT)
# -------------------------------------------------
if not os.path.isdir(AUTO_DIR):
    print(f"❌ Auto folder not found: {AUTO_DIR}")
    sys.exit(1)

if not os.path.isdir(TRUCK_DIR):
    print(f"❌ Truck folder not found: {TRUCK_DIR}")
    sys.exit(1)
