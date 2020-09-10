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
    dbc.Row([
        dbc.Col(
            dbc.Card(
                html.H4(children='Modelado de Glaciares Mediante el Alg. del Diamante Cuadrado',
                        className="text-center text-light bg-dark"),
                body=True, color="dark")
            , className="mb-4")
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Semilla para el generador"),
                    dbc.Input(placeholder="Semilla...", type="number", value=0, id="input_semilla"),
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
    if (anio==1950):
        altura_min=9
        altura_max=10
        variabilidad=0.7
        temp="4.9°C"
    elif (anio==1960):
        altura_min=8.8696
        altura_max=9.8696
        variabilidad=0.6913
        temp="5°C"
    elif (anio==1970):
        altura_min=8.8044
        altura_max=9.8044
        variabilidad=0.6869
        temp="6.05°C"
    elif (anio==1980):
        altura_min=8.6088
        altura_max=9.6088
        variabilidad=0.6739
        temp="6.2°C"
    elif (anio==1990):
        altura_min=8.45232
        altura_max=9.45232
        variabilidad=0.6635
        temp="6.32°C"
    elif (anio==2000):
        altura_min=8.0872
        altura_max=9.0872
        variabilidad=0.6391
        temp="6.6°C"
    elif (anio==2010):
        altura_min=7.8916
        altura_max=8.8916
        variabilidad=0.6261
        temp="6.75°C"
    elif (anio==2020):
        altura_min=7.5656
        altura_max=8.5656
        variabilidad=0.6
        temp="7°C"
    elif (anio==2030):
        altura_min=6.9136
        altura_max=7.9136
        variabilidad=0.5609
        temp="7.5°C"
    elif (anio==2040):
        altura_min=6.2616
        altura_max=7.2616
        variabilidad=0.5175
        temp="8°C"
    elif (anio==2050):
        altura_min=4.9576
        altura_max=5.9576
        variabilidad=0.4306
        temp="9°C"
    elif (anio==2060):
        altura_min=3.6536
        altura_max=4.6536
        variabilidad=0.3437
        temp="10°C"
    elif (anio==2070):
        altura_min=3.0016
        altura_max=4.0016
        variabilidad=0.3
        temp="10.5°C"
    elif (anio==2080):
        altura_min=1.5672
        altura_max=2.5672
        variabilidad=0.2047
        temp="11.6°C"
    else:
        altura_min=0
        altura_max=1
        variabilidad=0.1
        temp="12.8°C"

    #para mostrar medidas de altura mas realistas (en metros)
    altura_min=altura_min*7 
    altura_max=altura_max*7

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

    fig.update_layout(scene = dict(
                        xaxis = dict(ticks='',visible=False),
                        yaxis = dict(ticks='',visible=False),
                        zaxis = dict(ticks='',visible=False),
                    ),
                    width=1000,
                    height=700,
                    margin=dict(t=0, r=100, l=100, b=0)
                )

    return fig
