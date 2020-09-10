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
                    html.H4(children='Modelado de Glaciares Mediante el Alg. del Diamante Cuadrado',
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
            dbc.Col(
                html.Div([
                    html.H5("Longitud del lado"),
                    dbc.Input(placeholder="Longitud", type="number", min=10, max=100, value=25, id="input_longitud"),
                ],
                id="styled-numeric-input",
                ),
                width=3
            ),
            
            dbc.Col([
                html.H4("Año"),
                dcc.Slider(
                    id='slider_anio',
                    min=1950,
                    max=2090,
                    value=2020,
                    step=None,
                    marks={i: f'{i}' for i in range(1950, 2091, 10)}
                )
            ], width=6
            )
        ]),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='graph_glaciares'),
                width={'size': 10, 'offset': 1}
            )
        )
    ])
])
# Define callback to update graph
@app.callback(
    Output('graph_glaciares', 'figure'),
    [Input('slider_anio', 'value'),
     Input('input_semilla', 'value'),
     Input('input_longitud', 'value')]
)

def update_figure(anio, semilla, longitud):
    factor_var=0.0869 #cambio de variabilidad x cambio de °C
    factor_altura=9.13 #cambio de altura x cambio de °C
    temp_default=7 #en °C para el año 2020
    altura_min_defaut=53 #en metros para el año 2020
    altura_max_default=60 #en metros para el año 2020
    variabilidad_default=0.6 #para el año 2020

    temps = {
        1950: 4.9,
        1960: 5,
        1970: 6.05,
        1980: 6.2,
        1990: 6.32,
        2000: 6.6,
        2010: 6.75,
        2020: 7,
        2030: 7.5,
        2040: 8,
        2050: 9,
        2060: 10,
        2070: 10.5,
        2080: 11.6,
        2090: 12.8
    }

    temp = temps[anio]
    #asignacion de parametros para configurar la figura    
    altura_min=altura_min_defaut + factor_altura*(temp_default-temp)
    altura_max=altura_max_default + factor_altura*(temp_default-temp)
    variabilidad=variabilidad_default + factor_var*(temp_default-temp)
    temp=f'{temp}°C'

    Z = generar_terreno(
            tamaño=(longitud, longitud),
            altura_min=altura_min,
            altura_max=altura_max,
            variabilidad=variabilidad,
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
    z = np.array([fila_z_minimo, Z[:,0]])
    
    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ---------- Pared 2:
    x = np.array([fila_lineal, fila_lineal])
    y = np.array([fila_de_ceros, fila_de_ceros])
    z = np.array([fila_z_minimo, Z[0,:]])   

    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ---------- Pared 3:
    x = np.array([fila_lineal, fila_lineal])
    y = np.array([fila_de_valor_limite, fila_de_valor_limite])
    z = np.array([fila_z_minimo, Z[longitud-1,:]])   

    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ---------- Pared 4:
    x = np.array([fila_de_valor_limite, fila_de_valor_limite])
    y = np.array([fila_lineal, fila_lineal])
    z = np.array([fila_z_minimo, Z[:, longitud-1]]) 

    superficies.append(go.Surface(x = x, y = y, z = z, colorscale=[[0,'rgb(192,229,232)'],[1,'rgb(66,146,198)']],cmin=z_minimo, cmax=z_maximo, reversescale=True, showscale=False))
#   ----------- Piso:
    x, y = np.meshgrid(fila_lineal, fila_lineal)
    z = np.full((longitud, longitud), z_minimo)
    
    superficies.append(go.Surface(x = x, y = y, z = z, colorscale='blues', showscale=False))

    fig = go.Figure(data = superficies)

    fig.update_layout(
                    title=f'Año {anio}, temperatura promedio: {temp}',
                    titlefont={'size':30},
                    scene = dict(
                        xaxis = dict(ticks='',visible=False),
                        yaxis = dict(ticks='',visible=False),
                        zaxis = dict(ticks='',visible=False),
                    ),
                    width=1000,
                    height=700,
                    margin=dict(t=50, r=100, l=100, b=0)
                )

    return fig
