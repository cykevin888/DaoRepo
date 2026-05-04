def count_lucky_pairs(prices, k):
    n = len(prices)
    count = 0

    # 枚举所有 i < j 的商品对
    for i in range(n):
        for j in range(i + 1, n):
            # 价格差的绝对值等于 k 就计数
            if abs(prices[i] - prices[j]) == k:
                count += 1

    return count


def main():
    n = int(input().strip())
    prices = list(map(int, input().split()))
    k = int(input().strip())

    result = count_lucky_pairs(prices, k)
    print(result)


if __name__ == "__main__":
    main()