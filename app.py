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
fig = px.scatter(data, x="Date", y="SentimentScore",
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
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in data],
                value='SongSentiment, total (births per woman)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        #className="menu"
        style={'width': '80%', 'display': 'inline-block'}),

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
    html.Div(children = [
        dcc.Graph(id="compare-sentiment-to-features")
    ])
    
])
      
     #])

@app.callback(
    Output('songposition', 'figure'),
    Input('song-position-slider', 'value'))
def update_figure(position):
    filtered_data = data[data.Position == position]
    
    fig = px.scatter(filtered_data, x="Date", y="SentimentScore", 
                size="Position", hover_data=["SongName", "Artist"], 
                color="Position")

    compare_features = data[data]

    fig1 = px.scatter(chosen_data, x="Date", y="SentimentScore", 
                size="Position", hover_data=["SongName", "Artist"], 
                color="Position")
    

    
    fig.update_layout(transition_duration=500)

    return fig






if __name__ == "__main__":
    app.run_server(debug=True)