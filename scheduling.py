import random

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = 0
        self.turnaround_time = 0

def fcfs(processes):
    processes.sort(key=lambda p: p.arrival_time)
    # the sorting is only done to jump to next process quickly
    current_time = 0
    schedule = [] # the order in which the processes finished execution
    total_burst_time = 0
    avg_turnaround_time,avg_waiting_time,cpu_utilisation = 0,0,0
    for process in processes:
        process.start_time = max(current_time, process.arrival_time) # if the process is not yet arrived , we wait for it
        # if a process came before the other ends , he waits , else he directly starts running
        current_time = process.start_time + process.burst_time
        process.completion_time = current_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
       
        total_burst_time += process.burst_time # the total time taken by all processes
        avg_turnaround_time += process.turnaround_time # the average time between arrival and completion among all processes
        avg_waiting_time += process.waiting_time       # the average waiting time among all processes(a process is waiting if it is in the system but not running)  
        schedule.append(process.pid)

    makespan = processes[-1].completion_time   # the total time taken by all processes
    # we assume that the cpu utilization starts counting since time 0(for all algorithms)
    cpu_utilisation = ( total_burst_time/ makespan) * 100  # the sum of running time divided by the makespan (in percentage)
    avg_turnaround_time /= len(processes) # take the average of the turnaround time
    avg_waiting_time /= len(processes) # take the average of the waiting time
    return schedule, avg_turnaround_time,   avg_waiting_time, cpu_utilisation


def sjf(processes): 
    l = len(processes)
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    current_time, schedule = 0, []
    avg_turnaround_time,avg_waiting_time,total_burst_time = 0,0,0
    while processes:
        available = [p for p in processes if p.arrival_time <= current_time]
        # all processes that can be runned now
        # if no process is available , we go to the time of the start of next process 
        if not available: 
            current_time = processes[0].arrival_time
            continue
        process = min(available, key=lambda p: p.burst_time)
        #the process with the shortest burst time is selected
        processes.remove(process)
        process.start_time = current_time

        current_time += process.burst_time
        process.completion_time = current_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

        avg_waiting_time += process.waiting_time
        avg_turnaround_time += process.turnaround_time
        total_burst_time += process.burst_time
    
        schedule.append(process.pid)
    avg_turnaround_time /= l
    avg_waiting_time /= l
    makespan = current_time 
    cpu_utilization = (total_burst_time/makespan) *100
    return schedule, avg_turnaround_time, avg_waiting_time,cpu_utilization




def priority_scheduling(processes): # Priority Scheduling (Non-Preemptive)
    # HIGH PRIORITY MEANS LOW NUMBER 
    avg_turnaround_time,avg_waiting_time = 0,0
    l = len(processes)
    processes.sort(key=lambda x: (x.arrival_time, x.priority)) # sort by arrival time and then by priority
    current_time, schedule = 0, []
    total_burst_time = 0
    while processes:
        available = [p for p in processes if p.arrival_time <= current_time] # all processes that can be runned now
        if not available:
            current_time = processes[0].arrival_time
            continue
        process = min(available, key=lambda p: p.priority) # the process with the highest priority
        processes.remove(process)
        process.start_time = current_time
        current_time += process.burst_time
        process.completion_time = current_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

        avg_waiting_time += process.waiting_time
        avg_turnaround_time += process.turnaround_time
        total_burst_time += process.burst_time

        schedule.append(process.pid) # Non preemptive so it will run to completion
    avg_turnaround_time /= l
    avg_waiting_time /= l
    makespan = (current_time)
    cpu_utilization = (total_burst_time/makespan) * 100
    return schedule, avg_turnaround_time, avg_waiting_time,cpu_utilization


  

def round_robin(processes, quantum=1):
    for p in processes:
        p.remaining_time = p.burst_time
    processes.sort(key=lambda p: p.arrival_time) # sort by arrival time
    queue = []
    current_time = 0
    schedule = []
    remaining = processes[:]
    avg_turnaround_time, avg_waiting_time, total_burst_time = 0, 0, 0
    timeline = [] # to keep track of the execution timeline, we will use it to show the order of execution in the Gantt chart

    while queue or remaining:
        if queue:
            p = queue.pop(0)
            exec_time = min(p.remaining_time, quantum) # each process will run for a quantum time or the remaining time(whichever is smaller)
            start_exec = current_time
            current_time += exec_time
            p.remaining_time -= exec_time
            timeline.append((p.pid, start_exec, current_time))

            while remaining and remaining[0].arrival_time <= current_time: # add all processes that have arrived when we were executing
                queue.append(remaining.pop(0))

            if p.remaining_time == 0: # the process has finished executing, save its informations
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                avg_waiting_time += p.waiting_time
                avg_turnaround_time += p.turnaround_time
                total_burst_time += p.burst_time
                schedule.append(p.pid)
            else:
                queue.append(p)
        else:
            current_time = remaining[0].arrival_time
            while remaining and remaining[0].arrival_time <= current_time:
                queue.append(remaining.pop(0))

    avg_turnaround_time /= len(processes)
    avg_waiting_time /= len(processes)
    makespan = current_time 
    cpu_util = (total_burst_time / makespan) * 100
    return schedule, avg_turnaround_time, avg_waiting_time, cpu_util, timeline



def priority_rr(processes, quantum=1):
    for p in processes:
        p.remaining_time = p.burst_time
    processes.sort(key=lambda p: p.arrival_time) # sort by arrival time
    current_time = processes[0].arrival_time
    timeline = []
    avg_turnaround_time, avg_waiting_time, total_burst_time = 0, 0, 0
    schedule = []
    queue = [p for p in processes if p.arrival_time <= current_time] # select the processes that have arrived
    queue = sorted(queue, key=lambda p: p.priority) # sort by priority
    
    while queue:
        p = queue.pop(0) # take the process with the highest priority among the available processes
        if p.arrival_time > current_time:
            current_time = p.arrival_time
        start_exec = current_time
        exec_time = min(p.remaining_time, quantum)
        p.remaining_time -= exec_time
        current_time += exec_time
        timeline.append((p.pid, start_exec, current_time))

        if p.remaining_time == 0:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            avg_waiting_time += p.waiting_time
            avg_turnaround_time += p.turnaround_time
            total_burst_time += p.burst_time
            schedule.append(p.pid)
        else:
            queue.append(p)

        incoming = [x for x in processes if x.remaining_time > 0 and x.arrival_time <= current_time and x not in queue] # add new processes that have arrived and were not in the queue
        queue.extend(incoming)
        if not queue: # if no process is left in the queue, we need to wait for the next process to arrive(shift the current time)
            future = [x for x in processes if x.remaining_time > 0 and x.arrival_time > current_time]
            if future:
                current_time = min(f.arrival_time for f in future)
                queue.extend([x for x in future if x.arrival_time <= current_time])
        queue = sorted(queue, key=lambda p: p.priority) # we sort the available processes by priority to take the one with the highest priority in the next iteration

    avg_turnaround_time /= len(processes)
    avg_waiting_time /= len(processes)
    makespan = current_time 
    cpu_util = (total_burst_time / makespan) * 100
    return schedule, avg_turnaround_time, avg_waiting_time, cpu_util, timeline


file = "processes.txt"
# Reading processes from a file(.txt .csv)
def read_processes_from_file(filepath):
    processes = []
    with open(filepath, 'r') as file:
        for lineno, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue  # skip empty lines

            parts = line.split(',')
            if not (3 <= len(parts) <= 4):
                raise ValueError(f"[Line {lineno}] Expected 3 or 4 values, got {len(parts)}: {line}")

            try:
                parts = list(map(int, parts))
            except ValueError:
                raise ValueError(f"[Line {lineno}] Non-integer value found: {line}")

            pid, arrival, burst = parts[:3]
            priority = parts[3] if len(parts) == 4 else 0

            # Check for negative values
            if any(val < 0 for val in [pid, arrival, burst, priority]):
                raise ValueError(f"[Line {lineno}] Negative value not allowed: {line}")

            processes.append(Process(pid, arrival, burst, priority))
    return processes

# Generating random processes(random arrival and burst times)
def generate_random_processes(n, arrival_range=(0, 10), burst_range=(1, 10), priority_range=(0, 5)):
    processes = []
    for i in range(1, n + 1):
        arrival_time = random.randint(*arrival_range)
        burst_time = random.randint(*burst_range)
        priority = random.randint(*priority_range)
        processes.append(Process(pid=i, arrival_time=arrival_time, burst_time=burst_time, priority=priority))
    return processes


# function to print the processes in a formatted table
def print_processes(processes):
    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<8}{'Priority':<10}{'Remaining':<10}{'Completion':<12}")
    print("-" * 55)
    for p in processes:
        print(f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<8}{p.priority:<10}{p.remaining_time:<10}"
              f"{p.completion_time if p.completion_time is not None else '-':<12}")

algorithms = {
    "FCFS": fcfs,
    "SJF": sjf,
    "Priority": priority_scheduling,
    "Round Robin": round_robin,
    "Priority + RR": priority_rr
}