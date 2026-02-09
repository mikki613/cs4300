from src.task7 import get_status_code

def test_get_status_code():
    code = get_status_code("https://example.com")
    assert code == 200