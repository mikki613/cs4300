from pathlib import Path

def count_words(filename):
    base_path = Path(__file__).resolve().parent.parent
    file_path = base_path / filename

    with open(file_path, "r") as file:
        text = file.read()

    words = text.split()
    return len(words)
