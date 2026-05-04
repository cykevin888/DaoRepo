def build_order(adj, root):
    parent = [-1] * len(adj)
    parent[root] = root
    order = [root]
    head = 0

    while head < len(order):
        node = order[head]
        head += 1

        for nxt in adj[node]:
            if nxt == parent[node]:
                continue
            parent[nxt] = node
            order.append(nxt)

    return parent, order


def get_max_leaf_to_leaf_product(values, adj):
    n = len(values)
    if n == 1:
        return values[0]
    if n == 2:
        return values[0] * values[1]

    root = 0
    for i in range(n):
        if len(adj[i]) >= 2:
            root = i
            break

    parent, order = build_order(adj, root)
    down_max = [0] * n
    down_min = [0] * n
    best_answer = None

    for node in reversed(order):
        child_values = []

        for nxt in adj[node]:
            if nxt == parent[node]:
                continue
            child_values.append((down_max[nxt], down_min[nxt]))

        if not child_values:
            down_max[node] = values[node]
            down_min[node] = values[node]
            continue

        possible_down = []
        for child_max, child_min in child_values:
            possible_down.append(values[node] * child_max)
            possible_down.append(values[node] * child_min)

        down_max[node] = max(possible_down)
        down_min[node] = min(possible_down)

        if len(child_values) >= 2:
            for i in range(len(child_values)):
                for j in range(i + 1, len(child_values)):
                    a_max, a_min = child_values[i]
                    b_max, b_min = child_values[j]

                    for left in (a_max, a_min):
                        for right in (b_max, b_min):
                            value = values[node] * left * right
                            if best_answer is None or value > best_answer:
                                best_answer = value

    return best_answer


def solve():
    n = int(input().strip())
    values = list(map(int, input().split()))
    edge_count, _ = map(int, input().split())
    adj = [[] for _ in range(n)]

    for _ in range(edge_count):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        adj[a].append(b)
        adj[b].append(a)

    print(get_max_leaf_to_leaf_product(values, adj))


def main():
    solve()


if __name__ == "__main__":
    main()
