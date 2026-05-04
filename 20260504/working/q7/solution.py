def count_not_common(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    count = 0

    # list1 中不在 list2 的元素（保留重复）
    for x in list1:
        if x not in set2:
            count += 1

    # list2 中不在 list1 的元素（保留重复）
    for x in list2:
        if x not in set1:
            count += 1

    return count


def main():
    n = int(input().strip())
    list1 = list(map(int, input().split()))
    m = int(input().strip())
    list2 = list(map(int, input().split()))

    print(count_not_common(list1, list2))


if __name__ == "__main__":
    main()