def normalize_ids(likes):
    n = len(likes)
    if n == 0:
        return likes, 0

    if min(likes) == 1 and max(likes) == n:
        return [x - 1 for x in likes], 1

    return likes, 0


def better_path(path_a, path_b):
    if len(path_a) != len(path_b):
        return len(path_a) > len(path_b)
    return sorted(path_a) < sorted(path_b)


def solve():
    n = int(input().strip())
    likes = list(map(int, input().split()))
    likes, offset = normalize_ids(likes)

    indegree = [0] * n
    for x in likes:
        indegree[x] += 1

    best_path = []
    for i in range(n):
        best_path.append([i])

    queue = []
    for i in range(n):
        if indegree[i] == 0:
            queue.append(i)

    head = 0
    removed = [False] * n

    while head < len(queue):
        node = queue[head]
        head += 1
        removed[node] = True
        nxt = likes[node]

        candidate = best_path[node] + [nxt]
        if better_path(candidate, best_path[nxt]):
            best_path[nxt] = candidate

        indegree[nxt] -= 1
        if indegree[nxt] == 0:
            queue.append(nxt)

    state = [0] * n
    cycles = []

    for i in range(n):
        if removed[i] or state[i] != 0:
            continue

        order = []
        pos = {}
        cur = i

        while state[cur] == 0:
            state[cur] = 1
            pos[cur] = len(order)
            order.append(cur)
            cur = likes[cur]

        if state[cur] == 1 and cur in pos:
            cycle = order[pos[cur]:]
            cycles.append(cycle)

        for node in order:
            state[node] = 2

    best_cycle = []
    pair_union = []

    for cycle in cycles:
        if len(cycle) == 2:
            a = cycle[0]
            b = cycle[1]

            path_a = best_path[a][:-1]
            path_b = best_path[b][:-1]
            pair_union.extend(path_a)
            pair_union.append(a)
            pair_union.append(b)
            pair_union.extend(path_b)
        else:
            candidate = sorted(cycle)
            if len(candidate) > len(best_cycle) or (len(candidate) == len(best_cycle) and candidate < best_cycle):
                best_cycle = candidate

    pair_union = sorted(pair_union)

    if len(pair_union) > len(best_cycle):
        answer = pair_union
    elif len(pair_union) < len(best_cycle):
        answer = best_cycle
    else:
        if pair_union and (not best_cycle or pair_union < best_cycle):
            answer = pair_union
        else:
            answer = best_cycle

    if offset == 1:
        answer = [x + 1 for x in answer]

    print(*answer)


def main():
    solve()


if __name__ == "__main__":
    main()
