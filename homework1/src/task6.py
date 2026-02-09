def count_words(filename):
    with open(filename, "r") as file:
        text = file.read()
    
    words = text.split()
    return len(words)


if __name__ == "__main__":
    print(count_words("task6_read_me.txt"))