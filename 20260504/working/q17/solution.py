def replace_with_index(arr):
    n = len(arr)
    answer = [0] * n

    for index in range(n):
        value = arr[index]
        answer[value] = index

    return answer


def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))

    result = replace_with_index(arr)
    print(*result)


def main():
    solve()


if __name__ == "__main__":
    main()
