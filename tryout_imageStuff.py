import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
#from pandas_datareader import data as web
from datetime import datetime as dt
import plotly.graph_objs as go


app = dash.Dash()
app.layout = html.Div(children=[
    html.H1('Hello Dash', style={'background-image': 'url(/assets/collage.jpg)',
    'background-repeat': 'repeat', 'position':'fixed',
  'width':'100%',
  'height':'100%',
  'top':'0px',
  'left':'0px',
  'z-index':'1000',
  'padding': 20})
    ])

if __name__ == '__main__':
    app.run_server(debug=True)