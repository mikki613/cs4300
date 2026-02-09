from src.task3 import check_number, first_10_primes, sum_1_to_100

def test_check_number():
    assert check_number(10) == "positive"
    assert check_number(-5) == "negative"
    assert check_number(0) == "zero"

def test_first_10_primes():
    assert first_10_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_sum_1_to_100():
    assert sum_1_to_100() == 5050