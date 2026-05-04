def min_price(n, m1, p1, m2, p2):
    best = None

    # 枚举第一家商店买多少 lot，剩余部分必须能被第二家整除。
    for count1 in range(n // m1 + 1):
        remain = n - count1 * m1
        if remain % m2 != 0:
            continue

        count2 = remain // m2
        cost = count1 * p1 + count2 * p2

        if best is None or cost < best:
            best = cost

    return best


def solve():
    n = int(input().strip())
    m1, p1 = map(int, input().split())
    m2, p2 = map(int, input().split())

    print(min_price(n, m1, p1, m2, p2))


def main():
    solve()


if __name__ == "__main__":
    main()
