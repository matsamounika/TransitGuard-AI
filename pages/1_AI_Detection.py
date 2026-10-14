"""
TransitGuard AI - Module 1: AI Object Detection
Real edge AI inference using pretrained Ultralytics YOLOv8.
Detects passengers, luggage, backpacks, and transit equipment locally on CPU.
"""

import sys
import io
from pathlib import Path
import streamlit as st
from PIL import Image
import pandas as pd

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import (
    APP_NAME,
    DEFAULT_MODEL_NAME,
    CONFIDENCE_THRESHOLD,
    COLOR_PRIMARY,
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_DANGER,
    SAMPLE_IMAGES_DIR,
)
from detection import run_yolo_detection, load_yolo_model
from database import insert_alert
from sample_images.create_sample import download_or_generate_samples


# Page Configuration
st.set_page_config(
    page_title=f"AI Object Detection - {APP_NAME}",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Module 1: AI Object Detection")
st.caption(
    "Pretrained lightweight YOLOv8 edge inference. "
    "All processing executes locally on your CPU—no images or biometrics are ever uploaded to external clouds."
)

# Sidebar Controls
st.sidebar.header("⚙️ Detection Settings")

# Model info badge
st.sidebar.markdown(
    f"""
    <div style="background-color: #1E293B; padding: 10px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 15px;">
        <span style="color: #94A3B8; font-size: 0.8rem;">Active Model:</span><br>
        <b style="color: #38BDF8;">{DEFAULT_MODEL_NAME}</b> (Nano, ~6.2MB)<br>
        <span style="color: #10B981; font-size: 0.75rem;">● CPU-Optimized Edge Inference</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Confidence Slider
conf_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=0.90,
    value=float(CONFIDENCE_THRESHOLD),
    step=0.05,
    help="Higher values suppress ambiguous detections. Lower values capture fainter objects.",
)

# Class Filtering Multi-select
COMMON_CLASSES = ["person", "suitcase", "backpack", "handbag", "bicycle", "chair"]
selected_classes = st.sidebar.multiselect(
    "Target Transit Classes",
    options=COMMON_CLASSES,
    default=["person", "suitcase", "backpack", "handbag"],
    help="Filter inference output to focus on passengers and potential pathway obstacles.",
)

# Image Source Selection
st.sidebar.markdown("---")
image_source = st.sidebar.radio(
    "Image Source",
    options=["Upload My Own Image", "Use Bundled Sample Image"],
    index=1,
)

# Main Processing Flow
input_image = None
image_name = "sample"

if image_source == "Upload My Own Image":
    uploaded_file = st.file_uploader(
        "Upload Station Photo or CCTV Frame (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        help="Upload an image from a train or bus transit station.",
    )
    if uploaded_file is not None:
        try:
            input_image = Image.open(uploaded_file).convert("RGB")
            image_name = uploaded_file.name
        except Exception as e:
            st.error(f"Error loading uploaded image: {e}")
    else:
        st.info("👆 Please upload an image or switch to **'Use Bundled Sample Image'** in the sidebar to test immediately.")

else:
    # Ensure sample images exist
    download_or_generate_samples()
    available_samples = list(SAMPLE_IMAGES_DIR.glob("*.jpg")) + list(SAMPLE_IMAGES_DIR.glob("*.png"))

    if available_samples:
        sample_options = {p.name: p for p in available_samples}
        chosen_sample_name = st.selectbox(
            "Select a Preloaded Transit Scene:",
            options=list(sample_options.keys()),
            index=0,
        )
        sample_path = sample_options[chosen_sample_name]
        input_image = Image.open(sample_path).convert("RGB")
        image_name = sample_path.name
    else:
        st.warning("No sample images found. Please upload an image using the sidebar option.")

# If an image is ready, run real YOLO inference
if input_image is not None:
    st.markdown("---")

    with st.spinner("⚡ Running local YOLO edge inference on CPU..."):
        try:
            results = run_yolo_detection(
                image_input=input_image,
                conf_threshold=conf_threshold,
                model_name=DEFAULT_MODEL_NAME,
                filter_classes=selected_classes if selected_classes else None,
            )
        except Exception as err:
            st.error(f"YOLO Inference Error: {err}")
            results = None

    if results is not None:
        # Top KPI Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("⚡ Inference Speed", f"{results['inference_time_ms']} ms")
        with m2:
            st.metric("👥 Passengers", results["passengers_count"])
        with m3:
            st.metric("🧳 Luggage / Obstacles", results["obstacles_count"])
        with m4:
            st.metric("📦 Total Detections", results["total_detections"])

        st.markdown("")

        # Visual Comparison Columns
        col_orig, col_annotated = st.columns(2)

        with col_orig:
            st.subheader("📷 Original CCTV / Station Frame")
            st.image(results["original_image"], use_container_width=True, caption=f"Source: {image_name}")

        with col_annotated:
            st.subheader("🎯 YOLO Edge Detection Output")
            st.image(
                results["annotated_image"],
                use_container_width=True,
                caption=f"Detected: {results['total_detections']} objects ({results['inference_time_ms']}ms)",
            )

            # Download annotated image button
            annotated_pil = Image.fromarray(results["annotated_image"])
            buf = io.BytesIO()
            annotated_pil.save(buf, format="JPEG", quality=90)
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Download Annotated Image",
                data=byte_im,
                file_name=f"transitguard_detection_{image_name}",
                mime="image/jpeg",
                use_container_width=True,
            )

        # Tabular Detections Breakdown
        st.markdown("---")
        st.subheader("📋 Detected Objects Breakdown")

        detections_list = results["detections"]
        if detections_list:
            table_data = []
            for idx, det in enumerate(detections_list, start=1):
                box = det["bbox"]
                table_data.append({
                    "Index": idx,
                    "Class": det["class_name"].capitalize(),
                    "Category": det["category"],
                    "Confidence": f"{int(det['confidence'] * 100)}%",
                    "Bounding Box [X1, Y1, X2, Y2]": f"[{box[0]}, {box[1]}, {box[2]}, {box[3]}]",
                })

            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Quick Alert Dispatch Bridge
            with st.expander("🚨 Dispatch Alert to Transit Central Database"):
                st.write(
                    "Send an automated or verified observation from this detection to the local SQLite alerts registry."
                )
                col_z, col_s = st.columns(2)
                with col_z:
                    alert_zone = st.text_input("Station Zone", value="Platform 1 - Accessible Pathway")
                with col_s:
                    alert_severity = st.selectbox("Severity Level", ["Low", "Medium", "High", "Critical"], index=1)

                alert_notes = st.text_area(
                    "Alert Description",
                    value=f"Automated AI detection identified {results['obstacles_count']} luggage/obstacle items and {results['passengers_count']} passengers in {alert_zone}.",
                )

                if st.button("📤 Record Alert in SQLite Database", type="primary"):
                    alert_id = insert_alert(
                        alert_type="Object Detected",
                        zone=alert_zone,
                        severity=alert_severity,
                        description=alert_notes,
                        status="Pending",
                        metadata={
                            "total_objects": results["total_detections"],
                            "passengers": results["passengers_count"],
                            "obstacles": results["obstacles_count"],
                            "inference_ms": results["inference_time_ms"],
                        },
                    )
                    st.success(f"✅ Alert successfully registered with ID: **{alert_id}**! Viewable in the Alerts Dashboard.")

        else:
            st.warning("No target objects detected at this confidence threshold. Try lowering the threshold in the sidebar.")
