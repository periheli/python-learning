from queue import Queue
from re import S
from threading import Thread


def gen_from_queue(queue: Queue):
    while True:
        item = queue.get()
        if item is StopIteration:
            queue.put(StopIteration)
            break
        yield item


def send_to_queue(source, queue: Queue):
    for item in source:
        queue.put(item)
    queue.put(StopIteration)


if __name__ == "__main__":

    def consumer(queue: Queue, thread_id: int = 0):
        print(f"Thread {thread_id} started")
        for item in gen_from_queue(queue):
            print(f"[{thread_id}] Consumed", item)
        print("Done consuming")

    queue = Queue()
    consumer_thread = Thread(target=consumer, args=(queue, 1))
    consumer_thread.start()
    consumer_thread_2 = Thread(target=consumer, args=(queue, 2))
    consumer_thread_2.start()

    send_to_queue(range(5), queue)
