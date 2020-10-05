# Esta pagina permite experimentar con los distintos parametros del algoritmo, observando los resultado online
import dash
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
    
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    html.H4(children='PARÁMETROS DEL ALGORITMO',
                            className="text-center text-light bg-dark"),
                    body=True, color="dark")
                , className="mb-4"
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Semilla"),
                    dbc.Input(type="number", value=1, id="input_semilla"),
                ],
                id="styled-numeric-input",
                ),
                width=3
            ),
            dbc.Col(
                html.Div([
                    html.H5("Longitud del lado"),
                    dbc.Input(placeholder="Longitud", type="number", min=10, max=100, value=100, id="input_longitud"),
                ],
                id="styled-numeric-input",
                ),
                width=3
            ),
            dbc.Col([
                html.H5("Altura máxima"),
                dcc.Slider(
                    id='slider_altura_max',
                    min=5,
                    max=10,
                    value=10,
                    marks={i: f'{i}' for i in range(5,11)}
                )],
                width=6
            ),
        ]),
        dbc.Row([
            dbc.Col([
                html.H5("Variabilidad del Terreno"),
                dcc.Slider(
                    id='slider_variabilidad',
                    min=0,
                    max=100,
                    value=50,
                    marks={i: f'{i/100}' for i in range(0,101,10)}
                )],
                width=6    
            ),
            dbc.Col([
                html.H5("Altura mínima"),
                dcc.Slider(
                    id='slider_altura_min',
                    min=0,
                    max=5,
                    value=0,
                    marks={i: f'{i}' for i in range(0,6)}
                )],
                width=6
            )
        ]),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='graph_experimentacion'),
                width={'size': 10, 'offset':1}
            )
        )
    ])  
])
# Define callback to update graph
@app.callback(
    Output('graph_experimentacion', 'figure'),
    [Input('input_semilla', 'value'),
     Input('input_longitud', 'value'),
     Input('slider_variabilidad', 'value'),
     Input('slider_altura_min', 'value'),
     Input('slider_altura_max', 'value')]
)

def update_figure(semilla, longitud, variabilidad, altura_min, altura_max):
    Z = generar_terreno(
            tamaño=(longitud, longitud),
            altura_min=altura_min,
            altura_max=altura_max,
            variabilidad=variabilidad/100,
            semilla=semilla
        )

    z_minimo = np.min(Z)
    z_maximo= np.max(Z)

    fila_de_ceros = np.full(longitud, 0)
    fila_z_minimo = np.full(longitud, z_minimo)
    fila_de_valor_limite = np.full(longitud, longitud-1)
    fila_lineal = np.linspace(0, longitud-1, longitud)

    superficies = [go.Surface(z=Z, colorscale='blues', reversescale=True, showscale=False)] 
    
#   ---------- Pared 1:
    x = np.array([fila_de_ceros, fila_de_ceros])
    y = np.array([fila_lineal, fila_lineal])
    z = np.array([fila_de_ceros, Z[:,0]])
    
    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ---------- Pared 2:
    x = np.array([fila_lineal, fila_lineal])
    y = np.array([fila_de_ceros, fila_de_ceros])
    z = np.array([fila_de_ceros, Z[0,:]])   

    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ---------- Pared 3:
    x = np.array([fila_lineal, fila_lineal])
    y = np.array([fila_de_valor_limite, fila_de_valor_limite])
    z = np.array([fila_de_ceros, Z[longitud-1,:]])   

    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ---------- Pared 4:
    x = np.array([fila_de_valor_limite, fila_de_valor_limite])
    y = np.array([fila_lineal, fila_lineal])
    z = np.array([fila_de_ceros, Z[:, longitud-1]]) 

    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ----------- Piso:
    x, y = np.meshgrid(fila_lineal, fila_lineal)
    z = np.full((longitud, longitud), 0)
    
    superficies.append(go.Surface(x = x, y = y, z = z, colorscale='blues', showscale=False))
    
    fig = go.Figure(data = superficies)

    fig.update_layout(
        width=1000,
        height=700,
        margin=dict(t=0, r=100, l=100, b=0)
    )

    return fig
