# 🎯 CareerLens AI — Intelligent Interview & Career Readiness Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

CareerLens AI is an intelligent interview preparation and evaluation platform that parses resumes, matches job descriptions, and conducts realistic voice-driven technical and company-specific mock interviews. It features dynamic project authenticity probing, AI-powered conversational follow-ups, CS core drills, and real-time fullscreen proctoring to help candidates comprehensively test and elevate their interview readiness.

---

## ✨ Key Features

1. **📄 Comprehensive NLP Resume Analysis & ATS Scoring**
   - Extracts contact details, technical skills across 7 categories, standard sections, and quantifiable metrics.
   - Enhanced Named Entity Recognition (NER) for Persons, Organizations, Colleges, Certifications, and Dates.
   - Computes transparent ATS compatibility scoring with actionable improvement checklists.

2. **🔍 Project Authenticity Probing**
   - Automatically extracts claimed projects from the candidate's resume (or infers realistic projects based on detected skills).
   - In every interview, systematically poses deep architectural and engineering questions citing the exact project name.

3. **📄 Resume-Aware Dynamic Question Generation**
   - Formulates tailored technical questions targeting the candidate's specific detected skills (Python, Java, React, SQL, Cloud, ML/DL, Docker, etc.), internships, certifications, and measurable impact.

4. **🔁 Intelligent Concept-Linked Follow-Up Engine**
   - Automatically addresses candidate by name (e.g. *"So Adarsh..."*).
   - Detects mentioned concepts in speech transcripts (e.g., *"Artificial Intelligence"*) and seamlessly pivots to advanced counterparts (e.g., *"Deep Learning and Neural Networks"*), architectural trade-offs, or under-the-hood mechanisms.

5. **📚 CS Core Subject Practice & Model Answers**
   - Extensive interactive question bank covering Operating Systems, DBMS & SQL, Computer Networks, Object-Oriented Programming (OOP), and Data Structures & Algorithms (DSA).
   - Instant answer evaluation, scoring, and full expert model answers.

6. **🛡️ Full-Screen Anti-Cheating Proctoring Engine**
   - Locks interview window in fullscreen mode.
   - Restricts shortcut keys (`Alt+Tab`, `Ctrl+Tab`, `Ctrl+C/V`, `Ctrl+F`, `F12`, `PrintScreen`, `Win`, `Esc`, `Alt+F4`, `Ctrl+W`, `Ctrl+L`, `F11`).
   - Issues progressive warnings and automatically cancels interview upon repeated violations.

7. **🎙️ Voice-Driven Speech-to-Text & Synthesized Voice**
   - Integrated browser audio capture using `faster-whisper`.
   - Realistic multi-accent voice synthesis (US, Indian, British English).

---

## 🚀 Quickstart & Local Setup

### 1. Clone repository
```bash
git clone https://github.com/ADARSH-TKD/CAREERLENS-AI.git
cd CAREERLENS-AI
```

### 2. Create virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run application
```bash
streamlit run app.py
```

---

## ☁️ Deployment on Streamlit Community Cloud (share.streamlit.io)

1. Fork or push this repository to your GitHub account: `https://github.com/ADARSH-TKD/CAREERLENS-AI`
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New app"** and select:
   - **Repository:** `ADARSH-TKD/CAREERLENS-AI`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy!**

> **Note**: Automated dependencies (`requirements.txt`, `packages.txt` for OCR/ffmpeg, and `nltk.txt` for NLTK corpora) are pre-configured in the repository root for zero-config deployment.
