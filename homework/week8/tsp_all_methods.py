#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旅行推銷員問題 (Traveling Salesman Problem, TSP) 解法集合
包含以下五種方法：
1. 改良法（2-opt 局部搜尋改善）
2. 爬山演算法（Hill Climbing）
3. 模擬退火法（Simulated Annealing）
4. 梯度下降法（Gradient Descent / 路徑梯度式局部搜尋）
5. 貪婪演算法（Nearest Neighbor）
"""

import math
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

# 設定隨機種子以便重現結果
random.seed(123)
np.random.seed(123)


class TSP:
    def __init__(self, cities: List[Tuple[float, float]]):
        """
        初始化 TSP
        :param cities: 城市座標列表 [(x1,y1), (x2,y2), ...]
        """
        self.cities = cities
        self.n = len(cities)
        # 預計算距離矩陣以提升效率
        self.distance_matrix = self._build_distance_matrix()
    
    def _build_distance_matrix(self) -> np.ndarray:
        """建立城市間距離矩陣"""
        dist_matrix = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(i+1, self.n):
                dx = self.cities[i][0] - self.cities[j][0]
                dy = self.cities[i][1] - self.cities[j][1]
                d = math.sqrt(dx*dx + dy*dy)
                dist_matrix[i][j] = d
                dist_matrix[j][i] = d
        return dist_matrix
    
    def path_distance(self, path: List[int]) -> float:
        """
        計算路徑總距離（路徑為城市索引列表，假設首尾相連形成迴圈）
        :param path: 城市訪問順序
        :return: 總距離
        """
        if len(path) == 0:
            return float('inf')
        total = 0.0
        for i in range(len(path)):
            from_city = path[i]
            to_city = path[(i + 1) % len(path)]
            total += self.distance_matrix[from_city][to_city]
        return total
    
    def plot_path(self, path: List[int], title: str, save_path: str = None):
        """
        繪製 TSP 路徑
        :param path: 城市訪問順序
        :param title: 圖表標題
        :param save_path: 儲存路徑（若為 None 則顯示圖表）
        """
        if len(path) == 0:
            return
        # 建立閉環路徑座標
        plot_coords = [self.cities[i] for i in path] + [self.cities[path[0]]]
        x = [c[0] for c in plot_coords]
        y = [c[1] for c in plot_coords]
        
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, 'b-o', linewidth=2, markersize=8)
        plt.scatter(x, y, c='red', s=100, zorder=5)
        
        # 標註城市編號
        for i, idx in enumerate(path):
            plt.annotate(str(idx), (self.cities[idx][0], self.cities[idx][1]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=12)
        
        plt.title(f'{title}\n路徑長度: {self.path_distance(path):.4f}', fontsize=14)
        plt.xlabel('X 座標')
        plt.ylabel('Y 座標')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"圖表已儲存至: {save_path}")
        else:
            plt.show()
        plt.close()
    
    @staticmethod
    def random_path(n: int) -> List[int]:
        """產生隨機路徑"""
        path = list(range(n))
        random.shuffle(path)
        return path


class TSPSolver:
    def __init__(self, tsp: TSP):
        self.tsp = tsp
    
    def greedy_nearest_neighbor(self) -> Tuple[List[int], float]:
        """
        方法 5: 貪婪演算法（最近鄰居法）
        從起點開始，每次選擇最近未訪問的城市
        """
        print("=" * 60)
        print("方法 5: 貪婪演算法（最近鄰居法 Nearest Neighbor）")
        print("=" * 60)
        
        n = self.tsp.n
        if n == 0:
            return [], 0.0
        
        start = 0
        visited = [False] * n
        path = [start]
        visited[start] = True
        current = start
        
        for _ in range(n - 1):
            best_next = -1
            best_dist = float('inf')
            for j in range(n):
                if not visited[j]:
                    d = self.tsp.distance_matrix[current][j]
                    if d < best_dist:
                        best_dist = d
                        best_next = j
            path.append(best_next)
            visited[best_next] = True
            current = best_next
        
        dist = self.tsp.path_distance(path)
        print(f"路徑: {path}")
        print(f"總距離: {dist:.4f}")
        print()
        return path, dist
    
    def two_opt(self, path: List[int], max_iterations: int = 1000) -> Tuple[List[int], float]:
        """
        方法 1: 改良法（2-opt 局部搜尋）
        透過移除兩條邊並重新連接來改善路徑
        """
        print("=" * 60)
        print("方法 1: 改良法（2-opt 局部搜尋）")
        print("=" * 60)
        
        current_path = path[:]
        n = len(current_path)
        improved = True
        iterations = 0
        
        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            for i in range(n - 1):
                for j in range(i + 2, n):
                    # 嘗試 2-opt 交換：移除 (i,i+1) 和 (j,j+1)，連接 (i,j) 和 (i+1,j+1)
                    new_path = current_path[:]
                    # 反轉 i+1 到 j 之間的路徑
                    new_path[i+1:j+1] = reversed(current_path[i+1:j+1])
                    
                    if self.tsp.path_distance(new_path) < self.tsp.path_distance(current_path):
                        current_path = new_path
                        improved = True
                        break
                if improved:
                    break
        
        dist = self.tsp.path_distance(current_path)
        print(f"初始路徑長度: {self.tsp.path_distance(path):.4f}")
        print(f"改善後路徑: {current_path}")
        print(f"改善後距離: {dist:.4f}")
        print(f"迭代次數: {iterations}")
        print()
        return current_path, dist
    
    def hill_climbing(self, initial_path: List[int] = None, max_iterations: int = 10000) -> Tuple[List[int], float]:
        """
        方法 2: 爬山演算法（Hill Climbing）
        每次產生鄰近解，如果更好就接受，否則拒絕
        """
        print("=" * 60)
        print("方法 2: 爬山演算法（Hill Climbing）")
        print("=" * 60)
        
        n = self.tsp.n
        if initial_path is None:
            current_path = self.tsp.random_path(n)
        else:
            current_path = initial_path[:]
        
        current_dist = self.tsp.path_distance(current_path)
        best_path = current_path[:]
        best_dist = current_dist
        
        for iteration in range(max_iterations):
            # 產生鄰近解：隨機交換兩個城市
            new_path = current_path[:]
            i, j = random.sample(range(n), 2)
            new_path[i], new_path[j] = new_path[j], new_path[i]
            new_dist = self.tsp.path_distance(new_path)
            
            if new_dist < current_dist:
                current_path = new_path
                current_dist = new_dist
                if current_dist < best_dist:
                    best_path = current_path[:]
                    best_dist = current_dist
        
        print(f"初始距離: {self.tsp.path_distance(initial_path if initial_path else best_path):.4f}")
        print(f"最佳路徑: {best_path}")
        print(f"最佳距離: {best_dist:.4f}")
        print(f"迭代次數: {max_iterations}")
        print()
        return best_path, best_dist
    
    def simulated_annealing(self, initial_path: List[int] = None, 
                           initial_temp: float = 10000.0,
                           cooling_rate: float = 0.995,
                           max_iterations: int = 10000) -> Tuple[List[int], float]:
        """
        方法 3: 模擬退火法（Simulated Annealing）
        允許以一定機率接受較差的解，避免陷入局部最優
        """
        print("=" * 60)
        print("方法 3: 模擬退火法（Simulated Annealing）")
        print("=" * 60)
        
        n = self.tsp.n
        if initial_path is None:
            current_path = self.tsp.random_path(n)
        else:
            current_path = initial_path[:]
        
        current_dist = self.tsp.path_distance(current_path)
        best_path = current_path[:]
        best_dist = current_dist
        temp = initial_temp
        
        for iteration in range(max_iterations):
            # 產生鄰近解
            new_path = current_path[:]
            if random.random() < 0.5:
                # 交換兩個城市
                i, j = random.sample(range(n), 2)
                new_path[i], new_path[j] = new_path[j], new_path[i]
            else:
                # 反轉一段路徑（更適合 TSP）
                i = random.randint(0, n - 2)
                j = random.randint(i + 1, n - 1)
                new_path[i:j+1] = reversed(new_path[i:j+1])
            
            new_dist = self.tsp.path_distance(new_path)
            delta = new_dist - current_dist
            
            # Metropolis 準則
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current_path = new_path
                current_dist = new_dist
                if current_dist < best_dist:
                    best_path = current_path[:]
                    best_dist = current_dist
            
            temp *= cooling_rate
        
        print(f"初始溫度: {initial_temp}")
        print(f"冷卻率: {cooling_rate}")
        print(f"最佳路徑: {best_path}")
        print(f"最佳距離: {best_dist:.4f}")
        print(f"迭代次數: {max_iterations}")
        print()
        return best_path, best_dist
    
    def gradient_descent_tsp(self, initial_path: List[int] = None, 
                            learning_rate: float = 0.01,
                            max_iterations: int = 5000) -> Tuple[List[int], float]:
        """
        方法 4: 梯度下降法（Gradient Descent）
        此處採用「路徑梯度」概念：透過評估局部交換對總距離的影響來選擇改善方向
        類似於最陡下降法（Steepest Descent）
        """
        print("=" * 60)
        print("方法 4: 梯度下降法（Steepest Descent / 路徑梯度法）")
        print("=" * 60)
        
        n = self.tsp.n
        if initial_path is None:
            current_path = self.tsp.random_path(n)
        else:
            current_path = initial_path[:]
        
        current_dist = self.tsp.path_distance(current_path)
        best_path = current_path[:]
        best_dist = current_dist
        
        for iteration in range(max_iterations):
            best_move = None
            best_delta = 0  # 只接受負的 delta（改善）
            
            # 嘗試所有可能的兩點交換，找出最陡下降方向
            for i in range(n):
                for j in range(i + 1, n):
                    new_path = current_path[:]
                    new_path[i], new_path[j] = new_path[j], new_path[i]
                    new_dist = self.tsp.path_distance(new_path)
                    delta = new_dist - current_dist
                    if delta < best_delta:  # 找最負的 delta
                        best_delta = delta
                        best_move = (i, j)
            
            if best_move is None or best_delta >= 0:
                # 無法再改善，達到局部最優
                break
            
            # 執行最佳移動
            i, j = best_move
            current_path[i], current_path[j] = current_path[j], current_path[i]
            current_dist += best_delta
            
            if current_dist < best_dist:
                best_path = current_path[:]
                best_dist = current_dist
        
        print(f"初始距離: {self.tsp.path_distance(initial_path if initial_path else best_path):.4f}")
        print(f"最佳路徑: {best_path}")
        print(f"最佳距離: {best_dist:.4f}")
        print(f"實際迭代次數: {iteration + 1}")
        print(f"（梯度下降：每步選擇最陡下降方向）")
        print()
        return best_path, best_dist


def main():
    """主程式：測試所有五種方法"""
    print("\n" + "=" * 60)
    print("旅行推銷員問題 (TSP) 五種解法比較")
    print("=" * 60 + "\n")
    
    # 產生測試城市（可自行調整城市數量和座標）
    num_cities = 10
    print(f"測試案例：{num_cities} 個城市（隨機產生）")
    
    # 使用固定種子產生城市，方便比較
    np.random.seed(42)
    cities = [(np.random.rand(), np.random.rand()) for _ in range(num_cities)]
    
    # 顯示城市座標
    print("城市座標:")
    for i, (x, y) in enumerate(cities):
        print(f"  城市 {i}: ({x:.4f}, {y:.4f})")
    print()
    
    # 建立 TSP 實例
    tsp = TSP(cities)
    solver = TSPSolver(tsp)
    
    results = {}
    
    # 方法 5: 貪婪演算法（作為基準和初始解）
    path_greedy, dist_greedy = solver.greedy_nearest_neighbor()
    results['貪婪演算法（最近鄰居）'] = (path_greedy, dist_greedy)
    
    # 方法 1: 改良法（2-opt），以貪婪解為起點
    path_2opt, dist_2opt = solver.two_opt(path_greedy)
    results['改良法（2-opt）'] = (path_2opt, dist_2opt)
    
    # 方法 2: 爬山演算法
    path_hc, dist_hc = solver.hill_climbing(initial_path=path_greedy)
    results['爬山演算法（Hill Climbing）'] = (path_hc, dist_hc)
    
    # 方法 3: 模擬退火法
    path_sa, dist_sa = solver.simulated_annealing(initial_path=path_greedy)
    results['模擬退火法（Simulated Annealing）'] = (path_sa, dist_sa)
    
    # 方法 4: 梯度下降法
    path_gd, dist_gd = solver.gradient_descent_tsp(initial_path=path_greedy)
    results['梯度下降法（Steepest Descent）'] = (path_gd, dist_gd)
    
    # 結果比較
    print("=" * 60)
    print("結果比較")
    print("=" * 60)
    print(f"{'方法':<30} {'路徑長度':<15} {'相對改善':<15}")
    print("-" * 60)
    
    base_dist = dist_greedy
    for method_name, (path, dist) in results.items():
        improvement = ((base_dist - dist) / base_dist * 100) if base_dist > 0 else 0
        print(f"{method_name:<30} {dist:<15.4f} {improvement:>+.2f}%")
    
    print("=" * 60)
    print()
    
    # 找出最佳解
    best_method = min(results.items(), key=lambda x: x[1][1])
    print(f"🏆 最佳解: {best_method[0]}，路徑長度 = {best_method[1][1]:.4f}")
    print(f"   路徑: {best_method[1][0]}")
    print()
    
    # 繪製各方法的路徑圖
    print("正在繪製路徑圖...")
    for method_name, (path, dist) in results.items():
        safe_name = method_name.replace('（', '_').replace('）', '').replace(' ', '_')
        tsp.plot_path(path, method_name)
    
    print("\n所有測試完成！")


if __name__ == "__main__":
    main()
