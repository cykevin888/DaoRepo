def find_best_gap(houses):
    houses.sort(key=lambda item: item[1])

    best_gap = -1
    best_pair = None

    for i in range(len(houses) - 1):
        left_num, left_pos = houses[i]
        right_num, right_pos = houses[i + 1]
        gap = right_pos - left_pos
        pair = [left_num, right_num]
        pair.sort()

        if gap > best_gap:
            best_gap = gap
            best_pair = pair

    return best_pair


def solve():
    n, _ = map(int, input().split())
    houses = []

    for _ in range(n):
        h, p = map(int, input().split())
        houses.append([h, p])

    answer = find_best_gap(houses)
    print(answer[0], answer[1])


def main():
    solve()


if __name__ == "__main__":
    main()
