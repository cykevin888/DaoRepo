def stable_even_then_odd(arr):
    evens = []
    odds = []

    for num in arr:
        if num % 2 == 0:
            evens.append(num)
        else:
            odds.append(num)

    return evens + odds


def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))

    result = stable_even_then_odd(arr)
    print(*result)


def main():
    solve()


if __name__ == "__main__":
    main()
