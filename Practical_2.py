from multiprocessing import Process, Queue
import time
import random


def producer(queue):
    for i in range(5):
        item = random.randint(1, 100)
        print(f"Producer produced: {item}")
        queue.put(item)
        time.sleep(random.random())


def consumer(queue):
    for i in range(5):
        item = queue.get()
        print(f"Consumer consumed: {item}")
        time.sleep(random.random())


if __name__ == "__main__":
    q = Queue()

    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Producer and Consumer have finished.")
