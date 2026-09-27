"""
nlp_features.py  –  All advanced NLP features for CareerLens AI
================================================================
Features:
  1. jd_match_score          – Resume ↔ Job Description TF-IDF cosine similarity
  2. generate_followup        – Smart follow-up question from previous answer
  3. fluency_report           – Readability, vocabulary richness, sentence stats
  4. semantic_keyword_match   – spaCy vector-based synonym-aware keyword matching
  5. ner_resume_dashboard     – Enhanced NER entity extraction and categorisation
  6. weakness_cluster_report  – Cluster weak answers by topic after interview
"""

import re
from collections import defaultdict


# ──────────────────────────────────────────────────────────────
# 1. Resume <-> Job Description Matcher (TF-IDF + cosine)
# ──────────────────────────────────────────────────────────────
def jd_match_score(resume_text: str, jd_text: str) -> dict:
    """
    Returns:
      match_pct        – 0-100 percentage overall cosine similarity
      matched_keywords – list of JD keywords found in resume
      missing_keywords – list of JD keywords NOT found in resume
      suggestions      – short human-readable tips
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        return {"match_pct": 0, "matched_keywords": [], "missing_keywords": [],
                "suggestions": ["Install scikit-learn to enable JD matching."]}

    docs = [resume_text, jd_text]
    try:
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf = vec.fit_transform(docs)
        sim = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
        match_pct = round(sim * 100)
    except Exception:
        match_pct = 0

    jd_lower = jd_text.lower()
    resume_lower = resume_text.lower()
    jd_tokens_raw = re.findall(r"\b[a-z][a-z0-9#+\-.]{2,}\b", jd_lower)
    _stop = {
        "the","and","for","are","with","you","your","will","this","that","have","has","from",
        "not","but","can","was","were","been","our","their","more","also","any","all","its",
        "they","who","what","how","into","about","would","should","could","must","may","which",
        "required","experience","skills","role","work","team","company","candidate","responsible",
        "working","including","strong","ability","knowledge","years","minimum","excellent",
        "good","etc","other","well","both","use","using","used","based","along","across",
        "provides","provide","develop","development","ensure","manage","support","help","focus",
    }
    jd_keywords = [t for t in dict.fromkeys(jd_tokens_raw) if t not in _stop and len(t) > 3][:80]
    matched = [k for k in jd_keywords if k in resume_lower]
    missing = [k for k in jd_keywords if k not in resume_lower]

    suggestions = []
    if match_pct < 40:
        suggestions.append("Low match — rewrite key bullet points to mirror JD language.")
    elif match_pct < 65:
        suggestions.append("Moderate match — add more JD-specific keywords to your resume.")
    else:
        suggestions.append("Good match — fine-tune missing keywords for higher ATS scores.")
    if missing[:5]:
        suggestions.append(f"Consider adding: {', '.join(missing[:5])}")

    return {
        "match_pct": match_pct,
        "matched_keywords": matched[:30],
        "missing_keywords": missing[:30],
        "suggestions": suggestions,
    }


# ──────────────────────────────────────────────────────────────
# 2. Smart Follow-Up Question Generator
# ──────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────
# 2. Smart Concept-Aware Follow-Up Question Generator
# ──────────────────────────────────────────────────────────────

_CONCEPT_KNOWLEDGE = [
    {
        "patterns": [r"\bartificial\s+intell?igen\w*\b", r"\bai\b"],
        "display": "Artificial Intelligence",
        "related": "deep learning and neural networks",
        "explain": "can you explain what it is and how machine learning algorithms learn patterns from training data",
        "tradeoff": "how do you evaluate bias, hallucination, or prediction drift in AI models"
    },
    {
        "patterns": [r"\bdeep\s+learning\b", r"\bneural\s+networks?\b", r"\bcnn\b", r"\brnn\b", r"\blstm\b", r"\btransformers?\b"],
        "display": "Deep Learning",
        "related": "backpropagation, gradient descent, and convolutional neural networks",
        "explain": "can you explain how activation functions and weight updates work during model training",
        "tradeoff": "how would you prevent overfitting and handle the vanishing gradient problem"
    },
    {
        "patterns": [r"\bmachine\s+learning\b", r"\bsupervised\b", r"\bunsupervised\b", r"\bclustering\b", r"\bregression\b", r"\bclassification\b"],
        "display": "Machine Learning",
        "related": "feature engineering, hyperparameter tuning, and cross-validation",
        "explain": "can you explain what it is and how you evaluate performance using precision, recall, and ROC-AUC",
        "tradeoff": "how do you handle high-dimensional sparse data and class imbalance"
    },
    {
        "patterns": [r"\bnlp\b", r"\bnatural\s+language\s+processing\b", r"\btokenization\b", r"\blemmatization\b", r"\bword2vec\b", r"\bembeddings?\b"],
        "display": "Natural Language Processing",
        "related": "transformer self-attention, BERT, and dense semantic embeddings",
        "explain": "can you explain how tokenization and semantic word representations work under the hood",
        "tradeoff": "what are the computational trade-offs between TF-IDF and deep contextual embeddings"
    },
    {
        "patterns": [r"\breact\b", r"\breact\.?js\b", r"\bvirtual\s+dom\b", r"\buseeffect\b", r"\busestate\b", r"\bhছেনs\b"],
        "display": "React",
        "related": "Virtual DOM reconciliation, state management, and component lifecycle",
        "explain": "can you explain what it is and how the Virtual DOM minimizes expensive browser reflows",
        "tradeoff": "how do you prevent unnecessary re-renders using useMemo, useCallback, or React.memo"
    },
    {
        "patterns": [r"\bjava\b", r"\bjvm\b", r"\bspring\s+boot\b", r"\bgarbage\s+collect\w*\b"],
        "display": "Java",
        "related": "JVM memory management, garbage collection, and multithreading",
        "explain": "can you explain how the Java Virtual Machine manages heap versus stack memory allocation",
        "tradeoff": "how do you handle memory leaks and race conditions in concurrent Java applications"
    },
    {
        "patterns": [r"\bpython\b", r"\bgil\b", r"\bpandas\b", r"\bnumpy\b", r"\bflask\b", r"\bdjango\b"],
        "display": "Python",
        "related": "the Global Interpreter Lock (GIL), generators, and asynchronous event loops",
        "explain": "can you explain how Python manages memory via reference counting and garbage collection",
        "tradeoff": "how would you overcome CPU-bound bottlenecks given Python's single-threaded GIL"
    },
    {
        "patterns": [r"\bsql\b", r"\bdatabases?\b", r"\bdbms\b", r"\bmysql\b", r"\bpostgresql\b", r"\bnormalization\b"],
        "display": "databases and SQL",
        "related": "indexing strategies, B-trees, and query optimization",
        "explain": "can you explain what normalization is and how indexing speeds up query execution",
        "tradeoff": "how do ACID transaction isolation levels protect against dirty reads and phantom rows"
    },
    {
        "patterns": [r"\bnosql\b", r"\bmongodb\b", r"\bdocument\s+db\b", r"\bredis\b", r"\bcaching\b"],
        "display": "NoSQL and caching",
        "related": "eventual consistency, distributed sharding, and in-memory key-value lookups",
        "explain": "can you explain when you would choose NoSQL over a relational database",
        "tradeoff": "how do you handle cache invalidation and data synchronization bottlenecks"
    },
    {
        "patterns": [r"\bdocker\b", r"\bcontainers?\b", r"\bcontainerization\b", r"\bdockerfile\b"],
        "display": "Docker containerization",
        "related": "Kubernetes pod orchestration and microservice deployment pipelines",
        "explain": "can you explain how Docker containers differ from virtual machines at the OS kernel level",
        "tradeoff": "how do multi-stage Docker builds reduce container attack surface and image size"
    },
    {
        "patterns": [r"\bkubernetes\b", r"\bk8s\b", r"\bpods?\b", r"\bhelm\b"],
        "display": "Kubernetes",
        "related": "automated rolling deployments, service discovery, and horizontal pod autoscaling",
        "explain": "can you explain how Kubernetes monitors node health and triggers pod self-healing",
        "tradeoff": "how do you configure resource requests and limits to prevent noisy neighbor problems"
    },
    {
        "patterns": [r"\bcloud\b", r"\baws\b", r"\bazure\b", r"\bgcp\b", r"\bserverless\b", r"\blambda\b"],
        "display": "Cloud Computing",
        "related": "serverless computing, microservices, and multi-region high availability",
        "explain": "can you explain what it is and how cloud elasticity differs from simple scalability",
        "tradeoff": "how do you design cloud architectures to minimize egress costs and maintain security compliance"
    },
    {
        "patterns": [r"\bapis?\b", r"\brest\b", r"\brestful\b", r"\bendpoint\b", r"\bmicroservices?\b"],
        "display": "REST APIs and Microservices",
        "related": "idempotency, API rate limiting, and JWT authentication tokens",
        "explain": "can you explain what makes an API RESTful and how you structure HTTP status codes",
        "tradeoff": "how do circuit breakers and exponential backoff prevent cascading microservice outages"
    },
    {
        "patterns": [r"\boop\b", r"\bobject[\s\-]oriented\b", r"\bencapsulation\b", r"\binheritance\b", r"\bpolymorphism\b", r"\babstraction\b"],
        "display": "Object-Oriented Programming",
        "related": "SOLID design principles, design patterns, and interface segregation",
        "explain": "can you explain what it is and how runtime polymorphism differs from compile-time polymorphism",
        "tradeoff": "why do modern software architects often prefer composition over inheritance"
    },
    {
        "patterns": [r"\bthreads?\b", r"\bmultithreading\b", r"\bconcurrency\b", r"\bdeadlocks?\b", r"\bmutex\b", r"\bsemaphore\b"],
        "display": "multithreading and concurrency",
        "related": "race conditions, deadlocks, and thread-safe lock-free data structures",
        "explain": "can you explain how threads share memory and how you prevent concurrent write corruption",
        "tradeoff": "what are the four Coffman conditions for a deadlock and how do you break them"
    },
    {
        "patterns": [r"\bdsa\b", r"\bdata\s+structures?\b", r"\balgorithms?\b", r"\bbinary\s+search\b", r"\blinked\s+list\b", r"\btree\b", r"\bgraph\b", r"\bhash\s*map\b"],
        "display": "Data Structures & Algorithms",
        "related": "time and space complexity trade-offs and worst-case algorithmic analysis",
        "explain": "can you explain how hash collision resolution or tree balancing works under the hood",
        "tradeoff": "how would you optimize this algorithm if the input data was too large to fit in RAM"
    },
    {
        "patterns": [r"\bproject\b", r"\bapplication\b", r"\bsystem\b", r"\bplatform\b", r"\barchitecture\b"],
        "display": "your project",
        "related": "scalability, automated integration testing, and CI/CD pipelines",
        "explain": "can you explain what the core architectural flow was and your exact technical role",
        "tradeoff": "what was the single biggest technical roadblock you hit and how did you resolve it"
    },
    {
        "patterns": [r"\bteam\b", r"\bagile\b", r"\bscrum\b", r"\bsprint\b", r"\bcollaboration\b"],
        "display": "team collaboration and Agile",
        "related": "sprint retrospectives, code reviews, and resolving technical blockers",
        "explain": "can you explain how you handle technical disagreements or scope creep during a sprint",
        "tradeoff": "how do you balance pushing new features with paying down technical debt"
    },
]


def generate_followup(answer_text: str, current_question: str = "", candidate_name: str = "there", project_name: str = "") -> str:
    """
    Generate an intelligent, highly personalized follow-up question that:
    1. Addresses candidate directly by first name.
    2. Explicitly references the technical concept just mentioned in their answer.
    3. Seamlessly links to related deep technical concepts or probes for under-the-hood understanding.
    
    Examples:
      - 'So Adarsh, as you mentioned Artificial Intelligence, do you know about deep learning and neural networks?'
      - 'As you mentioned Artificial Intelligence, can you explain what it is in detail and how algorithms learn from data?'
    """
    import random
    raw_name = candidate_name.strip() if candidate_name else ""
    first_name = raw_name.split()[0].capitalize() if raw_name and raw_name.lower() != "there" else ""
    prefix = f"So {first_name}, " if first_name else ""

    text = (answer_text or "").strip()
    lower = text.lower()

    # 1. Match against concept knowledge base
    matched_concept = None
    for item in _CONCEPT_KNOWLEDGE:
        for pat in item["patterns"]:
            m = re.search(pat, lower)
            if m:
                matched_concept = item
                break
        if matched_concept:
            break

    # If project was referenced or answer is part of project probe
    if project_name and ("project" in lower or project_name.lower() in lower or "built" in lower):
        display = f"your project '{project_name}'"
        style = random.choice([1, 2, 3])
        if style == 1:
            return f"{prefix}as you mentioned {display}, do you know how you would scale its database and architecture if concurrent users grew tenfold?"
        elif style == 2:
            return f"As you mentioned {display}, can you explain what technical trade-offs you made when selecting the stack and designing the APIs?"
        else:
            return f"{prefix}regarding {display}, how did you test edge cases and what was the hardest bug you personally fixed?"

    if matched_concept:
        disp = matched_concept["display"]
        rel = matched_concept["related"]
        expl = matched_concept["explain"]
        trade = matched_concept["tradeoff"]

        style = random.choice([1, 2, 3])
        if style == 1:
            # "So Adarsh, as you mentioned Artificial Intelligence, do you know about deep learning..."
            return f"{prefix}as you mentioned {disp}, do you know about {rel} and how it relates to what you described?"
        elif style == 2:
            # "As you mentioned Artificial Intelligence, can you explain what it is..."
            return f"As you mentioned {disp}, {expl}?"
        else:
            return f"{prefix}as you mentioned {disp}, {trade}?"

    # 2. Dynamic NLP Extraction if not in static knowledge base
    extracted_phrase = None
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        # Find non-stopword, non-pronoun noun chunk
        chunks = [chunk.text.strip() for chunk in doc.noun_chunks 
                  if not chunk.root.is_stop and not chunk.root.is_punct and len(chunk.text.split()) <= 4 and chunk.root.pos_ in ("NOUN", "PROPN")]
        if chunks:
            extracted_phrase = chunks[-1]
    except Exception:
        pass

    if not extracted_phrase:
        # Fallback to key technical words in text
        candidates = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b|\b[a-z]{4,}\b", text)
        stop_words = {"this", "that", "there", "their", "where", "which", "about", "could", "would", "should", "because", "really", "basically"}
        valid = [c for c in candidates if c.lower() not in stop_words and len(c) > 3]
        if valid:
            extracted_phrase = valid[0]

    if extracted_phrase:
        return f"{prefix}as you mentioned '{extracted_phrase}', can you explain what it is in detail and walk me through a practical example of how you applied it?"

    # Fallback for very brief answers
    if len(text.split()) < 15:
        return f"{prefix}that was a concise summary — could you elaborate with a concrete technical example or code-level implementation detail?"

    return f"{prefix}how would this approach change if you had to optimize for high throughput, low latency, and zero downtime in production?"



# ──────────────────────────────────────────────────────────────
# 3. Answer Fluency and Vocabulary Report
# ──────────────────────────────────────────────────────────────

_FILLERS = ["um","uh","like","basically","actually","you know","sort of","kind of",
            "right","okay so","so yeah","i mean"]
_PASSIVE_VERBS = re.compile(r"\b(is|are|was|were|be|been|being)\s+\w+ed\b")

def fluency_report(text: str) -> dict:
    if not text or not text.strip():
        return {"readability_score": 0, "grade_level": 0, "ttr": 0,
                "avg_words_per_sent": 0, "filler_count": 0, "passive_count": 0,
                "word_count": 0, "sentence_count": 0, "unique_words": 0,
                "suggestions": ["No answer provided."], "rating": "Poor"}

    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"\b[a-zA-Z']+\b", text)
    word_count = len(words)
    sent_count = max(len(sentences), 1)
    syllables = _count_syllables(text)

    asl = word_count / sent_count
    asw = syllables / max(word_count, 1)
    flesch = max(0, min(100, round(206.835 - (1.015 * asl) - (84.6 * asw))))
    grade = max(1, min(20, round(0.39 * asl + 11.8 * asw - 15.59, 1)))

    lower_words = [w.lower() for w in words]
    unique = len(set(lower_words))
    ttr = round(unique / max(word_count, 1), 3)

    lower_text = text.lower()
    filler_count = sum(len(re.findall(r"\b" + re.escape(f) + r"\b", lower_text)) for f in _FILLERS)
    passive_count = len(_PASSIVE_VERBS.findall(lower_text))

    suggestions = []
    if word_count < 30:
        suggestions.append("Answer is too short — aim for at least 50 words in a technical response.")
    if filler_count > 2:
        suggestions.append(f"Reduce filler words ({filler_count} detected) for a more confident delivery.")
    if passive_count > 2:
        suggestions.append(f"Switch {passive_count} passive constructions to active voice.")
    if ttr < 0.45:
        suggestions.append("Vocabulary is repetitive — vary your word choices to sound more articulate.")
    if flesch < 40:
        suggestions.append("Sentences are complex — use shorter, clearer sentences.")
    if asl > 25:
        suggestions.append(f"Average sentence length is {asl:.0f} words — try breaking long sentences into two.")
    if not suggestions:
        suggestions.append("Great fluency! Clear, varied, and well-structured.")

    if flesch >= 60 and filler_count <= 1 and ttr >= 0.55 and word_count >= 40:
        rating = "Excellent"
    elif flesch >= 45 and filler_count <= 3 and word_count >= 25:
        rating = "Good"
    elif word_count >= 15:
        rating = "Needs Work"
    else:
        rating = "Poor"

    return {
        "readability_score": flesch,
        "grade_level": grade,
        "ttr": ttr,
        "avg_words_per_sent": round(asl, 1),
        "filler_count": filler_count,
        "passive_count": passive_count,
        "word_count": word_count,
        "sentence_count": sent_count,
        "unique_words": unique,
        "suggestions": suggestions,
        "rating": rating,
    }

def _count_syllables(text: str) -> int:
    count = 0
    for word in re.findall(r"\b[a-zA-Z]+\b", text):
        w = re.sub(r"e$", "", word.lower())
        count += max(1, len(re.findall(r"[aeiou]+", w)))
    return count


# ──────────────────────────────────────────────────────────────
# 4. Semantic Keyword Match (spaCy vectors + fallback)
# ──────────────────────────────────────────────────────────────

def semantic_keyword_match(answer_text: str, keywords: list, threshold: float = 0.55) -> dict:
    if not keywords:
        return {"matched": [], "missed": [], "score_pct": 0}
    lower = answer_text.lower()
    matched, missed = [], []
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        answer_doc = nlp(lower)
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in lower:
                matched.append(kw)
                continue
            kw_doc = nlp(kw_lower)
            if kw_doc.has_vector and answer_doc.has_vector and kw_doc.similarity(answer_doc) >= threshold:
                matched.append(kw)
                continue
            kw_tokens = [t for t in kw_doc if not t.is_stop and t.has_vector]
            ans_tokens = [t for t in answer_doc if not t.is_stop and t.has_vector]
            if kw_tokens and ans_tokens and any(
                kt.similarity(at) >= threshold for kt in kw_tokens for at in ans_tokens
            ):
                matched.append(kw)
            else:
                missed.append(kw)
    except Exception:
        _synonyms = {
            "heap": ["priority queue","min-heap","max-heap"],
            "recursion": ["recursive","call stack","base case"],
            "concurrency": ["thread","parallel","mutex","synchronize"],
            "normalization": ["normal form","redundancy","1nf","2nf","3nf"],
            "encapsulation": ["data hiding","private","getter","setter"],
            "polymorphism": ["overload","override","runtime","compile-time"],
            "abstraction": ["interface","abstract class"],
            "inheritance": ["parent","child","extends","subclass"],
            "acid": ["atomicity","consistency","isolation","durability"],
            "deadlock": ["circular wait","resource hold","preemption"],
        }
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in lower:
                matched.append(kw)
            elif any(s in lower for s in _synonyms.get(kw_lower, [])):
                matched.append(kw)
            else:
                missed.append(kw)

    return {"matched": matched, "missed": missed, "score_pct": round(len(matched) / max(len(keywords), 1) * 100)}


# ──────────────────────────────────────────────────────────────
# 5. Enhanced NER Resume Dashboard
# ──────────────────────────────────────────────────────────────

_DEGREE_PAT = re.compile(
    r"\b(b\.?tech|m\.?tech|bca|mca|b\.?sc|m\.?sc|b\.?e|m\.?e|phd|ph\.d|mba|b\.?com|m\.?com"
    r"|bachelor|master|doctorate|diploma)\b", re.IGNORECASE)
_CERT_PAT = re.compile(
    r"\b(aws\s+certified|azure\s+certified|gcp\s+certified|google\s+certified|oracle\s+certified"
    r"|cissp|ceh|pmp|scrum master|csm|comptia|rhce|mcse|ccna|ccnp|java\s+certification"
    r"|python\s+certification|machine learning\s+certificate)\b", re.IGNORECASE)
_YEAR_PAT = re.compile(r"\b(19|20)\d{2}\b")
_COLLEGE_PAT = re.compile(
    r"\b(iit|nit|bits|vit|srm|manipal|university|college|institute of technology"
    r"|engineering college|deemed|autonomous)\b", re.IGNORECASE)

def ner_resume_dashboard(resume_text: str, spacy_entities: list) -> dict:
    result = {"persons": [], "organisations": [], "locations": [], "dates_years": [],
              "degrees": [], "certifications": [], "colleges": [], "money_metrics": [], "misc": []}
    for ent in spacy_entities:
        label = ent.get("label", "")
        text = ent.get("text", "").strip()
        if not text:
            continue
        if label == "PERSON":      result["persons"].append(text)
        elif label == "ORG":       result["organisations"].append(text)
        elif label == "GPE":       result["locations"].append(text)
        elif label == "DATE":      result["dates_years"].append(text)
        elif label == "MONEY":     result["money_metrics"].append(text)
        else:                      result["misc"].append(f"{label}: {text}")

    for m in _DEGREE_PAT.finditer(resume_text):
        v = m.group(0)
        if v not in result["degrees"]: result["degrees"].append(v)
    for m in _CERT_PAT.finditer(resume_text):
        v = m.group(0)
        if v not in result["certifications"]: result["certifications"].append(v)
    for m in _YEAR_PAT.finditer(resume_text):
        v = m.group(0)
        if v not in result["dates_years"]: result["dates_years"].append(v)
    for m in _COLLEGE_PAT.finditer(resume_text):
        v = m.group(0)
        if v not in result["colleges"]: result["colleges"].append(v)

    for key in result:
        result[key] = list(dict.fromkeys(result[key]))
    return result


# ──────────────────────────────────────────────────────────────
# 6. Personalized Weakness Cluster Report
# ──────────────────────────────────────────────────────────────

_TOPIC_KEYWORDS = {
    "Data Structures & Algorithms": ["array","linked list","tree","graph","heap","stack","queue","sort","search","hash","dp","dynamic programming","recursion","complexity","big o"],
    "Object-Oriented Programming":  ["oop","class","object","encapsulation","inheritance","polymorphism","abstraction","interface","abstract","overload","override"],
    "Databases & SQL":              ["sql","database","query","join","index","normalization","transaction","acid","primary key","foreign key","schema","dbms","relational","nosql","mongodb"],
    "Java & JVM":                   ["java","jvm","thread","garbage collection","stream","lambda","exception","generics","collections","spring","hibernate","jdk"],
    "Operating Systems":            ["os","process","thread","deadlock","memory","paging","scheduling","semaphore","mutex","virtual memory","kernel","cpu"],
    "Networking":                   ["tcp","udp","http","dns","ip","osi","protocol","socket","bandwidth","latency","firewall","ssl","tls","routing"],
    "Cloud & DevOps":               ["cloud","aws","azure","gcp","docker","kubernetes","microservice","ci/cd","devops","container","serverless","scalability","rest","api"],
    "AI / Machine Learning":        ["machine learning","deep learning","neural network","nlp","model","training","overfitting","supervised","unsupervised","reinforcement","feature","accuracy"],
    "System Design":                ["design","scalable","architecture","load balancer","cache","cdn","database design","distributed","consistency","availability","partition"],
    "Behavioral & Soft Skills":     ["team","conflict","deadline","challenge","communication","leadership","project","stakeholder","prioritize","collaboration"],
    "Security":                     ["sql injection","xss","authentication","authorization","encryption","https","oauth","jwt","firewall","vulnerability"],
    "Embedded & Automotive":        ["embedded","rtos","microcontroller","autosar","ecu","firmware","pointer","real time","interrupt","driver"],
}

_LEARNING_LINKS = {
    "Data Structures & Algorithms": "https://www.geeksforgeeks.org/data-structures/",
    "Object-Oriented Programming":  "https://refactoring.guru/design-patterns",
    "Databases & SQL":              "https://www.w3schools.com/sql/",
    "Java & JVM":                   "https://docs.oracle.com/en/java/",
    "Operating Systems":            "https://www.geeksforgeeks.org/operating-systems/",
    "Networking":                   "https://www.geeksforgeeks.org/computer-network-tutorials/",
    "Cloud & DevOps":               "https://aws.amazon.com/training/",
    "AI / Machine Learning":        "https://www.coursera.org/specializations/machine-learning-introduction",
    "System Design":                "https://github.com/donnemartin/system-design-primer",
    "Behavioral & Soft Skills":     "https://www.themuse.com/advice/behavioral-interview-questions-answers-examples",
    "Security":                     "https://owasp.org/www-project-top-ten/",
    "Embedded & Automotive":        "https://www.geeksforgeeks.org/embedded-systems-tutorial/",
}

def weakness_cluster_report(answers: list) -> list:
    clusters = defaultdict(lambda: {"questions": [], "scores": [], "link": ""})
    for a in answers:
        if a.get("score", 100) >= 60:
            continue
        q_text = (a.get("question", "") + " " + a.get("feedback", "")).lower()
        best_topic, best_hits = "General", 0
        for topic, kws in _TOPIC_KEYWORDS.items():
            hits = sum(1 for kw in kws if kw in q_text)
            if hits > best_hits:
                best_hits, best_topic = hits, topic
        clusters[best_topic]["questions"].append(a["question"])
        clusters[best_topic]["scores"].append(a["score"])
        clusters[best_topic]["link"] = _LEARNING_LINKS.get(best_topic, "https://www.geeksforgeeks.org/")
    result = []
    for topic, data in sorted(clusters.items(), key=lambda x: -len(x[1]["questions"])):
        scores = data["scores"]
        result.append({
            "topic": topic,
            "count": len(scores),
            "questions": data["questions"],
            "scores": scores,
            "avg_score": round(sum(scores) / max(len(scores), 1)),
            "link": data["link"],
        })
    return result
