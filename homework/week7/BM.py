
def boyer_moore(text, pattern):
    n = len(text)
    m = len(pattern)

    if m == 0:
        return []

    # 記錄每個字元在 pattern 中最右側的位置
    last = {}
    for i, ch in enumerate(pattern):
        last[ch] = i

    positions = []
    shift = 0

    while shift <= n - m:
        j = m - 1

        # 從右往左比較
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            positions.append(shift)

            # 移動一格，以免漏掉重疊的匹配
            shift += 1
        else:
            # 壞字元規則
            bad_char_shift = j - last.get(text[shift + j], -1)
            shift += max(1, bad_char_shift)

    return positions


text = "ABAAABCDABC"
pattern = "ABC"

print(boyer_moore(text, pattern))
