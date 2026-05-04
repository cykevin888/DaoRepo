def count_pairs_with_difference(arr, k):
    if k < 0:
        return 0

    freq = {}
    for num in arr:
        if num not in freq:
            freq[num] = 0
        freq[num] += 1

    answer = 0

    if k == 0:
        for num in freq:
            count = freq[num]
            answer += count * (count - 1) // 2
    else:
        for num in freq:
            other = num + k
            if other in freq:
                answer += freq[num] * freq[other]

    return answer


def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    k = int(input().strip())

    print(count_pairs_with_difference(arr, k))


def main():
    solve()


if __name__ == "__main__":
    main()
