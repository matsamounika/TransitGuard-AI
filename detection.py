"""
TransitGuard AI - Computer Vision & YOLO Detection Engine
Handles lightweight pretrained YOLO inference, CPU optimization,
bounding-box visualization, and object classification for transit environments.
"""

import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union
import numpy as np
from PIL import Image
import cv2

from config import DEFAULT_MODEL_NAME, CONFIDENCE_THRESHOLD, CLASS_PERSON, LUGGAGE_CLASSES


# In-memory model cache for non-Streamlit execution or fallbacks
_MODEL_CACHE: Dict[str, Any] = {}


def load_yolo_model(model_name: str = DEFAULT_MODEL_NAME):
    """
    Load a pretrained YOLO model (default: yolov8n.pt ~6MB).
    Implements caching and handles missing weights / download errors gracefully.
    """
    global _MODEL_CACHE
    if model_name in _MODEL_CACHE:
        return _MODEL_CACHE[model_name]

    try:
        from ultralytics import YOLO
    except ImportError as e:
        raise ImportError(
            "The 'ultralytics' package is not installed. "
            "Please run: pip install ultralytics"
        ) from e

    try:
        # Load or download model; runs lightweight on laptop CPU
        model = YOLO(model_name)
        _MODEL_CACHE[model_name] = model
        return model
    except Exception as e:
        raise RuntimeError(
            f"Failed to load YOLO model '{model_name}'. "
            "If this is your first run without internet access, "
            "please connect to download the lightweight yolov8n weights (~6MB), "
            f"or place 'yolov8n.pt' directly in the project directory. Error: {str(e)}"
        )


def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
    """Convert PIL Image (RGB) to OpenCV format (BGR)."""
    rgb_array = np.array(pil_image.convert("RGB"))
    return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)


def cv2_to_pil(cv2_image: np.ndarray) -> Image.Image:
    """Convert OpenCV format (BGR) to PIL Image (RGB)."""
    rgb_array = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_array)


def classify_category(class_id: int, class_name: str) -> str:
    """
    Categorize detected objects for transit hub accessibility context.
    """
    if class_id == CLASS_PERSON or class_name.lower() == "person":
        return "Passenger"
    elif class_id in LUGGAGE_CLASSES or class_name.lower() in ["suitcase", "backpack", "handbag"]:
        return "Luggage / Potential Obstacle"
    elif class_name.lower() in ["bicycle", "motorcycle", "cart"]:
        return "Wheeled Vehicle"
    else:
        return "Station Object"


def draw_detection_boxes(
    image_rgb: np.ndarray,
    detections: List[Dict[str, Any]],
    line_thickness: int = 2,
) -> np.ndarray:
    """
    Draw modern, high-contrast bounding boxes and label tags onto an image.
    Works directly with RGB numpy array and returns annotated RGB numpy array.
    """
    annotated = image_rgb.copy()
    h, w, _ = annotated.shape

    # Color palette for detection classes (RGB format)
    COLOR_PASSENGER = (59, 130, 246)       # Vibrant Blue
    COLOR_OBSTACLE = (239, 68, 68)        # Crimson Red
    COLOR_OTHER = (16, 185, 129)          # Emerald Green

    for det in detections:
        box = det["bbox"]
        x1, y1, x2, y2 = [int(v) for v in box]
        class_name = det["class_name"]
        conf = det["confidence"]
        category = det["category"]

        # Clamp coordinates to image boundaries
        x1 = max(0, min(x1, w - 1))
        y1 = max(0, min(y1, h - 1))
        x2 = max(0, min(x2, w - 1))
        y2 = max(0, min(y2, h - 1))

        if category == "Passenger":
            box_color = COLOR_PASSENGER
        elif category == "Luggage / Potential Obstacle":
            box_color = COLOR_OBSTACLE
        else:
            box_color = COLOR_OTHER

        # Draw bounding rectangle
        cv2.rectangle(annotated, (x1, y1), (x2, y2), box_color, line_thickness)

        # Build label text: e.g. "Suitcase 88%"
        label_text = f"{class_name.capitalize()} {int(conf * 100)}%"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1

        (text_w, text_h), baseline = cv2.getTextSize(label_text, font, font_scale, font_thickness)

        # Draw label background chip
        chip_y1 = max(0, y1 - text_h - baseline - 6)
        chip_y2 = y1
        chip_x1 = x1
        chip_x2 = min(w, x1 + text_w + 10)

        cv2.rectangle(annotated, (chip_x1, chip_y1), (chip_x2, chip_y2), box_color, -1)
        # White text inside chip
        cv2.putText(
            annotated,
            label_text,
            (chip_x1 + 5, chip_y2 - baseline - 2),
            font,
            font_scale,
            (255, 255, 255),
            font_thickness,
            lineType=cv2.LINE_AA,
        )

    return annotated


def run_yolo_detection(
    image_input: Union[Image.Image, np.ndarray, str, Path],
    conf_threshold: float = CONFIDENCE_THRESHOLD,
    model_name: str = DEFAULT_MODEL_NAME,
    filter_classes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Execute real pretrained YOLO inference on an input image.
    
    Returns structured results:
    - detections: list of dicts with bbox [x1, y1, x2, y2], conf, class_id, class_name, category
    - counts: dict of counts per class
    - annotated_image: RGB numpy array
    - original_image: RGB numpy array
    - inference_time_ms: execution speed in ms
    - passengers_count: int
    - obstacles_count: int
    """
    # 1. Normalize image into RGB numpy array
    if isinstance(image_input, (str, Path)):
        pil_img = Image.open(str(image_input)).convert("RGB")
        original_rgb = np.array(pil_img)
    elif isinstance(image_input, Image.Image):
        original_rgb = np.array(image_input.convert("RGB"))
    elif isinstance(image_input, np.ndarray):
        if len(image_input.shape) == 2:
            original_rgb = cv2.cvtColor(image_input, cv2.COLOR_GRAY2RGB)
        elif image_input.shape[2] == 4:
            original_rgb = cv2.cvtColor(image_input, cv2.COLOR_RGBA2RGB)
        else:
            original_rgb = image_input.copy()
    else:
        raise ValueError("Unsupported image input type.")

    # 2. Load model
    model = load_yolo_model(model_name)

    # 3. Perform prediction on CPU
    start_time = time.perf_counter()
    results = model.predict(
        source=original_rgb,
        conf=conf_threshold,
        device="cpu",
        verbose=False,
    )
    inference_time_ms = round((time.perf_counter() - start_time) * 1000, 1)

    detections: List[Dict[str, Any]] = []
    class_counts: Dict[str, int] = {}
    passengers_count = 0
    obstacles_count = 0

    # 4. Parse detected boxes
    if results and len(results) > 0:
        first_res = results[0]
        boxes = first_res.boxes

        if boxes is not None:
            for box in boxes:
                coords = box.xyxy[0].cpu().numpy().tolist()  # [x1, y1, x2, y2]
                confidence = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                class_name = model.names.get(class_id, f"class_{class_id}")

                category = classify_category(class_id, class_name)

                # Filter if user selected a subset of classes
                if filter_classes and class_name.lower() not in [c.lower() for c in filter_classes]:
                    continue

                detections.append({
                    "bbox": [round(c, 1) for c in coords],
                    "confidence": round(confidence, 3),
                    "class_id": class_id,
                    "class_name": class_name,
                    "category": category,
                })

                class_counts[class_name] = class_counts.get(class_name, 0) + 1
                if category == "Passenger":
                    passengers_count += 1
                elif category == "Luggage / Potential Obstacle":
                    obstacles_count += 1

    # 5. Render annotated output image
    annotated_rgb = draw_detection_boxes(original_rgb, detections)

    return {
        "detections": detections,
        "counts": class_counts,
        "total_detections": len(detections),
        "passengers_count": passengers_count,
        "obstacles_count": obstacles_count,
        "annotated_image": annotated_rgb,
        "original_image": original_rgb,
        "inference_time_ms": inference_time_ms,
        "image_size": (original_rgb.shape[1], original_rgb.shape[0]),  # (width, height)
    }
