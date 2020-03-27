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

df_url = 'https://datos.alcobendas.org/dataset/9cc894a1-8cfb-4dfe-a29f-fb197aa03ae0/resource/eff1bb9c-110e-4962-8370-d78589f987c2/download/uso-de-autobuses.csv'
df = round(pd.read_csv(df_url),2)
df.rename(columns={'Línea':'Line', 'Año':'Year'}, inplace=True)

years = df.Year.unique().tolist()
line = df.Line.unique().tolist()

app = dash.Dash(__name__)
server = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    children=["Select the line and the year that you want to observe:",
    dcc.Dropdown(
            id='filter_dropdown',
            options=[{'label':st, 'value':st} for st in line],
            value = line[0]
            ),
    dcc.Dropdown(
            id='filter_dropdown_y',
            options=[{'label':yr, 'value':yr} for yr in years],
            value= years[0]
            ),
    dash_table.DataTable(id='table-container', columns=[{'id': c, 'name': c} for c in df.columns.values]) ]
)

@app.callback(
    Output('table-container', 'data'),
    [Input('filter_dropdown', 'value') ])
def display_table(line):
    dff = df[df.Line==line]
    return dff.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)