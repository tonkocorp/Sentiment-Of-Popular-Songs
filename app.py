import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

import plotly.express as px
import sqlite3
import MySQLStatements as sql

#SQL--------------------------------------------------------------
conn = sqlite3.connect('songs.db')
data = pd.read_sql_query(sql.selectAll, conn)
print(data)

# get the average of all sentiment scores for the day
avg = pd.read_sql_query(sql.averageSentiment,conn)
print(avg)
comparison = pd.read_sql_query(sql.tempoVersus,conn)
print(comparison)

#-----------------------------------------------------------------
data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%y")
data.sort_values("Date", inplace=True)

intOnly = pd.read_sql_query(sql.intValues,conn)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
        "href": "style.css"
    },
]

#Graphs-----------------------------------------------------------
'''
fig1 = px.scatter(data, x="Date", y="SentimentScore",
                 size="SongName", color="SongName", hover_name="Artist",
                 log_x=True, size_max=60)
'''


#-----------------------------------------------------------------


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Sentiment Analysis of the Top Songs on Spotify: Daily Updates!"

app.layout = html.Div(
    children=[html.Div(
            children=[
                html.P(children="🎼 = 🙂 or 🙃  ", className="header-emoji"),
                html.H1(
                    children="Sentiment of the Top Songs on Spotify", className="header-title"
                ),
                html.P(
                    children="This projects scrapes the top 10 songs and their audio features from Spotify every Day"
                    " It then retrieves lyrics from those Songs from the Genius API"
                    " Lyrics are then run through a Sentiment Analysis",
                    className="header-description",
                ),
            ],
            className="header",
        ),
       

        html.Div(
            dcc.Graph(
            figure={
                "data": [
                    {
                        "x": avg["Date"],
                        "y": avg["AVG(SentimentScore)"],
                        "type": "lines",
                    },
                ], 
                "layout": {"title": "Average Sentiment over Time"},
            }, 
        ),className ="card", style={'width': '50%', 'display': 'inline-block','position': 'right'},
        ),
        html.Div(
            children = [
        dcc.Graph(id="songposition"),
        dcc.Slider(
        id='song-position-slider',
        min=data['Position'].min(),
        max=data['Position'].max(),
        marks={str(position): str(position) for position in data['Position'].unique()},
       
        step=None,
        value=data['Position'].max(),
    )],style={'width': '49%', 'display': 'right' },), 
    html.Div(id='slider-output-container'),
    
    html.Div([
        html.Div([

        html.Div([
            dcc.Dropdown( 
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in intOnly],
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
                options=[{'label': i, 'value': i} for i in intOnly],
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

   
])
    
])
      
     #])

@app.callback(
    Output('songposition', 'figure'),
    Input('song-position-slider', 'value'))
def update_figure(position):
    filtered_data = data[data.Position == position]
    
    fig1 = px.scatter(filtered_data, x="Date", y="SentimentScore", 
                size="Position", hover_data=["SongName", "Artist"], 
                color="Position")
    
    fig1.update_layout(transition_duration=500)

    return fig1


@app.callback(
    Output('Compare-Features', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    )
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):
    

    fig = px.scatter(data, x=xaxis_column_name,
                     y=yaxis_column_name,
                     hover_name=yaxis_column_name,
                     
                     color = "Position",
                     hover_data=["SongName", "Artist"],
                     
                     )

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig






if __name__ == "__main__":
    app.run_server(debug=True)