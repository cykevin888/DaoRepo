def count_digit_occurrences(needle, haystack):
    # 把数字转成字符串后逐个字符统计
    needle_char = str(needle)
    text = str(haystack)

    count = 0
    for ch in text:
        if ch == needle_char:
            count += 1
    return count


def main():
    needle = int(input().strip())
    haystack = int(input().strip())

    result = count_digit_occurrences(needle, haystack)
    print(result)


if __name__ == "__main__":
    main()