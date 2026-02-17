import pytest
from src.task2 import get_data_types


@pytest.mark.parametrize(
    "index, expected_type",
    [
        (0, int),
        (1, float),
        (2, str),
        (3, bool),
    ],
)
def test_task2_types(index, expected_type):
    values = get_data_types()
    assert isinstance(values[index], expected_type)


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, 10),
        (1, 3.14),
        (2, "Python"),
        (3, True),
    ],
)
def test_task2_values(index, expected_value):
    values = get_data_types()
    assert values[index] == expected_value

    