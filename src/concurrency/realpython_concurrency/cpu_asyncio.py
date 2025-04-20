import asyncio


async def main():
    tasks = [fib(35) for _ in range(20)]
    await asyncio.gather(*tasks, return_exceptions=True)


async def fib(n: int):
    return n if n < 2 else await fib(n - 1) + await fib(n - 2)
