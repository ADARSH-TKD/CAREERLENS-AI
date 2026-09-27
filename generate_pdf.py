import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "CareerLens AI — Complete Technical & User Documentation")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential & Proprietary — CareerLens AI Architecture Report")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()


def build_pdf(filename="document.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1e1b4b")
    c_secondary = colors.HexColor("#4338ca")
    c_accent = colors.HexColor("#6366f1")
    c_dark = colors.HexColor("#0f172a")
    c_body = colors.HexColor("#334155")
    c_card_bg = colors.HexColor("#f8fafc")
    c_border = colors.HexColor("#e2e8f0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_secondary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_dark,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_body,
        spaceAfter=7
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_body,
        leftIndent=15,
        spaceAfter=4
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_body
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark
    )
    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )
    callout_style = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # Title Banner Block
    story.append(Paragraph("CareerLens AI — System Documentation", title_style))
    story.append(Paragraph("Comprehensive Technical Reference, Architecture Pipeline & Testing Manual", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=0, spaceAfter=14))

    # SECTION 1: OBJECTIVE
    story.append(Paragraph("1. Executive Summary & Objective", h1_style))
    story.append(Paragraph(
        "<b>CareerLens AI</b> is an intelligent, multi-modal career readiness and technical interview evaluation platform. "
        "Modern job seekers frequently struggle with generic interview preparation tools that fail to interrogate the candidate's actual projects, "
        "while recruiters and interviewers struggle to verify whether claimed skills and resumes represent genuine hands-on competence.",
        body_style
    ))
    story.append(Paragraph(
        "The primary objective of CareerLens AI is to provide an authentic, adaptive, and automated interview simulation that:",
        body_style
    ))
    story.append(Paragraph("• <b>Audits Resumes with Transparent NLP:</b> Parses candidate resumes to evaluate ATS (Applicant Tracking System) compatibility, detect 7 skill clusters, and identify missing sections without black-box opacity.", bullet_style))
    story.append(Paragraph("• <b>Validates Project Authenticity:</b> Automatically extracts claimed project names from the candidate's resume and conducts targeted architecture and roadblock probing in every interview.", bullet_style))
    story.append(Paragraph("• <b>Generates Resume-Aware Interviews:</b> Replaces one-size-fits-all static question sets with personalized questions derived specifically from candidate-claimed languages, tools, and experiences.", bullet_style))
    story.append(Paragraph("• <b>Engages in Intelligent Conversational Follow-Ups:</b> Analyzes the candidate's spoken responses in real-time, extracts mentioned technical concepts, and asks natural, name-addressed follow-up questions connecting to advanced technical domains.", bullet_style))
    story.append(Paragraph("• <b>Drills CS Fundamentals:</b> Offers dedicated interactive drills with instant evaluation and model solutions across Operating Systems, DBMS, Networks, OOP, and DSA.", bullet_style))
    story.append(Paragraph("• <b>Enforces Academic Integrity:</b> Incorporates a client-side proctoring engine with full-screen enforcement, key restriction, audio warning synthesizer, and automated cancellation upon repeated violations.", bullet_style))

    story.append(Spacer(1, 10))

    # SECTION 2: TECHSTACK USED
    story.append(Paragraph("2. System Architecture & Tech Stack", h1_style))
    story.append(Paragraph(
        "CareerLens AI is built with a modular, lightweight Python architecture designed to run seamlessly in both local environments and resource-constrained cloud containers (e.g. Streamlit Community Cloud):",
        body_style
    ))

    tech_data = [
        [Paragraph("Tier", table_header), Paragraph("Technology", table_header), Paragraph("Role & Architecture Details", table_header)],
        [
            Paragraph("Presentation & UI", table_cell_bold),
            Paragraph("Streamlit 1.37+", table_cell),
            Paragraph("Reactive single-page web framework; manages session states, audio capture widgets, progress meters, and dynamic tabs.", table_cell)
        ],
        [
            Paragraph("Styling System", table_cell_bold),
            Paragraph("Vanilla CSS & Glassmorphism", table_cell),
            Paragraph("Custom dark-themed visual design with CSS grid cards, SVG circular score indicators, and smooth micro-animations.", table_cell)
        ],
        [
            Paragraph("Speech Recognition", table_cell_bold),
            Paragraph("faster-whisper (tiny/int8)", table_cell),
            Paragraph("Quantized CTranslate2 implementation of OpenAI Whisper running locally on CPU (~150MB footprint) for voice transcription.", table_cell)
        ],
        [
            Paragraph("Speech Synthesis", table_cell_bold),
            Paragraph("HTML5 Web Speech API", table_cell),
            Paragraph("Zero-latency, client-side browser voice synthesizer supporting American, British, and Indian English accents.", table_cell)
        ],
        [
            Paragraph("NLP & Parsing", table_cell_bold),
            Paragraph("spaCy, NLTK, PyMuPDF", table_cell),
            Paragraph("Local tokenization, lemmatization, named-entity recognition, PDF binary stream extraction, and OCR image reading.", table_cell)
        ],
        [
            Paragraph("Proctoring Sandbox", table_cell_bold),
            Paragraph("Vanilla JS + Web Audio", table_cell),
            Paragraph("Browser full-screen event listener, shortcut key interception, synthesizer beeps, and security query parameter state machine.", table_cell)
        ],
    ]
    t_tech = Table(tech_data, colWidths=[110, 120, 274])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tech)

    story.append(Spacer(1, 14))

    # SECTION 3: LIBRARIES & PURPOSE
    story.append(Paragraph("3. Detailed Library Breakdown & Purpose", h1_style))
    story.append(Paragraph(
        "Each Python library in CareerLens AI was chosen specifically to eliminate external paid API dependencies while maximizing execution speed:",
        body_style
    ))

    lib_data = [
        [Paragraph("Library", table_header), Paragraph("Specific Feature / Purpose", table_header), Paragraph("Implementation Location", table_header)],
        [
            Paragraph("<b>streamlit</b>", table_cell),
            Paragraph("Core application server, state management (session_state), user interface rendering, and live audio inputs.", table_cell),
            Paragraph("<code>app.py</code>", table_cell)
        ],
        [
            Paragraph("<b>nltk</b>", table_cell),
            Paragraph("Sentence tokenization (<code>sent_tokenize</code>), word segmentation (<code>word_tokenize</code>), stopword filtering, and lemmatization (<code>WordNetLemmatizer</code>).", table_cell),
            Paragraph("<code>utils/nlp_engine.py</code>", table_cell)
        ],
        [
            Paragraph("<b>spacy</b>", table_cell),
            Paragraph("Named Entity Recognition (extracting organizations, institutions, names, dates), and linguistic noun-chunk extraction for adaptive follow-ups.", table_cell),
            Paragraph("<code>utils/nlp_engine.py</code><br/><code>utils/nlp_features.py</code>", table_cell)
        ],
        [
            Paragraph("<b>scikit-learn</b>", table_cell),
            Paragraph("<code>TfidfVectorizer</code> and <code>cosine_similarity</code> for mathematical resume-to-job-description textual alignment scoring.", table_cell),
            Paragraph("<code>utils/nlp_features.py</code>", table_cell)
        ],
        [
            Paragraph("<b>PyMuPDF</b> (fitz)", table_cell),
            Paragraph("Direct in-memory PDF text extraction without saving temporary files to disk, supporting multi-page candidate resumes.", table_cell),
            Paragraph("<code>utils/resume_parser.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Pillow & pytesseract</b>", table_cell),
            Paragraph("Optical Character Recognition (OCR) fallback for candidates uploading scanned document images (JPG/PNG).", table_cell),
            Paragraph("<code>utils/resume_parser.py</code>", table_cell)
        ],
        [
            Paragraph("<b>faster-whisper</b>", table_cell),
            Paragraph("High-performance speech-to-text inference on CPU with automatic Voice Activity Detection (VAD) to filter background noise.", table_cell),
            Paragraph("<code>utils/speech.py</code>", table_cell)
        ],
        [
            Paragraph("<b>av</b> (PyAV)", table_cell),
            Paragraph("Direct audio demuxing and decoding from web browser WebM audio containers to PCM arrays for Whisper.", table_cell),
            Paragraph("<code>utils/speech.py</code>", table_cell)
        ],
    ]
    t_lib = Table(lib_data, colWidths=[90, 274, 140])
    t_lib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_lib)

    story.append(PageBreak())

    # SECTION 4: DIFFERENT METHODS USED
    story.append(Paragraph("4. Core Methodologies & Algorithms", h1_style))

    story.append(Paragraph("4.1 Project Authenticity Probing Algorithm", h2_style))
    story.append(Paragraph(
        "To verify whether a candidate genuinely authored the projects listed on their resume, the platform employs a two-tier extraction and probing pipeline:",
        body_style
    ))
    story.append(Paragraph("1. <b>Section & Heading Demarcation:</b> Scans for <code>PROJECTS</code>, <code>ACADEMIC PROJECTS</code>, or <code>TECHNICAL PROJECTS</code> section headers, isolating content lines preceding the next standard section.", bullet_style))
    story.append(Paragraph("2. <b>Title Disambiguation:</b> Filters out operational bullet points (lines beginning with action verbs like <i>Developed</i>, <i>Implemented</i>, <i>Built</i>) and identifies clean project names (e.g. <i>'Smart Attendance System'</i>) while extracting associated tech stack tokens.", bullet_style))
    story.append(Paragraph("3. <b>Realistic Skill-Based Fallback:</b> If no explicit project heading is present, an intelligent inference engine constructs a realistic project title based on the candidate's detected skills (e.g., Python + ML yields <i>'AI-Powered Predictive Analytics System'</i>).", bullet_style))
    story.append(Paragraph("4. <b>Dynamic Question Formulation:</b> Generates a mandatory Q1 interview question explicitly citing the project name: <i>'So [Name], on your resume you highlighted your project [Project Name]... Could you walk me through the end-to-end architecture, your personal contributions, and the single hardest bug you encountered?'</i>", bullet_style))

    story.append(Paragraph("4.2 Intelligent Concept-Aware Follow-Up Engine", h2_style))
    story.append(Paragraph(
        "Instead of asking rigid or generic follow-ups, CareerLens AI inspects the candidate's transcribed spoken answer in real time:",
        body_style
    ))
    story.append(Paragraph("• <b>Linguistic Concept Identification:</b> Matches spoken words against a technical ontology (e.g., <i>'Artificial Intelligence'</i>, <i>'Deep Learning'</i>, <i>'React'</i>, <i>'SQL'</i>, <i>'Docker'</i>).", bullet_style))
    story.append(Paragraph("• <b>Dual Formulation Modes:</b> Alternates between: (a) <i>Related Concept Pivot</i> (e.g., <i>'So Adarsh, as you mentioned Artificial Intelligence, do you know about deep learning and neural networks?'</i>) and (b) <i>Under-the-Hood Probe</i> (e.g., <i>'As you mentioned Artificial Intelligence, can you explain what it is and how algorithms learn patterns from data?'</i>).", bullet_style))
    story.append(Paragraph("• <b>Dynamic spaCy Noun-Chunk Fallback:</b> If the concept is outside the static knowledge base, spaCy extracts the root noun phrase from the candidate's response to construct an organic follow-up.", bullet_style))

    story.append(Paragraph("4.3 Mathematical Resume ↔ Job Description Matching", h2_style))
    story.append(Paragraph(
        "The system calculates text similarity using TF-IDF (Term Frequency-Inverse Document Frequency) and cosine distance:",
        body_style
    ))
    story.append(Paragraph(
        "<code>TF-IDF(t, d, D) = TF(t, d) × ln[(1 + |D|) / (1 + DF(t, D))] + 1</code><br/>"
        "<code>Cosine Similarity = (V_resume · V_jd) / (||V_resume|| × ||V_jd||)</code>",
        callout_style
    ))
    story.append(Paragraph(
        "The computed angle between vectors yields an exact match percentage (0–100%), while set difference operations between the JD vocabulary and resume tokens highlight missing ATS keywords.",
        body_style
    ))

    story.append(Paragraph("4.4 Full-Screen Anti-Cheating & Keyboard Sandboxing", h2_style))
    story.append(Paragraph(
        "A client-side security harness enforces strict proctoring during the interview:",
        body_style
    ))
    story.append(Paragraph("• <b>Fullscreen Lock:</b> Hooks into <code>document.documentElement.requestFullscreen()</code>. Exiting fullscreen immediately increments the warning counter.", bullet_style))
    story.append(Paragraph("• <b>Shortcut Interception:</b> Intercepts <code>keydown</code> events, suppressing default browser actions for <code>Alt+Tab</code>, <code>Ctrl+Tab</code>, <code>Ctrl+C</code>, <code>Ctrl+V</code>, <code>Ctrl+F</code>, <code>F12</code>, <code>PrintScreen</code>, <code>Win</code>, <code>Esc</code>, <code>Alt+F4</code>, <code>Ctrl+W</code>, and <code>Ctrl+L</code>.", bullet_style))
    story.append(Paragraph("• <b>Synthetic Audio Beeps:</b> Uses the Web Audio API (<code>AudioContext</code>) to play a dual-tone alert tone (880Hz / 440Hz) when a violation occurs.", bullet_style))
    story.append(Paragraph("• <b>Four-Strike Termination:</b> Upon the 4th infraction, the interview is cancelled, the session is cleared, and an urgent cancellation banner is displayed.", bullet_style))

    story.append(Spacer(1, 10))

    # SECTION 5: COMPLETE APPLICATION PIPELINE
    story.append(Paragraph("5. Complete Step-by-Step Application Pipeline", h1_style))
    
    pipeline_steps = [
        ("Step 1: Ingestion & Upload", "The user uploads a PDF or image resume (or pastes raw text) and enters their name on the Home dashboard."),
        ("Step 2: NLP Analysis & Profiling", "PyMuPDF/pytesseract extracts the text. The NLP pipeline performs sentence tokenization, stopword cleaning, lemmatization, and regex matching across 7 technical categories. Entities (persons, organizations, universities) are extracted via spaCy NER."),
        ("Step 3: ATS Score Calculation", "A deterministic ATS scoring engine evaluates the profile against 10 critical criteria (contact channels, section completeness, skill density, formatting), outputting an ATS Score (0–100%) and an actionable checklist."),
        ("Step 4: Job Description Matching (Optional)", "The candidate pastes a target Job Description. The TF-IDF cosine similarity engine produces a match percentage and lists specific missing technical keywords."),
        ("Step 5: Interview Configuration", "Candidate selects their target company (Microsoft, Google, Amazon, Deloitte, Cognizant, Wipro, TCS, JP Morgan, Cisco, or Custom JD), interview mode (Practice or 60s Timed), and voice accent."),
        ("Step 6: Interview Orchestration", "The sequence starts with Q0 (Introduction), followed by Q1 (Project Authenticity Probe citing candidate's project name), Q2+ (Resume-Aware Questions + Company Questions)."),
        ("Step 7: Real-Time Audio & Evaluation", "Candidate records answers via the browser audio input. faster-whisper transcribes speech; NLP evaluation checks expected concepts, filler words, fluency, and generates automatic follow-up questions."),
        ("Step 8: Final Diagnostic Report", "Upon completion, the application aggregates performance metrics: overall score, concept coverage, vocabulary diversity, filler word analysis, and specific improvement recommendations.")
    ]

    for title, desc in pipeline_steps:
        story.append(Paragraph(f"<b>{title}:</b> {desc}", body_style))

    story.append(PageBreak())

    # SECTION 6: COMPLETE TESTING MANUAL
    story.append(Paragraph("6. Complete Step-by-Step Testing Manual", h1_style))
    story.append(Paragraph(
        "This section provides quality assurance procedures to test every module of CareerLens AI thoroughly:",
        body_style
    ))

    tests = [
        {
            "id": "TC-01",
            "name": "Resume Upload & Text Extraction (PDF / OCR)",
            "steps": "1. Navigate to '[Home]'.<br/>2. Upload sample PDF (e.g. <code>sample_resume/software.pdf</code>) or paste raw text.<br/>3. Enter candidate name (e.g. <i>'Adarsh Nayak'</i>).<br/>4. Click 'Analyze Resume'.",
            "expected": "Extracted text populates the preview box; ATS Score card displays with breakdown; detected skills and contact details appear with green checkmarks."
        },
        {
            "id": "TC-02",
            "name": "Resume <-> Job Description TF-IDF Matcher",
            "steps": "1. In the JD section, paste a job posting requiring Python, Docker, and AWS.<br/>2. Click 'Calculate Match Score'.",
            "expected": "Match percentage is computed; matched keywords are shown in green; missing keywords appear with recommendations."
        },
        {
            "id": "TC-03",
            "name": "Project Authenticity Probing Verification",
            "steps": "1. Ensure resume contains a project title (e.g. <i>'Smart Attendance System'</i>).<br/>2. Select any company and start the interview.<br/>3. Complete Q0 (Introduction).<br/>4. Observe Q1 prompt.",
            "expected": "Q1 explicitly cites the project: <i>'So Adarsh, on your resume you highlighted your project 'Smart Attendance System'...'</i> with cyan '[PROJECT PROBE]' badge."
        },
        {
            "id": "TC-04",
            "name": "Intelligent Concept Follow-Up Verification",
            "steps": "1. In Q1, record or type an answer mentioning <i>'Artificial Intelligence'</i>.<br/>2. Click 'STOP / SUBMIT'.<br/>3. Observe next question.",
            "expected": "System automatically generates Q1.1 addressing candidate: <i>'So Adarsh, as you mentioned Artificial Intelligence, do you know about deep learning...'</i> with yellow '[FOLLOW-UP]' badge."
        },
        {
            "id": "TC-05",
            "name": "Resume-Aware Question Verification",
            "steps": "1. Upload a resume listing React, Docker, and Machine Learning.<br/>2. Start an interview with 5 questions.<br/>3. Inspect questions Q2 and Q3.",
            "expected": "Questions directly reference candidate's detected skills: <i>'So Adarsh, your resume mentions React...'</i> with purple '[RESUME-AWARE]' badge."
        },
        {
            "id": "TC-06",
            "name": "CS Core Subject Practice & Drill Verification",
            "steps": "1. Navigate to '[CS Core]' tab.<br/>2. Filter by subject (e.g. 'Operating Systems') and difficulty.<br/>3. Click '[Random Question]'.<br/>4. Type answer and click 'Submit Answer'.<br/>5. Click 'Reveal Model Answer'.",
            "expected": "System evaluates concept coverage, relevance, and shows complete expert model solution."
        },
        {
            "id": "TC-07",
            "name": "Fullscreen Proctoring & Key Restriction Testing",
            "steps": "1. Start an interview.<br/>2. Click '[Enter Fullscreen Mode]'.<br/>3. Press forbidden keys: <code>Alt+Tab</code>, <code>Ctrl+C</code>, <code>F12</code>, or <code>Esc</code>.",
            "expected": "Default browser actions are blocked; red warning modal appears; warning count increments from 1/4 to 2/4; synthetic warning beep sounds."
        },
        {
            "id": "TC-08",
            "name": "Proctoring Cancellation Enforcement",
            "steps": "1. Trigger 4 proctoring infractions during an active interview session.",
            "expected": "On the 4th infraction, interview terminates immediately; full-screen exits; '[URGENT WARNING: Your interview has been CANCELLED]' banner is displayed."
        },
        {
            "id": "TC-09",
            "name": "Voice Transcription & Interview Report",
            "steps": "1. Record answer via browser microphone.<br/>2. Verify transcription matches spoken words.<br/>3. Complete all questions in the interview.",
            "expected": "System generates comprehensive Diagnostic Report with overall score, vocabulary richness, filler word analysis, and strengths/weaknesses."
        },
    ]

    for tc in tests:
        tc_table_data = [
            [Paragraph(f"<b>{tc['id']}: {tc['name']}</b>", table_header), Paragraph("", table_header)],
            [Paragraph("<b>Testing Steps:</b>", table_cell_bold), Paragraph(tc['steps'], table_cell)],
            [Paragraph("<b>Expected Result:</b>", table_cell_bold), Paragraph(tc['expected'], table_cell)],
        ]
        t_tc = Table(tc_table_data, colWidths=[110, 394])
        t_tc.setStyle(TableStyle([
            ('SPAN', (0,0), (1,0)),
            ('BACKGROUND', (0,0), (-1,0), c_secondary),
            ('GRID', (0,0), (-1,-1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_tc)
        story.append(Spacer(1, 7))

    # SECTION 7: DEPLOYMENT VERIFICATION
    story.append(Paragraph("7. Cloud Deployment & Troubleshooting Guide", h1_style))
    story.append(Paragraph(
        "CareerLens AI is packaged for continuous deployment to <b>Streamlit Community Cloud (share.streamlit.io)</b>. "
        "The root repository contains three automated deployment descriptors:",
        body_style
    ))
    story.append(Paragraph("• <b>requirements.txt:</b> Specifies exact pre-built Python wheels. Standardizes on <code>en-core-web-sm @ URL</code> syntax to ensure installation during the container build step without runtime permission errors.", bullet_style))
    story.append(Paragraph("• <b>nltk.txt:</b> Automates NLTK corpora provisioning (<code>punkt</code>, <code>stopwords</code>, <code>wordnet</code>) during image build.", bullet_style))
    story.append(Paragraph("• <b>packages.txt:</b> Instructs the Debian package manager to install <code>tesseract-ocr</code> and <code>ffmpeg</code> for OCR and audio processing.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Document successfully created: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "document.pdf"
    build_pdf(out_file)
