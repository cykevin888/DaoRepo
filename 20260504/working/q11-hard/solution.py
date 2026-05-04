def find_next_task(tasks, finished, current_time):
    chosen = -1
    i = 0

    while i < len(tasks):
        request_time, duration = tasks[i]

        if not finished[i] and request_time <= current_time:
            if chosen == -1:
                chosen = i
            else:
                chosen_request, chosen_duration = tasks[chosen]

                if duration < chosen_duration:
                    chosen = i
                elif duration == chosen_duration and request_time < chosen_request:
                    chosen = i

        i += 1

    return chosen


def move_to_next_request_time(tasks, finished, current_time):
    next_time = -1
    i = 0

    while i < len(tasks):
        request_time, duration = tasks[i]

        if not finished[i] and request_time > current_time:
            if next_time == -1 or request_time < next_time:
                next_time = request_time

        i += 1

    return next_time


def get_average_waiting_time(request_times, durations):
    tasks = []
    i = 0

    while i < len(request_times):
        tasks.append((request_times[i], durations[i]))
        i += 1

    tasks.sort()

    if not tasks:
        return 0

    current_time = tasks[0][0]
    total_waiting_time = 0
    total_tasks = len(tasks)
    finished = [False] * total_tasks
    finished_count = 0

    while finished_count < total_tasks:
        next_task = find_next_task(tasks, finished, current_time)

        if next_task == -1:
            current_time = move_to_next_request_time(tasks, finished, current_time)
            continue

        request_time, duration = tasks[next_task]
        start_time = current_time
        waiting_time = start_time - request_time
        total_waiting_time += waiting_time
        current_time += duration
        finished[next_task] = True
        finished_count += 1

    return total_waiting_time // total_tasks


def solve():
    req_size = int(input())
    request_times = list(map(int, input().split()))

    dur_size = int(input())
    durations = list(map(int, input().split()))

    if req_size != dur_size:
        print(0)
        return

    answer = get_average_waiting_time(request_times, durations)
    print(answer)


if __name__ == "__main__":
    solve()
