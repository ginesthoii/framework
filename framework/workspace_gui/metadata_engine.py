import os
import mimetypes
from datetime import datetime

try:
    from extract_pdf_metadata import get_pdf_metadata
    from extract_text_from_pdf import extract_pdf_text
except:
    get_pdf_metadata = None
    extract_pdf_text = None

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except:
    Image = None


def safe_date(dt):
    if not dt:
        return None
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d")
    return str(dt)


def extract_metadata(path: str) -> dict:
    ext = os.path.splitext(path)[1].lower()

    mime, _ = mimetypes.guess_type(path)

    if mime and "pdf" in mime:
        return extract_pdf_metadata_full(path)

    if mime and mime.startswith("image/"):
        return extract_image_metadata(path)

    if ext in [".txt", ".md"]:
        return extract_textfile_metadata(path)

    # fallback: just use filename
    return {
        "title": os.path.splitext(os.path.basename(path))[0],
        "category": "",
        "author": "",
        "date_created": fs_date(path),
        "date_modified": fs_date(path),
        "keywords": [],
        "confidence": 0.30
    }


# ------------------------------------------------------------
# PDF LOGIC
# ------------------------------------------------------------

def extract_pdf_metadata_full(path):
    meta = {
        "title": "",
        "author": "",
        "subject": "",
        "keywords": [],
        "date_created": fs_date(path),
        "date_modified": fs_date(path),
        "page_count": None,
        "category": "document",
        "confidence": 0.60
    }

    # Use your real PDF metadata
    if get_pdf_metadata:
        pdf_meta = get_pdf_metadata(path)
        if pdf_meta:
            meta["title"] = pdf_meta.get("title") or meta["title"]
            meta["author"] = pdf_meta.get("author") or meta["author"]
            meta["subject"] = pdf_meta.get("subject") or meta["subject"]
            meta["keywords"] = pdf_meta.get("keywords", [])

    # Get text to improve intelligence
    text = ""
    if extract_pdf_text:
        try:
            text = extract_pdf_text(path)
        except:
            text = ""

    # Simple NLP heuristic:
    # classify document type
    lowered = text.lower()

    if "permit" in lowered:
        meta["category"] = "permit"
        meta["confidence"] += 0.15

    if "invoice" in lowered or "amount due" in lowered:
        meta["category"] = "invoice"
        meta["confidence"] += 0.20

    if "contract" in lowered or "terms" in lowered:
        meta["category"] = "contract"
        meta["confidence"] += 0.20

    # detect agency keywords
    agencies = ["dnr", "usda", "irs", "missouri", "department"]
    for a in agencies:
        if a in lowered:
            meta["keywords"].append(a)

    # fallback title from first line
    if not meta["title"] and text:
        first = text.split("\n")[0].strip()[:80]
        meta["title"] = first

    return meta


# ------------------------------------------------------------
# IMAGE / EXIF LOGIC
# ------------------------------------------------------------

def extract_image_metadata(path):
    meta = {
        "title": os.path.splitext(os.path.basename(path))[0],
        "author": "",
        "category": "image",
        "keywords": [],
        "date_created": fs_date(path),
        "date_modified": fs_date(path),
        "confidence": 0.50
    }

    if not Image:
        return meta

    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif:
            return meta

        cleaned = {}
        for tag, val in exif.items():
            name = TAGS.get(tag, tag)
            cleaned[name] = val

        # date
        dt = cleaned.get("DateTimeOriginal")
        if dt:
            meta["date_created"] = dt.split(" ")[0].replace(":", "-")
            meta["confidence"] += 0.20

        # camera info
        camera = cleaned.get("Model")
        if camera:
            meta["keywords"].append(camera)

        return meta

    except:
        return meta


# ------------------------------------------------------------
# TEXTFILE LOGIC
# ------------------------------------------------------------

def extract_textfile_metadata(path):
    meta = {
        "title": os.path.splitext(os.path.basename(path))[0],
        "author": "",
        "category": "text",
        "keywords": [],
        "date_created": fs_date(path),
        "date_modified": fs_date(path),
        "confidence": 0.40
    }

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except:
        return meta

    lowered = text.lower()

    if "# " in text:
        header = text.split("\n")[0].replace("#", "").strip()
        meta["title"] = header

    if "todo" in lowered:
        meta["keywords"].append("todo")
        meta["category"] = "notes"

    return meta


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def fs_date(path):
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
