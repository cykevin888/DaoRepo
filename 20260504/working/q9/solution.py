def quick_power(base, exponent, mod):
    result = 1
    base = base % mod

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2

    return result


def encrypt_code(secret_code, first_key, second_key):
    MOD = 1000000007

    # 第一步：计算 S^N % 10
    first_result = quick_power(secret_code, first_key, 10)

    # 第二步：计算 (S^N % 10)^M % 1000000007
    final_result = quick_power(first_result, second_key, MOD)

    return final_result


def main():
    secret_code = int(input())
    first_key = int(input())
    second_key = int(input())

    result = encrypt_code(secret_code, first_key, second_key)
    print(result)


if __name__ == "__main__":
    main()