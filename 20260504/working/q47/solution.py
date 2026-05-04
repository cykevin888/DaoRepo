def build_tree(n, edges):
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return graph


def solve():
    n, r = map(int, input().split())
    edges = []
    raw_edges = []

    for _ in range(r):
        a, b = map(int, input().split())
        raw_edges.append((a, b))
        edges.append((a - 1, b - 1))

    graph = build_tree(n, edges)
    parent = [-1] * n
    parent[0] = 0
    order = [0]
    head = 0

    while head < len(order):
        node = order[head]
        head += 1

        for nxt in graph[node]:
            if nxt == parent[node]:
                continue
            parent[nxt] = node
            order.append(nxt)

    subtree = [1] * n

    for node in range(len(order) - 1, 0, -1):
        current = order[node]
        subtree[parent[current]] += subtree[current]

    best_value = -1
    best_pair = None

    for node in range(1, n):
        size = subtree[node]
        value = size * (n - size)
        pair = [node + 1, parent[node] + 1]
        pair.sort()

        if value > best_value:
            best_value = value
            best_pair = pair
        elif value == best_value and pair < best_pair:
            best_pair = pair

    print(best_pair[0], best_pair[1])


def main():
    solve()


if __name__ == "__main__":
    main()
