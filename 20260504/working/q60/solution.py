def remove_vowels(text):
    vowels = "aeiouAEIOU"
    answer = []

    for ch in text:
        if ch not in vowels:
            answer.append(ch)

    return "".join(answer)


def solve():
    text = input().strip()
    print(remove_vowels(text))


def main():
    solve()


if __name__ == "__main__":
    main()
