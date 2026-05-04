def generate_next_states(s, length):
    """生成当前字符串 s 在本步（固定反转长度 length）能得到的所有新状态"""
    n = len(s)
    states = set()

    for i in range(n - length + 1):
        part = s[i:i + length]
        rev = part[::-1]

        # 题目要求这一步必须真正改变字符串
        if part == rev:
            continue

        new_s = s[:i] + rev + s[i + length:]
        states.add(new_s)

    return states


def min_steps_to_convert(str1, str2):
    # 长度不同，必然无解
    if len(str1) != len(str2):
        return -1

    # 反转操作不会改变 0/1 的总数，不一致则无解
    if str1.count('1') != str2.count('1'):
        return -1

    # 已经相等，0 步
    if str1 == str2:
        return 0

    n = len(str1)
    current_states = {str1}

    # step=1 时反转长度 2，step=2 时长度 3，...
    for step in range(1, n):
        length = step + 1
        next_states = set()

        for s in current_states:
            next_states.update(generate_next_states(s, length))

        if str2 in next_states:
            return step

        if not next_states:
            return -1

        current_states = next_states

    return -1


def main():
    str1 = input().strip()
    str2 = input().strip()
    print(min_steps_to_convert(str1, str2))


if __name__ == "__main__":
    main()
