def build_segments(bus_lines):
    segments = []

    for start, end in bus_lines:
        # 保证每个区间都是左小右大，方便后面统一合并。
        if start > end:
            start, end = end, start

        segments.append([start, end])

    return segments


def merge_segments(segments):
    if not segments:
        return []

    segments.sort()
    merged = []

    current_start = segments[0][0]
    current_end = segments[0][1]

    i = 1
    while i < len(segments):
        next_start = segments[i][0]
        next_end = segments[i][1]

        # 有重叠时，把当前区间向右扩展即可。
        if next_start <= current_end:
            if next_end > current_end:
                current_end = next_end
        else:
            # 没有重叠，先保存当前合并结果，再开始新的区间。
            merged.append([current_start, current_end])
            current_start = next_start
            current_end = next_end

        i += 1

    merged.append([current_start, current_end])
    return merged


def get_total_distance(bus_lines):
    segments = build_segments(bus_lines)
    merged = merge_segments(segments)
    total_distance = 0

    for start, end in merged:
        # 站点之间单位距离相等，所以区间长度就是 end - start。
        total_distance += end - start

    return total_distance


def solve():
    first_line = list(map(int, input().split()))
    if not first_line:
        print(0)
        return

    n = first_line[0]
    pair_size = first_line[1]

    bus_lines = []
    count = 0

    while count < n:
        start, end = map(int, input().split())
        bus_lines.append([start, end])
        count += 1

    answer = get_total_distance(bus_lines)
    print(answer)


if __name__ == "__main__":
    solve()
