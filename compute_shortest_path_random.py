import sys, copy, random, time

# 条件
s = 0 # 始点
t = 20 # 終点
n = t - s + 1 # 頂点数
m = 100 # 辺の本数
minWeight = -100 # 辺重みの最小値
maxWeight = 100 # 辺重みの最大値

T = [] # 暫定解
x = sys.maxsize # 暫定解の値
nodeCount = 0 # 探索ノード数

# 最短単純路を計算する分枝アルゴリズム
# P: 探索パス
# l: Pの長さ
# u: 探索頂点
# t: 終点
# G: 隣接リスト
# d: 辺重み
def computeShortestPathBranch(P: list[int], l: int, u: int, t: int, G: list[list[int]], d: dict[(int, int), int], visited: list[bool]):
    global T, x, nodeCount
    nodeCount += 1
    if nodeCount % 1000000 == 0:
        print(f"\r\t\tnodeCount: {nodeCount // 1000000}M", end='')
    P.append(u)
    visited[u] = True
    if u == t:
        if l < x:
            T = copy.deepcopy(P)
            x = l
    else:
        for v in G[u]:
            if not visited[v]:
                l += d[(u, v)]
                computeShortestPathBranch(P, l, v, t, G, d, visited)
                l -= d[(u, v)]
    P.pop()
    visited[u] = False

# |E\P|ステップ以内の単純とは限らないパスで最短のものをベルマンフォード法で求める
# （ベルマンフォードは，例えば負閉路を複数回周ることで短い値を取ろうとするので単純路でなくなる）
def getLow(P: list[int], G: list[list[int]], d: dict[(int, int), int]): 
    dp = [[sys.maxsize for _ in range(s,t+1)] for _ in range(n - len(P) + 1)]
    dp[0][P[-1]] = 0
    
    for k in range(1,n - len(P) + 1):
        dp[k] = copy.deepcopy(dp[k-1])
        for u in range(s,t+1):
            if ((not u in P) or u==P[-1]):
                for v in G[u]:
                    if ((not v in P) or v==P[-1]):
                        dp[k][v] = min(dp[k][v],dp[k-1][u]+d[(u,v)])
        
    return dp[n - len(P)][t]

# 最短単純路を計算する分枝限定アルゴリズム
# P: 探索パス
# l: Pの長さ
# u: 探索頂点
# t: 終点
# G: 隣接リスト
# d: 辺重み
def computeShortestPathBranchAndBound(P: list[int], l: int, u: int, t: int, G: list[list[int]], d: dict[(int, int), int], visited: list[bool]):
    global T, x, nodeCount

    nodeCount += 1
    if nodeCount % 1000 == 0:
        if nodeCount >= 1000000:
            print(f"\r\t\tnodeCount: {nodeCount // 1000000}M{nodeCount // 1000}K", end='')
        else:
            print(f"\r\t\tnodeCount: {nodeCount // 1000}K", end='')
    P.append(u)

    if getLow(P,G,d) + l > x:
        P.pop()
        return

    visited[u] = True
    if u == t:
        if l < x:
            T = copy.deepcopy(P)
            x = l
    else:
        for v in G[u]:
            if not visited[v]:
                l += d[(u, v)]
                computeShortestPathBranchAndBound(P, l, v, t, G, d, visited)
                l -= d[(u, v)]
    P.pop()
    visited[u] = False

def main():
    global T, x, u, t, nodeCount, minWeight, maxWeight
    random.seed(12) # 再現できるようにシードを固定しておく
    
    edges = []
    for u in range(s, t+1):
        for v in range(s, t+1):
            if u == v:
                continue # self loop
            w = random.randint(minWeight, maxWeight)
            edges.append((u, v, w))
    random.shuffle(edges)
    edges = edges[:m]


    G = [[] for _ in range(m)] # 隣接リスト
    d = {} # 辺重み
    for u, v, w in edges:
        G[u].append(v)
        d[(u, v)] = w
    
    visited = [False for _ in range(s, t+1)]
    
    print("computeShortestPathBranchAndBound")
    start = time.process_time()
    computeShortestPathBranchAndBound([], 0, s, t, G, d, visited)
    end = time.process_time()
    print()

    print(f"\t最適解: {T}")
    print(f"\t最適値: {x}")
    print(f"\t探索ノード数: {nodeCount}")
    print(f"\t経過時間: {end-start}[s]")

    visited = [False for _ in range(s, t+1)]
    T = []
    x = sys.maxsize
    nodeCount = 0
    
    print("computeShortestPathBranch")
    start = time.process_time()
    computeShortestPathBranch([], 0, s, t, G, d, visited)
    end = time.process_time()
    print()

    print(f"\t最適解: {T}")
    print(f"\t最適値: {x}")
    print(f"\t探索ノード数: {nodeCount}")
    print(f"\t経過時間: {end-start}[s]")


if __name__ == "__main__":
    main()
