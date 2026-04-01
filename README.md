# Agri-Scan Agent

A professional, farmer-focused crop health assistant built with **Streamlit**, **YOLOv8**, and **Groq LLMs**.

Agri-Scan Agent helps users upload a leaf image, detect potential disease symptoms, and receive practical treatment guidance in clear, actionable language.

---

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Key Features](#2-key-features)
- [3. How It Works](#3-how-it-works)
- [4. Tech Stack](#4-tech-stack)
- [5. Repository Structure](#5-repository-structure)
- [6. Prerequisites](#6-prerequisites)
- [7. Installation](#7-installation)
- [8. Configuration](#8-configuration)
- [9. Running the Application](#9-running-the-application)
- [10. Usage Guide](#10-usage-guide)
- [11. CI Severity Policy](#11-ci-severity-policy)
- [12. Testing Strategy](#12-testing-strategy)
- [13. Troubleshooting](#13-troubleshooting)
- [14. Security and Privacy Notes](#14-security-and-privacy-notes)
- [15. Known Limitations](#15-known-limitations)
- [16. Roadmap](#16-roadmap)
- [17. Contributing](#17-contributing)
- [18. Changelog](#18-changelog)
- [19. License](#19-license)

---

## 1. Project Overview

Agri-Scan Agent is an AI-assisted crop-health application intended for rapid, practical field support.

It combines:

1. **Visual diagnosis** using a YOLO model to identify disease indicators from leaf images.
2. **Decision support** using a Groq-hosted large language model to produce treatment suggestions.
3. **Simple web delivery** via Streamlit for fast deployment and usability.

The current implementation targets a prototype-to-pilot workflow and is intended to support—not replace—expert agronomic judgment.

---

## 2. Key Features

- **Image upload workflow** for leaf photo analysis.
- **YOLO-based detection output** with confidence scores.
- **Annotated visualization** of model detections.
- **Automated treatment guidance** with organic, chemical, and prevention suggestions.
- **Farmer-friendly response style** designed for clarity and practical action.
- **Graceful fallback behavior** when remote model download or LLM calls fail.

---

## 3. How It Works

1. User uploads a crop leaf image in the Streamlit interface.
2. The app loads the YOLO model (local weights or download fallback path).
3. Inference runs and returns detected classes + confidence.
4. The app sends diagnosis context to Groq for treatment recommendations.
5. User receives:
   - Detection details,
   - Annotated image,
   - Suggested treatment and preventive guidance.

---

## 4. Tech Stack

- **Frontend/UI:** Streamlit
- **Vision Model:** Ultralytics YOLO
- **LLM Inference:** Groq API
- **Core Language:** Python
- **Configuration:** `.env` via `python-dotenv`
- **Image Processing:** Pillow / NumPy

---

## 5. Repository Structure

```text
agri-scan-agent/
├── app.py              # Main Streamlit app (UI + inference + LLM recommendation flow)
├── agent_logic.py      # Treatment recommendation helper logic
├── model_loader.py     # YOLO model loader helper
├── utils.py            # Shared utility helpers
├── requirements.txt    # Python dependencies
├── best.pt             # Model artifact currently checked into repository root
├── README.md           # Project documentation
└── CHANGELOG.md        # Project change history
```

> Note: some app logic references `assets/best.pt`, while `best.pt` currently exists at repository root. Aligning artifact location is recommended as a follow-up.

---

## 6. Prerequisites

- Python **3.10+** recommended
- `pip` available
- Groq API key
- (Optional) virtual environment tool (`venv`, `conda`, etc.)

---

## 7. Installation

```bash
# 1) Clone repository
git clone <your-repo-url>
cd agri-scan-agent

# 2) (Optional) create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt
```

---

## 8. Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Model file configuration

Expected model path in the app code is typically:

```text
assets/best.pt
```

If using a local model file, ensure the path in code and the file location are consistent.

---

## 9. Running the Application

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in terminal output (typically `http://localhost:8501`).

---

## 10. Usage Guide

1. Launch the app.
2. Upload a clear, well-lit leaf image.
3. Click **Analyze Crop Health**.
4. Review:
   - Detection labels and confidence,
   - Annotated image output,
   - Recommended treatment plan.
5. Use recommendations as guidance and validate with local agronomy experts when stakes are high.

---

## 11. CI Severity Policy

### Enforced in CI today

CI currently uses a **critical-only fail gate**:

- **Fail** when one or more `critical` findings are present.
- **Pass** when there are no `critical` findings, even if `serious`, `moderate`, or `low` findings are present.

### Aspirational policy

The target policy is to **fail on `serious` or higher** once the current baseline of `serious` issues is reduced.

- `moderate` and `low` findings remain non-blocking and are tracked for triage.

### Roadmap for threshold escalation

1. Burn down current `serious` issues.
2. Flip the CI gate to fail on `serious` + `critical`.
3. Re-evaluate after a stabilization window.

### Test naming and severity-language consistency

Use exact severity terms in test names to keep pass/fail behavior unambiguous:


- `test_ci_fails_on_critical_findings`
- `test_ci_passes_with_serious_when_no_critical`
- `test_ci_passes_with_moderate_and_low_when_no_critical`

---

## 12. Testing Strategy

Current repository state emphasizes application behavior and documentation. A recommended testing baseline is:

- Unit tests for helper logic (`agent_logic.py`, `model_loader.py`, `utils.py`)
- Integration tests for image upload → inference → recommendation flow
- Smoke tests for Streamlit startup and environment configuration
- CI policy checks aligned with documented severity gates

---

## 13. Troubleshooting

### App fails to start

- Verify dependencies are installed: `pip install -r requirements.txt`
- Confirm Python version compatibility.

### Groq errors or empty recommendations

- Ensure `GROQ_API_KEY` is set in `.env`
- Check internet access and API availability

### Model load failures

- Ensure the model file path in code matches actual file location
- If using download fallback, verify network access and repository ID configuration

---

## 14. Security and Privacy Notes

- Do **not** commit `.env` files or API keys.
- Treat uploaded agricultural images as potentially sensitive operational data.
- Validate generated treatment suggestions against regional regulations and safety standards.

---

## 15. Known Limitations

- Model path conventions are not fully standardized across files.
- Detection quality depends on image quality and model training coverage.
- LLM output is advisory and may require expert validation.

---

## 16. Roadmap

- Normalize model artifact handling and path conventions.
- Expand automated tests and CI enforcement coverage.
- Improve domain-specific recommendation accuracy and localization.
- Add telemetry/monitoring for reliability and model performance.

---

## 17. Contributing

Contributions are welcome. Suggested process:

1. Create a branch for your change.
2. Keep changes scoped and well-documented.
3. Update README/CHANGELOG when behavior changes.
4. Open a pull request with rationale, implementation notes, and validation steps.

---

## 18. Changelog

See [CHANGELOG.md](CHANGELOG.md) for project history.

---

## 19. License

No license file is currently present in this repository. Add a `LICENSE` file to define usage and distribution terms.

