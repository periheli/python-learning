def main():
    for _ in range(20):
        fib(35)


def fib(n: int):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
