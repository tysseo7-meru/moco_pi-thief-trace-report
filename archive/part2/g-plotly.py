#plotly

# pip install plotly

import plotly.graph_objs as go

fig = go.Figure(data=[go.Scatter(
    x=[0, 1, 2, 3, 4],
    y=[0, 1, 2, 3, 4],
    mode='lines+markers',
    line=dict(width=1),
    marker=dict(size=7),
    text=['1->2', '2->3', '3->4', '4->5', '5->2'],
    hovertext=['1->2', '2->3', '3->4', '4->5', '5->2'],
    hoverinfo='text'
)])

fig.update_layout(
    title='Directed Graph',
    title_x=0.5,
    xaxis_title='X Axis Title',
    yaxis_title='Y Axis Title',
    width=800,
    height=600,
    showlegend=False,
    hovermode='closest',
    margin=dict(l=0, r=0, t=50, b=0)
)

fig.show()

