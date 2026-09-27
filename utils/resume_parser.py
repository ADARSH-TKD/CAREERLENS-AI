from pathlib import Path

def extract_resume_text(file, kind):
    try:
        if kind == "pdf":
            import fitz
            data = file.read()
            doc = fitz.open(stream=data, filetype="pdf")
            return "\n".join(page.get_text() for page in doc).strip()
        if kind == "image":
            from PIL import Image
            import pytesseract
            img = Image.open(file)
            return pytesseract.image_to_string(img).strip()
    except Exception:
        return ""
    return ""
