# Esta pagina es para modelar el derretimiento de glaciares
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
                    html.H4(children='Modelado del Desplazamiento del Glaciar',
                            className="text-center text-light bg-dark"),
                    body=True, color="dark")
                , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Semilla"),
                    dbc.Input(type="number", value=0, id="input_semilla"),
                ],
                id="styled-numeric-input",
                ),
                width=3
            ),
            dbc.Col([
                html.H4("Tiempo"),
                dcc.Slider(
                    id='slider_tiempo',
                    min=1,
                    max=25,
                    value=1,
                    step=1
                )
            ], width=6
            )
        ]),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='graph_retrocesos'),
                width={'size': 10, 'offset': 1}
            )
        )
    ])
])
# Define callback to update graph
@app.callback(
    Output('graph_retrocesos', 'figure'),
    [Input('slider_tiempo', 'value'),
     Input('input_semilla', 'value')]
)

def update_figure(tiempo, semilla):    
    variabilidad_default = 0.6 
    longitud = 50
    Z = generar_terreno(
            tamaño=(longitud, longitud),
            altura_min=0,
            altura_max=5,
            variabilidad=variabilidad_default,
            semilla=semilla
        )
    fila_de_ceros = np.full(longitud, 0)
    fila_de_valor_limite = np.full(longitud, longitud-1)
    fila_lineal = np.linspace(0, longitud-1, longitud)

    z_minimo = np.min(Z)
    z_maximo= np.max(Z)


    superficies = [go.Surface(z=Z[:, :-tiempo], colorscale='blues', reversescale=True, showscale=False)] 
    
#   ---------- Pared 1:
    x = np.array([fila_de_ceros, fila_de_ceros])
    y = np.array([fila_lineal, fila_lineal])
    z = np.array([fila_de_ceros, Z[:,0]])
    
    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ---------- Pared 2:
    x = np.array([fila_lineal[:-tiempo], fila_lineal[:-tiempo]])
    y = np.array([fila_de_ceros[:-tiempo], fila_de_ceros[:-tiempo]])
    z = np.array([fila_de_ceros[:-tiempo], Z[0,:][:-tiempo]])  

    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ---------- Pared 3:
    x = np.array([fila_lineal[:-tiempo], fila_lineal[:-tiempo]])
    y = np.array([fila_de_valor_limite[:-tiempo], fila_de_valor_limite[:-tiempo]])
    z = np.array([fila_de_ceros[:-tiempo], Z[longitud-1,:][:-tiempo]])   

    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ---------- Pared 4:
    x = np.array([fila_de_valor_limite - tiempo, fila_de_valor_limite - tiempo])
    y = np.array([fila_lineal, fila_lineal])
    z = np.array([fila_de_ceros, Z[:, -tiempo-1]]) 

    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))

    fig = go.Figure(data = superficies)

    fig.update_layout(
        scene = dict(
            xaxis = dict(ticks='', visible=False, range=[0,longitud]),
            yaxis = dict(ticks='',visible=False),
            zaxis = dict(ticks='',visible=False),
        ),
        scene_camera = dict(
            eye=dict(x=1.2, y=0.1, z=1)
        ),
        width=1000,
        height=700,
        margin=dict(t=50, r=100, l=100, b=0)
    )

    return fig
