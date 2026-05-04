def count_less_than_k(arr, k):
    count = 0

    for num in arr:
        if num < k:
            count += 1

    return count


def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    k = int(input().strip())

    print(count_less_than_k(arr, k))


def main():
    solve()


if __name__ == "__main__":
    main()
