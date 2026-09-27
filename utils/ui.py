import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root { --bg:#07050d; --panel:#100b19; --panel2:#171022; --purple:#8b5cf6; --violet:#c084fc; --text:#f5f3ff; --muted:#aaa2bb; }
    .stApp { background: radial-gradient(circle at 15% 0%, #211039 0, transparent 32%), radial-gradient(circle at 90% 10%, #291045 0, transparent 25%), var(--bg); color:var(--text); font-family:Inter,sans-serif; }
    .block-container { max-width:1180px; padding-top:2.8rem; padding-bottom:3rem; }
    .brand { font-weight:800; letter-spacing:.08em; font-size:1.05rem; padding-top:.45rem; }
    .brand span { color:var(--violet); } .brand small { color:#8b7b9d; }
    .navline { height:1px; background:linear-gradient(90deg,transparent,#6d28d9,transparent); margin:16px 0 30px; }
    div[data-testid='stHorizontalBlock'] .nav-btn button { min-height:42px!important; font-size:.82rem!important; }
    .timer-normal { color:#e9d5ff!important; } .timer-danger { color:#ff9f9f!important; animation:pulse 1s infinite; }
    .stAudioInput { margin-top:8px; }
    .hero { padding:48px 10px 34px; }
    .eyebrow { color:#b88cff; font-size:.76rem; font-weight:700; letter-spacing:.2em; }
    h1 { font-size:clamp(2.3rem,5vw,4.7rem)!important; line-height:1.02!important; margin:10px 0 18px!important; letter-spacing:-.055em; }
    h1 span { background:linear-gradient(90deg,#a78bfa,#e9d5ff); -webkit-background-clip:text; color:transparent; }
    .hero p { color:var(--muted); max-width:680px; font-size:1.05rem; line-height:1.7; }
    .glass { background:linear-gradient(145deg,rgba(24,16,37,.88),rgba(11,8,17,.9)); border:1px solid rgba(167,139,250,.18); border-radius:22px; padding:25px; box-shadow:0 15px 50px rgba(0,0,0,.25); margin-bottom:18px; }
    .stButton>button { border-radius:12px!important; border:1px solid rgba(167,139,250,.2)!important; background:#120d1b!important; color:#eee8ff!important; font-weight:600!important; transition:.2s!important; }
    .stButton>button:hover { border-color:#a78bfa!important; transform:translateY(-1px); box-shadow:0 0 25px rgba(139,92,246,.18); }
    .stButton>button[kind="primary"] { background:linear-gradient(90deg,#6d28d9,#8b5cf6)!important; border:0!important; }
    .metric { background:linear-gradient(145deg,#171022,#0e0916); border:1px solid rgba(192,132,252,.16); padding:18px; border-radius:17px; }
    .metric .label { color:#a9a0b9; font-size:.78rem; } .metric .value { font-size:1.7rem; font-weight:800; margin-top:4px; } .metric .hint { color:#746b82; font-size:.72rem; }
    .company-card { padding:18px 20px; min-height:165px; border-radius:20px; background:linear-gradient(145deg,#171022,#0c0912); border:1px solid rgba(167,139,250,.15); margin-bottom:10px; display:flex; flex-direction:column; justify-content:space-between; transition:all .2s ease; }
    .company-card:hover { border-color:rgba(167,139,250,.45); transform:translateY(-2px); box-shadow:0 8px 30px rgba(109,40,217,.18); }
    .company-logo-container { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.08); border-radius:12px; padding:6px 12px; display:inline-flex; align-items:center; width:fit-content; }
    .company-icon { width:42px; height:42px; display:grid; place-items:center; border-radius:12px; background:#24133a; color:#c4b5fd; font-weight:800; font-size:1.1rem; }
    .company-card h3 { margin:10px 0 2px; font-size:1.1rem; } .company-card p { color:#81778e; font-size:.8rem; margin:0; }
    .score { text-align:center; font-size:4rem; font-weight:800; background:linear-gradient(90deg,#a78bfa,#e9d5ff); -webkit-background-clip:text; color:transparent; padding:12px; }
    .check { padding:11px 12px; border-radius:11px; margin:7px 0; background:#0c0912; font-size:.88rem; }
    .good { color:#c4f7dc; } .warn { color:#f7d7a5; }
    .muted { color:#7f758d; font-size:1rem; }
    .pipeline { color:#c4b5fd; line-height:2; background:#0a0710; padding:18px; border-radius:14px; }
    .question-meta { color:#a78bfa; font-size:.75rem; font-weight:800; letter-spacing:.15em; }
    .timer { text-align:right; color:#e9d5ff; font-weight:700; }
    .question-card { display:flex; gap:18px; align-items:center; padding:28px; margin:18px 0; border-radius:22px; background:linear-gradient(145deg,#1b1028,#0c0811); border:1px solid rgba(192,132,252,.2); }
    .avatar { font-size:2.5rem; } .bubble { font-size:1.2rem; line-height:1.6; }
    .mic-card { text-align:center; padding:25px; border-radius:22px; background:radial-gradient(circle,#28123f,#0c0811 65%); border:1px solid rgba(139,92,246,.2); }
    .mic { font-size:3.2rem; animation:pulse 1.8s infinite; } .mic-title { font-weight:700; margin-top:6px; } .mic-sub { color:#81778e; font-size:.82rem; }
    @keyframes pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.07)} }
    .report-hero { display:flex; gap:30px; align-items:center; padding:28px; border-radius:24px; background:linear-gradient(120deg,#211034,#0c0811); border:1px solid rgba(192,132,252,.2); margin-bottom:18px; }
    .report-score { font-size:5rem; font-weight:800; color:#d8b4fe; line-height:1; } .report-score small { font-size:1rem; color:#81778e; }
    @media(max-width:700px){ .hero{padding-top:25px}.glass{padding:18px}.report-hero{flex-direction:column;align-items:flex-start}.report-score{font-size:4rem} }
    </style>
    """, unsafe_allow_html=True)

import base64
from pathlib import Path
import functools

COMPANY_LOGO_MAP = {
    "Microsoft": "Microsoft_logo_(2012).svg.webp",
    "Google": "Google__G__logo.svg.webp",
    "Amazon": "Amazon_logo.svg.webp",
    "TCS": "Tata_Consultancy_Services_old_logo.svg.webp",
    "Infosys": "Infosys_logo.svg.webp",
    "Accenture": "Accenture.svg.webp",
    "Wipro": "Wipro_Primary_Logo_Color_RGB.svg.webp",
    "Cognizant": "Cognizant_logo_2022.svg.webp",
    "HCLTech": "HCLTech_logo.png",
    "Tech Mahindra": "Tech_Mahindra_New_Logo.svg.webp",
    "LTIMindtree": "LTIMindtree-logo.png",
    "Capgemini": "Capgemini_201x_logo.svg.webp",
    "IBM": "IBM_logo.svg.webp",
    "Deloitte": "Logo_of_Deloitte.svg.webp",
    "PwC": "PwC_Company_Logo.svg.webp",
    "Cisco": "Cisco_logo_blue_2016.svg.webp",
    "JP Morgan Chase": "J_P_Morgan_Logo_2008_1.svg.webp",
    "BNP Paribas": "BNP_Paribas.svg.webp",
    "KPIT Technologies": "KPIT_Technologies_Logo.svg.webp",
}

@functools.lru_cache(maxsize=32)
def get_company_logo_b64(company: str) -> str:
    filename = COMPANY_LOGO_MAP.get(company)
    if not filename:
        return ""
    path = Path("logo_company") / filename
    if not path.exists():
        return ""
    try:
        data = path.read_bytes()
        mime = "image/png" if filename.endswith(".png") else "image/webp"
        encoded = base64.b64encode(data).decode("utf-8")
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return ""

def get_company_logo_html(company: str, height: int = 34, max_width: int = 120) -> str:
    b64 = get_company_logo_b64(company)
    if b64:
        return (
            f"<div class='company-logo-container' style='height:{height+10}px;margin-bottom:8px;'>"
            f"<img src='{b64}' alt='{company}' style='max-height:{height}px;max-width:{max_width}px;object-fit:contain;' />"
            f"</div>"
        )
    initial = company[0] if company else "?"
    return f"<div class='company-icon'>{initial}</div>"

def metric_card(label, value, hint=""):
    st.markdown(f"<div class='metric'><div class='label'>{label}</div><div class='value'>{value}</div><div class='hint'>{hint}</div></div>", unsafe_allow_html=True)

def score_ring(score):
    return f"<div class='score'>{score}<span style='font-size:1rem;color:#81778e'> / 100</span></div>"

def section_title(title):
    st.markdown(f"<h3 style='margin-top:0'>{title}</h3>", unsafe_allow_html=True)

@functools.lru_cache(maxsize=1)
def get_interview_background_b64() -> str:
    # Try optimized WebP first for instant loading
    webp_path = Path("background.webp")
    if webp_path.exists():
        try:
            data = webp_path.read_bytes()
            encoded = base64.b64encode(data).decode("utf-8")
            return f"data:image/webp;base64,{encoded}"
        except Exception:
            pass

    # Fallback to background.png
    png_path = Path("background.png")
    if png_path.exists():
        try:
            data = png_path.read_bytes()
            encoded = base64.b64encode(data).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
        except Exception:
            pass
    return ""

def inject_interview_room_bg():
    b64 = get_interview_background_b64()
    if b64:
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(7, 5, 13, 0.40), rgba(7, 5, 13, 0.60)), url('{b64}') !important;
            background-size: cover !important;
            background-position: center top !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        .question-card {{
            background: linear-gradient(145deg, rgba(27, 16, 40, 0.82), rgba(12, 8, 17, 0.88)) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1.5px solid rgba(192, 132, 252, 0.35) !important;
            box-shadow: 0 16px 50px rgba(0, 0, 0, 0.5) !important;
        }}
        .mic-card {{
            background: radial-gradient(circle, rgba(40, 18, 63, 0.82), rgba(12, 8, 17, 0.88) 65%) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1.5px solid rgba(139, 92, 246, 0.35) !important;
            box-shadow: 0 16px 50px rgba(0, 0, 0, 0.5) !important;
        }}
        .glass {{
            background: linear-gradient(145deg, rgba(24, 16, 37, 0.82), rgba(11, 8, 17, 0.88)) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(167, 139, 250, 0.25) !important;
        }}
        .company-card {{
            background: linear-gradient(145deg, rgba(23, 16, 34, 0.82), rgba(12, 9, 18, 0.88)) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
        }}
        </style>
        """, unsafe_allow_html=True)
