from pathlib import Path

def count_words(filename):
    base_path = Path(__file__).resolve().parent.parent
    file_path = base_path / filename

    if not file_path.exists():
        raise FileNotFoundError(f"{filename} not found")

    text = file_path.read_text(encoding="utf-8")
    return len(text.split()) 