import os
from pathlib import Path

import streamlit as st
from ultralytics import YOLO


MODEL_CANDIDATES = [
    Path("assets") / "best.pt",
    Path("best.pt"),
]


@st.cache_resource
def load_model() -> YOLO:
    """Load the agricultural YOLO model from known project paths.

    The app intentionally does not fall back to a generic COCO model, because that
    can produce irrelevant classes and unsafe treatment recommendations.
    """
    for model_path in MODEL_CANDIDATES:
        if model_path.exists():
            return YOLO(str(model_path))

    searched = ", ".join(str(path) for path in MODEL_CANDIDATES)
    raise FileNotFoundError(
        "Agricultural model weights not found. "
        f"Expected one of: {searched}. "
        "Place best.pt in assets/ or repository root."
    )
