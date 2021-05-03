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
    },
]

#Graphs-----------------------------------------------------------
'''
fig = px.scatter(data, x="Date", y="SentimentScore",
                 size="SongName", color="SongName", hover_name="Artist",
                 log_x=True, size_max=60)

'''
fig = px.scatter(data, x="Tempo", y="SentimentScore")

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
        style={'width': '49%', 'display': 'inline-block'}),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": avg["Date"],
                        "y": avg["AVG(SentimentScore)"],
                        "type": "lines",
                    },
                ], 
                "layout": {"title": "Sentiment over Time"},
            }, className ="card",
        ),
        dcc.Graph(figure = fig)
      
    ])






if __name__ == "__main__":
    app.run_server(debug=True)