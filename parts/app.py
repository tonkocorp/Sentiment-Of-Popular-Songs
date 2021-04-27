import dash # helps init
import dash_core_components as dcc # allow interactive
import dash_html_components as html #access html tags
import pandas as pd

data = pd.read_csv("avocado.csv")
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

#init the dash class
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"
app.layout = html.Div(
    children=[
        html.P(children="🥑", className="header-emoji"),
        #add heading
        html.H1(
            children="Avocado Assalytics",
            className="header-title",
        ),
        html.P(
            children="Analyze the behavior of avocado prices"
            " and the number of avocados sold in the US"
            " between 2015 and 2018",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AveragePrice"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Price of Avocados"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Total Volume"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Avacados Sold"},
            },
        ),
    ]
)

if __name__ == "__main__":
    #debug=True means we can make changes to the app
    # without having to restart the server! 
    app.run_server(debug=True)