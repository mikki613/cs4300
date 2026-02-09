from src.task2 import get_data_types

def test_task2_types():
    my_int, my_float, my_string, my_bool = get_data_types()

    assert isinstance(my_int, int)
    assert isinstance(my_float, float)
    assert isinstance(my_string, str)
    assert isinstance(my_bool, bool)

def test_task2_values():
    my_int, my_float, my_string, my_bool = get_data_types()

    assert my_int == 10
    assert my_float == 3.14
    assert my_string == "Python"
    assert my_bool is True
    