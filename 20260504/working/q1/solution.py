def arrange_even_then_odd(nums):
    evens = []
    odds = []

    for x in nums:
        if x % 2 == 0:
            evens.append(x)
        else:
            odds.append(x)

    return evens + odds


def main():
    n = int(input().strip())
    nums = list(map(int, input().split()))

    result = arrange_even_then_odd(nums)
    print(result)


if __name__ == "__main__":
    main()