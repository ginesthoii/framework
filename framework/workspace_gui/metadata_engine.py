import os


def extract_metadata(path: str) -> dict:
    """
    Stub: return minimal fake metadata.
    Later, plug in your:
      - PDF metadata
      - EXIF
      - Office metadata
      - video metadata
    """
    return {
        "title": os.path.splitext(os.path.basename(path))[0],
        "author": "",
        "category": "",
    }
