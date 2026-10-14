"""
TransitGuard AI - Module 2: Wheelchair Ramp Obstruction Detection
Interactive ROI calibration and bounding-box overlap computation.
"""

import streamlit as st

st.set_page_config(page_title="Ramp Monitoring - TransitGuard", page_icon="♿", layout="wide")

st.title("♿ Module 2: Wheelchair Ramp Obstruction Monitoring")
st.markdown("Geometric ROI overlap analysis to detect luggage and obstacles blocking accessible pathways.")

st.info("⚡ **Stage 1 Active**: Interactive ramp ROI marking and obstacle overlap heuristics will be implemented in **Stage 3**.")

st.markdown("""
### Upcoming Capabilities:
- Interactive wheelchair ramp ROI selection
- Real-time overlap computation between obstacles (suitcases, bags) and ramp ROI
- Exclusion of 'person' class by default
- Configurable obstruction sensitivity threshold
- Generation of 'No Obstruction' vs 'Possible Obstruction' alerts
""")
