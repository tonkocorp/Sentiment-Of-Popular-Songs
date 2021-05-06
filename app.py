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
#print(avg)
comparison = pd.read_sql_query(sql.tempoVersus,conn)
#print(comparison)
position = pd.read_sql_query(sql.position,conn)
print(position)

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


fig1 = px.scatter(position, x="Position", y="SentimentScore", 
                 hover_data=["SongName", "Artist"], 
                 size = "Position",
                color="Position",title="Sentiment of Todays Top Songs According to Position")
#-----------------------------------------------------------------


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Sentiment Analysis of the Top Songs on Spotify: Daily Updates!"

app.layout = html.Div(
    children=[html.Div(
            children=[
                html.P( className="header-image"),
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
         html.Div( children=[
                                html.H4(
                                    className='what-is',
                                    children='Whats is this project?'
                                ),
                                html.P(
                                    """
                                    The idea of this project is that the music we listen too
                                    says something about us as a society. So music can be seen as
                                    """
                                ),
                                html.P(
                                    """
                                    Each point on the graph is the average sentiment score of the Top Songs for that day.
                                    The process of attaing these scores is as follows.
                                    1. 
                                     
                                    """
                                ),
                                html.P(
                                    """
                                   
                                    """
                                ),
                            ]),
       
       

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
        ),className ="card", style={'width': '90%', 'display': 'inline-block','margin': 'auto', 'justify-content': 'space-evenly'}
        ),

        html.Div( children=[
                                html.H4(
                                    className='what-is',
                                    children='Whats up with these Graphs?'
                                ),
                                html.P(
                                    """
                                    The Graph on the left retrieves the 10 most recent songs added,
                                    to the databse and displays them in terms of their individual 
                                    Sentiment Scores. 
                                    """
                                ),
                                html.P(
                                    """
                                    Each point on the graph is the average sentiment score of the Top Songs for that day.
                                     
                                    """
                                ),
                                html.P(
                                    """
                                    Read more about the component here:
                                    https://github.com/plotly/react-alignment-viewer
                                    """
                                ),
                                
                            ],style = {'text-align': 'right', 'float': 'right'}),
        html.Div(
            children = [
        dcc.Graph(id="songposition", figure = fig1),
       
    ],style={'width': '49%', 'display': 'right' },), 
    
    
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
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        
    ]),

    dcc.Graph(id='Compare-Features'),

   
])
    
])
      
     #])

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