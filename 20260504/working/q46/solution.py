def max_internal_run(s):
    n = len(s)
    best = 0
    i = 0

    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1

        # 题目要求连续段不能出现在字符串的开头或结尾。
        if i > 0 and j < n:
            length = j - i
            if length > best:
                best = length

        i = j

    return best


def solve():
    n = int(input().strip())
    s = input().strip()

    print(max_internal_run(s))


def main():
    solve()


if __name__ == "__main__":
    main()
