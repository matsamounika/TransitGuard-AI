"""
TransitGuard AI - Module 5 & 6: Alerts & Admin Dashboard
Unified incident monitoring, dispatch management, and metrics.
"""

import streamlit as st

st.set_page_config(page_title="Alerts Dashboard - TransitGuard", page_icon="🔔", layout="wide")

st.title("🔔 Module 5 & 6: Alerts & Admin Dashboard")
st.markdown("Real-time incident feed, status transitions, and SQLite-backed audit log.")

st.info("⚡ **Stage 1 Active**: SQLite database and interactive alert management will be implemented in **Stage 6 & 7**.")

st.markdown("""
### Upcoming Capabilities:
- Live KPI cards: Total Alerts, Ramp Blocks, High Crowd Events, Pending vs Resolved
- Filterable and searchable alerts table
- Workflow status updates: 'Pending' ➔ 'In Progress' ➔ 'Resolved'
- Interactive alert breakdown charts
""")
