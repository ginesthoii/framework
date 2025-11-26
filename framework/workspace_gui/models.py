from dataclasses import dataclass
from typing import Dict


@dataclass
class FileMetadata:
    path: str
    raw_metadata: Dict
