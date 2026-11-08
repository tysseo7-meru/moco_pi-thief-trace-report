
g=[
  ['GDS73', 'GB6EJ', 'GAHPB'],
  ['GDS73', 'GB6EJ', 'GBU6M'],
  ['GDS73', 'GB6EJ', 'GDOSR'],
  ['GDS73', 'GB6EJ', 'GDXKL'],
  ['GDS73', 'GB6EJ'],
  ['GDS73', 'GCGTB', 'GB2Q4'],
  ['GDS73', 'GCGTB', 'GBDUF'],
  ['GDS73', 'GCGTB', 'GCG2P'],
  ['GDS73', 'GCGTB', 'GCN3T'],
  ['GDS73', 'GCGTB', 'GCUAN'],
  ['GDS73', 'GCGTB', 'GCWVJ'],
  ['GDS73', 'GCGTB', 'GDAET'],
  ['GDS73', 'GCGTB', 'GDWZS'],
  ['GDS73', 'GDTYS', 'GDKTK'],
  ['GDS73', 'GDZGW', 'GA4I7'],
  ['GDS73', 'GDZGW', 'GANIB'],
  ['GDS73', 'GDZGW', 'GB2IC'],
  ['GDS73', 'GDZGW', 'GCFGW'],
  ['GDS73', 'GDZGW', 'GCNZX'],
  ['GDS73', 'GDZGW', 'GCZHC'],
  ['GDS73', 'GDZGW', 'GD7Y7']
]

import plotly.graph_objects as go

# ノードの定義
nodes = set()
for edge in g:
    nodes.update(edge)
nodes = list(nodes)

# エッジの定義
edge_x = []
edge_y = []
for i, edge in enumerate(g):
    for j in range(len(edge)-1):
        x0, y0 = nodes.index(edge[j]), i
        x1, y1 = nodes.index(edge[j+1]), i
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

# ノードとエッジを描画
fig = go.Figure()

# ノードを描画
for i, node in enumerate(nodes):
    fig.add_trace(go.Scatter(
        x=[i],
        y=[0],
        mode="markers+text",
        marker=dict(size=20),
        text=node,
        textposition="middle center"
    ))
    fig.add_trace(go.Scatter(
        x=[i-0.5, i-0.5, i+0.5, i+0.5, i-0.5],
        y=[-0.5, 0.5, 0.5, -0.5, -0.5],
        mode="lines",
        line=dict(color="black")
    ))

# エッジを描画
fig.add_trace(go.Scatter(
    x=edge_x,
    y=edge_y,
    mode="lines",
    line=dict(color="black", width=2),
    hoverinfo="none",
    arrowhead=2
))

# グラフレイアウトを設定
fig.update_layout(
    showlegend=False,
    xaxis=dict(
        visible=False,
        range=[-1, len(nodes)],
    ),
    yaxis=dict(
        visible=False,
        range=[-1, len(g)]
    ),
    margin=dict(l=10, r=10, t=10, b=10),
    height=400
)

# グラフを表示
fig.show()
