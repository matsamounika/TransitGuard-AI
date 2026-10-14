"""
TransitGuard AI - Module 3: Crowd Density Monitoring
Monitors passenger density within transit boarding zones and platforms.
"""

import streamlit as st

st.set_page_config(page_title="Crowd Monitoring - TransitGuard", page_icon="👥", layout="wide")

st.title("👥 Module 3: Crowd Density Monitoring")
st.markdown("Automated passenger counting within platform zones to avoid bottlenecks.")

st.info("⚡ **Stage 1 Active**: Passenger counting and configurable density thresholds will be implemented in **Stage 4**.")

st.markdown("""
### Upcoming Capabilities:
- Platform zone marking
- Object centroid filtering for passenger counts
- Dynamic threshold adjustment (Low, Moderate, High)
- Overcrowding warning indicators
""")
