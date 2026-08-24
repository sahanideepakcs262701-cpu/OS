import threading
import time
print("Deepak Sahani")

mutex = threading.Semaphore(1)
rw_mutex = threading.Semaphore(1)
queue = threading.Semaphore(1)

read_count = 0
shared_data = 0

def reader(reader_id, delay):
    global read_count

    time.sleep(delay)

    queue.acquire()
    mutex.acquire()

    read_count += 1

    if read_count == 1:
        rw_mutex.acquire()

    mutex.release()
    queue.release()

    print(f"Reader {reader_id} is reading. Shared Data = {shared_data}", flush=True)

    time.sleep(0.15)

    mutex.acquire()

    read_count -= 1

    if read_count == 0:
        rw_mutex.release()

    mutex.release()


def writer(writer_id, delay):
    global shared_data

    time.sleep(delay)

    queue.acquire()
    rw_mutex.acquire()
    queue.release()

    shared_data += 1

    print(f"Writer {writer_id} is writing. New Shared Data = {shared_data}", flush=True)

    time.sleep(0.15)

    rw_mutex.release()


threads = [
    threading.Thread(target=reader, args=(1, 0.1)),
    threading.Thread(target=writer, args=(1, 0.4)),
    threading.Thread(target=reader, args=(0, 0.7)),
    threading.Thread(target=writer, args=(0, 1.0)),
    threading.Thread(target=reader, args=(2, 1.3))
]

for t in threads:
    t.start()

for t in threads:
    t.join()

print("All readers and writers have finished.", flush=True)
