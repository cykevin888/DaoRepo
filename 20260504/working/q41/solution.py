def heap_push(heap, value):
    heap.append(value)
    index = len(heap) - 1

    while index > 0:
        parent = (index - 1) // 2
        if heap[parent] >= heap[index]:
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
        largest = index

        if left < size and heap[left] > heap[largest]:
            largest = left
        if right < size and heap[right] > heap[largest]:
            largest = right

        if largest == index:
            break

        heap[index], heap[largest] = heap[largest], heap[index]
        index = largest

    return top


def min_stops(dist, fuel, target, start_energy):
    stalls = []
    for i in range(len(dist)):
        stalls.append((dist[i], fuel[i]))
    stalls.sort()

    heap = []
    stops = 0
    reach = start_energy
    index = 0
    n = len(stalls)

    while reach < target:
        while index < n and stalls[index][0] <= reach:
            heap_push(heap, stalls[index][1])
            index += 1

        if not heap:
            return -1

        reach += heap_pop(heap)
        stops += 1

    return stops


def solve():
    n = int(input().strip())
    dist = list(map(int, input().split()))
    fuel = list(map(int, input().split()))
    target, start_energy = map(int, input().split())

    print(min_stops(dist, fuel, target, start_energy))


def main():
    solve()


if __name__ == "__main__":
    main()
