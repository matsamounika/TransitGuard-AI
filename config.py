"""
TransitGuard AI - System Configuration
Centralized settings, constants, and paths for the Edge AI Accessibility platform.
"""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "transitguard.db"
SAMPLE_IMAGES_DIR = BASE_DIR / "sample_images"
ASSETS_DIR = BASE_DIR / "assets"

# Application Metadata
APP_NAME = "TransitGuard AI"
APP_SUBTITLE = "Privacy-Preserving Edge AI for Micro-Accessibility and Safety in Public Transit Hubs"
APP_VERSION = "0.8.0-prototype"

# YOLO Model Settings
# yolov8n is an ultra-lightweight (~6MB) pretrained model ideal for laptop edge inference
DEFAULT_MODEL_NAME = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.35

# COCO Class IDs of interest for Transit Accessibility
# 0: person
# 24: backpack, 26: handbag, 28: suitcase
CLASS_PERSON = 0
LUGGAGE_CLASSES = {
    24: "backpack",
    26: "handbag",
    28: "suitcase",
    1: "bicycle",
    56: "chair",
}

# Micro-Accessibility & Obstruction Parameters
# Overlap ratio between object bounding box and ramp ROI to trigger alert
DEFAULT_OBSTRUCTION_OVERLAP_THRESHOLD = 0.15  # 15% overlap triggers possible obstruction

# Crowd Density Boundaries (demonstration thresholds)
DEFAULT_CROWD_THRESHOLDS = {
    "low": 3,       # 0 to 3 people: Low / Normal
    "moderate": 7,  # 4 to 7 people: Moderate
    # > 7 people: High / Overcrowded Alert
}

# UI Color Palette (Hex Codes)
COLOR_SUCCESS = "#10B981"  # Emerald Green (Normal / Clear)
COLOR_WARNING = "#F59E0B"  # Amber Orange (Warning / Moderate)
COLOR_DANGER = "#EF4444"   # Crimson Red (Critical / Obstruction / High Crowd)
COLOR_PRIMARY = "#3B82F6"  # Electric Blue (Highlights & Accent)
COLOR_NAVY_BG = "#0B1120"  # Deep Navy Slate (Background)
COLOR_CARD_BG = "#1E293B"  # Card / Surface Slate
