def sym_diff(expr):
    # 常數
    if isinstance(expr, (int, float)):
        return 0

    # 變數 x
    if expr == "x":
        return 1

    # 其他變數，例如 y
    if isinstance(expr, str):
        return 0

    op = expr[0]
    left = expr[1]
    right = expr[2]

    # 加法
    if op == "add":
        return ("add", sym_diff(left), sym_diff(right))

    # 減法
    if op == "sub":
        return ("sub", sym_diff(left), sym_diff(right))

    # 乘法法則
    if op == "mul":
        return (
            "add",
            ("mul", sym_diff(left), right),
            ("mul", left, sym_diff(right))
        )

    # 除法法則
    if op == "div":
        return (
            "div",
            ("sub",
                ("mul", sym_diff(left), right),
                ("mul", left, sym_diff(right))
            ),
            ("pow", right, 2)
        )

    # 次方
    if op == "pow":
        # 假設 exponent 是常數
        return (
            "mul",
            ("mul", right, ("pow", left, right - 1)),
            sym_diff(left)
        )

def simplify(expr):

    # 數字
    if isinstance(expr, (int, float)):
        return expr

    # 變數
    if isinstance(expr, str):
        return expr

    op = expr[0]
    left = simplify(expr[1])
    right = simplify(expr[2])

    # 加法
    if op == "add":

        if left == 0:
            return right

        if right == 0:
            return left

        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right

        return ("add", left, right)

    # 減法
    if op == "sub":

        if right == 0:
            return left

        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left - right

        return ("sub", left, right)

    # 乘法
    if op == "mul":

        if left == 0 or right == 0:
            return 0

        if left == 1:
            return right

        if right == 1:
            return left

        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left * right

        return ("mul", left, right)

    # 除法
    if op == "div":

        if left == 0:
            return 0

        if right == 1:
            return left

        return ("div", left, right)

    # 次方
    if op == "pow":

        if right == 0:
            return 1

        if right == 1:
            return left

        return ("pow", left, right)

# expr = ("pow", "x", 2)

expr = (
    "add",
    ("pow", "x", 2),
    ("mul", 3, "x")
)

result = sym_diff(expr)
result = simplify(result)

print(result)