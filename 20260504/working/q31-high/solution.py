def is_right_rotation(word1, word2):
    if len(word1) != len(word2):
        return False
    return word1 in (word2 + word2)


def solve():
    word1 = input().strip()
    word2 = input().strip()

    if is_right_rotation(word1, word2):
        print(1)
    else:
        print(-1)


def main():
    solve()


if __name__ == "__main__":
    main()
