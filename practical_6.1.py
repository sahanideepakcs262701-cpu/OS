from collections import deque

processes = [
    ("P1", 0, 5),
    ("P2", 4, 2),
    ("P3", 5, 4)
]

quantum = 2


def round_robin(processes, quantum):
    processes = sorted(processes, key=lambda x: x[1])

    remaining = {p[0]: p[2] for p in processes}
    completion = {}
    first_response = {}
    queue = deque()

    time = 0
    index = 0
    context_switches = 0
    last_process = None
    gantt = []

    while index < len(processes) or queue:

        if not queue:
            time = max(time, processes[index][1])

            while index < len(processes) and processes[index][1] <= time:
                queue.append(processes[index])
                index += 1

        process = queue.popleft()
        pid, arrival, burst = process

        if pid not in first_response:
            first_response[pid] = time - arrival

        if last_process is not None and last_process != pid:
            context_switches += 1

        execution = min(quantum, remaining[pid])

        start = time
        time += execution
        remaining[pid] -= execution

        gantt.append((pid, start, time))
        last_process = pid

        while index < len(processes) and processes[index][1] <= time:
            queue.append(processes[index])
            index += 1

        if remaining[pid] > 0:
            queue.append(process)
        else:
            completion[pid] = time

    results = []

    for pid, arrival, burst in processes:
        turnaround = completion[pid] - arrival
        waiting = turnaround - burst
        response = first_response[pid]

        results.append((pid, arrival, burst, completion[pid],
                        turnaround, waiting, response))

    return results, context_switches, gantt


def fcfs(processes):
    processes = sorted(processes, key=lambda x: x[1])

    time = 0
    context_switches = 0
    results = []
    gantt = []

    for pid, arrival, burst in processes:

        if time < arrival:
            time = arrival

        start = time
        time += burst

        completion = time
        turnaround = completion - arrival
        waiting = turnaround - burst
        response = start - arrival

        results.append((pid, arrival, burst, completion,
                        turnaround, waiting, response))

        gantt.append((pid, start, time))
        context_switches += 1

    return results, max(0, context_switches - 1), gantt


def display(title, results, context_switches, gantt):
    print("\n" + title)
    print("-" * 80)

    print("Gantt Chart:")
    for pid, start, end in gantt:
        print(f"| {pid} ({start}-{end}) ", end="")
    print("|")

    print("\nProcess\tAT\tBT\tCT\tTAT\tWT\tRT")

    total_tat = 0
    total_wt = 0
    total_rt = 0

    for pid, at, bt, ct, tat, wt, rt in results:
        print(f"{pid}\t{at}\t{bt}\t{ct}\t{tat}\t{wt}\t{rt}")

        total_tat += tat
        total_wt += wt
        total_rt += rt

    n = len(results)

    print(f"\nAverage Turnaround Time: {total_tat / n:.2f} ms")
    print(f"Average Waiting Time:    {total_wt / n:.2f} ms")
    print(f"Average Response Time:   {total_rt / n:.2f} ms")
    print(f"Context Switches:        {context_switches}")


rr_results, rr_switches, rr_gantt = round_robin(processes, quantum)
fcfs_results, fcfs_switches, fcfs_gantt = fcfs(processes)

display("ROUND ROBIN (Time Quantum = 2 ms)",
        rr_results, rr_switches, rr_gantt)

display("FCFS",
        fcfs_results, fcfs_switches, fcfs_gantt)
