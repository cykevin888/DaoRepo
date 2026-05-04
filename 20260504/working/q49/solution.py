def sort_by_frequency(arr):
    freq = {}
    first_index = {}
    order = []

    for index in range(len(arr)):
        num = arr[index]
        if num not in freq:
            freq[num] = 0
            first_index[num] = index
            order.append(num)
        freq[num] += 1

    order.sort(key=lambda x: (-freq[x], first_index[x]))

    answer = []
    for num in order:
        count = freq[num]
        for _ in range(count):
            answer.append(num)

    return answer


def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))

    result = sort_by_frequency(arr)
    print(*result)


def main():
    solve()


if __name__ == "__main__":
    main()
