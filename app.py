"""Agri-Scan Streamlit application."""

import logging

import streamlit as st
from PIL import Image

from agent_logic import get_treatment_plan
from model_loader import load_model

CONFIDENCE_THRESHOLD = 0.5
MAX_API_CALLS_PER_SESSION = 5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    st.set_page_config(
        page_title="🌱 Agri-Scan Agent",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        .report-box {
            background: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #4CAF50;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        .stButton>button {
            background: #4CAF50;
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🌱 Agri-Scan: Autonomous Crop Health Agent")
    st.markdown("*Upload a leaf image → AI detects disease → Agent recommends treatment*")

    with st.sidebar:
        st.header("ℹ️ About This Tool")
        st.write("**🔍 Vision Model:** YOLOv8 (Custom Trained)")
        st.write("**🧠 AI Agent:** Groq + Llama 3.1")
        language = st.selectbox(
            "🌐 Select Language",
            ["English", "Español", "Français", "हिन्दी (Hindi)"],
            index=0,
        )
        st.divider()
        st.info("💡 Use clear, well-lit photos of a single leaf for best accuracy.")

    if "api_calls" not in st.session_state:
        st.session_state.api_calls = 0

    if st.session_state.api_calls >= MAX_API_CALLS_PER_SESSION:
        st.error("You have reached the maximum number of free analyses for this session.")
        st.stop()

    uploaded_file = st.file_uploader(
        "📤 Upload Leaf Image",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG",
    )

    if uploaded_file is None:
        st.info("👆 Please upload a leaf image to begin AI analysis.")
        return

    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📷 Uploaded Image", use_container_width=True)

    if not st.button("🔍 Analyze Crop Health", type="primary", use_container_width=True):
        return

    with st.spinner("🤖 AI Agent is diagnosing your crop..."):
        try:
            model = load_model()
            results = model.predict(image, conf=CONFIDENCE_THRESHOLD, save=False, verbose=False)
            detections = results[0].boxes

            if len(detections) == 0:
                st.success("🟢 Great news! No disease detected in this image.")
                st.markdown(
                    '<div class="report-box">✅ Your plant appears healthy! Continue regular monitoring.</div>',
                    unsafe_allow_html=True,
                )
                return

            top_box = detections[0]
            top_class = model.names[int(top_box.cls[0])]
            top_conf = float(top_box.conf[0])
            treatment = get_treatment_plan(top_class, top_conf, language)
            st.session_state.api_calls += 1

            annotated = results[0].plot()
            annotated_img = Image.fromarray(annotated[..., ::-1])

            st.success("Analysis complete")
            tab1, tab2, tab3 = st.tabs(["🎯 Detection Image", "🩺 Treatment Plan", "ℹ️ Raw Details"])

            with tab1:
                st.image(annotated_img, caption="Detection result", use_container_width=True)

            with tab2:
                st.markdown(f'<div class="report-box">{treatment}</div>', unsafe_allow_html=True)

            with tab3:
                for idx, box in enumerate(detections, start=1):
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[cls_id]
                    st.write(f"#{idx}: `{class_name}` — Confidence `{conf:.1%}`")

            if top_conf < 0.6:
                st.warning("⚠️ Low confidence detection. Please verify with a local expert.")

            st.write("Was this diagnosis helpful?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("👍 Yes"):
                    st.toast("Thanks for the feedback!")
            with c2:
                if st.button("👎 No"):
                    st.toast("Thanks, we will use this to improve.")

            logger.info("Detection completed class=%s confidence=%.3f", top_class, top_conf)

        except FileNotFoundError as exc:
            st.error(f"❌ Model Error: {exc}")
            st.stop()
        except Exception as exc:
            logger.exception("Unexpected analysis error")
            st.error(f"❌ Unexpected Error: {type(exc).__name__}")
            st.exception(exc)


if __name__ == "__main__":
    main()
