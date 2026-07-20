import threading
import time

def task(name):
    print(f"{name} started")
    time.sleep(2)
    print(f"{name} finished")

print("\n===== Sequential Execution =====")

start_time = time.time()

task("Task 1")
task("Task 2")
task("Task 3")
task("Task 4")

end_time = time.time()

print(f"\nSequential Execution Time: {end_time - start_time:.2f} seconds")

print("\n===== Threaded Execution =====")

threads = []

start_time = time.time()

for i in range(1, 5):
    t = threading.Thread(target=task, args=(f"Task {i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.time()

print(f"\nThreaded Execution Time: {end_time - start_time:.2f} seconds")
