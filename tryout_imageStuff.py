import dash
import dash_html_components as html
import base64

app = dash.Dash()



app.layout = html.Div([
    html.Img(src='https://i.scdn.co/image/ab67616d0000b2737359994525d219f64872d3b1')
])

if __name__ == '__main__':
    app.run_server(debug=True)