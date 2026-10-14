"""
TransitGuard AI - Module 4: Privacy & Ethics Centre
Documentation of edge-first data handling, anonymization, and limitations.
"""

import streamlit as st

st.set_page_config(page_title="Privacy Centre - TransitGuard", page_icon="🔒", layout="wide")

st.title("🔒 Module 4: Privacy & Ethics Centre")
st.markdown("Privacy-by-Design principles for public transit surveillance.")

st.info("⚡ **Stage 1 Active**: OpenCV Gaussian face-blurring and anonymization demonstrations will be integrated in **Stage 5**.")

st.markdown("""
### Core Privacy Architecture:
1. **Edge-First Local Processing**: No video feeds or passenger imagery leave the local edge device.
2. **Zero Facial Recognition**: The system has no facial recognition library or identity database.
3. **Data Minimization**: Only incident metadata (timestamp, obstacle type, confidence) is saved. Raw images are not persistently stored.
4. **Gaussian Face Blurring**: Optional on-the-fly blurring for review dashboards.
5. **Honest Limitations**: Blurring does not equal 100% anonymization; true privacy comes from local computation and immediate memory deallocation.
""")
