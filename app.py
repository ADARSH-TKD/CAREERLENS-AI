import streamlit as st
from pathlib import Path
import json
import time

from utils.resume_parser import extract_resume_text
from utils.nlp_engine import analyze_resume
from utils.scoring import calculate_ats_score
from utils.interview_engine import (
    get_questions, build_resume_questions, evaluate_answer,
    get_company_label, generate_jd_questions,
    generate_project_authenticity_question
)
from utils.speech import transcribe_audio, speak_text_html
from utils.ui import inject_css, metric_card, score_ring, section_title
from utils.nlp_features import (
    jd_match_score, generate_followup, fluency_report,
    semantic_keyword_match, ner_resume_dashboard, weakness_cluster_report
)
from utils.cs_core_bank import (
    CS_CORE_SUBJECTS, CS_CORE_QUESTIONS, get_all_cs_subjects,
    get_cs_questions, get_random_cs_question, search_cs_bank
)
from utils.proctoring import get_proctoring_html, get_proctoring_exit_html

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

DATA_DIR = Path("data")
QUESTION_FILE = DATA_DIR / "questions.json"

def init_state():
    defaults = {
        "page": "home",
        "name": "",
        "resume_text": "",
        "resume_analysis": None,
        "ats": None,
        "company": None,
        "mode": None,
        "questions": [],
        "q_index": 0,
        "answers": [],
        "current_transcript": "",
        "recording": False,
        "interview_voice": "Professional Male (US)",
        "interview_started": False,
        "report": None,
        "question_started_at": None,
        "jd_text": "",
        "jd_result": None,
        # Follow-up state machine
        "pending_followup": None,      # dict with question to ask as follow-up
        "answering_followup": False,    # True while user is answering a follow-up
        "followup_parent_idx": -1,      # index of the parent question
        # CS Core section states
        "cs_active_subject": "All CS Core Subjects",
        "cs_active_difficulty": "All Difficulties",
        "cs_current_question": None,
        "cs_evaluation": None,
        "cs_history": [],
        "cs_view": "drill",
        # Full-Screen Proctoring states
        "proctoring_warnings": 0,
        "interview_cancelled": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def nav():
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    cols = st.columns([1.7, 1, 1, 1, 1.15, 1])
    with cols[0]:
        st.markdown("<div class='brand'>CAREER<span>LENS</span> <small>AI</small></div>", unsafe_allow_html=True)
    pages = [
        ("🏠 Home", "home"),
        ("📄 Analysis", "analysis"),
        ("🎙️ Interview", "interview"),
        ("📚 CS Core", "cs_core"),
        ("📊 Report", "report"),
    ]
    for i, (label, page) in enumerate(pages, start=1):
        with cols[i]:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                if page == "analysis" and not st.session_state.resume_analysis:
                    st.session_state.page = "home"
                    st.warning("Analyze a resume first.")
                elif page == "report" and not st.session_state.report:
                    st.session_state.page = "interview"
                    st.warning("Complete an interview first to generate a report.")
                else:
                    st.session_state.page = page
                st.rerun()
    st.markdown("<div class='navline'></div>", unsafe_allow_html=True)

def home():
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">NLP CAREER TOOLKIT</div>
      <h1>Understand your resume.<br><span>Practice your interview.</span></h1>
      <p>A simple Streamlit prototype that analyzes your resume and lets you practice a company-style technical interview.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("Start with your resume")
    st.session_state.name = st.text_input("Your name", value=st.session_state.name, placeholder="Enter your name")

    method = st.radio("Resume input", ["Upload PDF", "Upload JPG / PNG", "Paste text"], horizontal=True)

    text = ""
    if method == "Upload PDF":
        f = st.file_uploader("Upload PDF", type=["pdf"])
        if f:
            text = extract_resume_text(f, "pdf")
    elif method == "Upload JPG / PNG":
        f = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
        if f:
            text = extract_resume_text(f, "image")
    else:
        text = st.text_area("Paste resume text", height=220, placeholder="Paste your resume content here...")

    st.markdown("**Or try a sample resume**")
    samples = {
        "Software Engineer": """Alex Kumar
alex.kumar@gmail.com | +91 9876543210 | github.com/alexkumar

SUMMARY
Software engineering student with experience in Java, Spring Boot and MySQL.

EDUCATION
B.Tech Computer Science Engineering

SKILLS
Java, Python, Spring Boot, MySQL, Git, DSA, OOP

PROJECTS
Railway Reservation System using Java and MySQL.
AI DSA Visualizer using Python and NLP.

EXPERIENCE
Software Development Intern — Built REST APIs and database modules.

CERTIFICATIONS
Java Programming
""",
        "Data Analyst": """Priya Sharma
priya@example.com | +91 9000000000 | linkedin.com/in/priya

SUMMARY
Data analyst skilled in Python, SQL, Excel and data visualization.

EDUCATION
B.Tech Computer Science

SKILLS
Python, SQL, MySQL, Pandas, NumPy, Matplotlib, Power BI

PROJECTS
Sales analytics dashboard and customer data analysis.

EXPERIENCE
Data Analytics Intern — cleaned datasets and created reports.

CERTIFICATIONS
Data Analytics
""",
        "ML / NLP Engineer": """Rahul Das
rahul@example.com | github.com/rahuldas

SUMMARY
Machine learning student interested in NLP and deep learning.

EDUCATION
B.Tech Artificial Intelligence and Machine Learning

SKILLS
Python, NLP, Machine Learning, Deep Learning, NLTK, spaCy, Gensim, Word2Vec

PROJECTS
NLP text preprocessing pipeline using NLTK and spaCy.
Word2Vec semantic similarity visualization.

EXPERIENCE
AI Intern — performed data preprocessing and model experimentation.
"""
    }
    scols = st.columns(3)
    for i, title in enumerate(samples):
        with scols[i]:
            if st.button(title, key=f"sample_{i}"):
                text = samples[title]
                st.session_state.name = st.session_state.name or "Candidate"

    if st.button("✦ ANALYZE RESUME", type="primary", use_container_width=True):
        if not st.session_state.name.strip():
            st.warning("Please enter your name first.")
        elif not text or len(text.strip()) < 40:
            st.warning("Please upload a readable resume or paste enough resume text.")
        else:
            with st.spinner("Running NLP analysis..."):
                analysis = analyze_resume(text)
                ats = calculate_ats_score(analysis)
            st.session_state.resume_text = text
            st.session_state.resume_analysis = analysis
            st.session_state.ats = ats
            st.session_state.page = "analysis"
            st.rerun()

    # ── JD Paste section (inline on Home) ─────────────────────────────────
    st.markdown("---")
    st.markdown("📄 **Paste Job Description** *(Optional — for JD-based interview practice)*")
    jd_input = st.text_area(
        "Paste Job Description here",
        value=st.session_state.get("jd_text", ""),
        height=160,
        placeholder="Copy the full job description from LinkedIn, Naukri, or a company website and paste it here...",
        key="home_jd_input",
    )
    if jd_input.strip() != st.session_state.get("jd_text", "").strip():
        st.session_state.jd_text = jd_input
    if jd_input.strip():
        st.success('\u2713 JD saved! Choose "Custom JD" in the Interview Lab to get questions tailored to this role.')
    st.markdown("</div>", unsafe_allow_html=True)

def analysis_page():
    a = st.session_state.resume_analysis
    ats = st.session_state.ats
    st.markdown(f"## Resume Analysis <span class='muted'>/ {st.session_state.name}</span>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("ATS Compatibility", f"{ats['score']}/100", "Explainable prototype score")
    with c2: metric_card("Skills Found", str(len(a["skills"])), "From configured skill list")
    with c3: metric_card("Sections", f"{len(a['sections'])}", "Detected resume sections")
    with c4: metric_card("Entities", str(len(a["entities"])), "spaCy NER results")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1, 1.25])
    with left:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        section_title("ATS compatibility")
        st.markdown(score_ring(ats["score"]), unsafe_allow_html=True)
        for item in ats["checks"]:
            icon = "✓" if item["ok"] else "⚠"
            cls = "good" if item["ok"] else "warn"
            st.markdown(f"<div class='check {cls}'>{icon} {item['text']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        section_title("Detected profile")
        st.markdown("**Skills**")
        st.write(", ".join(a["skills"]) if a["skills"] else "No configured skills detected.")
        st.markdown("**Sections detected**")
        st.markdown("**Claimed / Inferred Projects**")
        projs = a.get("projects", [])
        if projs:
            proj_str = " • ".join([f"{p['name']}" + (" *(Inferred)*" if p.get("inferred") else "") for p in projs[:3]])
            st.write(proj_str)
        else:
            st.write("No explicit projects detected.")
        st.markdown("**Contact signals**")
        st.write(f"Email: {'✓' if a['contact']['email'] else '—'}  |  Phone: {'✓' if a['contact']['phone'] else '—'}  |  GitHub: {'✓' if a['contact']['github'] else '—'}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        section_title("Enhanced NER Dashboard 🆕")
        ner = ner_resume_dashboard(st.session_state.resume_text, a["entities"])
        ner_labels = {
            "persons": ("👤","Persons"),
            "organisations": ("🏢","Organisations"),
            "locations": ("📍","Locations"),
            "degrees": ("🎓","Degrees"),
            "certifications": ("🏆","Certifications"),
            "colleges": ("🏫","Colleges/Universities"),
            "dates_years": ("📅","Dates & Years"),
        }
        found_any = False
        for key, (icon, label) in ner_labels.items():
            vals = ner.get(key, [])
            if vals:
                found_any = True
                st.markdown(f"**{icon} {label}**")
                st.caption("  •  ".join(vals[:10]))
        if not found_any:
            st.caption("No enhanced entities detected.")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        section_title("NLP pipeline")
        st.markdown("""
        <div class='pipeline'>
        Raw text → Tokenization → Normalization → Stopwords → Lemmatization<br>
        ↓<br>
        POS Tagging → Regex → NER → Skill Extraction → ATS Score
        </div>
        """, unsafe_allow_html=True)
        st.caption("Built with NLTK, spaCy, Python re and a configurable skill dictionary.")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🎙️ Go to Interview Practice", type="primary", use_container_width=True):
        st.session_state.page = "interview"
        st.rerun()


# ──────────────────────────────────────────────────────────────────
# JD Match Page (Feature 1 – TF-IDF Cosine Match)
# ──────────────────────────────────────────────────────────────────
def jd_match_page():
    st.markdown("## 🔗 Resume ↔ Job Description Matcher")
    st.caption("Paste a job description and see how well your resume matches it using TF-IDF NLP analysis.")

    if not st.session_state.resume_text:
        st.warning("⚠️ Analyze your resume first on the Home page.")
        if st.button("🏠 Go to Home"):
            st.session_state.page = "home"
            st.rerun()
        return

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.session_state.jd_text = st.text_area(
        "📄 Paste Job Description here",
        value=st.session_state.jd_text,
        height=250,
        placeholder="Copy-paste the full job description from LinkedIn, Naukri, company website, etc..."
    )

    if st.button("✨ ANALYZE MATCH", type="primary", use_container_width=True):
        if len(st.session_state.jd_text.strip()) < 50:
            st.warning("Please paste a proper job description (at least 50 characters).")
        else:
            with st.spinner("🧠 Running TF-IDF similarity analysis..."):
                st.session_state.jd_result = jd_match_score(
                    st.session_state.resume_text,
                    st.session_state.jd_text
                )
    st.markdown("</div>", unsafe_allow_html=True)

    r = st.session_state.jd_result
    if r:
        st.markdown("<br>", unsafe_allow_html=True)
        pct = r["match_pct"]
        color = "#22c55e" if pct >= 65 else "#f59e0b" if pct >= 40 else "#ef4444"
        label = "Strong Match" if pct >= 65 else "Moderate Match" if pct >= 40 else "Low Match"

        st.markdown(f"""
        <div class='glass' style='text-align:center;padding:2rem'>
          <div style='font-size:4rem;font-weight:900;color:{color}'>{pct}%</div>
          <div style='font-size:1.2rem;color:{color};font-weight:600'>{label}</div>
          <div style='color:#94a3b8;margin-top:.4rem'>Resume ↔ Job Description Cosine Similarity</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            section_title("✅ Matched Keywords")
            if r["matched_keywords"]:
                for kw in r["matched_keywords"]:
                    st.markdown(f"<div class='check good'>✓ {kw}</div>", unsafe_allow_html=True)
            else:
                st.caption("No keyword matches found.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            section_title("❌ Missing Keywords")
            if r["missing_keywords"]:
                for kw in r["missing_keywords"]:
                    st.markdown(f"<div class='check warn'>⚠ {kw}</div>", unsafe_allow_html=True)
            else:
                st.caption("No major gaps detected!")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        section_title("💡 Suggestions")
        for tip in r["suggestions"]:
            st.markdown(f"> {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

def interview_dashboard():
    st.markdown("## Interview Lab")
    st.caption("Company-style practice — questions are curated for practice, not official company questions.")

    # Custom JD card (shown only when JD is pasted)
    has_jd = bool(st.session_state.get("jd_text", "").strip())
    if has_jd:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1e1b4b,#312e81);border:2px solid #6366f1;
             border-radius:14px;padding:1rem 1.3rem;margin-bottom:1rem'>
          <div style='font-size:1.6rem'>📄</div>
          <h3 style='color:#a5b4fc;margin:.2rem 0'>Custom JD Interview</h3>
          <p style='color:#94a3b8;font-size:13px'>Questions tailored to the job description you pasted</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("★ Practice Custom JD", key="company_custom_jd", use_container_width=False):
            st.session_state.company = "Custom JD"
        st.markdown("---")

    # CS Core Practice Shortcut
    st.markdown("""
    <div style='background:linear-gradient(135deg,#131127,#20113a);border:1px solid rgba(167,139,250,.35);
         border-radius:14px;padding:1rem 1.3rem;margin-bottom:1rem;'>
      <div style='font-size:1.4rem'>📚</div>
      <h4 style='color:#e9d5ff;margin:.2rem 0'>CS Core Subject Practice & Model Answers</h4>
      <p style='color:#a9a0b9;font-size:13px;margin:0'>Operating Systems, DBMS & SQL, Computer Networks, OOP, and DSA with instant random drills & full model answers.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Practice CS Core Subjects (OS, DBMS, CN, OOP, DSA)", key="open_cs_core_drill", use_container_width=True):
        st.session_state.page = "cs_core"
        st.rerun()
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    companies = [
        "Microsoft", "Google", "Amazon", "TCS",
        "Infosys", "Accenture", "Wipro", "Cognizant",
        "HCLTech", "Tech Mahindra", "LTIMindtree", "Capgemini",
        "IBM", "Deloitte", "PwC", "Cisco",
        "JP Morgan Chase", "BNP Paribas", "KPIT Technologies",
    ]
    cols = st.columns(4)
    for i, company in enumerate(companies):
        with cols[i % 4]:
            st.markdown(f"<div class='company-card'><div class='company-icon'>{company[0]}</div><h3>{company}</h3><p>Technical • Core CS • Resume</p></div>", unsafe_allow_html=True)
            if st.button(f"Practice {company}", key=f"company_{company}"):
                st.session_state.company = company

    if st.session_state.company:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        c_label = st.session_state.company
        if c_label == "Custom JD":
            st.markdown("### 📄 Custom JD Interview")
            st.caption("Questions will be generated from your pasted job description.")
        else:
            st.markdown(f"### {c_label} Practice")

        voice_options = [
            "Professional Male (US)",
            "Professional Female (US)",
            "Executive British Male (UK)",
            "British Female (UK)",
            "Indian Professional Male (IN)",
            "Indian Professional Female (IN)",
            "Friendly AI Coach (Neutral)",
        ]
        curr_voice = st.session_state.get("interview_voice", voice_options[0])
        default_idx = voice_options.index(curr_voice) if curr_voice in voice_options else 0

        v1, v2 = st.columns([3, 1])
        with v1:
            selected_voice = st.selectbox(
                "Interview_voices",
                voice_options,
                index=default_idx,
                help="Select the AI interviewer's voice tone and accent",
            )
            st.session_state.interview_voice = selected_voice
        with v2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("🔊 Test Voice", use_container_width=True):
                preview_phrase = f"Hello! I am your {selected_voice} interviewer. Let's begin the interview."
                st.components.v1.html(speak_text_html(preview_phrase, selected_voice), height=0)

        mode = st.radio("Interview mode", ["Timed", "Practice"], horizontal=True)
        st.session_state.mode = mode
        count = st.slider("Number of questions", 3, 10, 5)
        if c_label == "Custom JD":
            st.info("📄 Questions will be generated from your job description + resume skills.")
        else:
            st.info("The interview combines company questions with skills detected in your uploaded resume.")

        if st.button("▶ START INTERVIEW", type="primary", use_container_width=True):
            name = st.session_state.name.strip() or "there"
            first_name = name.split()[0].capitalize()

            # Q0: Introduction question (always first)
            intro_q = {
                "category": "Introduction",
                "question": f"So {first_name}, tell me about yourself — your background, skills, and what you are looking for in this role.",
                "keywords": ["background","skills","experience","project","education","goal","looking"],
                "is_intro": True,
            }

            # Q1: Project Authenticity Probing (included in every interview)
            analysis = st.session_state.resume_analysis or {}
            projs = analysis.get("projects", [])
            primary_proj = projs[0] if projs else "Full-Stack Project"
            project_probe_q = generate_project_authenticity_question(first_name, primary_proj)

            # Resume-Aware Questions generated specifically from candidate's resume
            resume_qs = build_resume_questions(analysis, st.session_state.resume_text or "", first_name)

            # Company or Custom JD Questions
            if c_label == "Custom JD":
                jd_txt = st.session_state.get("jd_text", "")
                company_or_jd_qs = generate_jd_questions(jd_txt, st.session_state.resume_text or "")
            else:
                company_or_jd_qs = get_questions(c_label)

            import random
            random.shuffle(resume_qs)
            random.shuffle(company_or_jd_qs)

            # Seamlessly blend resume-aware questions and company/JD questions
            other_pool = []
            if resume_qs:
                other_pool.extend(resume_qs[:max(1, (count - 2) // 2)])
            other_pool.extend(company_or_jd_qs)
            random.shuffle(other_pool)

            needed = max(0, count - 2)
            if count <= 1:
                all_questions = [intro_q]
            elif count == 2:
                all_questions = [intro_q, project_probe_q]
            else:
                all_questions = [intro_q, project_probe_q] + other_pool[:needed]

            st.session_state.questions = all_questions
            st.session_state.q_index = 0
            st.session_state.answers = []
            st.session_state.current_transcript = ""
            st.session_state.last_transcribed_id = None
            st.session_state.interview_started = True
            st.session_state.question_started_at = time.time()
            st.session_state.pending_followup = None
            st.session_state.answering_followup = False
            st.session_state.followup_parent_idx = -1
            # Reset proctoring state
            st.query_params.clear()
            st.session_state.proctoring_warnings = 0
            st.session_state.interview_cancelled = False
            st.session_state.page = "interview_room"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def _submit_answer(q, transcript):
    result = evaluate_answer(q, transcript)
    sem = semantic_keyword_match(transcript, q.get("keywords", []))
    result["semantic_score"] = sem["score_pct"]
    result["semantic_missed"] = sem["missed"]
    return result

def _advance(total):
    idx = st.session_state.q_index
    st.session_state.current_transcript = ""
    st.session_state.last_transcribed_id = None
    st.session_state.pending_followup = None
    st.session_state.answering_followup = False
    if idx + 1 < total:
        st.session_state.q_index += 1
        st.session_state.question_started_at = time.time()
    else:
        st.session_state.report = build_report(st.session_state.answers)
        st.session_state.page = "report"

def interview_room():
    import random

    # ── Check for Proctoring Cancellation ──────────────────────────────────
    if st.session_state.get("interview_cancelled", False) or st.query_params.get("interview_cancelled") == "true":
        st.session_state.interview_cancelled = True
        st.components.v1.html(get_proctoring_exit_html(), height=0)
        st.markdown("""
        <div style='max-width:720px;margin:35px auto;background:linear-gradient(145deg,#230d12,#130709);border:2px solid #ef4444;border-radius:24px;padding:36px;box-shadow:0 0 60px rgba(239,68,68,0.3);'>
          <div style='text-align:center;'>
            <div style='font-size:3.8rem;margin-bottom:8px;'>⚠️</div>
            <h1 style='color:#ef4444;font-size:2.2rem;letter-spacing:-0.03em;margin:0 0 16px;'>⚠️ URGENT WARNING</h1>
          </div>
          <div style='background:rgba(239,68,68,0.12);border:1.5px solid rgba(239,68,68,0.45);border-radius:16px;padding:22px;margin:20px 0;'>
            <p style='color:#fee2e2;font-size:1.15rem;font-weight:700;line-height:1.6;margin:0 0 14px;'>
              Your interview has been CANCELLED with immediate effect due to a serious issue with your application. 🚨
            </p>
            <p style='color:#fca5a5;font-size:0.95rem;line-height:1.6;margin:0;'>
              Failure to resolve the issue within the required time may result in permanent removal from the interview process and you may no longer be considered for this opportunity.<br>
              <strong style='color:#ffffff;'>Do not ignore this notice.</strong>
            </p>
          </div>
          <div style='margin-top:20px;text-align:center;'>
            <p style='color:#94a3b8;font-size:13px;'>Multiple proctoring violations (unauthorized keys / leaving full-screen mode) were logged during your session.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        c_a, c_b, c_c = st.columns([1, 2, 1])
        with c_b:
            if st.button("🔄 Return to Dashboard", type="primary", use_container_width=True):
                st.query_params.clear()
                st.session_state.interview_cancelled = False
                st.session_state.proctoring_warnings = 0
                st.session_state.page = "interview"
                st.rerun()
        return

    # ── Activate Full-Screen Proctoring Lock ─────────────────────────────────
    st.components.v1.html(get_proctoring_html(max_warnings=4), height=0)

    qs = st.session_state.questions
    if not qs:
        st.session_state.page = "interview"
        st.rerun()
        return

    idx = st.session_state.q_index
    total = len(qs)
    answering_followup = st.session_state.get("answering_followup", False)
    pending_followup   = st.session_state.get("pending_followup", None)

    if answering_followup and pending_followup:
        q = pending_followup
        q_label = f"Q{idx}.1"
        is_followup_round = True
    else:
        q = qs[idx]
        q_label = f"Q{idx}"
        is_followup_round = False

    company_lbl = st.session_state.company or "Interview"
    st.markdown(f"## {get_company_label(company_lbl)} Interview")

    prog = (idx + (0.5 if is_followup_round else 0)) / total
    st.progress(min(prog, 1.0))

    top = st.columns([3, 1])
    with top[0]:
        if is_followup_round:
            badge_html = "<span style='color:#f59e0b;margin-left:6px;font-size:11px'>🔁 FOLLOW-UP</span>"
        elif q.get("is_intro"):
            badge_html = "<span style='color:#22c55e;margin-left:6px;font-size:11px'>🌟 INTRO</span>"
        elif q.get("is_project_probe"):
            badge_html = "<span style='color:#38bdf8;margin-left:6px;font-size:11px'>🔍 PROJECT PROBE</span>"
        elif q.get("is_resume"):
            badge_html = "<span style='color:#a855f7;margin-left:6px;font-size:11px'>📄 RESUME-AWARE</span>"
        else:
            badge_html = ""
        st.markdown(
            f"<div class='question-meta'>{q_label} / {total} • {q['category']}{badge_html}</div>",
            unsafe_allow_html=True
        )
    with top[1]:
        if st.session_state.mode == "Timed":
            LIMIT = 60
            if not st.session_state.question_started_at:
                st.session_state.question_started_at = time.time()
            remaining = max(0, LIMIT - int(time.time() - st.session_state.question_started_at))
            st.markdown(
                f"""
                <div id="career-timer" class="timer timer-normal">&#x23F1; <span id="career-seconds">{remaining:02d}</span> sec</div>
                <script>
                (() => {{
                  let left = {remaining};
                  const el = document.getElementById("career-seconds");
                  const box = document.getElementById("career-timer");
                  const tick = setInterval(() => {{
                    left -= 1;
                    if (!el) {{ clearInterval(tick); return; }}
                    el.textContent = String(Math.max(left, 0)).padStart(2, "0");
                    if (left <= 10) box.className = "timer timer-danger";
                    if (left <= 0) {{ clearInterval(tick); el.textContent = "00"; }}
                  }}, 1000);
                }})();
                </script>
                """,
                unsafe_allow_html=True
            )

    curr_voice = st.session_state.get("interview_voice", "Professional Male (US)")
    avatar = "&#x1F469;&#x200D;&#x1F4BC;" if "Female" in curr_voice else "&#x1F468;&#x200D;&#x1F4BC;"
    bubble_border = "border:2px solid #f59e0b;" if is_followup_round else ""
    st.markdown(
        f"<div class='question-card' style='{bubble_border}'>"
        f"<div class='avatar'>{avatar}</div>"
        f"<div><div style='font-size:12px;color:#a5b4fc;font-weight:600;margin-bottom:4px'>"
        f"&#x1F399;&#xFE0F; {curr_voice}</div>"
        f"<div class='bubble'>{q['question']}</div></div></div>",
        unsafe_allow_html=True
    )
    st.components.v1.html(speak_text_html(q["question"], curr_voice), height=0)

    col_rep, _ = st.columns([1.5, 4])
    with col_rep:
        if st.button("&#x1F50A; Replay", key=f"replay_{idx}_{is_followup_round}"):
            st.components.v1.html(speak_text_html(q["question"], curr_voice), height=0)

    st.markdown(
        "<div class='mic-card'><div class='mic'>&#x1F399;&#xFE0F;</div>"
        "<div class='mic-title'>Speak your answer</div>"
        "<div class='mic-sub'>Click the microphone, speak clearly, stop recording, then wait for transcription.</div></div>",
        unsafe_allow_html=True
    )

    if st.session_state.mode == "Timed" and st.session_state.question_started_at:
        remaining = 60 - int(time.time() - st.session_state.question_started_at)
        if remaining <= 0:
            answer_text = st.session_state.current_transcript.strip() or "(No answer submitted)"
            result = _submit_answer(q, answer_text)
            st.session_state.answers.append(result)
            _advance(total)
            st.rerun()

    audio_key = f"audio_{idx}_{is_followup_round}"
    audio = st.audio_input("&#x1F399;&#xFE0F; Click to record your answer", key=audio_key)
    if audio:
        audio_bytes = audio.getvalue()
        audio_id = (audio_key, len(audio_bytes),
                    hash(audio_bytes[:1000] + audio_bytes[-1000:] if len(audio_bytes) > 2000 else audio_bytes))
        if st.session_state.get("last_transcribed_id") != audio_id:
            with st.spinner("Transcribing..."):
                transcript_val = transcribe_audio(audio)
            st.session_state.last_transcribed_id = audio_id
            if transcript_val:
                st.session_state.current_transcript = transcript_val
                st.success("\u2713 Voice converted to text. Review it below, then submit.")
            else:
                st.warning("Could not detect clear speech. Please speak clearly or type your answer below.")

    transcript = st.text_area(
        "Transcript / answer",
        value=st.session_state.current_transcript,
        height=150,
        placeholder="Your spoken answer will appear here..."
    )
    st.session_state.current_transcript = transcript

    if transcript.strip() and len(transcript.split()) >= 8:
        fl = fluency_report(transcript)
        col_fa, col_fb, col_fc, col_fd = st.columns(4)
        with col_fa: st.metric("&#x1F4F9; Fluency", fl["rating"])
        with col_fb: st.metric("&#x1F4DD; Words", fl["word_count"])
        with col_fc: st.metric("&#x1F6AB; Fillers", fl["filler_count"])
        with col_fd: st.metric("&#x1F4D6; Readability", f"{fl['readability_score']}/100")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("\u23f9 STOP / SUBMIT", use_container_width=True, key=f"submit_{idx}_{is_followup_round}"):
            if transcript.strip():
                result = _submit_answer(q, transcript)
                st.session_state.answers.append(result)
                st.session_state.current_transcript = ""
                st.session_state.last_transcribed_id = None

                if is_followup_round:
                    _advance(total)
                    st.rerun()
                else:
                    should_followup = q.get("is_intro", False) or q.get("is_project_probe", False) or random.random() < 0.50
                    if should_followup:
                        name_str = st.session_state.name.strip() or "there"
                        c_first = name_str.split()[0].capitalize()
                        p_name = q.get("project_name", "")
                        fq_text = generate_followup(transcript, q["question"], candidate_name=c_first, project_name=p_name)
                        st.session_state.pending_followup = {
                            "category": q["category"],
                            "question": fq_text,
                            "keywords": q.get("keywords", []),
                            "is_followup": True,
                        }
                        st.session_state.answering_followup = True
                        st.session_state.question_started_at = time.time()
                        st.rerun()
                    else:
                        _advance(total)
                        st.rerun()
            else:
                st.warning("Please provide an answer first.")

    with c2:
        disabled = st.session_state.mode == "Timed"
        if st.button("NEXT QUESTION", disabled=disabled, use_container_width=True, key=f"next_{idx}_{is_followup_round}"):
            if transcript.strip():
                result = _submit_answer(q, transcript)
                st.session_state.answers.append(result)
            else:
                st.session_state.answers.append(evaluate_answer(q, ""))
            _advance(total)
            st.rerun()

    with c3:
        if st.button("\u21a9 EXIT", use_container_width=True, key=f"exit_{idx}_{is_followup_round}"):
            st.components.v1.html(get_proctoring_exit_html(), height=0)
            st.session_state.current_transcript = ""
            st.session_state.last_transcribed_id = None
            st.session_state.pending_followup = None
            st.session_state.answering_followup = False
            st.session_state.page = "interview"
            st.rerun()


def build_report(answers):
    if not answers:
        return {"score": 0, "answers": []}
    score = round(sum(a["score"] for a in answers) / len(answers))
    technical = round(sum(a["concept_score"] for a in answers) / len(answers))
    relevance = round(sum(a["relevance"] for a in answers) / len(answers))
    strengths, weaknesses = [], []
    for a in answers:
        strengths.extend(a["strengths"])
        weaknesses.extend(a["weaknesses"])
    return {
        "score": score,
        "technical": technical,
        "relevance": relevance,
        "answers": answers,
        "strengths": list(dict.fromkeys(strengths))[:5],
        "weaknesses": list(dict.fromkeys(weaknesses))[:5],
    }

def report_page():
    r = st.session_state.report
    if not r:
        st.info("Complete an interview to see the report.")
        return

    st.components.v1.html(get_proctoring_exit_html(), height=0)
    st.markdown("## Interview Report")
    st.markdown("<div class='report-hero'>", unsafe_allow_html=True)
    st.markdown(f"<div class='report-score'>{r['score']}<small>/100</small></div>", unsafe_allow_html=True)
    st.markdown(f"<div><h2>{st.session_state.company} • {st.session_state.mode}</h2><p>{len(r['answers'])} questions attempted</p></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: metric_card("Technical / Concepts", f"{r['technical']}%", "Concept coverage")
    with c2: metric_card("Answer Relevance", f"{r['relevance']}%", "Question ↔ answer")
    with c3: metric_card("Questions", str(len(r["answers"])), "Attempted")

    left, right = st.columns(2)
    with left:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        section_title("Strengths")
        for x in r["strengths"] or ["Complete more questions to build a stronger signal."]:
            st.markdown(f"<div class='check good'>✓ {x}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        section_title("Improvement areas")
        for x in r["weaknesses"] or ["Keep practicing structured technical answers."]:
            st.markdown(f"<div class='check warn'>⚠ {x}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Feature 6: Weakness Cluster Report ───────────────────────────────────
    clusters = weakness_cluster_report(r["answers"])
    if clusters:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        section_title("🧩 Personalized Learning Roadmap (NLP Weakness Clusters)")
        st.caption("Topics where you scored below 60 — ranked by how many questions you struggled with.")
        for cl in clusters:
            bar_pct = max(5, cl["avg_score"])
            bar_color = "#ef4444" if cl["avg_score"] < 35 else "#f59e0b" if cl["avg_score"] < 55 else "#3b82f6"
            st.markdown(f"""
            <div style='margin:.6rem 0;padding:.8rem 1rem;background:rgba(255,255,255,.04);
                 border-radius:10px;border-left:3px solid {bar_color}'>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <span style='font-weight:700;color:#e2e8f0'>{cl['topic']}</span>
                <span style='color:{bar_color};font-weight:600'>{cl['avg_score']}/100 avg</span>
              </div>
              <div style='background:#1e293b;border-radius:4px;height:6px;margin:.4rem 0'>
                <div style='background:{bar_color};width:{bar_pct}%;height:6px;border-radius:4px'></div>
              </div>
              <span style='font-size:12px;color:#94a3b8'>{cl['count']} weak answer(s) — 
                <a href='{cl["link"]}' target='_blank' style='color:#818cf8'>Study resource →</a>
              </span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Question-wise analysis with Fluency + Semantic ────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    section_title("Question-wise analysis")
    for i, a in enumerate(r["answers"], 1):
        sem_txt = ""
        if a.get("semantic_score") is not None:
            sem_txt = f" • Semantic: {a['semantic_score']}%"
        fl = fluency_report(a.get("answer", ""))
        with st.expander(f"{i}. {a['question']}  —  {a['score']}/100"):
            st.write(a["feedback"])
            st.caption(f"Words: {a['word_count']} • Sentences: {a['sentence_count']} • Filler words: {a['fillers']}{sem_txt}")
            # Fluency sub-report
            st.markdown(f"""
            <div style='margin-top:.5rem;padding:.6rem .9rem;background:rgba(99,102,241,.08);
                 border-radius:8px;border:1px solid rgba(99,102,241,.2)'>
              <span style='font-size:11px;color:#a5b4fc;font-weight:700'>FLUENCY REPORT</span><br>
              <span style='color:#e2e8f0'>📈 Rating: <b>{fl['rating']}</b> • Readability: {fl['readability_score']}/100 • Vocab richness: {fl['ttr']}</span><br>
              <span style='font-size:12px;color:#94a3b8'>{' '.join(fl['suggestions'])}</span>
            </div>""", unsafe_allow_html=True)
            if a.get("semantic_missed"):
                st.caption(f"Semantically missed concepts: {', '.join(a['semantic_missed'][:5])}")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🎙️ Practice Again", type="primary", use_container_width=True):
        st.session_state.page = "interview"
        st.rerun()

def _cs_random_drill_view():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2.5, 1.8, 1.8])
    with c1:
        subject_options = ["All CS Core Subjects"] + list(CS_CORE_SUBJECTS.keys())
        curr_subj = st.session_state.get("cs_active_subject", "All CS Core Subjects")
        idx_subj = subject_options.index(curr_subj) if curr_subj in subject_options else 0
        new_subj = st.selectbox("Subject Filter", subject_options, index=idx_subj, key="cs_subj_select")
        if new_subj != curr_subj:
            st.session_state.cs_active_subject = new_subj
            st.session_state.cs_current_question = get_random_cs_question(
                new_subj, st.session_state.get("cs_active_difficulty")
            )
            st.session_state.cs_evaluation = None
            st.rerun()

    with c2:
        diff_options = ["All Difficulties", "Easy", "Medium", "Hard"]
        curr_diff = st.session_state.get("cs_active_difficulty", "All Difficulties")
        idx_diff = diff_options.index(curr_diff) if curr_diff in diff_options else 0
        new_diff = st.selectbox("Difficulty Filter", diff_options, index=idx_diff, key="cs_diff_select")
        if new_diff != curr_diff:
            st.session_state.cs_active_difficulty = new_diff
            st.session_state.cs_current_question = get_random_cs_question(
                st.session_state.get("cs_active_subject"), new_diff
            )
            st.session_state.cs_evaluation = None
            st.rerun()

    with c3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("🎲 Pick Random Question", key="cs_btn_random_pick", use_container_width=True):
            curr_id = st.session_state.cs_current_question.get("id") if st.session_state.cs_current_question else None
            st.session_state.cs_current_question = get_random_cs_question(
                st.session_state.get("cs_active_subject"),
                st.session_state.get("cs_active_difficulty"),
                exclude_id=curr_id
            )
            st.session_state.cs_evaluation = None
            st.rerun()

    # Ensure a question is active
    if not st.session_state.get("cs_current_question"):
        st.session_state.cs_current_question = get_random_cs_question(
            st.session_state.get("cs_active_subject"),
            st.session_state.get("cs_active_difficulty")
        )

    q = st.session_state.get("cs_current_question")
    if not q:
        st.warning("No questions found matching your filter criteria. Try adjusting the subject or difficulty.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Question Display Card
    subj_icon = CS_CORE_SUBJECTS.get(q["subject"], "💻")
    diff_badge_color = "#34d399" if q["difficulty"] == "Easy" else ("#fbbf24" if q["difficulty"] == "Medium" else "#f87171")
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;align-items:center;margin-top:10px;margin-bottom:6px;'>
        <div>
            <span style='background:rgba(167,139,250,.15);border:1px solid rgba(167,139,250,.3);color:#c4b5fd;padding:4px 10px;border-radius:12px;font-size:12px;font-weight:700;'>
                {subj_icon} {q['subject']}
            </span>
            <span style='color:#a78bfa;font-size:13px;margin-left:8px;font-weight:600;'>
                Topic: {q['topic']}
            </span>
        </div>
        <span style='background:rgba(255,255,255,.05);border:1px solid {diff_badge_color}44;color:{diff_badge_color};padding:3px 9px;border-radius:10px;font-size:11px;font-weight:700;'>
            {q['difficulty']}
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='question-card' style='margin:12px 0 18px;'>
      <div class='avatar'>🤖</div>
      <div class='bubble' style='font-weight:600;color:#f5f3ff;'>{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Audio Speaker control
    v_cols = st.columns([2, 5])
    with v_cols[0]:
        if st.button("🔊 Read Question Aloud", key=f"cs_speak_{q['id']}", use_container_width=True):
            voice = st.session_state.get("interview_voice", "Professional Male (US)")
            st.components.v1.html(speak_text_html(q["question"], voice), height=0)

    st.markdown("---")

    # Answering section
    st.markdown("#### ✍️ Your Answer")
    tab_voice, tab_text = st.tabs(["🎙️ Speak Answer (Microphone)", "⌨️ Type Answer"])
    
    transcript = ""
    with tab_voice:
        st.caption("Click to record your voice answer via microphone:")
        audio_val = st.audio_input("Record your answer", key=f"cs_audio_{q['id']}")
        if audio_val:
            try:
                transcript = transcribe_audio(audio_val.read())
                if transcript:
                    st.success(f"✓ Transcribed: {transcript}")
                else:
                    st.warning("Could not transcribe speech. Please type your answer or try again.")
            except Exception as e:
                st.warning(f"Voice transcription note: {e}")

    with tab_text:
        text_val = st.text_area(
            "Type your response",
            value=transcript if transcript else st.session_state.get(f"cs_text_{q['id']}", ""),
            height=130,
            placeholder="Structure your answer with definitions, properties, comparisons, and examples...",
            key=f"cs_text_area_{q['id']}"
        )

    final_ans = (transcript or text_val).strip()

    col_sub, col_next = st.columns([2.5, 1.5])
    with col_sub:
        if st.button("🎯 Submit Answer & Evaluate", type="primary", use_container_width=True, key=f"cs_submit_{q['id']}"):
            if not final_ans:
                st.warning("Please record or type your answer before submitting.")
            else:
                eval_res = evaluate_answer(q, final_ans)
                sem = semantic_keyword_match(final_ans, q.get("keywords", []))
                eval_res["semantic_score"] = sem["score_pct"]
                eval_res["semantic_missed"] = sem["missed"]
                eval_res["fluency"] = fluency_report(final_ans)
                eval_res["subject"] = q["subject"]
                eval_res["topic"] = q["topic"]
                st.session_state.cs_evaluation = eval_res
                st.session_state.cs_history.append({
                    "id": q["id"],
                    "question": q["question"],
                    "subject": q["subject"],
                    "topic": q["topic"],
                    "score": eval_res["score"],
                    "semantic_score": sem["score_pct"],
                })
                st.rerun()

    with col_next:
        if st.button("➡️ Next Random Question", use_container_width=True, key=f"cs_next_btn_{q['id']}"):
            st.session_state.cs_current_question = get_random_cs_question(
                st.session_state.get("cs_active_subject"),
                st.session_state.get("cs_active_difficulty"),
                exclude_id=q["id"]
            )
            st.session_state.cs_evaluation = None
            st.rerun()

    # Evaluation Feedback Card
    ev = st.session_state.get("cs_evaluation")
    if ev:
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,rgba(30,20,50,.9),rgba(15,10,25,.95));
                    border:1px solid rgba(167,139,250,.35);border-radius:18px;padding:20px;margin-top:12px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <h3 style='margin:0;color:#e9d5ff;'>Evaluation: <span style='color:#a78bfa;'>{ev['score']}/100</span></h3>
                <span style='color:#94a3b8;font-size:12px;'>Semantic Match: {ev.get('semantic_score', 0)}%</span>
            </div>
            <p style='color:#cbd5e1;margin:8px 0;'>{ev['feedback']}</p>
        </div>
        """, unsafe_allow_html=True)

        fb_c1, fb_c2 = st.columns(2)
        with fb_c1:
            st.markdown("<b>Concepts Covered:</b>", unsafe_allow_html=True)
            hits = [k for k in q.get("keywords", []) if k.lower() in ev.get("answer", "").lower()]
            if hits:
                for h in hits:
                    st.markdown(f"<div class='check good'>✓ {h}</div>", unsafe_allow_html=True)
            else:
                st.caption("No specific expected keywords matched.")

        with fb_c2:
            st.markdown("<b>Expected Concepts to Include:</b>", unsafe_allow_html=True)
            missed = [k for k in q.get("keywords", []) if k.lower() not in ev.get("answer", "").lower()]
            if missed:
                for m in missed:
                    st.markdown(f"<div class='check warn'>⚠ {m}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='check good'>✓ Excellent coverage of all key terms!</div>", unsafe_allow_html=True)

        if "fluency" in ev:
            fl = ev["fluency"]
            st.markdown(f"""
            <div style='margin-top:10px;padding:.6rem .9rem;background:rgba(99,102,241,.08);
                 border-radius:10px;border:1px solid rgba(99,102,241,.25)'>
                <span style='font-size:11px;color:#a5b4fc;font-weight:700'>NLP FLUENCY & DELIVERY</span><br>
                <span style='color:#e2e8f0;font-size:13px;'>📈 Delivery Rating: <b>{fl.get('rating','Good')}</b> • Readability: {fl.get('readability_score', 70)}/100 • Vocabulary Richness: {fl.get('ttr', 0.8)}</span><br>
                <span style='font-size:12px;color:#94a3b8;'>{' '.join(fl.get('suggestions', []))}</span>
            </div>
            """, unsafe_allow_html=True)

    # Model Answer Expander
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    with st.expander("💡 View Complete Subject Model Answer & Key Points", expanded=bool(ev)):
        st.markdown(f"### 📘 Model Answer ({q['subject']} • {q['topic']})")
        st.markdown(q["answer"])
        
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Key Interview Points to Mention:")
        for pt in q.get("key_points", []):
            st.markdown(f"• {pt}")

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.markdown(f"**Expected Technical Keywords:** `{', '.join(q.get('keywords', []))}`")

    st.markdown("</div>", unsafe_allow_html=True)

    # Session Stats
    hist = st.session_state.get("cs_history", [])
    if hist:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        section_title("📊 Your CS Core Practice Session")
        s1, s2, s3 = st.columns(3)
        with s1:
            metric_card("Questions Practiced", str(len(hist)), "In this session")
        with s2:
            avg_sc = round(sum(h["score"] for h in hist) / len(hist))
            metric_card("Average Score", f"{avg_sc}/100", "Across all questions")
        with s3:
            last_subj = hist[-1]["subject"]
            metric_card("Last Practiced", last_subj, hist[-1].get("topic", ""))
        st.markdown("</div>", unsafe_allow_html=True)

def _cs_knowledge_bank_view():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    section_title("📖 Subject-Wise CS Core Knowledge Bank")
    st.caption("Browse textbook-quality model answers and key interview takeaways organized by CS subject.")

    search_q = st.text_input("🔍 Search question, topic, or keyword...", "", key="cs_bank_search")
    
    subjects = ["All Subjects"] + list(CS_CORE_SUBJECTS.keys())
    tabs = st.tabs([f"{CS_CORE_SUBJECTS.get(s, '📚')} {s}" if s in CS_CORE_SUBJECTS else "📚 All Subjects" for s in subjects])

    for idx, s in enumerate(subjects):
        with tabs[idx]:
            if s == "All Subjects":
                questions = search_cs_bank(search_q) if search_q else CS_CORE_QUESTIONS
            else:
                raw_pool = [q for q in CS_CORE_QUESTIONS if q["subject"] == s]
                questions = [q for q in raw_pool if (not search_q or search_q.lower() in f"{q['topic']} {q['question']} {q['answer']} {' '.join(q['keywords'])}".lower())]

            if not questions:
                st.caption(f"No questions found matching your filter.")
            else:
                for q_idx, q in enumerate(questions, start=1):
                    diff_badge_color = "#34d399" if q["difficulty"] == "Easy" else ("#fbbf24" if q["difficulty"] == "Medium" else "#f87171")
                    with st.expander(f"{q_idx}. [{q['subject']}] {q['topic']}: {q['question']}"):
                        st.markdown(f"""
                        <div style='display:flex;gap:10px;margin-bottom:8px;'>
                            <span style='background:rgba(167,139,250,.15);color:#c4b5fd;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700;'>
                                {q['subject']}
                            </span>
                            <span style='background:rgba(255,255,255,.05);color:{diff_badge_color};padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700;'>
                                {q['difficulty']}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("#### 📘 Model Answer:")
                        st.markdown(q["answer"])

                        st.markdown("#### 🎯 Key Interview Points:")
                        for pt in q.get("key_points", []):
                            st.markdown(f"• {pt}")

                        st.markdown(f"**Keywords:** `{', '.join(q.get('keywords', []))}`")
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("🎯 Practice This Question in Drill", key=f"bank_practice_{idx}_{q['id']}"):
                            st.session_state.cs_current_question = q
                            st.session_state.cs_view = "drill"
                            st.session_state.cs_evaluation = None
                            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def cs_core_page():
    st.markdown("""
    <div class="hero" style="padding: 24px 10px 18px;">
      <div class="eyebrow">CS CORE MASTERCLASS</div>
      <h1 style="margin: 6px 0 12px !important;">Core CS Practice & Answers</h1>
      <p>Sharpen your fundamentals in Operating Systems, DBMS & SQL, Computer Networks, OOP, and DSA. Practice random questions with instant AI evaluation or explore full subject-wise model answers.</p>
    </div>
    """, unsafe_allow_html=True)

    v1, v2 = st.columns([1, 1])
    drill_selected = st.session_state.get("cs_view", "drill") == "drill"
    with v1:
        if st.button("🎲 Random Question Drill", use_container_width=True, type="primary" if drill_selected else "secondary"):
            st.session_state.cs_view = "drill"
            st.rerun()
    with v2:
        if st.button("📖 Subject-Wise Q&A Knowledge Bank", use_container_width=True, type="primary" if not drill_selected else "secondary"):
            st.session_state.cs_view = "bank"
            st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if st.session_state.get("cs_view", "drill") == "drill":
        _cs_random_drill_view()
    else:
        _cs_knowledge_bank_view()

def main():
    nav()
    page = st.session_state.page
    if page == "home":
        home()
    elif page == "analysis":
        analysis_page()
    elif page == "interview":
        interview_dashboard()
    elif page == "interview_room":
        interview_room()
    elif page == "jd_match":
        jd_match_page()
    elif page == "cs_core":
        cs_core_page()
    elif page == "report":
        report_page()

if __name__ == "__main__":
    main()
