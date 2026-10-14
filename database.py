"""
TransitGuard AI - Database Module
SQLite persistent storage for AI incident alerts and manual maintenance reports.
Thread-safe, lightweight, and operates 100% locally on the edge device.
"""

import sqlite3
import json
from datetime import datetime
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any

from config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    """
    Establish a connection to the local SQLite database.
    Configures row_factory to sqlite3.Row for convenient dict-style column access.
    """
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DATABASE_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Initialize SQLite tables for alerts and maintenance logs if they don't already exist.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. AI & Accessibility Alerts Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_id TEXT UNIQUE NOT NULL,
                alert_type TEXT NOT NULL,
                zone TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                metadata TEXT
            )
            """
        )

        # 2. Manual Station Maintenance Reports Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS maintenance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id TEXT UNIQUE NOT NULL,
                facility_type TEXT NOT NULL,
                location TEXT NOT NULL,
                issue_description TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Reported',
                timestamp TEXT NOT NULL,
                reported_by TEXT DEFAULT 'Station Staff'
            )
            """
        )

        # Indexes for rapid filtering and dashboard generation
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_maintenance_status ON maintenance(status);")

        conn.commit()


def insert_alert(
    alert_type: str,
    zone: str,
    severity: str,
    description: str,
    status: str = "Pending",
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Insert a new alert into SQLite and return its unique identifier.
    
    Args:
        alert_type: Type of alert (e.g. 'Ramp Obstruction', 'Platform Overcrowding', 'Unattended Baggage')
        zone: Station location (e.g. 'Platform 1 Accessible Ramp', 'East Gate Concourse')
        severity: 'Low', 'Medium', 'High', or 'Critical'
        description: Human-readable explanation of the detected event
        status: Initial workflow state ('Pending', 'In Progress', 'Resolved')
        metadata: Optional dictionary with bounding box stats, overlap %, or crowd counts
    """
    init_db()
    
    # Generate human-friendly ID like ALT-20261014-A1B2
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_code = datetime.now().strftime("%Y%m%d")
    short_suffix = uuid.uuid4().hex[:4].upper()
    alert_id = f"ALT-{date_code}-{short_suffix}"

    meta_str = json.dumps(metadata) if metadata else None

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO alerts (alert_id, alert_type, zone, timestamp, severity, description, status, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (alert_id, alert_type, zone, timestamp_str, severity, description, status, meta_str),
        )
        conn.commit()

    return alert_id


def get_alerts(
    limit: int = 100,
    status: Optional[str] = None,
    alert_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve alerts ordered by most recent first.
    """
    init_db()
    query = "SELECT * FROM alerts WHERE 1=1"
    params = []

    if status and status != "All":
        query += " AND status = ?"
        params.append(status)

    if alert_type and alert_type != "All":
        query += " AND alert_type = ?"
        params.append(alert_type)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def update_alert_status(alert_id: str, new_status: str) -> bool:
    """
    Update workflow status for an alert ('Pending', 'In Progress', 'Resolved').
    """
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alerts SET status = ? WHERE alert_id = ?",
            (new_status, alert_id),
        )
        conn.commit()
        return cursor.rowcount > 0


def insert_maintenance_report(
    facility_type: str,
    location: str,
    issue_description: str,
    priority: str,
    reported_by: str = "Station Staff",
    status: str = "Reported",
) -> str:
    """
    Log a manual physical infrastructure maintenance issue.
    """
    init_db()
    date_code = datetime.now().strftime("%Y%m%d")
    short_suffix = uuid.uuid4().hex[:4].upper()
    report_id = f"MNT-{date_code}-{short_suffix}"
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO maintenance (report_id, facility_type, location, issue_description, priority, status, timestamp, reported_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (report_id, facility_type, location, issue_description, priority, status, timestamp_str, reported_by),
        )
        conn.commit()

    return report_id


def get_maintenance_reports(limit: int = 100, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve manual maintenance reports.
    """
    init_db()
    query = "SELECT * FROM maintenance WHERE 1=1"
    params = []

    if status and status != "All":
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def update_maintenance_status(report_id: str, new_status: str) -> bool:
    """
    Update status of a maintenance report ('Reported', 'Under Repair', 'Fixed').
    """
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE maintenance SET status = ? WHERE report_id = ?",
            (new_status, report_id),
        )
        conn.commit()
        return cursor.rowcount > 0


def get_dashboard_metrics() -> Dict[str, int]:
    """
    Calculate summary metrics for KPIs and charts across the system.
    """
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM alerts;")
        total_alerts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'Pending';")
        pending_alerts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'In Progress';")
        in_progress_alerts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'Resolved';")
        resolved_alerts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity IN ('High', 'Critical');")
        high_severity_alerts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts WHERE alert_type = 'Ramp Obstruction';")
        ramp_alerts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts WHERE alert_type = 'Platform Overcrowding';")
        crowd_alerts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM maintenance;")
        total_maintenance = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM maintenance WHERE status != 'Fixed';")
        open_maintenance = cursor.fetchone()[0]

    return {
        "total_alerts": total_alerts,
        "pending_alerts": pending_alerts,
        "in_progress_alerts": in_progress_alerts,
        "resolved_alerts": resolved_alerts,
        "high_severity_alerts": high_severity_alerts,
        "ramp_alerts": ramp_alerts,
        "crowd_alerts": crowd_alerts,
        "total_maintenance": total_maintenance,
        "open_maintenance": open_maintenance,
    }


def seed_demo_data_if_empty() -> None:
    """
    Seeds a few realistic transit events if the database has zero records.
    Ensures judges immediately see realistic operational history during demonstration.
    """
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alerts;")
        count = cursor.fetchone()[0]
        if count == 0:
            insert_alert(
                alert_type="Ramp Obstruction",
                zone="Platform 1 Wheelchair Ramp",
                severity="High",
                description="Unattended suitcase (confidence 87%) detected in designated wheelchair ramp pathway (overlap: 28%).",
                status="Pending",
                metadata={"overlap_ratio": 0.28, "class": "suitcase", "confidence": 0.87},
            )
            insert_alert(
                alert_type="Platform Overcrowding",
                zone="Central Concourse Escalator Landing",
                severity="Critical",
                description="High passenger density detected: 11 persons in monitoring zone (threshold: 7). Risk of escalator exit bottleneck.",
                status="In Progress",
                metadata={"passenger_count": 11, "threshold": 7, "density_level": "High"},
            )
            insert_alert(
                alert_type="Ramp Obstruction",
                zone="South Transit Gate Ramp",
                severity="Medium",
                description="Backpack placed at ramp base. Path clearance restricted to 65%.",
                status="Resolved",
                metadata={"overlap_ratio": 0.18, "class": "backpack", "confidence": 0.79},
            )

        cursor.execute("SELECT COUNT(*) FROM maintenance;")
        mnt_count = cursor.fetchone()[0]
        if mnt_count == 0:
            insert_maintenance_report(
                facility_type="Escalator",
                location="North Platform 2 Upward Escalator",
                issue_description="Comb plate tooth cracked; potential snagging hazard for walking canes and wheel rims.",
                priority="Critical",
                reported_by="Platform Lead Officer",
                status="Under Repair",
            )
            insert_maintenance_report(
                facility_type="Tactile Paving",
                location="Main Ticket Hall Tactile Guidance Path",
                issue_description="Loose tactile tiles near ticketing machine 4; guidance path disoriented.",
                priority="Medium",
                reported_by="Accessibility Inspector",
                status="Reported",
            )
