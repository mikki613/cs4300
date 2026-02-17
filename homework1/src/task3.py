def check_number(num):
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else:
        return "zero"


def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


def first_10_primes():
    primes = []
    num = 2

    while len(primes) < 10:
        if is_prime(num):
            primes.append(num)
        num += 1

    return primes


def print_first_10_primes():
    primes = first_10_primes()

    for p in primes:
        print(p)


def sum_1_to_100():
    total = 0
    i = 1

    while i <= 100:
        total += i
        i += 1

    return total


if __name__ == "__main__":
    print(check_number(10))
    print(check_number(-5))
    print(check_number(0))

    print_first_10_primes()

    print(sum_1_to_100())
