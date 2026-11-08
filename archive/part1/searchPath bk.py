
#### pip install requests
#### pip install scipy

import json
import requests
import sys
import re

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque





NX=0

#networkx on
NX=1





#test
#f = open('foo.txt', 'r')

# GDS7 -to
f = open('to/t.csv', 'r')

# GDVG -from
#f = open('to/GDGV-from.csv', 'r')

# GDVG -to
#f = open('GDGV-to.csv', 'r')

# GDS7 -from
#f = open('from/from.csv', 'r')


#f = open('to/GB6E-to.csv', 'r')
#f = open('GB6EJ-from.csv', 'r')

#f = open('gafy-to-ath200.csv', 'r')

l_file = f.readlines()
f.close()




l_file2 = [s for s in l_file if 'amount' in s]

l01=[]
for xxx in l_file2:
  ll=xxx.split(",")
  l01.append(ll[3]+","+ll[5])

l02=[]
l02 = sorted(set(l01), key=l01.index)

l03=[] # org of txList
l04=[] #        txList
d01={}
for xxx in l02:
  ll=xxx.split(",")
  l03.append([ll[0],ll[1]])
  adr_from = ll[0][:4]
  adr_to   = ll[1][:4]
  l04.append([adr_from,adr_to])

  if adr_from not in d01:
    d01[adr_from] = [adr_to]
  else:
    d01[adr_from].append(adr_to)

#for xxx in l04:
#  print(xxx)

'''
for k, v in d01.items():
  print("key:" + k)
  print(v)
  print("")
'''



l05=[] # for add_node tmp
txList=[]
ii=0
for xxx in l04:
  l05.append(xxx[0])
  l05.append(xxx[1])
  '''
  if xxx[1]=="GDGV":
     ii+=1
     print(str(ii)+" "+xxx[0],"->",xxx[1])
  '''



l06=[] ## for add_node
l06 = sorted(set(l05), key=l05.index)

#print("######################################")
#for xxx in l04:
#  print(xxx)

def find_path(graph, start, end, path=[]):
    # 現在のノードをpathに追加
    path = path + [start]

    # ベースケース：現在のノードが終了ノードである場合、pathを返す
    if start == end:
        return path

    # 開始ノードから到達可能なノードを取得
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            # 深さ優先探索で、終了ノードが見つかるまで再帰的に探索を続ける
            new_path = find_path(graph, node, end, path)
            if new_path:
                return new_path

    # 終了ノードが見つからなかった場合、Noneを返す
    return None

def find_all_paths(graph, start, end, path=[]):
    # 現在のノードをpathに追加
    path = path + [start]

    # ベースケース：現在のノードが終了ノードである場合、pathを返す
    if start == end:
        return [path]

    # 開始ノードから到達可能なノードを取得
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            # 深さ優先探索で、終了ノードが見つかるまで再帰的に探索を続ける
            new_paths = find_all_paths(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)

    # 全てのパスを返す
    return paths



'''
{'GAFY': ['GDDV', 'GBUK', 'GATJ', 'GDVR', 'GBXA'], 'GB7X': ['GAFY', 'GATJ', 'GBXA'], 'GBVK': ['GAFY']}
という有指向グラフの中で２点のノードの最短距離のパスを出力する
'''

'''
def shortest_path(graph, start, end):
    # グラフのノードを訪問するためのキューを用意する
    queue = deque([start])
    
    # ノード間の距離を記録する辞書を用意する
    distances = {start: 0}
    
    # ノード間の最短距離を記録する辞書を用意する
    shortest_paths = {start: [start]}
    
    while queue:
        node = queue.popleft()
        # ノードから到達可能なノードを調べる
        for neighbor in graph.get(node, []):
            # 到達可能なノードが初めて訪問する場合、キューに追加する
            if neighbor not in distances:
                queue.append(neighbor)
                distances[neighbor] = distances[node] + 1
                shortest_paths[neighbor] = shortest_paths[node] + [neighbor]
            # 既に訪問している場合、より短い距離があるかどうかを調べる
            elif distances[neighbor] > distances[node] + 1:
                distances[neighbor] = distances[node] + 1
                shortest_paths[neighbor] = shortest_paths[node] + [neighbor]
                
    return shortest_paths.get(end, [])
'''



shortest_paths = []

# 最短パスを求める
#v1

def shortest_path01(graph, start, end):
    queue = deque([start])
    distances = {start: 0}
    shortest_paths = {start: [start]}
    
    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in distances:
                queue.append(neighbor)
                distances[neighbor] = distances[node] + 1
                shortest_paths[neighbor] = shortest_paths[node] + [neighbor]
            elif distances[neighbor] > distances[node] + 1:
                distances[neighbor] = distances[node] + 1
                shortest_paths[neighbor] = shortest_paths[node] + [neighbor]
                
    return shortest_paths.get(end, [])


#v2
from collections import deque

'''
graph = {'GAFY': ['GDDV', 'GBUK', 'GATJ', 'GDVR', 'GBXA'],
         'GB7X': ['GAFY', 'GATJ', 'GBXA'],
         'GBVK': ['GAFY']}

start_node = 'GAFY'
end_node = 'GBXA'
'''



# 最短パスを求める
def shortest_path02(graph, start, end):
    queue = deque([start])
    distances = {start: 0}
    shortest_paths = {start: [start]}
    
    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in distances:
                queue.append(neighbor)
                distances[neighbor] = distances[node] + 1
                shortest_paths[neighbor] = shortest_paths[node] + [neighbor]
            elif distances[neighbor] > distances[node] + 1:
                distances[neighbor] = distances[node] + 1
                shortest_paths[neighbor] = shortest_paths[node] + [neighbor]
                
    return shortest_paths.get(end, [])


# 最短パスをリストに格納する
#shortest_paths = shortest_path(graph, start_node, end_node)

# 結果を出力する
#print(shortest_paths)



#v3

'''
使用しているグラフは辞書です。重みづけはできません。辞書のkeyがとあるノードであり、value内list内要素が別のノードかつ、keyノードからのエッジとして定義しています。
# グラフの例
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D']
}
これを踏まえて, 指定した始点ノードから終点ノードまでの最短パスを抽出するPythonコードを書いてください。上記グラフの例では’D'がグラフのノードとして定義されていませんが、その場合はエッジを持たないノードと判断してください

'''
import heapq

def dijkstra03(graph, start, end):
    heap = [(0, start)]
    visited = set()
    distances = {start: 0}
    parents = {start: None}
    
    while heap:
        (distance, node) = heapq.heappop(heap)
        
        if node == end:
            path = []
            while node is not None:
                path.append(node)
                node = parents[node]
            return path[::-1]
        
        if node in visited:
            continue
        
        visited.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor in visited:
                continue
            neighbor_distance = distances.get(neighbor, float('inf'))
            new_distance = distance + 1
            if new_distance < neighbor_distance:
                heapq.heappush(heap, (new_distance, neighbor))
                distances[neighbor] = new_distance
                parents[neighbor] = node
                
    return []


'''

# グラフの例
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D']
}

start_node = 'A'
end_node = 'D'
shortest_path = dijkstra(graph, start_node, end_node)
print(f"The shortest path from {start_node} to {end_node} is {shortest_path}")

'''

#v4
import heapq

def dijkstra4(graph, start, end):
    queue = [(0, start)]
    visited = set()
    distances = {start: 0}
    predecessors = {}

    while queue:
        (cost, current) = heapq.heappop(queue)
        if current == end:
            path = []
            while current in predecessors:
                path.append(current)
                current = predecessors[current]
            path.append(start)
            path.reverse()
            return path
        visited.add(current)
        for neighbor, weight in graph.get(current, {}).items():
            if neighbor in visited:
                continue
            new_cost = distances[current] + weight
            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
                predecessors[neighbor] = current
    return []


#v5
from collections import deque

def shortest_path05(graph, start, end):
    queue = deque([start])
    visited = set()
    paths = {start: [start]}
    
    while queue:
        current = queue.popleft()
        visited.add(current)
        if current == end:
            return paths[current]
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                queue.append(neighbor)
                paths[neighbor] = paths[current] + [neighbor]
    
    return []


'''
使用しているグラフは辞書です。重みづけはできません。辞書のkeyがとあるノードであり、value内list内要素が別のノードかつ、keyノードからのエッジとして定義しています。
# グラフの例
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D']
}
これを踏まえて, 指定した始点ノードから終点ノードまでの最短パスを抽出するPythonコードを書いてください。上記グラフの例では’D'がグラフのノードとして定義されていませんが、その場合はエッジを持たないノードと判断してください

ベルマンフォード法を使ってすべてのエッジの重みを１として最短パスを抽出するコードを書いて。最短経路が複数存在する場合１つだけ抽出してください。



以下に定義した有指向グラフ内の指定した始点ノードから終点ノードまでの最短パスを抽出するPythonコードを書いてみました。
# グラフの例
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D']
}

使用しているグラフは辞書です。全てのエッジの重みは１とします。辞書のkeyがとあるノードであり、value内list内要素が別のノードかつ、keyノードからのエッジとして定義しています。上記グラフ例では’D'がグラフのノードとして定義されていませんが、その場合はエッジを持たないノードと判断してください。


以下が、Pythonコードです。


#v6
'''
from collections import defaultdict

def bellman_ford_shortest_path06(graph, start, end):
    dist = defaultdict(lambda: float('inf'))
    prev = defaultdict(lambda: None)
    dist[start] = 0

    # Perform V-1 iterations
    for i in range(len(graph) - 1):
        # Iterate over all edges
        for u in graph:
            for v in graph[u]:
                if dist[u] + 1 < dist[v]:
                    dist[v] = dist[u] + 1
                    prev[v] = u

    # Check for negative cycles
    for u in graph:
        for v in graph[u]:
            if dist[u] + 1 < dist[v]:
                raise ValueError("Graph contains a negative-weight cycle")

    # Extract shortest path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    return path


#おしいけどパスではなくノード１個だけでる


'''
使用しているグラフは辞書です。辞書のkeyがとあるノードであり、value内list内要素が別のノードかつ、keyノードからのエッジとして定義しています。
# グラフの例
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D']
}
これを踏まえて, 指定した始点ノードから終点ノードまでの最短パスを抽出するPythonコードを書いてください。上記グラフの例では’D'がグラフのノードとして定義されていませんが、その場合はエッジを持たないノードと判断してください

エッジの重みは１として最短パスを抽出するコードを書いて。最短経路が複数存在する場合１つだけ抽出してください。

'''
#v7
from collections import deque

def bfs_shortest_path07(graph, start, end):
    # 空のキューを作成し、始点ノードを追加する
    queue = deque([start])
    # 始点から各ノードまでの最短距離を格納する辞書を作成し、始点は0で初期化する
    shortest_distance = {start: 0}
    # 始点から各ノードへの最短パスを格納する辞書を作成する
    shortest_path = {start: [start]}
    
    while queue:
        # キューからノードを取り出す
        current_node = queue.popleft()
        # 終点に到達したら最短パスを返す
        if current_node == end:
            return shortest_path[current_node]
        # ノードに隣接するすべてのノードを探索する
        for neighbor in graph.get(current_node, []):
            # まだ探索していないノードであれば、キューに追加する
            if neighbor not in shortest_distance:
                queue.append(neighbor)
                # 始点から現在のノードまでの距離を計算し、辞書に追加する
                shortest_distance[neighbor] = shortest_distance[current_node] + 1
                # 始点から現在のノードまでの最短パスを計算し、辞書に追加する
                shortest_path[neighbor] = shortest_path[current_node] + [neighbor]
    # 終点に到達できなかった場合はNoneを返す
    return None


'''
以下のグラフで'GDS7'から'GDVG'の最短経路がみつかりません。経路は１２０万ほどあります。
例：
  ['GDS7', 'GDTY', 'GAIH', 'GDZG', 'GDMV', 'GCGT', 'GBSR', 'GB6E', 'GDGV']
'''

#v8
from collections import deque

def bfs_shortest_path08(graph, start, goal):
    explored = []
    queue = deque([[start]])

    if start == goal:
        return "That was easy! Start = goal"

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in explored:
            #neighbours = graph[node]
            neighbours = graph.get(node, [])
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                if neighbour == goal:
                    return new_path

            explored.append(node)

    return "So sorry, but a connecting path doesn't exist :("


#v9
'''
パスをいくつかみせた
'''
from collections import deque

def shortest_path9(graph, start, end):
    # キューと訪問済みリストを初期化
    queue = deque([[start]])
    visited = set()

    # キューが空になるまで繰り返す
    while queue:
        # キューの先頭を取得し、そのノードを訪問済みにする
        path = queue.popleft()
        node = path[-1]
        if node == end:
            return path
        elif node not in visited:
            visited.add(node)

            # キューに隣接ノードを追加する
            for neighbor in graph.get(node, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    
    # 最短経路が見つからない場合はNoneを返す
    return None

#V10
'''
'GDS7'から'GDVG'の最短経路がみつかりません。
追加情報ですが、keyにあるノードはvlaue内要素のエッジ先ノードとループしていることがあります
'''
from collections import deque

def bfs_shortest_path10(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None

#v11
'''
v10はまた  for neighbor in graph[node]:
KeyError: 'GA7H'

グラフの定義を再度説明

'''
def dijkstra11(graph, start, goal):
    # ダイクストラ法で最短経路を探索する関数
    # graph: 辞書型のグラフ
    # start: 探索開始地点
    # goal: 探索終了地点
    # 戻り値: startからgoalまでの最短経路とその距離

    # 前処理
    distances = {} # startからの距離
    for node in graph:
        distances[node] = float('inf')
    distances[start] = 0

    # 探索
    visited = []
    unvisited = list(graph.keys())
    while unvisited:
        # 未探索中でstartからの距離が最短のノードを選択
        current = None
        for node in unvisited:
            if node not in visited:
                if current is None:
                    current = node
                elif distances[node] < distances[current]:
                    current = node

        if current is None:
            break

        # 選択したノードから移動可能なノードを取得
        if current not in graph:
            continue
        for neighbor in graph[current]:
            if neighbor not in unvisited:
                continue
            # ここでの dist は、現在地から次のノードへの移動距離
            dist = distances[current] + graph[current][neighbor]
            if dist < distances[neighbor]:
                distances[neighbor] = dist
        visited.append(current)
        unvisited.remove(current)

    # 結果を返却
    if distances[goal] == float('inf'):
        return None
    path = [goal]
    last_node = goal
    while last_node != start:
        for node in graph:
            if last_node in graph[node]:
                if distances[last_node] == distances[node] + graph[node][last_node]:
                    path.append(node)
                    last_node = node
                    break
    path.reverse()
    return (path, distances[goal])

'''
改めてグラフを定義します。

使用しているグラフは辞書です。辞書のkeyがとあるノードであり、value内list内要素が別のノードかつ、keyノードからのエッジです。value内list内要素もノードであることにます。必要であれば、グラフに追加してください。全てのエッジの重みは１です。
# グラフの例
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D']
}
これを踏まえて, 指定した始点ノードから終点ノードまでの最短パスを抽出するPythonコードを書いてください。上記グラフの例では’D'がグラフのノードとして定義されていませんが、その場合はエッジを持たないノードと判断してください

'''
#v12
import heapq

def dijkstra12(graph, start, end):
    # 各ノードへの最短距離と前のノードを格納する辞書を用意する
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    # 始点ノードの最短距離は0とする
    distances[start] = 0
    # ノードを訪れるためのヒープを用意する
    heap = [(0, start)]
    while heap:
        # ヒープから最短距離のノードを取り出す
        current_distance, current_node = heapq.heappop(heap)
        # 現在の距離がすでに登録されている最短距離よりも大きい場合は無視する
        if current_distance > distances[current_node]:
            continue
        # 現在のノードからエッジで繋がっているノードを調べる
        for neighbor in graph[current_node]:
            # 現在のノードを経由した場合の距離を計算する
            distance = distances[current_node] + 1
            # 計算された距離が現在登録されている距離よりも小さい場合は更新する
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # このノードの前のノードを更新する
                previous_nodes[neighbor] = current_node
                # ヒープに新しい距離とノードを追加する
                heapq.heappush(heap, (distance, neighbor))
    # 終点ノードへの最短パスを返す
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()
    return path

'''
keyに存在せず、valueに存在するノードはエッジを持たないノードなので検索をスキップしてください。そうしないとエラーになります
'''
#v13
# ダイクストラ法で最短経路を求める
def dijkstra13(graph, start, end):
    # 初期化
    distances = {}
    previous = {}
    nodes = list(graph.keys())
    for node in nodes:
        distances[node] = float('inf')
    distances[start] = 0
    queue = nodes.copy()
    
    # メインループ
    while queue:
        # 未処理の中で最も近いノードを取り出す
        current = min(queue, key=lambda node: distances[node])
        queue.remove(current)
        
        # ゴールに到達したら経路を返す
        if current == end:
            path = []
            while current in previous:
                path.append(current)
                current = previous[current]
            path.append(start)
            path.reverse()
            return path
        
        # 未処理の中で最も近いノードから伸びるエッジをチェック
        if distances[current] == float('inf'):
            continue
        for neighbor in graph[current]:
            if neighbor not in graph:
                continue
            candidate_distance = distances[current] + 1
            if candidate_distance < distances[neighbor]:
                distances[neighbor] = candidate_distance
                previous[neighbor] = current
    
    # ゴールが見つからなければNoneを返す
    return None


#v14
'''
'GDS7'から'GDVG'の最短経路がとして、['GDS7']とだけ出力されてしまいます。これはどういう意味ですか？実際に使用しているgraphを再度以下に示します。
→パスが存在しないというから、パスを出力させるコードを見せる
'''
from collections import deque

def find_shortest_path14(graph, start, end):
    # 訪問済みのノードを格納する集合
    visited = set()

    # 探索用のキュー
    queue = deque()

    # 初期状態をキューに追加
    queue.append((start, [start]))

    while queue:
        # キューから先頭の要素を取り出す
        node, path = queue.popleft()

        # ノードが終了ノードであれば、経路を返す
        if node == end:
            return path

        # ノードが未訪問であれば、訪問済みにする
        if node not in visited:
            visited.add(node)

            # 探索中のノードに接続する全てのノードを取得し、キューに追加
            for neighbor in graph[node]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))

    # 到達不能な場合はNoneを返す
    return None


#v15
'''
改めてグラフを定義します。

使用しているグラフは辞書です。辞書のkeyがとあるノードであり、value内list内要素が別のノードかつ、keyノードからのエッジです。value内list内要素もノードであることにます。必要であれば、グラフに追加してください。全てのエッジの重みは１です。
# グラフの例
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D']
}
これを踏まえて, 指定した始点ノードから終点ノードまでの最短パスを抽出するPythonコードを書いてください。上記グラフの例では’D'がグラフのノードとして定義されていませんが、その場合はエッジを持たないノードと判断してください
'''
import heapq

def dijkstra15(graph, start, end):
    # 各ノードへの最短距離を格納する辞書
    distances = {node: float('inf') for node in graph}
    # 始点への最短距離は0
    distances[start] = 0
    # ヒープキューを初期化し、(始点からの距離, 始点)のタプルを追加する
    heap = [(0, start)]
    # 訪問済みのノードを格納する集合
    visited = set()

    while heap:
        # ヒープキューから最も距離が短いノードを取り出す
        (distance, current_node) = heapq.heappop(heap)

        # 訪問済みのノードはスキップする
        if current_node in visited:
            continue

        # 現在のノードを訪問済みとしてマークする
        visited.add(current_node)

        # ゴールノードに到達した場合、最短パスを返す
        if current_node == end:
            return distances[end]

        # 現在のノードから到達可能なノードについて、距離を更新する
        #for neighbor, distance_to_neighbor in graph[current_node].items():
        for neighbor, distance_to_neighbor in graph[current_node]:
            tentative_distance = distances[current_node] + distance_to_neighbor
            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                heapq.heappush(heap, (tentative_distance, neighbor))

    # ゴールノードに到達できない場合は、Noneを返す
    return None


#v16-19：なし

#v20
'''
定義したグラフ内の始点と終点の２ノードを指定して、最短経路を抽出するPythonコードを書いて

グラフの定義
グラフとはグラフ理論の有指向グラフです。
Pythonコードで使用するグラフは辞書です。
辞書のkeyが、とあるノードです。
辞書のvalue内list要素が別のノードであり、かつ、keyノードからのエッジとして定義しています。
全てのエッジの重みは１です
# グラフの例
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D']
    'D': []
}



'''
from collections import deque

def shortest_path20(graph, start, end):
    # 各ノードへの最短距離を保持する辞書と、最短経路を保持する辞書を初期化する
    distances = {node: None for node in graph}
    paths = {start: [start]}

    # 始点の距離は0とする
    distances[start] = 0

    # BFSアルゴリズムを使用して最短経路を計算する
    queue = deque([start])
    while queue:
        current_node = queue.popleft()
        for neighbor in graph[current_node]:
            if distances[neighbor] is None:
                distances[neighbor] = distances[current_node] + 1
                paths[neighbor] = paths[current_node] + [neighbor]
                queue.append(neighbor)

    # 最短経路を返す
    return paths.get(end)



#v21(実際のグラフを示す）

'''
グラフが大きいと？処理が終わらない
'''

import heapq

def dijkstra21(graph, start_node, end_node):
    # 始点から各ノードまでの距離を初期化
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0

    # 最短経路を求めるためのヒープ
    heap = [(0, start_node)]

    while heap:
        # ヒープから距離が最小のノードを取り出す
        (distance, node) = heapq.heappop(heap)

        # 終点に到達したら探索を終了
        if node == end_node:
            break

        # 現在のノードに隣接するノードを探索
        for adjacent_node in graph[node]:
            # 隣接するノードへの距離
            new_distance = distances[node] + 1 # 全てのエッジの重みが1なので+1

            # より短い経路が見つかった場合、距離を更新
            if new_distance < distances[adjacent_node]:
                distances[adjacent_node] = new_distance
                heapq.heappush(heap, (new_distance, adjacent_node))

    # 終点への最短距離と最短経路を返す
    return distances[end_node], get_shortest_path(graph, start_node, end_node, distances)

def get_shortest_path(graph, start_node, end_node, distances):
    # 最短経路を求めるためのスタック
    stack = [end_node]

    # 終点から始点まで、最短経路を辿る
    while stack[-1] != start_node:
        # スタックの先頭にあるノード
        current_node = stack[-1]

        # スタックの先頭にあるノードに隣接するノードを探索
        for adjacent_node in graph[current_node]:
            # スタックの先頭にあるノードから隣接するノードへの距離
            distance = distances[adjacent_node]

            # 隣接するノードが現在のノードよりも短い距離で到達できる場合、スタックに追加
            if distance == distances[current_node] - 1: # 全てのエッジの重みが1なので-1
                stack.append(adjacent_node)
                break

    # スタックにたまった最短経路を逆順にして返す
    return list(reversed(stack))











def graph( ):

  if NX==1:
    # グラフオブジェクトの作成
    G = nx.DiGraph()

    ## add node
    #for xxx in path:
    #  G.add_node(xxx)

    # add edge
    '''
    #for xxx in l04:
    #  G.add_edge(xxx[0],xxx[1])
    #  print(xxx[0],"->",xxx[1])
    for ii in range(len(path)-1):
      G.add_edge(path[ii],path[ii+1])
      print(path[ii],"->",path[ii+1])
    '''
    for lll in lpaths:
      for ii in range(len(lll)-1):
        G.add_edge(lll[ii],lll[ii+1])
        print(lll[ii],"->",lll[ii+1])



    # レイアウトの設定
    pos = nx.spring_layout(G)


    node_attributes = {  'node_size': 1200, 'node_color': 'lightblue', 'node_shape': 's', 'linewidths': 1, 'edgecolors': 'blue', 'alpha': 0.5}


    # 矢印の長さを調整する
    arrowsize = 30
    edge_attributes = {'alpha': 0.5, 'width': 2, 'arrowstyle': '->', 'arrowsize': arrowsize, 'connectionstyle': 'arc3,rad=.25'}




  # 図の描画
  #plt.figure(figsize=(8, 4))  # 2:1の比率にするために、図のサイズを指定
  #plt.figure(figsize=(150, 150))
  plt.figure(figsize=(30, 20))

  # ノードのラベルを表示するための辞書
  labels = {}
  for node in G.nodes():
      labels[node] = node

  # 四角形の大きさをラベルに合わせて自動調整するためのレイアウト
  pos = nx.spring_layout(G, k=0.8, seed=123)

  # ノードの四角形の大きさをラベルに合わせて自動調整
  node_sizes = [len(str(labels[node])) * 300 for node in G.nodes()]

  # 図の描画
  nx.draw_networkx_nodes(G, pos, **node_attributes)
  #nx.draw_networkx_edges(G, pos, alpha=0.5, width=2, arrowstyle="->", arrowsize=30)
  nx.draw_networkx_edges(G, pos, **edge_attributes)
  nx.draw_networkx_labels(G, pos, labels, font_size=12, font_family='sans-serif')
  plt.axis('off')
  plt.show()


#ddd={'a':1,'b':2,'c':3}
#print(ddd)
#print(list(ddd))


d02=d01

for k in list(d02):
  for edge in d02[k]:
    #print("dege for ",k," is ",edge)
    if edge not in d02:
      d02[edge]=[]

print(d02)



'''
l_path = find_path(d01, 'GDS7', 'GDGV')
print(l_path)
l_path = find_path(d01, 'GDS7', 'GDPY')
print(l_path)
l_path = find_path(d01, 'GDS7', 'GALI')
print(l_path)
l_path = find_path(d01, 'GDS7', 'GC6G')
print(l_path)
l_path = find_path(d01, 'GDS7', 'GAHP')
print(l_path)
'''

#print("### find_path###")
#l_path = find_path(d01, 'GDS7', 'GBCR')
#print(l_path)
#None
#l_path = find_path(d01, 'GBCR', 'GDS7')
#print(l_path)

#l_path = find_path(d01, 'GDGV', 'GBCR')
#print(l_path)
#None
#l_path = find_path(d01, 'GBCR', 'GDGV')
#print(l_path)


#l_paths = find_all_paths(d01, 'GDGV', 'GBCR')
#for xxx in l_paths:
#  print(xxx)
#print("length of pathes ... "+str(len(l_paths)))


#gds7->バーター
#l_path = find_path(d01, 'GDS7', 'GDPY')
#print(l_path)

'''
print("### find_all_paths ###")
l_paths = find_all_paths(d01, 'GDS7', 'GBCR')
for xxx in l_paths:
  print(xxx)
print("length of pathes ... "+str(len(l_paths)))



l_paths = find_all_paths(d01, 'GDS7', 'GDGV')
for xxx in l_paths:
  print(xxx)
print("length of pathes ... "+str(len(l_paths)))
'''



#print("### find_path###")
#l_path = find_path(d01, 'GAFY', 'GD4R')
#print(l_path)
#l_path = find_path(d01, 'GAFY', 'GA7H')
#print(l_path)

#print("### find_all_paths ###")
#l_paths = find_all_paths(d01, 'GAFY', 'GA7H')
#for xxx in l_paths:
#  print(xxx)
#print("length of pathes ... "+str(len(l_paths)))


'''
1	GA7HY7JCZXIK6T4MHMKEW2EKTQ4LYTRX3OGTVHFLOXPRZUD77V56CYZY	261,494 
2	GBGZ75ONFOUVLPIBGK7U5GM7THEY3ULJGISJMZXCCC3HFLXAJBBGPCLV	201,188 
3	GAHPB4GM625SQL6N7BKFMEIET3LPGXING4CKX4YU6EGGMVRMZGWANHLP	176,471 
4	GBN7U3PZGERFHY6L5X3ZSHZ3A5Y3MXJY43KQMAYY4LIFEMY7AWX55N4R	147,163 
5	GAP6445MHUSO3U2PNNEVEGPYP2XAJINJYVCNHLJVTYKUCUV6LK5IABPZ	130,679 
6	GBXS2VLVKKZ7ZVNTQ2WQAIIFIZXTIASF6ED6RYD7HPARFXO6XZIB4PSI	89,527 
7	GBFF6AGW2TBXKBEGJAKMXPYV3MRTGCIJ74J66YSBOILBMJRRGLSLJWV5	84,155 
8	GAD77VSCGR7NLK4MHG4J3QEQ7K2GNTBZNKGFNOXOND575U76DSAXAPTO	72,001 
9	GBMJFMU6A6L2PMPA5NU6LF747FIQ3F7M3SCFJTJXCRD7PMFEWJAGTZNF	54,118 
10	GCC3WKYXIR325NEJ6ATU4AON3F2M2SQKUNQWX3HYA5VFIGS4EMOMWBXI	42,370 
'''

lpath=[]
lpaths=[]

'''
lpath = shortest_path(d01, 'GAFY', 'GA7H')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GAFY', 'GBGZ')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GAFY', 'GAHP')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GAFY', 'GBNG')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GAFY', 'GBXS')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GAFY', 'GBFF')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GAFY', 'GAD7')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GAFY', 'GBMJ')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GAFY', 'GCC3')
lpaths.append(lpath)
'''

'''
lpath = shortest_path(d01, 'GDS7', 'GDVG')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GDS7', 'GB6E')
lpaths.append(lpath)
lpath = shortest_path(d01, 'GDVG', 'GCKL')
lpaths.append(lpath)
print(lpaths)
#l_path = find_path(d01, 'GDS7', 'GDGV')
#print(l_path)

print(d01['GDS7'])
print(d01['GDGV'])
print(d01['GDZG'])
'''

#print("################################")
#print(d01)
#print("################################")





shortest_distance = find_shortest_path14(d02, 'GDS7', 'GDVG')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GDS7', 'GB6E')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GDVG', 'GCKL')
lpaths.append(shortest_distance)

print(lpaths)
exit()









graph()

