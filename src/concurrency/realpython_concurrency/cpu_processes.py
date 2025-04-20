from concurrent.futures import ProcessPoolExecutor


def main():
    with ProcessPoolExecutor() as executor:
        executor.map(fib, [35] * 20)


def fib(n: int):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
