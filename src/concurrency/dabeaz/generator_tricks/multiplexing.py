from importlib import metadata
from queue import Queue
from threading import Thread

from gen_queue import gen_from_queue, send_to_queue


def gen_cat(sources):
    for source in sources:
        yield from source


def multiplex(sources):
    queue = Queue()
    consumers = []
    for src in sources:
        thread = Thread(target=send_to_queue, args=(src, queue))
        thread.start()
        consumers.append(gen_from_queue(queue))
    return gen_cat(consumers)


def gen_multiplex(sources):
    queue = Queue()

    def run_one(source, metadata):
        for item in source:
            queue.put((item, metadata))

    def run_all():
        thread_list: list[Thread] = []
        for i, source in enumerate(sources):
            thread = Thread(target=run_one, args=(source, i))
            thread.start()
            thread_list.append(thread)
        for thread in thread_list:
            thread.join()
        queue.put((StopIteration, None))

    Thread(target=run_all).start()
    while True:
        item, metadata = queue.get()
        if item is StopIteration:
            return
        yield item, metadata


if __name__ == "__main__":
    from follow import follow

    log1 = follow(open("logs/realtime-access.log"))
    log2 = follow(open("logs/realtime-access-2.log"))
    log3 = follow(open("logs/realtime-access.log"))
    # log = multiplex([log1, log2])
    # for line in log:
    #     print(line, end="")
    log = gen_multiplex([log1, log2, log3])
    for line, thread_id in log:
        print(f"[{thread_id}] {line}", end="")
