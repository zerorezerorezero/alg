# 使用遞迴
def hanoi(n, source, auxiliary, target):
    if n == 1:
        print(f"{source} -> {target}")
        return

    # 1. n-1 個盤子 A -> B
    hanoi(n - 1, source, target, auxiliary)

    # 2. 最大盤 A -> C
    print(f"{source} -> {target}")

    # 3. n-1 個盤子 B -> C
    hanoi(n - 1, auxiliary, source, target)


n = int(input("請輸入盤子數量："))

hanoi(n, "A", "B", "C")

#不使用遞迴
def hanoi_iterative(n, source, auxiliary, target):
    stack = []
    stack.append((n, source, auxiliary, target, 0))

    while stack:
        n, source, auxiliary, target, state = stack.pop()

        if n == 1:
            print(f"{source} -> {target}")
            continue

        if state == 0:
            stack.append((n - 1, auxiliary, source, target, 0))
            stack.append((n, source, auxiliary, target, 1))
            stack.append((n - 1, source, target, auxiliary, 0))

        elif state == 1:
            print(f"{source} -> {target}")


n = int(input("請輸入盤子數量："))
hanoi_iterative(n, "A", "B", "C")