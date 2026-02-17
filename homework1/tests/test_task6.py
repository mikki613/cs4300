import pytest
from src.task6 import count_words

@pytest.mark.parametrize(
    "filename, expected_count",
    [
        ("task6_read_me.txt", 104),
    ],
)
def test_count_words_known_files(filename, expected_count):
    assert count_words(filename) == expected_count


@pytest.mark.parametrize(
    "content, expected_count",
    [
        ("one two three", 3),
        ("   spaced   out   words   ", 3),
        ("", 0),
        ("\n\n", 0),
    ],
)
def test_count_words_tmp_files(tmp_path, content, expected_count):
    p = tmp_path / "sample.txt"
    p.write_text(content, encoding="utf-8")
    assert count_words(p) == expected_count


def test_count_words_missing_file():
    with pytest.raises(FileNotFoundError):
        count_words("this_file_does_not_exist.txt")
