def sort_parts(arr, k):
    left = arr[:k]
    right = arr[k:]

    left.sort()
    right.sort(reverse=True)

    return left + right


def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    k = int(input().strip())

    result = sort_parts(arr, k)
    print(*result)


def main():
    solve()


if __name__ == "__main__":
    main()
