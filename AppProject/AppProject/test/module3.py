import plotly.graph_objects as go

import numpy as np

fig = go.Figure()

trace_num = 2
point_num = 1000000
for i in range(trace_num):
    fig.add_trace(
        go.Scattergl(
                x = np.linspace(0, 1, point_num),
                y = np.random.randn(point_num)+(i*5)
        )
    )

fig.update_layout(showlegend=False)

fig.show()