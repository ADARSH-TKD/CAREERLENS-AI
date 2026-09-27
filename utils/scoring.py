def calculate_ats_score(a):
    sections = set(a["sections"])
    structure = min(100, round(len(sections) / 6 * 100))
    skills = min(100, round(len(a["skills"]) / 10 * 100))
    sections_score = min(100, round(len(sections) / 6 * 100))
    contact = round(sum([a["contact"]["email"], a["contact"]["phone"], a["contact"]["github"], a["contact"]["linkedin"]]) / 4 * 100)
    formatting = 100 if len(a["tokens"]) > 80 else 70 if len(a["tokens"]) > 40 else 40

    score = round(
        structure * .20 +
        skills * .25 +
        sections_score * .15 +
        contact * .10 +
        formatting * .10 +
        min(100, len(a["skills"]) / 8 * 100) * .20
    )

    checks = [
        {"ok": a["contact"]["email"], "text": "Email detected"},
        {"ok": a["contact"]["phone"], "text": "Phone number detected"},
        {"ok": "Skills" in sections, "text": "Skills section detected"},
        {"ok": "Projects" in sections, "text": "Projects section detected"},
        {"ok": a["contact"]["github"], "text": "GitHub link detected"},
        {"ok": len(a["skills"]) >= 6, "text": "Good coverage of configured skills"},
    ]
    return {"score": max(0, min(100, score)), "checks": checks}
