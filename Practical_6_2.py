from collections import deque

processes = [
    ("P1", 0, 5),
    ("P2", 1, 3),
    ("P3", 2, 6)
]

quantum = 2


def round_robin(processes, quantum):
    processes = sorted(processes, key=lambda x: x[1])

    remaining = {p[0]: p[2] for p in processes}
    completion = {}
    queue = deque()

    time = 0
    index = 0
    gantt = []

    while index < len(processes) or queue:

        if not queue:
            time = max(time, processes[index][1])

            while index < len(processes) and processes[index][1] <= time:
                queue.append(processes[index])
                index += 1

        pid, arrival, burst = queue.popleft()

        start = time
        execution = min(quantum, remaining[pid])
        time += execution
        remaining[pid] -= execution

        gantt.append((pid, start, time))

        while index < len(processes) and processes[index][1] <= time:
            queue.append(processes[index])
            index += 1

        if remaining[pid] > 0:
            queue.append((pid, arrival, burst))
        else:
            completion[pid] = time

    total_tat = 0
    total_wt = 0

    print("Gantt Chart:")
    for pid, start, end in gantt:
        print(f"| {pid} {start}-{end} ", end="")
    print("|")

    print("\nProcess\tAT\tBT\tCT\tTAT\tWT")

    for pid, arrival, burst in processes:
        ct = completion[pid]
        tat = ct - arrival
        wt = tat - burst

        total_tat += tat
        total_wt += wt

        print(f"{pid}\t{arrival}\t{burst}\t{ct}\t{tat}\t{wt}")

    n = len(processes)

    print(f"\nAverage Turnaround Time: {total_tat / n:.2f} ms")
    print(f"Average Waiting Time: {total_wt / n:.2f} ms")


round_robin(processes, quantum)
