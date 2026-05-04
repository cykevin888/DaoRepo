def count_occurrences(needle, haystack):
    target = str(needle)
    text = str(haystack)
    count = 0

    for ch in text:
        if ch == target:
            count += 1

    return count


def solve():
    needle = input().strip()
    haystack = input().strip()

    print(count_occurrences(needle, haystack))


def main():
    solve()


if __name__ == "__main__":
    main()
