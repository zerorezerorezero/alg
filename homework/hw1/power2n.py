# 方法 1
def power2n1(n):
    return 2**n

# 方法 2a：用遞迴
def power2n2a(n):
    if n == 0:
        return 1
    return power2n2a(n-1) + power2n2a(n-1)

# 方法2b：用遞迴
def power2n2b(n):
    if n == 0:
        return 1
    return 2 * power2n2b(n-1)

# 方法 3：用遞迴+查表
memo = {}
def power2n3(n):
    if n == 0:
        return 1
    if n in memo:
        return memo[n]

    memo[n] = power2n3(n - 1) + power2n3(n - 1)
    return memo[n]

# n=100

# print("1=",power2n1(100))
# print("2a=",power2n2a(100))
# print("2b=",power2n2b(100))
# print("3=",power2n3(100))

# AI給的 --- 時間計測工具函式 ---
import time

def benchmark(func, n):
    """傳入要測試的函式與參數 n，計算並印出執行時間"""
    start_time = time.perf_counter()  # 開始計時
    result = func(n)
    end_time = time.perf_counter()  # 結束計時

    execution_time = end_time - start_time  # 單位為秒
    print(
        f"[{func.__name__}] n={n} | 時間: {execution_time:.8f} 秒 | 位數: {len(str(result))} 位"
    )


# --- 測試執行 ---

N = 25  # 設為 25 方便測試方法 2a（若設 100，方法 2a 電腦會卡死）

print(f"=== 開始測試 n = {N} ===")
benchmark(power2n1, N)
benchmark(power2n2a, N)
benchmark(power2n2b, N)
benchmark(power2n3, N)
