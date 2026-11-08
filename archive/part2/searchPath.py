
#### pip install requests
#### pip install scipy

'''
import json
import requests
import sys
import re
'''


import networkx as nx
import matplotlib.pyplot as plt
from collections import deque





NX=0

#networkx on
NX=1





#test
#f = open('foo.txt', 'r')

# GDS7 -to
#f = open('to/t.csv', 'r')
#f = open('to_0421.csv', 'r')
#f = open('to_lib_debug.csv', 'r')
f = open('to_0501.csv', 'r')



# GDVG -from
#f = open('to/GDGV-from.csv', 'r')


# GDVG -to
#f = open('GDGV-to.csv', 'r')


# GDS7 -from
#f = open('from/from.csv', 'r')
#f = open('from_0430.csv', 'r')

#f = open('to/GB6E-to.csv', 'r')
#f = open('GB6EJ-from.csv', 'r')


# gafy -to -ath 200
#f = open('gafy-to-ath200.csv', 'r')

l_file = f.readlines()
f.close()




l_file2 = [s for s in l_file if 'created_at' in s]

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
  #adr_from = ll[0][:4]
  #adr_to   = ll[1][:4]
  #adr_from = ll[0][:5]
  #adr_to   = ll[1][:5]
  adr_from = ll[0][:6]
  adr_to   = ll[1][:6]
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











def graph( lpaths ):

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
      print(lll) #debug
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



d02=d01.copy()

for k in list(d02):
  for edge in d02[k]:
    #print("dege for ",k," is ",edge)
    if edge not in d02:
      d02[edge]=[]
for k in list(d02):
  ii=0
  f_loop = False
  for edge in d02[k]:
    if edge==k:
      f_loop = True
      break
    ii+=1
  if f_loop :
    d02[k].pop(ii)
#print(d02)




###########################

'''
shortest_distance = find_shortest_path14(d02, 'GDS73', 'GDGVI')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GDS73', 'GDPYU')
lpaths.append(shortest_distance)
print(lpaths)
'''

'''
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GA7HY')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GBGZ7')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GAHPB')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GBN7U')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GAP64')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GBXS2')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GBFF6')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GAD77')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GBMJF')
lpaths.append(shortest_distance)
shortest_distance = find_shortest_path14(d02, 'GAFYX', 'GCC3W')
lpaths.append(shortest_distance)
print(lpaths)
'''

'''
l_paths = find_all_paths(d02, 'GDS73', 'GDGVI')
for xxx in l_paths:
  print(xxx)
print("length of pathes ... "+str(len(l_paths)))
'''


#print("### find_path###")
#l_path = find_path(d02, 'GDS7', 'GBCR')
#print(l_path)

'''
l_end = [
    'GALIT',
    'GC6GT',
    'GCW2N',
    'GA7HY',
    'GAHPB',
    'GBU6M',
    'GBFF6',
    'GC742',
    'GBXS2',
    'GA7M5',
]
'''



#############################
start = 'GDS73T'
#start = 'GB6EJ'
#start = 'GCGTB'
#start = 'GDTYS'
#start = 'GDZGW'


l_adr = []
for xxx in l_file2:
  ll=xxx.split(",")
  l_adr.append(ll[3][0:6])
  l_adr.append(ll[5][0:6])

l_end = []
l_end = list(set(l_adr))


lpaths=[]
ii=0
for end in l_end:
  ii+=1
  if ii > 1000000 :
    break
  sp = find_shortest_path14(d02, start, end)
  if not sp==None:
    lpaths.append(sp)
print(lpaths)
'''
ハックアドレスGDS73
GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU
から大量送金（１０００π以上の送金）をフォワードトレース先アドレス数80kの総残高は55M Pi（PCM:7M、BaterMall:3M込み)…5/2時点

全てが盗難されたPiではないがオープンメインネットなると何割かは外にでる気がする



フォワードトレース：
GDS73から、１０００π以上の送金されたアドレスとそのまた先の大量送金アドレス、そのまた先の・・・と送金がなくなるまでアドレスを追跡
（トレース時間２４時間@i5-2430M,win10,python3）



'''
########################




'''
#for from_0430.csv
lpaths=[]
lpaths.append(find_shortest_path14(d02, 'GDGVIL', 'GDS73T'))
#lpaths.append(find_shortest_path14(d02, 'GABT7E', 'GDS73T'))
print(lpaths)
'''





graph(lpaths)

