"""Main Streamlit UI for Agri-Scan Agent."""

import streamlit as st
from PIL import Image

from agent_logic import iter_stream_text, stream_treatment_plan
from model_loader import load_vision_model, process_image


st.set_page_config(
    page_title="🌱 Agri-Scan Agent",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Initialize the vision model at startup (cached in model_loader).
model = load_vision_model()


def main() -> None:
    st.title("🌱 Agri-Scan Agent")
    st.caption("Upload a leaf image to detect disease and receive a treatment protocol.")

    with st.sidebar:
        st.header("Settings")
        selected_language = st.selectbox(
            "🌐 Language",
            ["English", "Español", "Français", "हिन्दी", "اردو"],
            index=0,
        )

    if "api_calls" not in st.session_state:
        st.session_state.api_calls = 0

    if st.session_state.api_calls >= 5:
        st.warning("You have reached the maximum of 5 analyses for this session.")
        st.stop()

    uploaded_file = st.file_uploader(
        "📤 Upload a leaf image",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG",
    )

    if uploaded_file is None:
        st.info("Please upload an image to begin analysis.")
        return

    preview = Image.open(uploaded_file).convert("RGB")
    st.image(preview, caption="Uploaded image", use_container_width=True)

    if not st.button("🔍 Analyze", type="primary", use_container_width=True):
        return

    # Rate-limiting counter increments when an analysis is requested.
    st.session_state.api_calls += 1

    detections, annotated_image = process_image(model, uploaded_file)
    if not detections:
        st.info("No disease detections found in the uploaded image.")
        st.stop()

    tab_image, tab_treatment = st.tabs(["📸 Image Analysis", "🩺 Treatment Protocol"])

    with tab_image:
        st.image(annotated_image, caption="Model detections", use_container_width=True)

    with tab_treatment:
        stream = stream_treatment_plan(
            detections=detections,
            target_language=selected_language,
        )
        st.write_stream(iter_stream_text(stream))


if __name__ == "__main__":
    main()
