def count_cache_misses(pages, capacity):
    if capacity == 0:
        return len(pages)

    cache = []
    front = 0
    present = {}
    misses = 0

    for page in pages:
        if page in present:
            continue

        misses += 1

        if len(cache) - front == capacity:
            old_page = cache[front]
            front += 1
            del present[old_page]

        cache.append(page)
        present[page] = True

    return misses


def solve():
    n = int(input().strip())
    pages = list(map(int, input().split()))
    capacity = int(input().strip())

    print(count_cache_misses(pages, capacity))


def main():
    solve()


if __name__ == "__main__":
    main()
