# Agri-Scan Agent Deployment & Preview Guide

This guide explains how to run and preview Agri-Scan Agent locally and deploy it to a public URL.

---

## 1) Prerequisites

- Python 3.10+
- Git
- A Groq API key
- Project model file at `assets/best.pt` (required; app fails safely if missing)

---

## 2) Local Preview (Recommended First)

### Step 1: Clone and enter the project

```bash
git clone <your-repo-url>
cd agri-scan-agent
```

### Step 2: Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
# Windows (PowerShell): .venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Add your model

Ensure the custom agricultural model file exists at:

```text
assets/best.pt
```

> If this file is missing, the app will show an error and stop by design.

### Step 5: Configure Streamlit secrets

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

### Step 6: Start Streamlit

```bash
streamlit run app.py
```

Open the local URL shown in terminal (commonly `http://localhost:8501`).

---

## 3) Local Functional Preview Checklist

After launching locally, verify:

1. The app loads without model errors.
2. Language selector appears in sidebar.
3. Image upload works (`.jpg`, `.jpeg`, `.png`).
4. Clicking **Analyze** shows:
   - `📸 Image Analysis` tab with annotated image
   - `🩺 Treatment Protocol` tab with streaming output
5. Session rate limit enforces stop after 5 analyses.

---

## 4) Deploy to Streamlit Community Cloud

### Step 1: Push code to GitHub

```bash
git add .
git commit -m "Prepare deployment"
git push origin <branch>
```

### Step 2: Create app in Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub.
3. Click **New app**.
4. Select repo and branch.
5. Set **Main file path** to `app.py`.

### Step 3: Configure secrets in Streamlit Cloud

In app settings → **Secrets**, add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

### Step 4: Ensure model file availability

`assets/best.pt` must be present in the deployed filesystem (committed, downloaded at build time, or mounted in deployment strategy).

### Step 5: Deploy

Click **Deploy** and wait for build logs to finish.

---

## 5) Optional: Docker Deployment (for custom hosting)

Use this if you need deployment outside Streamlit Cloud.

### Example Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and run

```bash
docker build -t agri-scan-agent .
docker run -p 8501:8501 \
  -e GROQ_API_KEY="your_groq_api_key_here" \
  agri-scan-agent
```

If using container environment variables, map them into Streamlit secrets strategy as needed.

---

## 6) Troubleshooting

### Error: Core agricultural model is missing

- Confirm file exists at `assets/best.pt`.
- Confirm path and file name case match exactly.

### No LLM response / API errors

- Verify `GROQ_API_KEY` in Streamlit secrets.
- Check Groq service availability and quota limits.

### Build fails on OpenCV in cloud

- Keep `opencv-python-headless` in `requirements.txt` (already included).
- Avoid GUI OpenCV package in server environments.

---

## 7) Production Hardening Recommendations

- Add centralized logging and metrics for detections and API failures.
- Add persistent rate limiting (IP/account-based) behind reverse proxy or API gateway.
- Add authentication if deploying publicly.
- Add CI checks (lint + tests + security scanning) before deployment.

---

## 8) Quick Preview Commands (Copy/Paste)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p .streamlit
printf 'GROQ_API_KEY = "your_groq_api_key_here"\n' > .streamlit/secrets.toml
streamlit run app.py
```
