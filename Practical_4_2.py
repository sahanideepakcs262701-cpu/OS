print("Deepak Sahani")
processes = ["P1", "P2", "P3", "P4"]
arrival_time = [0, 2, 4, 5]
burst_time = [7, 4, 1, 4]

completed = [False] * len(processes)
completion_time = [0] * len(processes)
turnaround_time = [0] * len(processes)
waiting_time = [0] * len(processes)

gantt = []
time = 0
count = 0

while count < len(processes):
    idx = -1
    minimum = float('inf')

    for i in range(len(processes)):
        if arrival_time[i] <= time and not completed[i]:
            if burst_time[i] < minimum:
                minimum = burst_time[i]
                idx = i

    if idx == -1:
        time += 1
        continue

    start = time
    time += burst_time[idx]
    end = time

    completion_time[idx] = end
    turnaround_time[idx] = end - arrival_time[idx]
    waiting_time[idx] = turnaround_time[idx] - burst_time[idx]

    completed[idx] = True
    count += 1

    gantt.append((processes[idx], start, end))

avg_wt = sum(waiting_time) / len(processes)
avg_tat = sum(turnaround_time) / len(processes)

print("\n========== Non-Preemptive SJF Scheduling ==========\n")
print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
    "Process", "AT", "BT", "CT", "TAT", "WT"))

for i in range(len(processes)):
    print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
        processes[i],
        arrival_time[i],
        burst_time[i],
        completion_time[i],
        turnaround_time[i],
        waiting_time[i]
    ))

print("\nAverage Waiting Time    = {:.2f}".format(avg_wt))
print("Average Turnaround Time = {:.2f}".format(avg_tat))

print("\n========== Gantt Chart ==========\n")

for p, s, e in gantt:
    print("+--------", end="")
print("+")

for p, s, e in gantt:
    print("|{:^8}".format(p), end="")
print("|")

for p, s, e in gantt:
    print("+--------", end="")
print("+")

print(gantt[0][1], end="")
for p, s, e in gantt:
    print("{:>9}".format(e), end="")
print()
