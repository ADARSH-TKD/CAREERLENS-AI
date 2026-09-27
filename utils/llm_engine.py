"""
CareerLens AI - LLM Engine (Google Gemini Integration)
Provides dynamic AI-powered question generation, project authenticity probing,
and answer evaluation using Google Gemini models with automatic zero-cost local NLP fallback.
"""

import os
import json
import re
import urllib.request
import urllib.error

# Attempt import of official google-genai SDK
try:
    from google import genai
    from google.genai import types
    _GENAI_SDK_AVAILABLE = True
except Exception:
    _GENAI_SDK_AVAILABLE = False


def get_gemini_api_key() -> str:
    """
    Retrieves the Gemini API key in order of priority:
    1. Streamlit Session State (Sidebar user input)
    2. Streamlit Cloud Secrets (st.secrets['GEMINI_API_KEY'])
    3. OS Environment variable ('GEMINI_API_KEY')
    """
    try:
        import streamlit as st
        # 1. UI sidebar input
        ui_key = st.session_state.get("gemini_api_key", "").strip()
        if ui_key:
            return ui_key
        # 2. Streamlit Secrets
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            sec_key = str(st.secrets["GEMINI_API_KEY"]).strip()
            if sec_key:
                return sec_key
    except Exception:
        pass

    # 3. Environment Variable
    env_key = os.getenv("GEMINI_API_KEY", "").strip()
    return env_key


def is_llm_available() -> bool:
    """Returns True if a valid-looking Gemini API key is configured."""
    key = get_gemini_api_key()
    return bool(key and len(key) >= 15)


def _call_gemini_rest(prompt: str, system_instruction: str, api_key: str, model: str = "gemini-2.5-flash") -> str:
    """
    Direct REST API call to Google Generative Language API.
    Zero-dependency fallback that works on any Python installation.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 200,
        }
    }
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=8) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        candidates = res_data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "").strip()
    return ""


def _clean_question_text(raw_text: str) -> str:
    """Clean conversational preambles, markdown formatting, or surrounding quotes."""
    text = (raw_text or "").strip()
    # Remove leading quotes or markdown backticks
    text = re.sub(r'^["\'`]+|["\'`]+$', '', text)
    # Remove common conversational preambles
    text = re.sub(r'^(Here is a follow-up question:?|Follow-up Question:?|Here is the question:?)\s*', '', text, flags=re.IGNORECASE)
    # If LLM generated multiple questions, keep only the first 1-2 sentences
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if lines:
        text = lines[0]
    return text.strip()


def generate_llm_followup(
    candidate_name: str,
    current_question: str,
    candidate_answer: str,
    project_name: str = "",
    role: str = "Software Engineer"
) -> str:
    """
    Calls Google Gemini to generate an adaptive, personalized technical follow-up question.
    Returns None if LLM is unavailable or fails, allowing graceful local fallback.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    first_name = candidate_name.strip().split()[0].capitalize() if candidate_name and candidate_name.lower() != "there" else ""
    name_instruction = f"Address the candidate directly as '{first_name}' (e.g. 'So {first_name}, as you mentioned [concept]...')" if first_name else "Start naturally (e.g. 'As you mentioned [concept]...')"

    system_instruction = (
        "You are an expert FAANG-level technical interviewer conducting a mock interview. "
        "Your task is to generate exactly ONE sharp, conversational follow-up question based on the candidate's last answer.\n\n"
        "Guidelines:\n"
        f"1. {name_instruction}.\n"
        "2. Directly pick out a technical concept, framework, tool, or metric from the candidate's answer.\n"
        "3. Probe deeper: ask about underlying internal mechanics, scalability trade-offs, edge-case failures, or a directly connected advanced topic.\n"
        "4. Keep the question strictly 1 to 2 sentences long.\n"
        "5. Output ONLY the question. Never add conversational filler, preambles, greetings, or explanations."
    )

    user_prompt = f"""Target Role: {role}
Current Interview Question: "{current_question}"
Candidate Answer: "{candidate_answer}"
{f'Candidate Mentioned Project: "{project_name}"' if project_name else ''}

Generate the single best follow-up question:"""

    # 1. Try google-genai SDK first
    if _GENAI_SDK_AVAILABLE:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                    max_output_tokens=160,
                )
            )
            if response and response.text:
                cleaned = _clean_question_text(response.text)
                if cleaned:
                    return cleaned
        except Exception as e:
            # Fall back to REST if SDK model name or version mismatch
            pass

    # 2. Try REST API fallback
    for m in ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]:
        try:
            raw = _call_gemini_rest(user_prompt, system_instruction, api_key, model=m)
            cleaned = _clean_question_text(raw)
            if cleaned:
                return cleaned
        except Exception:
            continue

    return None


def generate_llm_project_probe(
    candidate_name: str,
    project_name: str,
    project_desc: str = "",
    role: str = "Software Engineer"
) -> str:
    """
    Generates a deep technical project authenticity probing question using Gemini.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    first_name = candidate_name.strip().split()[0].capitalize() if candidate_name else ""
    greeting = f"So {first_name}, " if first_name else ""

    system_instruction = (
        "You are an expert technical interviewer verifying the authenticity of a candidate's claimed software project. "
        "Formulate ONE targeted, deep architectural or implementation question specifically mentioning the project by name.\n"
        "Focus on system architecture, database bottleneck resolution, concurrency, or the hardest bug they personally solved.\n"
        "Keep it strictly 1-2 sentences. Output ONLY the question."
    )

    user_prompt = f"""Project Name: {project_name}
Project Details: {project_desc or 'Full-stack software engineering project'}
Target Role: {role}

Generate a project authenticity question:"""

    if _GENAI_SDK_AVAILABLE:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                    max_output_tokens=150,
                )
            )
            if response and response.text:
                return _clean_question_text(response.text)
        except Exception:
            pass

    for m in ["gemini-2.5-flash", "gemini-1.5-flash"]:
        try:
            raw = _call_gemini_rest(user_prompt, system_instruction, api_key, model=m)
            cleaned = _clean_question_text(raw)
            if cleaned:
                return cleaned
        except Exception:
            continue

    return None


def generate_llm_answer_feedback(
    question: str,
    answer: str,
    category: str = "Technical"
) -> str:
    """
    Generates concise 2-sentence constructive evaluator feedback for the interview report.
    """
    api_key = get_gemini_api_key()
    if not api_key or not answer.strip():
        return ""

    system_instruction = (
        "You are a senior tech lead evaluating an interview answer. "
        "Provide exactly 2 concise, highly constructive sentences:\n"
        "Sentence 1: What was accurate or strong about their response.\n"
        "Sentence 2: Exactly what technical depth, algorithm details, or industry best practice they should add to make it outstanding.\n"
        "Be direct, polite, and technical."
    )

    user_prompt = f"Category: {category}\nQuestion: {question}\nCandidate Answer: {answer}\n\nProvide constructive evaluation:"

    if _GENAI_SDK_AVAILABLE:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.6,
                    max_output_tokens=150,
                )
            )
            if response and response.text:
                return response.text.strip()
        except Exception:
            pass

    for m in ["gemini-2.5-flash", "gemini-1.5-flash"]:
        try:
            raw = _call_gemini_rest(user_prompt, system_instruction, api_key, model=m)
            if raw:
                return raw.strip()
        except Exception:
            continue

    return ""
