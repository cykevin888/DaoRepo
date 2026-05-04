def heap_push(heap, item):
    heap.append(item)
    index = len(heap) - 1

    while index > 0:
        parent = (index - 1) // 2
        if heap[parent] <= heap[index]:
            break
        heap[parent], heap[index] = heap[index], heap[parent]
        index = parent


def heap_pop(heap):
    last = heap.pop()
    if not heap:
        return last

    top = heap[0]
    heap[0] = last
    index = 0
    size = len(heap)

    while True:
        left = index * 2 + 1
        right = left + 1
        smallest = index

        if left < size and heap[left] < heap[smallest]:
            smallest = left
        if right < size and heap[right] < heap[smallest]:
            smallest = right

        if smallest == index:
            break

        heap[index], heap[smallest] = heap[smallest], heap[index]
        index = smallest

    return top


def average_waiting_time(tasks):
    tasks.sort()
    heap = []
    time = 0
    index = 0
    n = len(tasks)
    total_wait = 0

    if n > 0:
        time = tasks[0][0]

    while index < n or heap:
        while index < n and tasks[index][0] <= time:
            request, duration = tasks[index]
            heap_push(heap, (duration, request))
            index += 1

        if not heap:
            time = tasks[index][0]
            continue

        duration, request = heap_pop(heap)
        total_wait += time - request
        time += duration

    return total_wait / n


def solve():
    n = int(input().strip())
    req = list(map(int, input().split()))
    dur = list(map(int, input().split()))

    tasks = []
    for i in range(n):
        tasks.append((req[i], dur[i]))

    answer = average_waiting_time(tasks)
    print("{:.2f}".format(answer))


def main():
    solve()


if __name__ == "__main__":
    main()
