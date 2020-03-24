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


app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
    html.H2('Public transport of Alcobendas'),
    dash_table.DataTable(
    id='table',
    columns=[{"name":i,"id":i} for i in df.columns],
    data=df.to_dict('records'),
    style_cell={'textAlign': 'center'},
    style_cell_conditional=[
        {
            'if':{'column_id':'Tipo de transporte'},
            'textAlign':'left'
        }],
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    column_selectable="single",
    #row_selectable="multi",
    #row_deletable=True,
    #selected_columns=[],
    #selected_rows=[],
    page_action="native",
    #page_current= 0,
    #page_size= 10,   
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)