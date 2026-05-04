def get_line_mask(points, i, j):
    x1, y1 = points[i]
    x2, y2 = points[j]
    mask = 0

    for index in range(len(points)):
        x, y = points[index]
        if (x - x1) * (y2 - y1) == (y - y1) * (x2 - x1):
            mask |= 1 << index

    return mask


def exact_cover(points):
    n = len(points)
    if n <= 1:
        return n

    line_masks = []
    for i in range(n):
        for j in range(i + 1, n):
            line_masks.append(get_line_mask(points, i, j))

    memo = {}

    def dp(mask):
        if mask == 0:
            return 0
        if mask in memo:
            return memo[mask]

        first_bit = mask & -mask
        first_index = first_bit.bit_length() - 1

        best = 1 + dp(mask ^ first_bit)

        for line_mask in line_masks:
            if (line_mask >> first_index) & 1:
                used = mask & line_mask
                if used:
                    value = 1 + dp(mask ^ used)
                    if value < best:
                        best = value

        memo[mask] = best
        return best

    return dp((1 << n) - 1)


def greedy_cover(points):
    remaining = list(range(len(points)))
    answer = 0

    while remaining:
        if len(remaining) <= 2:
            answer += 1
            break

        best_group = [remaining[0]]

        for i in range(len(remaining)):
            for j in range(i + 1, len(remaining)):
                p1 = points[remaining[i]]
                p2 = points[remaining[j]]
                group = []

                for idx in remaining:
                    x, y = points[idx]
                    if (x - p1[0]) * (p2[1] - p1[1]) == (y - p1[1]) * (p2[0] - p1[0]):
                        group.append(idx)

                if len(group) > len(best_group):
                    best_group = group

        remove = {}
        for idx in best_group:
            remove[idx] = True

        next_remaining = []
        for idx in remaining:
            if idx not in remove:
                next_remaining.append(idx)

        remaining = next_remaining
        answer += 1

    return answer


def solve():
    n = int(input().strip())
    points = []

    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))

    # 点数较小时使用精确状态压缩；点数过大时退化为贪心。
    if n <= 16:
        print(exact_cover(points))
    else:
        print(greedy_cover(points))


def main():
    solve()


if __name__ == "__main__":
    main()
