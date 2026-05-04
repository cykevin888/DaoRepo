def alternate_sort(arr):
    arr.sort()
    answer = []
    index = 0

    while index < len(arr):
        answer.append(arr[index])
        index += 2

    return answer


def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))

    result = alternate_sort(arr)
    print(*result)


def main():
    solve()


if __name__ == "__main__":
    main()
