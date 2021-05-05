import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Output, Input

import sqlite3
import MySQLStatements as sql

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
conn = sqlite3.connect('songs.db')
data = pd.read_sql_query(sql.selectAll, conn)

#available_indicators = data[data].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown( 
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in data],
                value='Tempo'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in data],
                value='SentimentScore'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='Compare-Features',),

    dcc.Slider(
        id='year--slider',
        min=data['Date'].min(),
        max=data['Date'].max(),
        value=data['Date'].max(),
        marks={str(date): str(date) for date in data['Date'].unique()},
        step=None
    )
])

@app.callback(
    Output('Compare-Features', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('year--slider', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dataf = data[data['Date'] == date]

    fig = px.scatter(x=dataf[dataf[data] == xaxis_column_name]['Value'],
                     y=dataf[dataf[data] == yaxis_column_name]['Value'],
                     hover_name=dataf[dataf[data] == yaxis_column_name]['SongName'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)