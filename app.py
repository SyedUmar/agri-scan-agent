"""
🌱 Agri-Scan: Autonomous Crop Health Agent
A Streamlit app that combines YOLOv8 crop disease detection with Groq AI agent for treatment recommendations.
"""

import streamlit as st
import os
from PIL import Image
import numpy as np
from ultralytics import YOLO
from groq import Groq
from dotenv import load_dotenv
import time

# ─────────────────────────────────────────────────────────────
# 1. LOAD ENVIRONMENT VARIABLES
# ─────────────────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"  # ✅ Current supported model
YOLO_MODEL_PATH = "assets/best.pt"
CONFIDENCE_THRESHOLD = 0.5

# ─────────────────────────────────────────────────────────────
# 2. CACHE MODEL LOADING (Prevents reloading on every interaction)
# ─────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
# MODEL LOADER WITH AUTO-DOWNLOAD (For Streamlit Cloud)
# ─────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
# MODEL LOADER WITH AUTO-DOWNLOAD (For Streamlit Cloud)
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_yolo_model():
    """Load YOLOv8 model, auto-download if missing"""
    
    model_path = "assets/best.pt"
    
    # If model doesn't exist locally, try to download
    if not os.path.exists(model_path):
        with st.spinner("📦 Downloading AI model (first run only)..."):
            try:
                # Option 1: Direct GitHub Raw URL (if you upload model to GitHub)
                # model_url = "https://raw.githubusercontent.com/YOUR_USERNAME/agri-scan-agent/main/assets/best.pt"
                
                # Option 2: Google Drive (public link) - convert to direct download
                # model_url = "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID"
                
                # Option 3: HuggingFace Hub (recommended for large files)
                from huggingface_hub import hf_hub_download
                
                # Upload your best.pt to HF: https://huggingface.co/new
                # Then use:
                model_path = hf_hub_download(
                    repo_id="your-username/agri-scan-models",  # Replace with your HF repo
                    filename="best.pt",
                    local_dir="assets"
                )
                
                st.success("✅ Model downloaded successfully!")
                
            except Exception as e:
                st.error(f"❌ Failed to download model: {str(e)}")
                st.info("💡 Fallback: Using pretrained YOLOv8n for demo")
                return YOLO("yolov8n.pt")  # Fallback to generic model
    
    return YOLO(model_path)

# ─────────────────────────────────────────────────────────────
# 3. GROQ AGENT FUNCTION (Treatment Plan Generator)
# ─────────────────────────────────────────────────────────────
def get_treatment_plan(disease_name, confidence):
    """
    Query Groq API to generate a farmer-friendly treatment plan.
    
    Args:
        disease_name (str): Detected disease class name
        confidence (float): Detection confidence (0.0 to 1.0)
    
    Returns:
        str: Formatted treatment recommendation
    """
    try:
        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        
        # Craft the prompt
        prompt = f"""
        You are an expert agricultural advisor helping farmers.
        
        DIAGNOSIS INFO:
        - Detected Disease: {disease_name}
        - AI Confidence: {confidence:.1f}%
        
        TASK: Provide a clear, actionable treatment plan with:
        1. ✅ Quick confirmation of the diagnosis (1 sentence)
        2. 🌿 One organic/natural remedy (affordable & accessible)
        3. 💊 One chemical treatment option (if disease is severe)
        4. 🛡️ One preventive measure to avoid future outbreaks
        
        GUIDELINES:
        - Keep total response under 150 words
        - Use simple, farmer-friendly language (avoid jargon)
        - Prioritize low-cost, locally available solutions
        - If confidence < 60%, suggest manual verification first
        """
        
        # Call Groq API
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,      # Low temperature = more focused responses
            max_tokens=400,       # Limit response length
            timeout=30            # Prevent hanging
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        # Return graceful error message
        return f"⚠️ Unable to generate treatment plan. Error: {str(e)}\n\n💡 Tip: Check your internet connection or try again later."

# ─────────────────────────────────────────────────────────────
# 4. MAIN STREAMLIT APP
# ─────────────────────────────────────────────────────────────
def main():
    # Page configuration
    st.set_page_config(
        page_title="🌱 Agri-Scan Agent",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better UI
    st.markdown("""
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
        .stButton>button:hover {
            background: #45a049;
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🌱 Agri-Scan: Autonomous Crop Health Agent")
    st.markdown("*Upload a leaf image → AI detects disease → Agent recommends treatment*")
    
    # Sidebar: Info & Settings
    with st.sidebar:
        st.header("ℹ️ About This Tool")
        st.write("**🔍 Vision Model:** YOLOv8 (Custom Trained)")
        st.write("**🧠 AI Agent:** Groq + Llama 3.1")
        st.write("**📊 Classes:** mildew, Rose_P01, Healthy")
        st.divider()
        st.info("💡 **Pro Tip:** Use clear, well-lit photos of single leaves for best accuracy.")
        st.caption("Built for farmers.")
    
    # Main Content: Image Upload
    uploaded_file = st.file_uploader("📤 Upload Leaf Image", type=["jpg", "jpeg", " "], help="Supported formats: JPG, JPEG, PNG")
    
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file).convert("RGB")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption="📷 Original Image", use_container_width=True)
        
        # Analyze Button
        if st.button("🔍 Analyze Crop Health", type="primary", use_container_width=True):
            with st.spinner("🤖 AI Agent is diagnosing your crop..."):
                try:
                    # ─── STEP 1: Run YOLO Inference ───
                    model = load_yolo_model()
                    results = model.predict(
                        image, 
                        conf=CONFIDENCE_THRESHOLD, 
                        save=False,
                        verbose=False  # Suppress console output
                    )
                    
                    # Get annotated image (with bounding boxes)
                    annotated = results[0].plot()
                    annotated_img = Image.fromarray(annotated[..., ::-1])  # BGR → RGB
                    
                    with col2:
                        st.image(annotated_img, caption="🎯 AI Detection Result", use_container_width=True)
                    
                    # ─── STEP 2: Process Detections ───
                    detections = results[0].boxes
                    
                    if len(detections) > 0:
                        st.success("✅ Disease Detected!")
                        
                        # Show detection details in expandable section
                        with st.expander("📊 Detection Details", expanded=True):
                            for i, box in enumerate(detections):
                                cls_id = int(box.cls[0])
                                conf = float(box.conf[0])
                                class_name = model.names[cls_id]
                                st.write(f"**#{i+1}**: `{class_name}` — Confidence: `{conf:.1%}`")
                        
                        # Get top detection for agent analysis
                        top_box = detections[0]
                        top_class = model.names[int(top_box.cls[0])]
                        top_conf = float(top_box.conf[0])
                        
                        # ─── STEP 3: Query AI Agent ───
                        st.markdown("### 🩺 AI Agent Treatment Plan")
                        
                        # Show loading status
                        status_text = st.empty()
                        status_text.info("🤔 Agent is analyzing disease severity & generating recommendations...")
                        
                        # Small delay for better UX (simulates "thinking")
                        time.sleep(1)
                        
                        # Get treatment plan from Groq
                        treatment = get_treatment_plan(top_class, top_conf)
                        
                        # Display result in styled box
                        st.markdown(f'<div class="report-box">{treatment}</div>', unsafe_allow_html=True)
                        status_text.success("✅ Analysis Complete!")
                        
                        # Optional: Add confidence warning
                        if top_conf < 0.6:
                            st.warning("⚠️ Low confidence detection. Please verify with an expert if symptoms persist.")
                    
                    else:
                        # No disease detected
                        st.info("🟢 Great news! No disease detected in this image.")
                        st.markdown("### 💡 Agent Suggestion")
                        st.markdown('<div class="report-box">✅ Your plant appears healthy! Continue regular monitoring, ensure proper watering, and maintain good field hygiene to prevent future issues.</div>', unsafe_allow_html=True)
                        
                except FileNotFoundError as e:
                    st.error(f"❌ Model Error: {str(e)}")
                    st.info("💡 Make sure `best.pt` is in the `assets/` folder.")
                except Exception as e:
                    st.error(f"❌ Unexpected Error: {type(e).__name__}")
                    st.exception(e)  # Shows full traceback for debugging
    
    else:
        # Empty state
        st.info("👆 Please upload a leaf image to begin AI analysis.")
        
        # Optional: Add demo button
        if st.button("🎬 Try with Sample Image"):
            st.warning("Demo feature: Add a sample image to `assets/sample.jpg` to enable this.")

# ─────────────────────────────────────────────────────────────
# 5. ENTRY POINT
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
