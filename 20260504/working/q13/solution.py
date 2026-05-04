def count_common_steps(x1, x2, v1, n, v2, father_set, last_pos):
    count = 0
    pos = x2 + v2
    while pos <= last_pos:
        if pos in father_set:
            count += 1
        pos += v2
    return count


def get_best_result(x1, x2, v1, n):
    father_positions = []
    father_set = {}

    for step in range(1, n + 1):
        pos = x1 + step * v1
        father_positions.append(pos)
        father_set[pos] = True

    best_f = 0
    best_v2 = 0
    last_pos = father_positions[-1]

    # 枚举 Martin 第一步会踩中的父亲脚印。
    for pos in father_positions:
        v2 = pos - x2
        if v2 <= 0:
            continue

        common = count_common_steps(x1, x2, v1, n, v2, father_set, last_pos)

        if common > best_f or (common == best_f and v2 > best_v2):
            best_f = common
            best_v2 = v2

    return best_f, best_v2


def solve():
    x1 = int(input().strip())
    x2 = int(input().strip())
    v1 = int(input().strip())
    n = int(input().strip())

    f, v2 = get_best_result(x1, x2, v1, n)
    print(f, v2)


def main():
    solve()


if __name__ == "__main__":
    main()
