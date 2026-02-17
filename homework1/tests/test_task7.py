from unittest.mock import patch, Mock
from src.task7 import get_status_code

def test_get_status_code():
    mock_response = Mock()
    mock_response.status_code = 200

    with patch("src.task7.requests.get", return_value=mock_response):
        assert get_status_code("https://example.com") == 200
