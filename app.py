import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np 
import dash_bootstrap_components as dbc # import the library
import dash_table
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from textwrap import dedent as d
import json

import pandas as pd

df_url = 'https://datos.alcobendas.org/dataset/9cc894a1-8cfb-4dfe-a29f-fb197aa03ae0/resource/eff1bb9c-110e-4962-8370-d78589f987c2/download/uso-de-autobuses.csv'
df = round(pd.read_csv(df_url),2)
df.rename(columns={'Línea':'Line', 'Año':'Year', 'Tipo de transporte':'Type'}, inplace=True)


dfm=pd.melt(df, id_vars =['Line','Year','Type'], value_vars =['Número anual de pasajeros','Expediciones por día laborable','Viajeros por día','Viajeros por expedición','Kilómetros anuales realizados'])

years = df.Year.unique().tolist()
line = df.Line.unique().tolist()
Bustype = df.Type.unique().tolist()
variables = dfm['variable'].unique()
bins = [0]

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

* Relations between variables: 

In this panel we can observe a plot that is called correlation plot, this is used to understand the behavior between then. For example, if we see a cloud of points that draw a diagonal that increase
from the down left side to the up rigth side the relation is positive. On the other hand, if that point cloud draws  a diagonal that decrease from the up left corner to  the down rigth corner we can say
that those two variable have a negative relation. Otherwise, we can say that the variables have not relation. 

* Differences between two types:

In the final tab we can see a box plot that let us to understand some differences between the two types of autobuses in the public transport of Alcobendas (Interurban and Urban)


'''

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='About', children=[
            dcc.Markdown(markdown_text)]),
        dcc.Tab(label='Data', children=[" In this tab you can see the data. You can filter the information selecting the line that you want to observe:",
            dcc.Dropdown(
                id='filter_dropdown',
                options=[{'label':st, 'value':st} for st in line],
                value = line[0]
            ),
            dash_table.DataTable(id='table-container', columns=[{'id': c, 'name': c} for c in df.columns.values]) ]),#Close tab=Data
        dcc.Tab(label='Distribution of variables', children=[" In this tab you can see a Histogram that let you to understand the distribution of variable that you will select in the next dropdown",
            dcc.Dropdown(
                id='crossfilter-yaxis-columnH',
                options=[{'label': i, 'value': i} for i in variables],
                value='Número anual de pasajeros'
            ),
            dcc.Graph(
                id='Histogram'    
            ),
            dcc.Slider(
                id='crossfilter-year--slider1',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].max(),
                marks={str(years): str(years) for years in df['Year'].unique()},
                step=None
            ),
            #dcc.Slider(
            #    id='crossfilter-bin-slider',
            #    min=0,
            #    max=20,
            #    value=10,
            #    marks={i: '{}'.format(i) for i in range(21)},
            #    step=1
            #) 
        ]),
        dcc.Tab(label='Relations between variables', children=[
            dcc.Markdown("""
                **Relations between variables**

                In this tab you can select two variables to observe their relation. Also, you can choose if you want to plot it in a linear
                way or using log. 

                Then, you will find different ways to know the informacion about the point, the first option is pass the mouse over the point, the second
                one is click de point, and the final option is select points using the rectangule tool, if you decide to use this option a table will be shown with all the information about your selection
            """),
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in variables],
                value='Número anual de pasajeros'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in variables],
                value='Kilómetros anuales realizados'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'line': '1'}]}
            ),
            dcc.Slider(
                id='crossfilter-year--slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].max(),
                marks={str(years): str(years) for years in df['Year'].unique()},
                step=None
            ),
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
             html.Pre(id='hover-data'),
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
             html.Pre(id='click-data'),
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.
            """),
             dash_table.DataTable(
                id='my-table',
                columns=[{"name": i, "id": i} for i in df.columns]
            )
        ]),
        dcc.Tab(label='Differences between two types', children=["In this panel you can observe the differences between the selected variables",
            dcc.Dropdown(
                id='crossfilter-yaxis-column_box',
                options=[{'label': i, 'value': i} for i in variables],
                value='Número anual de pasajeros'
            ),
            dcc.Graph(
                id='boxplot',
            ),
            dcc.Slider(
                id='crossfilter-year--sliderbox',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].max(),
                marks={str(years): str(years) for years in df['Year'].unique()},
                step=None
            ),
        ])
    ]) #Close Tabs
])

@app.callback(
    Output('table-container', 'data'),
    [Input('filter_dropdown', 'value') ])
def display_table(line):
    dff = df[df.Line==line]
    return dff.to_dict('records')

@app.callback(
    dash.dependencies.Output('Histogram', 'figure'),
    [dash.dependencies.Input('crossfilter-yaxis-columnH','value'),
     dash.dependencies.Input('crossfilter-year--slider1', 'value')])
def update_hist(yaxis_column_name,year_value):
    df1 = dfm[dfm['Year'] == year_value]
    return {
        'data': [
            go.Histogram(
            x=df1[df1['variable'] == yaxis_column_name]['value'],
            text=df1[df1['variable'] == yaxis_column_name]['Line'],
            customdata=df1[df1['variable'] == yaxis_column_name]['Line'],
            histnorm='probability',
            nbinsx=10
        )],
        'layout': {}
    }   

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    df1 = dfm[dfm['Year'] == year_value]
    return {
        'data': [dict(
            x=df1[df1['variable'] == xaxis_column_name]['value'],
            y=df1[df1['variable'] == yaxis_column_name]['value'],
            text=df1[df1['variable'] == yaxis_column_name]['Line'],
            customdata=df1[df1['variable'] == yaxis_column_name]['Line'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }

@app.callback(
    Output('hover-data', 'children'),
    [Input('crossfilter-indicator-scatter', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    [Input('crossfilter-indicator-scatter', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

@app.callback(
    Output('my-table', 'data'),
    [Input('crossfilter-indicator-scatter', 'selectedData')])
def display_selected_data(selected_data):
    if selected_data is None or len(selected_data) == 0:
        return []
    points = selected_data['points']
    if len(points) == 0:
        return []
    names = [x['text'] for x in points]
    return df[df['Line'].isin(names)].to_dict("rows")

@app.callback(
    dash.dependencies.Output('boxplot', 'figure'),
    [dash.dependencies.Input('crossfilter-yaxis-column_box','value'),
     dash.dependencies.Input('crossfilter-year--sliderbox', 'value')])
def update_box(yaxis_column_name,year_value):
    df1 = dfm[dfm['Year'] == year_value]
    return {
        'data': [
            go.Box(
            y=df1[df1['variable'] == yaxis_column_name]['value'],
            x=df1.Type
            #customdata=df1[df1['variable'] == yaxis_column_name]['Line'],
            )],
        'layout': {}
    }   


if __name__ == '__main__':
    app.run_server(debug=True)