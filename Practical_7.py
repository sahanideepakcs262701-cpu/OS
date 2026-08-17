import threading
import time

BUFFER_SIZE = 5
buffer = [None] * BUFFER_SIZE
in_index = 0
out_index = 0

mutex = threading.Semaphore(1)
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)

def producer():
    global in_index
    for item in range(1, 11):
        empty.acquire()
        mutex.acquire()

        buffer[in_index] = item
        print(f"Produced: {item}")
        in_index = (in_index + 1) % BUFFER_SIZE

        mutex.release()
        full.release()
        time.sleep(0.5)

def consumer():
    global out_index
    for _ in range(10):
        full.acquire()
        mutex.acquire()

        item = buffer[out_index]
        buffer[out_index] = None
        print(f"Consumed: {item}")
        out_index = (out_index + 1) % BUFFER_SIZE

        mutex.release()
        empty.release()
        time.sleep(1)

producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

print("Process completed successfully.")
