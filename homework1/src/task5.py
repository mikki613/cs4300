def get_favorite_books():
    books = [
        ("Harry Potter", "J.K. Rowling"),
        ("The Hobbit", "J.R.R. Tolkien"),
        ("1984", "George Orwell"),
        ("To Kill a Mockingbird", "Harper Lee"),
        ("The Great Gatsby", "F. Scott Fitzgerald")
    ]
    return books

def get_first_three_books():
    books = get_favorite_books()
    return books[:3]

def get_student_database():
    students = {
        "Ali": 1001,
        "Sara": 1002,
        "John": 1003,
        "Mehak": 1004
    }

    return students

if __name__ == "__main__":
    print(get_favorite_books())
    print(get_first_three_books())
    print(get_student_database())

