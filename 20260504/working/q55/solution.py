def is_perfect_square(num):
    root = int(num ** 0.5)
    return root * root == num


def count_discount_customers(bills):
    count = 0

    for bill in bills:
        if is_perfect_square(bill):
            count += 1

    return count


def solve():
    n = int(input().strip())
    bills = list(map(int, input().split()))

    print(count_discount_customers(bills))


def main():
    solve()


if __name__ == "__main__":
    main()
