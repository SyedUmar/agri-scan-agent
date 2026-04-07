"""LLM interaction layer for Agri-Scan treatment recommendation generation."""

import os
from typing import Iterable, Iterator, Sequence, Tuple

import streamlit as st
from groq import Groq
from streamlit.errors import StreamlitSecretNotFoundError
from tenacity import retry, stop_after_attempt, wait_exponential


def _get_groq_api_key() -> str:
    """Read Groq API key from Streamlit secrets, then environment fallback."""
    try:
        secret_key = st.secrets.get("GROQ_API_KEY")
    except StreamlitSecretNotFoundError:
        secret_key = None

    api_key = secret_key or os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ Missing GROQ_API_KEY in Streamlit secrets or environment variables.")
        st.stop()
    return api_key


def _format_detections(detections: Sequence[Tuple[str, float]]) -> str:
    """Convert model detections into compact prompt context."""
    if not detections:
        return "No disease detections were found."

    return "\n".join(
        f"- {class_name}: {confidence:.1%} confidence"
        for class_name, confidence in detections
    )


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2))
def stream_treatment_plan(detections, target_language: str = "English"):
    """Create a streaming Groq completion with retry handling.

    Args:
        detections: Iterable of (class_name, confidence) tuples.
        target_language: Language name for full response translation.

    Returns:
        Groq streaming response object.
    """
    client = Groq(api_key=_get_groq_api_key())
    detection_context = _format_detections(detections)

    prompt = f"""
You are an expert agronomist advising farmers on crop disease treatment.

Detection context:
{detection_context}

Instructions:
1) Use practical, farmer-friendly language.
2) Keep each section concise and actionable.
3) If confidence appears low or ambiguous, recommend manual verification.
4) Translate the entire final response into: {target_language}.
5) Output MUST be valid Markdown and follow this structure exactly:

## Diagnosis
- [Concise diagnosis summary]

## Organic Remedy
- [One low-cost organic remedy]

## Chemical Treatment
- [One responsible chemical option when necessary]

## Prevention
- [One preventive action for future outbreaks]
""".strip()

    return client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You produce safe, practical, agriculture-focused guidance.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
        stream=True,
    )


def iter_stream_text(stream: Iterable) -> Iterator[str]:
    """Yield plain text fragments from Groq streaming chunks for Streamlit rendering."""
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content if chunk.choices[0].delta else None
        if delta:
            yield delta


def get_treatment_plan(detections, target_language: str = "English") -> str:
    """Backward-compatible non-stream helper assembled from streamed chunks."""
    stream = stream_treatment_plan(detections, target_language=target_language)
    parts = list(iter_stream_text(stream))
    return "".join(parts).strip()
