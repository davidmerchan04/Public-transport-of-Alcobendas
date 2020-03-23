import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np 
import dash_bootstrap_components as dbc # import the library
import dash_table
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import json

import pandas as pd

db_url = 'https://datos.alcobendas.org/dataset/9cc894a1-8cfb-4dfe-a29f-fb197aa03ae0/resource/eff1bb9c-110e-4962-8370-d78589f987c2/download/uso-de-autobuses.csv'
db = pd.read_csv(db_url)



app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
    html.H2('Public transport of Alcobendas'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(dash.dependencies.Output('display-value', 'children'), [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)