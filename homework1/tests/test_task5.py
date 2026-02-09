from src.task5 import get_favorite_books, get_first_three_books, get_student_database

def test_books_list():
    books = get_favorite_books()
    assert isinstance(books, list)
    assert len(books) >= 3
    assert books[0] == ("Harry Potter", "J.K. Rowling")

def test_first_three_books():
    first_three = get_first_three_books()
    assert len(first_three) == 3

def test_student_database():
    students = get_student_database()
    assert isinstance(students, dict)
    assert students["Ali"] == 1001
    assert students["Mehak"] == 1004