def maximum_attendees(arr):
    # 题目编号是 1~N，转成 0~N-1，方便当下标使用
    favorite = []
    for x in arr:
        favorite.append(x - 1)

    n = len(favorite)

    # 1. 统计每个点的入度
    indegree = [0] * n
    for i in range(n):
        indegree[favorite[i]] += 1

    # 2. 拓扑剥离 + DP
    # dp[i] 表示：能接到 i 前面的最长链长度（不包含 i 自己）
    dp = [0] * n

    queue = []
    for i in range(n):
        if indegree[i] == 0:
            queue.append(i)

    head = 0
    while head < len(queue):
        cur = queue[head]
        head += 1

        nxt = favorite[cur]

        # DP 转移：cur 这条链可以接到 nxt 前面
        if dp[cur] + 1 > dp[nxt]:
            dp[nxt] = dp[cur] + 1

        indegree[nxt] -= 1
        if indegree[nxt] == 0:
            queue.append(nxt)

    # 3. 处理所有环
    visited = [False] * n
    max_cycle = 0   # 长度 >= 3 的最大环
    pair_sum = 0    # 所有长度为 2 的环的总贡献

    for i in range(n):
        if indegree[i] > 0 and not visited[i]:
            cycle_nodes = []
            cur = i

            while not visited[cur]:
                visited[cur] = True
                cycle_nodes.append(cur)
                cur = favorite[cur]

            cycle_len = len(cycle_nodes)

            if cycle_len == 2:
                a = cycle_nodes[0]
                b = cycle_nodes[1]
                # 2环两边都可以接最长链
                pair_sum += 2 + dp[a] + dp[b]
            else:
                if cycle_len > max_cycle:
                    max_cycle = cycle_len

    return max(max_cycle, pair_sum)


def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))

    print(maximum_attendees(arr))


if __name__ == "__main__":
    solve()