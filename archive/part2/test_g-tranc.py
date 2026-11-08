### pip install networkx


import networkx as nx
import matplotlib.pyplot as plt
import g-trance as gt

# グラフオブジェクトの作成
#G = nx.DiGraph()

'''
# ノードの追加
#G.add_node("GGGG")
gt.G.add_node("GAK7L")
gt.G.add_node("GCNVU")
gt.G.add_node("GD2DR")
gt.G.add_node("GDY7X")
gt.G.add_node("GDZN2")

'''

# エッジの追加
#G.add_edge("GGGE", "GGGG")
#G.add_edge("GGGG", "GGGB") 
gt.G.add_edge("GDY7X","GD2DR")
gt.G.add_edge("GDYUY","GAK7L")
gt.G.add_edge("GDZN2","GCNVU")

'''
# レイアウトの設定
pos = nx.spring_layout(G)


node_attributes = {  'node_size': 1200, 'node_color': 'lightblue', 'node_shape': 's', 'linewidths': 1, 'edgecolors': 'blue', 'alpha': 0.5}


# 矢印の長さを調整する
arrowsize = 30
edge_attributes = {'alpha': 0.5, 'width': 2, 'arrowstyle': '->', 'arrowsize': arrowsize, 'connectionstyle': 'arc3,rad=.25'}




# 図の描画
#plt.figure(figsize=(8, 4))  # 2:1の比率にするために、図のサイズを指定
plt.figure(figsize=(8, 8))

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
'''

