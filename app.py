import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

import plotly.express as px
import sqlite3
import MySQLStatements as sql

from flask import Flask
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
server = app.server
app.title = "Sentiment Analysis of the Top Songs on Spotify: Daily Updates (pending)!"

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
                                    
                                    The music we listen to says something about us and therefore the music we consume as  
                                    a society should give some indication about the cultural and emotional state as a whole.  
                                    This project pulls the top ten songs from Spotify every day, retrieves lyrics from the Genius  
                                    API, then runs them through simple sentiment analysis, with the idea that the sentiment of
                                    our biggest hits reflects the sentiment of society as a whole. 
                                  """  
                                    
                                ),
                                html.P(
                                    """
                                   However, because lyrics are only one part of a song, audio features are stored as well inside an SQL-Lite Database. The data is displayed here using Dash for python, Plotly, and some CSS.
                                   Finally, this data dashboard is hosted on a Heroku server.

                                    """
                                ),
                                html.P(
                                    """
                                   The graph below displays the average Sentiment score of the Top Ten Songs on Spotify.
                                   A score above 0 is considered positive while a score below is considered positive.
                                    """
                                )
                            ],style={'margin-left': '50px', 'margin-right': 'auto', 'width': '60em', 'font-size': 'Large', 'justify-content': 'center'}),
       
       

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
        ),className ="card", style={'width': '90%', 'display': 'inline-block','margin': '80px' , 'justify-content': 'space-evenly'}
        ),

        html.Div( children=[
                                html.H4(
                                    className='what-is',
                                    children='Whats up with these Graphs?'
                                ),
                                html.P(
                                    """
                                    The graph to the left displays the top ten ongs for the day according to their position on the chart. 
                                    This graph might be slightly misleading the top song is actually ‘position1.’ 
                                    Also the smaller the size the more popular the song is I’ve tried reversing this but so far to no avail.
                                    """
                                ),
                                html.P(
                                    """
                                    The graph below allows a user to compare features of all of the Top Songs on Spotify.
                                    The radio button on the right controls the values on the y axis while the one on the left controls features on the x-axis. It works well now but once the amount of songs reaches a certain point, it might be good to add some way to filter the data according to a date range probably using a slider.  

                                     
                                    """
                                ),
                                html.P(
                                    """
                                    
                                    """
                                ),
                                
                            ],style={'margin': '80px', 'width': '33em', 'text-align': 'left',  'float': 'right', 'font-size': 'Large'}),
        html.Div(
            children = [
        dcc.Graph(id="songposition", figure = fig1),
       
    ],className='card', style={ 'margin-left': '80px', 'width': '55%', 'display': 'left', 'margin': '80px' },), 
    
    
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
        ]),
        
    ],className='menu', style={'width': '50%',  'margin-left': '80px', 'margin-top': '40px',}),

    html.Div(

    dcc.Graph(id='Compare-Features'), className = 'card', style = {'margin': '80px'})

   
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
                     hover_data=["SongName", "Artist"]
                     
                     )

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig






if __name__ == "__main__":
    app.run_server(debug=True)