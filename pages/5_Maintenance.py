"""
TransitGuard AI - Module 7: Manual Maintenance Reporting
Allows staff to log physical infrastructure faults not detectable by camera.
"""

import streamlit as st

st.set_page_config(page_title="Maintenance - TransitGuard", page_icon="🛠️", layout="wide")

st.title("🛠️ Module 7: Manual Maintenance Reporting")
st.markdown("Ground staff portal for reporting broken escalators, damaged ramps, and physical barriers.")

st.info("⚡ **Stage 1 Active**: Form submission and SQLite storage will be implemented in **Stage 6**.")

st.markdown("""
### Upcoming Capabilities:
- Report broken escalators, elevators, damaged tactile paving, or blocked doors
- Tag location/platform number and priority level
- Store reports in SQLite with clear separation between AI-detected vs manual entries
""")
