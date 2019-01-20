import plotly.plotly as py 
import plotly.graph_objs as go 
import numpy as np 
from random import uniform

N = 500

trace0 = go.Scatter(
    x = np.array([uniform(0.8,0.9) for x in range(85)]),
    y = np.array([0 for x in range(85)]),
    name= 'Plant more Trees',
    mode= 'markers',
    marker= dict(
        size=10,
        color='rgba(152, 0, 0, 0.8)',
        line=dict(
            width = 2,
            color='rgb(2,4,7)'
        )
    )
)

trace1 = go.Scatter(
    x = np.array([uniform(0.03, 0.04) for x in range(3)]),
    y = np.array([2,3]),
    name= 'Trees for groundwater',
    mode= 'markers',
    marker= dict(
        size=10,
        color='rgba(152, 200, 0, 0.8)',
        line=dict(
            width = 2,
            color='rgb(2,4,7)'
        )
    )
)

data = [trace0, trace1]

layout = dict(
    title = 'Test',
    yaxis = dict(zeroline=False),
    xaxis = dict(zeroline=True)
)

fig = dict(data=data, layout=layout)
py.plot(fig, filname='styled-scatter')