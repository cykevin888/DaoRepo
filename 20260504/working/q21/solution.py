def reverse_substring(s, start, length):
    end = start + length
    return s[:start] + s[start:end][::-1] + s[end:]


def exact_min_steps(s, target):
    n = len(s)
    seen = {s: 0}
    queue = [s]
    head = 0

    while head < len(queue):
        current = queue[head]
        head += 1
        step = seen[current]

        if current == target:
            return step

        length = step + 2
        if length > n:
            continue

        for start in range(0, n - length + 1):
            nxt = reverse_substring(current, start, length)
            if nxt == current:
                continue
            if nxt not in seen:
                seen[nxt] = step + 1
                queue.append(nxt)

    return -1


def greedy_steps(s, target):
    n = len(s)
    current = s

    for step in range(1, n):
        length = step + 1
        best_string = current
        best_mismatch = n + 1

        # 当字符串较长时，使用“尽量减少错误位置”的贪心策略。
        for start in range(0, n - length + 1):
            candidate = reverse_substring(current, start, length)
            if candidate == current:
                continue

            mismatch = 0
            for i in range(n):
                if candidate[i] != target[i]:
                    mismatch += 1

            if mismatch < best_mismatch:
                best_mismatch = mismatch
                best_string = candidate

        if best_string == current:
            return -1

        current = best_string

        if current == target:
            return step

    return -1


def solve():
    s = input().strip()
    target = input().strip()

    if len(s) != len(target):
        print(-1)
        return

    if s == target:
        print(0)
        return

    if s.count("1") != target.count("1"):
        print(-1)
        return

    if len(s) <= 14:
        print(exact_min_steps(s, target))
    else:
        print(greedy_steps(s, target))


def main():
    solve()


if __name__ == "__main__":
    main()
