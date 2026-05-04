def count_less_than_k(nums, k):
    count = 0
    for x in nums:
        if x < k:
            count += 1
    return count


def main():
    n = int(input().strip())                 # 元素个数
    nums = list(map(int, input().split()))   # 列表
    k = int(input().strip())                 # 比较值 K

    # 如果你想更严谨，可取消下面两行注释
    # if len(nums) != n:
    #     nums = nums[:n]

    result = count_less_than_k(nums, k)
    print(result)


if __name__ == "__main__":
    main()