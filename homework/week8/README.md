# 皆使用opencode完成 包含以下內容

# 方法                             路徑長度            相對改善           
-----
### 貪婪演算法（最近鄰居）                    3.1224          +0.00%
### 改良法（2-opt）                     2.9031          +7.02%
### 爬山演算法（Hill Climbing）           2.9031          +7.02%
### 模擬退火法（Simulated Annealing）     2.9031          +7.02%
### 梯度下降法（Steepest Descent）        2.9031          +7.02%

### 可能是範例不夠複雜 所以只看得出貪婪演算法效果比較差


# 旅行推銷員問題 (TSP) 五種解法

本專案使用 Python 實作旅行推銷員問題（Traveling Salesman Problem）的五種求解方法，並提供路徑視覺化功能。

## 方法簡介

| 方法 | 類型 | 說明 |
|---|---|---|
| **1. 改良法（2-opt）** | 局部搜尋改善 | 從初始解開始，透過移除兩條邊並重新連接（反轉路徑片段）來改善路徑，直到無法改善為止。 |
| **2. 爬山演算法（Hill Climbing）** | 局部搜尋 | 從當前解隨機產生鄰近解，若鄰近解較好則接受，否則拒絕。容易陷入局部最優。 |
| **3. 模擬退火法（Simulated Annealing）** | 啟發式搜尋 | 借鑑金屬退火原理，初期允許以較高機率接受較差解，隨著溫度下降逐漸收斂，能跳出局部最優。 |
| **4. 梯度下降法（Steepest Descent）** | 最陡下降法 | 每一步都評估所有可能的交換，選擇能帶來最大改善（最陡下降）的方向執行，直到抵達局部最優。 |
| **5. 貪婪演算法（Nearest Neighbor）** | 建構式啟發式 | 從起點開始，每次選擇最近的未訪問城市，快速建構出一個可行解，常作為其他方法的初始解。 |

## 環境需求

需要以下 Python 套件：

```bash
pip install numpy matplotlib
```

## 使用方式

直接執行主程式：

```bash
python tsp_all_methods.py
```

程式會自動：
1. 產生 10 個隨機城市座標（使用固定種子，結果可重現）
2. 分別使用五種方法求解
3. 輸出每種方法的路徑、距離及比較結果
4. 顯示各方法的路徑視覺化圖表

## 檔案說明

- `tsp_all_methods.py` - 主程式，包含所有五種方法的實作
- `README.md` - 本說明檔案

## 程式結構

### TSP 類別
- `__init__(cities)`: 初始化，建立距離矩陣
- `path_distance(path)`: 計算路徑總距離
- `plot_path(path, title, save_path)`: 繪製路徑圖
- `random_path(n)`: 產生隨機路徑

### TSPSolver 類別
- `greedy_nearest_neighbor()`: 貪婪演算法
- `two_opt(path, max_iterations)`: 2-opt 改良法
- `hill_climbing(initial_path, max_iterations)`: 爬山演算法
- `simulated_annealing(initial_path, initial_temp, cooling_rate, max_iterations)`: 模擬退火法
- `gradient_descent_tsp(initial_path, learning_rate, max_iterations)`: 梯度下降法

## 調整參數

如需調整測試參數，可修改 `main()` 函式：

```python
num_cities = 10  # 城市數量
np.random.seed(42)  # 隨機種子
```

各演算法的參數也可在呼叫時調整，例如：

```python
solver.simulated_annealing(initial_path, initial_temp=10000.0, cooling_rate=0.995, max_iterations=10000)
solver.hill_climbing(initial_path, max_iterations=10000)
```

## 注意事項

- 本實作針對小型 TSP（預設 10 個城市）設計，適合學習理解各演算法原理
- 距離計算採用歐幾里得距離
- 路徑視覺化會彈出圖表視窗，若在無 GUI 環境執行，可改用 `save_path` 參數儲存圖片
- 為求簡潔與易懂，部分演算法使用簡化的鄰近操作（交換、反轉等）

## 學習重點

- **貪婪演算法**：建構式解法，速度快但解品質通常不佳
- **2-opt 改良法**：簡單有效的局部搜尋，能大幅改善初始解
- **爬山演算法**：單純的改善策略，可能停留在局部最優
- **模擬退火法**：透過機率接受較差解來探索解空間，更有機會找到全域較優解
- **梯度下降法**：系統性地搜尋最陡下降方向，收斂較快但也容易陷入局部最優
