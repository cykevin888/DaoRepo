def count_not_common(arr1, arr2):
    set1 = {}
    set2 = {}

    for num in arr1:
        set1[num] = True
    for num in arr2:
        set2[num] = True

    count = 0

    for num in arr1:
        if num not in set2:
            count += 1

    for num in arr2:
        if num not in set1:
            count += 1

    return count


def solve():
    n, m = map(int, input().split())
    arr1 = list(map(int, input().split()))
    arr2 = list(map(int, input().split()))

    print(count_not_common(arr1, arr2))


def main():
    solve()


if __name__ == "__main__":
    main()
