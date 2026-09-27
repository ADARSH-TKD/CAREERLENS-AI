import re

SKILLS = {
    "Programming": ["java", "python", "c++", "javascript"],
    "Web": ["react", "angular", "spring boot", "node.js"],
    "Database": ["mysql", "postgresql", "mongodb"],
    "Cloud": ["aws", "azure", "gcp"],
    "AI/ML": ["machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "word2vec", "opencv"],
    "DevOps": ["docker", "kubernetes", "git", "ci/cd"],
    "CS": ["dsa", "data structures", "algorithms", "oop", "dbms", "operating systems", "networking"],
}

SECTION_ALIASES = {
    "Summary": ["summary", "profile", "objective"],
    "Education": ["education", "academic"],
    "Skills": ["skills", "technical skills"],
    "Experience": ["experience", "work experience"],
    "Internships": ["internship", "internships"],
    "Projects": ["projects", "project"],
    "Certifications": ["certifications", "certificates"],
    "Achievements": ["achievements", "awards"],
    "Publications": ["publications", "research"],
    "Contact": ["contact"],
}

_nltk_checked = False

def _ensure_nltk_data():
    global _nltk_checked
    if _nltk_checked:
        return
    import nltk
    for res in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]:
        try:
            nltk.data.find(f"tokenizers/{res}" if "punkt" in res else f"corpora/{res}")
        except LookupError:
            try:
                nltk.download(res, quiet=True)
            except Exception:
                pass
    _nltk_checked = True


def analyze_resume(text):
    _ensure_nltk_data()
    import nltk
    import spacy
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        try:
            import spacy.cli
            spacy.cli.download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
        except Exception:
            nlp = None

    try:
        sentences = nltk.sent_tokenize(text)
    except Exception:
        sentences = re.split(r"(?<=[.!?])\s+", text)

    try:
        tokens = nltk.word_tokenize(text)
    except Exception:
        tokens = re.findall(r"\b[\w+#.-]+\b", text)

    try:
        sw = set(stopwords.words("english"))
    except Exception:
        sw = set()

    try:
        lem = WordNetLemmatizer()
        clean_tokens = [lem.lemmatize(t.lower()) for t in tokens if t.isalpha() and t.lower() not in sw]
    except Exception:
        clean_tokens = [t.lower() for t in tokens if t.isalpha() and t.lower() not in sw]

    lower = text.lower()

    found_skills = []
    for group, vals in SKILLS.items():
        for skill in vals:
            if re.search(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", lower):
                found_skills.append(skill.title() if skill != "c++" else "C++")

    sections = []
    for canonical, aliases in SECTION_ALIASES.items():
        if any(re.search(rf"(?im)^\s*{re.escape(a)}\s*:?\s*$", text) for a in aliases):
            sections.append(canonical)

    email = bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))
    phone = bool(re.search(r"(?:\+91[\s-]?)?[6-9]\d{9}", re.sub(r"[()]", "", text)))
    urls = re.findall(r"https?://\S+|(?:www\.)\S+", text)
    github = "github.com" in lower
    linkedin = "linkedin.com" in lower
    percentages = re.findall(r"\b\d{1,3}(?:\.\d+)?\s?%", text)
    cgpa = re.findall(r"\b\d(?:\.\d{1,2})?\s*(?:/10)?\s*cgpa\b|\bcgpa\s*[:\-]?\s*\d(?:\.\d{1,2})?", lower)

    entities = []
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in {"PERSON", "ORG", "GPE", "DATE", "MONEY"}:
                entities.append({"text": ent.text, "label": ent.label_})

    projects = extract_projects(text, found_skills)

    return {
        "sentences": sentences,
        "tokens": tokens,
        "clean_tokens": clean_tokens,
        "skills": list(dict.fromkeys(found_skills)),
        "sections": sections,
        "entities": entities,
        "projects": projects,
        "contact": {"email": email, "phone": phone, "github": github, "linkedin": linkedin, "urls": urls},
        "percentages": percentages,
        "cgpa": cgpa,
    }


def extract_projects(text: str, found_skills: list = None) -> list:
    """
    Extract claimed projects from resume text with name, clean title, and detected tech stack.
    Guarantees at least one project by falling back to skill-based realistic project inference.
    """
    if not text or not text.strip():
        return _fallback_projects(found_skills)

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    in_project_section = False
    
    # 1. Look for explicit project section
    project_headers = ["projects", "academic projects", "personal projects", "key projects", "project experience", "technical projects"]
    other_headers = ["education", "skills", "experience", "work experience", "certifications", "achievements", "publications", "contact", "summary", "objective"]

    sec_lines = []
    for line in lines:
        cleaned_h = re.sub(r"[:\-_#*]", "", line.strip().lower()).strip()
        if any(cleaned_h == h for h in project_headers):
            in_project_section = True
            continue
        elif in_project_section and any(cleaned_h == h for h in other_headers):
            in_project_section = False
            break
        elif in_project_section:
            sec_lines.append(line)

    candidates = []
    if sec_lines:
        for idx, line in enumerate(sec_lines):
            # Ignore bullet lines starting with common action verbs
            if re.match(r"^[-*•]\s*(?:developed|built|implemented|created|designed|used|worked|integrated|trained|achieved|optimized|collaborated|maintained|tested)\b", line, re.I):
                continue
            if re.match(r"^(?:developed|built|implemented|created|designed|used|worked|integrated|trained|achieved|optimized|collaborated|maintained|tested)\b", line, re.I):
                continue

            # Strip bullet markers or leading numbers
            clean = re.sub(r"^[-*•\d\.)\s]+", "", line).strip()
            # Split off date ranges or URLs
            clean = re.split(r"\s*\|\s*|\s*–\s*|\s*—\s*|\s*\(\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4})", clean)[0].strip()
            clean = re.sub(r"[\(\[\{].*?[\)\]\}]", "", clean).strip()

            if 3 <= len(clean) <= 65 and not clean.endswith("."):
                words = clean.split()
                if len(words) <= 9 and (any(w[0].isupper() for w in words if w.isalpha()) or any(k in clean.lower() for k in ["system", "app", "platform", "portal", "bot", "engine", "analyzer", "dashboard", "tool", "tracker", "web", "ai", "network", "management"])):
                    next_text = " ".join(sec_lines[idx:idx+3])
                    tech = [s for s in (found_skills or []) if s.lower() in next_text.lower()]
                    candidates.append({"name": clean, "tech_stack": tech, "inferred": False})

    # 2. If no candidate found from section, scan whole text with regex patterns
    if not candidates:
        project_regexes = [
            r"(?:project\s*(?:title)?\s*[:\-]|title\s*[:\-])\s*([A-Za-z0-9\s\-]{3,50})",
            r"(?:built|developed|created|designed)\s+(?:a|an)?\s*([A-Z][A-Za-z0-9\s\-]{2,40}\s+(?:System|App|Platform|Portal|Bot|Tracker|Engine|Analyzer|Dashboard|Tool|Classifier|Detector|Manager|Application))",
            r"\b([A-Z][A-Za-z0-9\s\-]{2,30}\s+(?:System|Application|App|Platform|Portal|Bot|Tracker|Engine|Analyzer|Dashboard|Tool|Classifier|Detector|Manager))\b",
        ]
        for pat in project_regexes:
            matches = re.findall(pat, text)
            for m in matches:
                clean_m = m.strip()
                if 3 <= len(clean_m) <= 60 and clean_m.lower() not in ["the project", "this project", "a project"]:
                    candidates.append({"name": clean_m, "tech_stack": [], "inferred": False})
                if len(candidates) >= 3:
                    break

    # Deduplicate candidates by lowercase name
    unique_projects = []
    seen = set()
    for c in candidates:
        low = c["name"].lower()
        if low not in seen and len(c["name"]) > 2:
            seen.add(low)
            unique_projects.append(c)

    return unique_projects if unique_projects else _fallback_projects(found_skills)


def _fallback_projects(found_skills: list = None) -> list:
    """Generate realistic inferred project when resume does not have explicit project headers."""
    skills = [s.lower() for s in (found_skills or [])]
    if any(s in skills for s in ["machine learning", "deep learning", "nlp", "ai"]):
        return [{
            "name": "AI-Powered Predictive Analytics & Intelligent NLP System",
            "tech_stack": ["Python", "Machine Learning", "NLP"],
            "inferred": True
        }]
    elif any(s in skills for s in ["react", "angular", "node.js", "javascript"]):
        return [{
            "name": "Full-Stack Responsive Web Application & Analytics Dashboard",
            "tech_stack": ["React", "Node.js", "REST APIs"],
            "inferred": True
        }]
    elif any(s in skills for s in ["java", "spring boot"]):
        return [{
            "name": "Enterprise Microservices Management & Database Platform",
            "tech_stack": ["Java", "Spring Boot", "MySQL"],
            "inferred": True
        }]
    elif any(s in skills for s in ["python"]):
        return [{
            "name": "Automated Data Ingestion & Real-Time Analytics Pipeline",
            "tech_stack": ["Python", "Data Processing", "APIs"],
            "inferred": True
        }]
    else:
        return [{
            "name": "Full-Stack Web & Database Management Platform",
            "tech_stack": ["Web Development", "Database", "Software Architecture"],
            "inferred": True
        }]

