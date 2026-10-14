"""
TransitGuard AI - Home & System Overview
Main landing page for the Privacy-Preserving Edge AI Transit Hub Monitoring System.
"""

import sys
from pathlib import Path

# Ensure the root directory is on the python search path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from config import APP_NAME, APP_SUBTITLE, APP_VERSION, COLOR_PRIMARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER

# Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} - Edge AI for Transit Accessibility",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (Dark Navy, Electric Blue Accents, Clean Card Components)
st.markdown(
    f"""
    <style>
    .main {{
        background-color: #0B1120;
    }}
    .hero-container {{
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }}
    .hero-title {{
        font-size: 2.4rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }}
    .hero-subtitle {{
        font-size: 1.15rem;
        color: #94A3B8;
        margin-bottom: 1rem;
        line-height: 1.6;
    }}
    .feature-card {{
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.5rem;
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .feature-card:hover {{
        border-color: {COLOR_PRIMARY};
    }}
    .feature-icon {{
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }}
    .feature-title {{
        font-size: 1.2rem;
        font-weight: 700;
        color: #F1F5F9;
        margin-bottom: 0.5rem;
    }}
    .feature-desc {{
        font-size: 0.95rem;
        color: #94A3B8;
        line-height: 1.5;
    }}
    .status-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        background-color: rgba(16, 185, 129, 0.15);
        color: {COLOR_SUCCESS};
        border: 1px solid {COLOR_SUCCESS};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation and Metadata
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title(APP_NAME)
    st.caption(f"Prototype Version: **{APP_VERSION}**")
    st.markdown("---")
    st.markdown("### 🚦 System Status")
    st.markdown(
        f'<span class="status-badge">● Edge Inference Ready</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.info(
        "🔒 **Local Edge Architecture**\n\n"
        "All visual processing runs strictly on your local machine. "
        "No imagery is transmitted to external cloud APIs or remote servers."
    )
    st.markdown("---")
    st.markdown("### 📌 Hackathon Quick Guide")
    st.markdown(
        """
        1. **AI Detection**: Upload & inspect station objects
        2. **Ramp Monitoring**: Wheelchair obstruction check
        3. **Crowd Monitoring**: Density & bottleneck detection
        4. **Alerts**: Real-time event log & dispatch
        5. **Maintenance**: Manual station issues reporting
        6. **Privacy Centre**: Anonymization & ethics
        """
    )

# Hero Section
st.markdown(
    f"""
    <div class="hero-container">
        <div class="hero-title">🛡️ {APP_NAME}</div>
        <div class="hero-subtitle">{APP_SUBTITLE}</div>
        <p style="color: #CBD5E1; margin: 0; font-size: 1rem;">
            Empowering wheelchair users, visually impaired passengers, and elderly citizens 
            by delivering automated, micro-accessibility barrier detection right at the transit edge.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Core Problem & Innovation Grid
st.subheader("💡 The Problem & Edge AI Solution")
col_prob, col_sol = st.columns(2)

with col_prob:
    st.error("### ⚠️ The Micro-Accessibility Gap")
    st.write(
        """
        - **Wheelchair Ramps Blocked**: Luggage, carts, and unattended boxes frequently obstruct ramps unnoticed.
        - **Bottlenecks & Crowds**: Unexpected platform bottlenecks trap passengers with limited mobility.
        - **Cloud Latency & High Bandwidth**: Transmitting 24/7 CCTV feeds to the cloud is expensive and introduces latency.
        - **Privacy Concerns**: Continuous public surveillance risks passenger biometric tracking and identity compromise.
        """
    )

with col_sol:
    st.success("### ⚡ The TransitGuard Innovation")
    st.write(
        """
        - **Edge-First Computation**: Lightweight YOLO models run locally on station edge hardware or laptops.
        - **Geometric Overlap Analysis**: Geometric intersection-over-union heuristics flag ramp obstacles without claiming certified infallibility.
        - **Privacy by Design**: Zero passenger facial recognition, zero biometric tracking, and optional OpenCV face-blurring.
        - **Actionable Micro-Alerts**: Fast dispatch alerts for ground staff to clear accessibility barriers promptly.
        """
    )

st.markdown("---")

# Feature Highlights Cards
st.subheader("🚀 System Capabilities")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">AI Object Detection</div>
            <div class="feature-desc">
                Pretrained Ultralytics YOLO inference detects luggage, backpacks, wheelchairs, 
                and people with confidence scores and downloadable annotated visual proofs.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">♿</div>
            <div class="feature-title">Ramp Obstruction Alert</div>
            <div class="feature-desc">
                Interactive Region of Interest (ROI) overlap calculation alerts staff when suitcases or 
                boxes block designated accessible ramps beyond configurable overlap thresholds.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">👥</div>
            <div class="feature-title">Crowd Density Monitoring</div>
            <div class="feature-desc">
                Monitors passenger density across critical transit zones (escalator landings, ticketing, boarding gates)
                to prevent dangerous crowd crushing.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
c4, c5, c6 = st.columns(3)

with c4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Privacy Protection</div>
            <div class="feature-desc">
                No identity tracking, no passenger profiling, minimal metadata storage in local SQLite,
                and built-in OpenCV Gaussian face blurring.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c5:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔔</div>
            <div class="feature-title">Alert Management & DB</div>
            <div class="feature-desc">
                Persistent SQLite alert log tracking timestamp, severity, station zone, and workflow statuses 
                (Pending, In Progress, Resolved).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c6:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🛠️</div>
            <div class="feature-title">Maintenance Reporting</div>
            <div class="feature-desc">
                Staff portal to report broken escalators, damaged tactile paving, or out-of-order elevators,
                distinguished from automated AI alerts.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Quick Diagnostic / System Info Check
st.subheader("🖥️ Edge Environment Diagnostic")
d1, d2, d3, d4 = st.columns(4)
with d1:
    st.metric("Inference Engine", "Ultralytics YOLO")
with d2:
    st.metric("Database Backend", "SQLite 3 (Local)")
with d3:
    st.metric("Processing Node", "Edge Client / Laptop")
with d4:
    st.metric("External Cloud Dependency", "None (100% Offline)")

st.caption("TransitGuard AI Prototype | Designed for AI Hackathon 2026")
