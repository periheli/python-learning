import asyncio
import itertools
import os
import random
import time


async def make_item(size: int = 5):
    return os.urandom(size).hex()


async def rand_sleep(caller: str | None = None):
    i = random.randint(0, 10)
    if caller is not None:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue):
    n = random.randint(0, 10)
    # Synchronous loop for each single producer
    for _ in itertools.repeat(None, n):
        await rand_sleep(caller=f"Producer {name}")
        i = await make_item()
        t = time.perf_counter()
        await q.put((i, name, t))
        print(f"Producer {name} added <{i}> to queue.")


async def consume(name: int, q: asyncio.Queue):
    while True:
        await rand_sleep(caller=f"Consumer {name}")
        i, prod, t = await q.get()
        end = time.perf_counter() - t
        print(
            f"Consumer {name} got element <{i}> "
            f"from producer {prod} in {end:0.5f} seconds."
        )
        q.task_done()


async def main(num_prods: int, num_cons: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(num_prods)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(num_cons)]

    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers. too
    for con in consumers:
        _ = con.cancel()


if __name__ == "__main__":
    import argparse

    random.seed(4444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--num_prods", type=int, default=5)
    parser.add_argument("-c", "--num_cons", type=int, default=10)

    namespace = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(
        main(num_prods=namespace.num_prods, num_cons=namespace.num_cons)
    )
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
