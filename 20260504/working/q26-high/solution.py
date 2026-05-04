def get_state_list(line, n):
    parts = line.split()
    if len(parts) == n:
        return list(map(int, parts))
    return [int(ch) for ch in parts[0].strip()]


def next_day(state):
    n = len(state)
    new_state = [0] * n

    for i in range(n):
        left = 0 if i == 0 else state[i - 1]
        right = 0 if i == n - 1 else state[i + 1]

        if left == right:
            new_state[i] = 0
        else:
            new_state[i] = 1

    return new_state


def state_key(state):
    key = ""
    for num in state:
        key += str(num)
    return key


def get_state_after_days(state, days):
    seen = {}
    order = []
    current = state[:]
    day = 0

    while day < days:
        key = state_key(current)

        if key in seen:
            cycle_start = seen[key]
            cycle_length = day - cycle_start
            remain = (days - cycle_start) % cycle_length
            final_key = order[cycle_start + remain]
            return [int(ch) for ch in final_key]

        seen[key] = day
        order.append(key)
        current = next_day(current)
        day += 1

    return current


def solve():
    n = int(input().strip())
    state = get_state_list(input().strip(), n)
    days = int(input().strip())

    result = get_state_after_days(state, days)
    print(*result)


def main():
    solve()


if __name__ == "__main__":
    main()
