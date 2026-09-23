import itertools

def solve_sat_truth_table(variables, formula):
    """
    系統性列舉真值表來解決 SAT 問題
    :param variables: 變數列表，例如 ['p', 'q', 'r']
    :param formula: 一個接受字典型態變數賦值並傳回布林值的函數
    """
    n = len(variables)
    # 產生所有 2^n 種 True/False 的組合
    truth_combinations = list(itertools.product([True, False], repeat=n))
    
    print("=" * 45)
    # 印出表頭
    header = " | ".join(variables) + " | Result"
    print(header)
    print("-" * 45)
    
    satisfying_assignments = []
    
    for combo in truth_combinations:
        # 將變數名稱與對應的真偽值打包成字典，例如 {'p': True, 'q': False}
        assignment = dict(zip(variables, combo))
        
        # 計算此賦值下的算式結果
        result = formula(assignment)
        
        # 格式化輸出該列真值表
        row_str = " | ".join(f"{str(assignment[var]):<5}" for var in variables)
        print(f"{row_str} | {result}")
        
        if result:
            satisfying_assignments.append(assignment)
            
    print("=" * 45)
    
    # 輸出最終 SAT 結論
    if satisfying_assignments:
        print(f"結論: SATISFIABLE (可滿足)")
        print("可滿足的變數賦值解答：")
        for ans in satisfying_assignments:
            print(" ", ans)
    else:
        print("結論: UNSATISFIABLE (不可滿足)")

# -------------------------------------------------------------
# 測試範例 1： (p or q) and (not p)
# -------------------------------------------------------------
print("測試 1: (p OR q) AND (NOT p)")
vars1 = ['p', 'q']
formula1 = lambda env: (env['p'] or env['q']) and (not env['p'])

solve_sat_truth_table(vars1, formula1)

print("\n")

# -------------------------------------------------------------
# 測試範例 2： p and (not p)
# -------------------------------------------------------------
print("測試 2: p AND (NOT p)")
vars2 = ['p']
formula2 = lambda env: env['p'] and (not env['p'])

solve_sat_truth_table(vars2, formula2)