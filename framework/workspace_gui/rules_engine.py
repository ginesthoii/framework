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
    """
    Generates a small list of filename suggestions based on:
      - settings
      - basic metadata
      - current filename
    This is the place where your “AI without AI” logic will grow.
    """
    base_dir, old_name = os.path.split(path)
    stem, ext = os.path.splitext(old_name)

    metadata = extract_metadata(path) or {}

    style = settings_manager.get_setting("naming_style", "snake_case")
    include_date = settings_manager.get_setting("include_date", True)
    date_format = settings_manager.get_setting("date_format", "YYYY-MM-DD")
    preset_name = settings_manager.get_setting("default_preset", "developer_standard")
    preset_template = settings_manager.get_preset(preset_name) or "{title}"

    date_str = None
    if include_date:
        date_str = _get_date_from_metadata_or_fs(path, date_format)

    components = {
        "date": date_str or "",
        "project": "project",
        "project_name": "project",
        "category": metadata.get("category", ""),
        "version": "v1",
        "title": metadata.get("title", "") or stem,
        "author": metadata.get("author", ""),
        "year": (date_str[:4] if date_str else "")
    }

    raw_name = preset_template.format(**components)
    raw_name = raw_name.strip("_- ")

    final_name = apply_style(raw_name, style) + ext.lower()

    suggestions = [
        final_name,
        apply_style(f"{components['title']}_{components['date']}", style) + ext.lower()
        if components["date"] else "",
        apply_style(stem, style) + ext.lower(),
    ]

    seen = set()
    result = []
    for s in suggestions:
        s = s.strip()
        if not s:
            continue
        if s not in seen:
            seen.add(s)
            result.append(s)

    return result or [old_name]


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
