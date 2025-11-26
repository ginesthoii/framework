import os
import datetime

from .metadata_engine import extract_metadata


def sanitize_component(text: str) -> str:
    if not text:
        return ""
    bad_chars = r'\/:*?"<>|'
    for c in bad_chars:
        text = text.replace(c, "_")
    return text.strip().replace(" ", "-")


def generate_name_suggestions(path: str, settings_manager):
    base_dir, old_name = os.path.split(path)
    stem, ext = os.path.splitext(old_name)

    metadata = extract_metadata(path)

    title = metadata.get("title") or stem
    category = metadata.get("category") or ""
    author = metadata.get("author") or ""
    date = metadata.get("date_created") or ""
    keywords = metadata.get("keywords") or []

    # Simple smart guesses
    primary_keyword = keywords[0] if keywords else ""
    doc_type = category

    # Build patterns
    suggestions = []

    # 1) Date + title
    if date:
        suggestions.append(f"{date}_{title}{ext}")

    # 2) Date + category + title
    if date and doc_type:
        suggestions.append(f"{date}_{doc_type}_{title}{ext}")

    # 3) Keyword + title
    if primary_keyword:
        suggestions.append(f"{primary_keyword}_{title}{ext}")

    # 4) Fallback: formatted stem
    suggestions.append(f"{stem.replace(' ','_')}{ext}")

    # Dedupe + clean
    cleaned = []
    seen = set()
    for s in suggestions:
        s = s.replace("__", "_").strip("_- ")
        if s not in seen:
            seen.add(s)
            cleaned.append(s)

    return cleaned


def _get_date_from_metadata_or_fs(path: str, date_format: str) -> str:
    ts = os.path.getmtime(path)
    dt = datetime.datetime.fromtimestamp(ts)
    if date_format == "YYYY-MM-DD":
        return dt.strftime("%Y-%m-%d")
    return dt.strftime("%Y-%m-%d")


def apply_style(text: str, style: str) -> str:
    text = sanitize_component(text)
    parts = [p for p in text.replace("-", " ").replace("_", " ").split(" ") if p]

    if style == "snake_case":
        return "_".join(p.lower() for p in parts)
    if style == "kebab_case":
        return "-".join(p.lower() for p in parts)
    if style == "camelCase":
        if not parts:
            return ""
        first = parts[0].lower()
        rest = [p.capitalize() for p in parts[1:]]
        return first + "".join(rest)
    if style == "PascalCase":
        return "".join(p.capitalize() for p in parts)

    return "_".join(parts)
