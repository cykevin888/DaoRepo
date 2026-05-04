def parse_row(line, cols):
    parts = line.split()
    if len(parts) == cols:
        return list(map(int, parts))
    return [int(ch) for ch in parts[0].strip()]


def largest_house(grid):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    best = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1 or visited[r][c]:
                continue

            stack = [[r, c]]
            visited[r][c] = True
            area = 0

            while stack:
                x, y = stack.pop()
                area += 1

                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx = x + dx
                    ny = y + dy

                    if nx < 0 or nx >= rows or ny < 0 or ny >= cols:
                        continue
                    if visited[nx][ny] or grid[nx][ny] != 1:
                        continue

                    visited[nx][ny] = True
                    stack.append([nx, ny])

            if area > best:
                best = area

    return best


def solve():
    rows, cols = map(int, input().split())
    grid = []

    for _ in range(rows):
        grid.append(parse_row(input().strip(), cols))

    print(largest_house(grid))


def main():
    solve()


if __name__ == "__main__":
    main()
