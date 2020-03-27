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

markdown_text='''

## About this app 
This app shows information about the public transport of Alcobendas. The data contains 84 variables about 28 bus lines for 3 years in Alcobendas. The variables that are described in this dataset are:

* Line: Is the number of the linebus

* Year: Corresponds to the year in which it was collected

* Tipo de transporte: Refers to the type of the line, it can be urban bus and interurban bus

* Número anual de pasajeros: Refers to the annual number of passengers in a certain line

* Expediciones por día: Refers to the number of times that the bus was in services

* Viajeros por día:Refers to the daily number of passengers in a certain line

* Viajeros por expedición: Refers to the number passengers in each time in which the bus was in services

* Kilometros anuales recorridos: Refers to the number of kilometers that the bus toured in a year.

In this app we can see: 

* Data:

In this first tab, we can observe the data of the public transport of Alcobendas in 2015,2016 and 2017. The table shows all the variable that contains the dataset,
if you want you can select only the information of the line that you prefer. 

* Variable distribution:

The variable distribution is shown with a histogram plot, this is use to understand the behavior of tha variable that are studied. In this panel
you can select the variable that you want to analyze. 

* Relations between variables 

In this panel we can observe a plot that is called correlation plot, this is used to understand the behavior between then. For example, if we see a cloud of points that draw a diagonal that increase
from the down left side to the up rigth side the relation is positive. On the other hand, if that point cloud draws  a diagonal that decrease from the up left corner to  the down rigth corner we can say
that those two variable have a negative relation. Otherwise, we can say that the variables have not relation. 

* Other statistic information

In the final tab we can see another type of plots that let us understand some differences between the two types of autobuses in the public transport of Alcobendas (Interurban and Urban)


'''

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='About', children=[
            dcc.Markdown(markdown_text)]),
        dcc.Tab(label='Data', children=["Select the line and the year that you want to observe:",
            dcc.Dropdown(
                id='filter_dropdown',
                options=[{'label':st, 'value':st} for st in line],
                value = line[0]
            ),
            dash_table.DataTable(id='table-container', columns=[{'id': c, 'name': c} for c in df.columns.values]) ]) #Close tab=Data
    ]) #Close Tabs
])

@app.callback(
    Output('table-container', 'data'),
    [Input('filter_dropdown', 'value') ])
def display_table(line):
    dff = df[df.Line==line]
    return dff.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)