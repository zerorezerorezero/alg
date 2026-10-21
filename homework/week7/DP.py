
def dp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    if m == 0:
        return []

    # DP[i][j]：
    # pattern 前 j 個字元是否匹配 text 中
    # 以 i-1 結尾的連續子字串
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    positions = []

    for i in range(1, n + 1):
        for j in range(1, min(i, m) + 1):
            if text[i - 1] == pattern[j - 1]:
                if j == 1:
                    dp[i][j] = True
                else:
                    dp[i][j] = dp[i - 1][j - 1]

            if j == m and dp[i][j]:
                positions.append(i - m)

    return positions


text = "ABAAABCDABC"
pattern = "ABC"

print(dp_search(text, pattern))
