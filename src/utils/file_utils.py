"""File utilities — handling, organizing, and saving outputs"""

from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to safe filename slug"""
    return text.lower().replace(" ", "-").replace("/", "-")[:40]


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: dict, path: Path) -> Path:
    """Save data as JSON"""
    import json
    ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path


def read_json(path: Path) -> dict:
    """Read JSON file"""
    import json
    with open(path, "r") as f:
        return json.load(f)
