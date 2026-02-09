# Homework 1 - CS4300/CS5300
## Student Information
**Name:** Mehak Hagemann  
**Course:** CS4300/CS5300
**Assignment:** Homework 1  
**GitHub Username:** mikki613  

---

## Project Description
This project contains the completed solutions for **Homework 1** in CS4300/CS5300.
The purpose of this assignment is to practice Python programming fundamentals
and unit testing using **pytest**.

Each homework task (Task 1 through Task 7) is implemented as a separate Python file.
All task solutions are located in the `src/` directory.  
Each task also includes a corresponding pytest test file located in the `tests/` directory.

All code has been tested using pytest and all tests pass successfully.

## Folder Structure
The project follows the required structure:
homework1/
│
├── src/
│ ├── task1.py
│ ├── task2.py
│ ├── task3.py
│ ├── task4.py
│ ├── task5.py
│ ├── task6.py
│ └── task7.py
│
├── tests/
│ ├── test_task1.py
│ ├── test_task2.py
│ ├── test_task3.py
│ ├── test_task4.py
│ ├── test_task5.py
│ ├── test_task6.py
│ └── test_task7.py
│
├── task6_read_me.txt
├── requirements.txt
└── README.md

## Task Summary

### Task 1: Introduction to Python and Testing
- Prints `"Hello, World!"` to the console.
- Includes a pytest test that verifies output using `capsys`.

### Task 2: Variables and Data Types
- Demonstrates basic Python data types:
  - integer
  - float
  - string
  - boolean
- Includes pytest tests to confirm correct types and values.

### Task 3: Control Structures
- Uses an if-statement to check if a number is positive, negative, or zero.
- Uses a loop to compute the first 10 prime numbers.
- Uses a while loop to compute the sum from 1 to 100.
- Includes pytest tests for each part.

### Task 4: Functions and Duck Typing
- Implements a function `calculate_discount(price, discount)` that calculates the final price.
- Works correctly with both integers and floats.
- Includes input validation and pytest tests for different cases.

### Task 5: Lists and Dictionaries
- Creates a list of favorite books (title and author).
- Uses slicing to return the first three books.
- Creates a dictionary representing a student database (name → student ID).
- Includes pytest tests to verify correct behavior.

### Task 6: File Handling
- Reads text from `task6_read_me.txt`.
- Counts the number of words in the file.
- Includes pytest tests verifying word count functionality.

### Task 7: Package Management
- Uses the `requests` package installed via pip.
- Demonstrates retrieving an HTTP status code from a URL.
- Includes pytest tests verifying correct behavior.

## Requirements
This project requires Python 3 and uses external Python packages listed in `requirements.txt`.

To install required packages, run:

```bash
pip install -r requirements.txt

To run all tests, navigate to the homework1 directory and run:

pytest
