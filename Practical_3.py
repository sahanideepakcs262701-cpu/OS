import threading
import time

def task(name):
    print(f"{name} started")
    time.sleep(2)
    print(f"{name} finished")

print("\n--- Sequential Execution ---")

start_time = time.time()

task("Task 1")
task("Task 2")

end_time = time.time()

print("Sequential Execution Time:", round(end_time - start_time, 2), "seconds")

print("\n--- Threaded Execution ---")

start_time = time.time()

t1 = threading.Thread(target=task, args=("Task 1",))
t2 = threading.Thread(target=task, args=("Task 2",))

t1.start()
t2.start()

t1.join()
t2.join()

end_time = time.time()

print("Threaded Execution Time:", round(end_time - start_time, 2), "seconds")
