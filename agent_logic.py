import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_treatment_plan(disease_name: str, confidence: float, language: str = "English") -> str:
    """Generate a concise farmer-friendly treatment plan from Groq."""
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
- Translate the final response fully into: {language}

Format your response exactly like this:
### 🩺 Diagnosis: [Name]
**Confidence:** High/Medium/Low

### 🌿 Organic Remedy
[1 sentence]

### 💊 Chemical Treatment
[1 sentence]

### 🛡️ Prevention
[1 sentence]
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"⚠️ Unable to generate treatment plan: {exc}"
