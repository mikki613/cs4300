import pytest 
from src.task4 import calculate_discount

def test_calculate_discount_int():
    assert calculate_discount(100, 20) == 80

def test_calculate_discount_float():
    assert calculate_discount(50.0, 10.0) == 45.0

def test_calculate_discount_mixed_types():
    assert calculate_discount(200, 12.5) == 175.0

def test_calculate_discount_invalid_discount():
    with pytest.raises(ValueError):
        calculate_discount(100, -5)

    with pytest.raises(ValueError):
        calculate_discount(100, 150)