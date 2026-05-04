def transform(arr):
    n = len(arr)
    res = [0] * n

    # arr[i] = v 说明数字 v 出现在下标 i
    # 所以在结果里应该是 res[v] = i
    for i, v in enumerate(arr):
        res[v] = i

    return res


def main():
    n = int(input().strip())
    arr = list(map(int, input().split()))

    result = transform(arr)
    print(*result)


if __name__ == "__main__":
    main()