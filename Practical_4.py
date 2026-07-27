print("Deepak Sahani")
processes = ["P1", "P2", "P3", "P4"]
arrival_time = [0, 1, 2, 3]
burst_time = [5, 3, 8, 6]
completion_time = []
turnaround_time = []
waiting_time = []
current_time = 0
for i in range(len(processes)):
    if current_time < arrival_time[i]:
        current_time = arrival_time[i]
    current_time += burst_time[i]
    completion_time.append(current_time)
for i in range(len(processes)):
    tat = completion_time[i] - arrival_time[i]
    wt = tat - burst_time[i]
    turnaround_time.append(tat)
    waiting_time.append(wt)
avg_wt = sum(waiting_time) / len(processes)
avg_tat = sum(turnaround_time) / len(processes)
print("\n========== FCFS Scheduling Result ==========")
print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
    "Process", "AT", "BT", "CT", "TAT", "WT"
))
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
print("\n========== Gantt Chart ==========")
for p in processes:
    print(f"| {p} ", end="")
print("|")
print("0", end="")
for ct in completion_time:
    print(f"\t{ct}", end="")
print()
