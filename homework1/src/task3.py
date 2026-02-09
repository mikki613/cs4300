def check_number(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"

def is_prime(num):
    if num < 2:
        return False

    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
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

def sum_1_to_100():
    total = 0
    i = 1

    while i <= 100:
        total += i
        i += 1

    return total 


if __name__ == "__main__":
    print(check_number(5))
    print(first_10_primes())
    print(sum_1_to_100())