from concurrent.futures import ThreadPoolExecutor


def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(fib, [35] * 20)


def fib(n: int):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
