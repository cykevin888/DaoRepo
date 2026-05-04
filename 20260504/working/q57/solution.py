def enough_projects(scores, p, q, total_projects):
    need = 0

    for score in scores:
        remain = score - total_projects * q
        if remain > 0:
            extra = p - q
            need += (remain + extra - 1) // extra
            if need > total_projects:
                return False

    return need <= total_projects


def min_projects(scores, p, q):
    if max(scores) == 0:
        return 0

    if p == q:
        max_score = max(scores)
        return (max_score + q - 1) // q

    left = 0
    right = 1

    while not enough_projects(scores, p, q, right):
        right *= 2

    while left < right:
        mid = (left + right) // 2
        if enough_projects(scores, p, q, mid):
            right = mid
        else:
            left = mid + 1

    return left


def solve():
    n = int(input().strip())
    scores = list(map(int, input().split()))
    p = int(input().strip())
    q = int(input().strip())

    print(min_projects(scores, p, q))


def main():
    solve()


if __name__ == "__main__":
    main()
