# Esta pagina permite experimentar con los distintos parametros del algoritmo, observando los resultado online
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
import plotly.graph_objects as go

from algoritmo import generar_terreno
import numpy as np
import pandas as pd


layout = html.Div([
    dbc.Row(
        dbc.Col(
                html.H1("Terrenos Interactivos")
           )
    ),
    dbc.Row(
        dbc.Col([
            html.H3("Altura Mínima del Terreno"),
            dcc.Slider(
                id='slider_altura_min',
                min=0,
                max=5,
                value=3,
                marks={i: f'{i}' for i in range(0,6)}
            )
        ])
    ),
    dbc.Row(
        dbc.Col([
            html.H3("Altura Máxima del Terreno"),
            dcc.Slider(
                id='slider_altura_max',
                min=5,
                max=10,
                value=7,
                marks={i: f'{i}' for i in range(5,11)}
            )
        ])
    ),
    dbc.Row(
        dbc.Col([
            html.H3("Variabilidad del Terreno"),
            dcc.Slider(
                id='slider_variabilidad',
                min=0,
                max=100,
                value=50,
                marks={i: f'{i/100}' for i in range(0,101,10)}
            )
        ])
    ),
    dbc.Row(
        dbc.Col([
            html.H3("Longitud del Lado 1"),
            dcc.Slider(
                id='slider_tamaño_x',
                min=1,
                max=25,
                value=5,
                marks={i: f'{i}' for i in range(1, 26, 2)}
            )
        ])
    ),
    dbc.Row(
        dbc.Col([
            html.H3("Longitud del Lado 2"),
            dcc.Slider(
                id='slider_tamaño_y',
                min=1,
                max=25,
                value=5,
                marks={i: f'{i}' for i in range(1, 26, 2)}
            )
        ])
    ),    
    dbc.Row(
        dbc.Col([
            dcc.Graph(id='graph_experimentacion')
        ])
    )]
)
# Define callback to update graph
@app.callback(
    Output('graph_experimentacion', 'figure'),
    [Input('slider_altura_min', 'value'),
     Input('slider_altura_max', 'value'),
     Input('slider_variabilidad', 'value'),
     Input('slider_tamaño_x', 'value'),
     Input('slider_tamaño_y', 'value')]
)

def update_figure(altura_min, altura_max, variabilidad, tamaño_x, tamaño_y):
    Z = generar_terreno(
            tamaño=(tamaño_x, tamaño_y),
            altura_min=altura_min,
            altura_max=altura_max,
            variabilidad=variabilidad/100,
            semilla=0
        )

    x = np.linspace(-tamaño_x/2, tamaño_x/2, tamaño_x)
    y = np.linspace(-tamaño_y/2, tamaño_y/2, tamaño_y)

    X,Y = np.meshgrid(x,y)
    
    fig = go.Figure(data=[go.Surface(z=Z, colorscale='Blues', reversescale=True)])
    return fig
