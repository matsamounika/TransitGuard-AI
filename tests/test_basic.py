"""
Unit tests for TransitGuard AI core modules.
Verifies configuration, SQLite database operations, and computer vision utilities.
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import APP_NAME, BASE_DIR, CONFIDENCE_THRESHOLD
from database import (
    init_db,
    insert_alert,
    get_alerts,
    update_alert_status,
    insert_maintenance_report,
    get_maintenance_reports,
    get_dashboard_metrics,
)
from detection import classify_category, draw_detection_boxes


def test_config_loaded():
    assert APP_NAME == "TransitGuard AI"
    assert BASE_DIR.exists()
    assert 0.0 < CONFIDENCE_THRESHOLD < 1.0


def test_database_operations():
    init_db()

    # 1. Test alert insertion
    alert_id = insert_alert(
        alert_type="Test Obstruction",
        zone="Test Platform Ramp",
        severity="Medium",
        description="Automated unit test alert",
        metadata={"test": True},
    )
    assert alert_id.startswith("ALT-")

    # 2. Test alert retrieval
    alerts = get_alerts(limit=5)
    assert len(alerts) > 0
    assert any(a["alert_id"] == alert_id for a in alerts)

    # 3. Test status update
    updated = update_alert_status(alert_id, "In Progress")
    assert updated is True

    # 4. Test maintenance report insertion
    mnt_id = insert_maintenance_report(
        facility_type="Escalator",
        location="West Gate",
        issue_description="Step grating damaged",
        priority="High",
    )
    assert mnt_id.startswith("MNT-")

    # 5. Test metrics calculation
    metrics = get_dashboard_metrics()
    assert "total_alerts" in metrics
    assert metrics["total_alerts"] >= 1


def test_detection_classification():
    assert classify_category(0, "person") == "Passenger"
    assert classify_category(28, "suitcase") == "Luggage / Potential Obstacle"
    assert classify_category(24, "backpack") == "Luggage / Potential Obstacle"
    assert classify_category(99, "clock") == "Station Object"


def test_drawing_boxes():
    img_rgb = np.zeros((100, 100, 3), dtype=np.uint8)
    dummy_detections = [{
        "bbox": [10, 10, 50, 50],
        "confidence": 0.85,
        "class_id": 28,
        "class_name": "suitcase",
        "category": "Luggage / Potential Obstacle",
    }]
    annotated = draw_detection_boxes(img_rgb, dummy_detections)
    assert annotated.shape == (100, 100, 3)
    assert np.any(annotated > 0)  # Drawing modified pixels
