# Esta pagina es para modelar el derretimiento de glaciares
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
                html.H1("MODELADO DEL DERRETIMIENTO DE GLACIARES")
           )
    ),
    dbc.Row(
        dbc.Col([
            html.H3("Año: "),
            dcc.Slider(
                id='slider_anio',
                min=1950,
                max=2090,
                value=2020,
                step=None,
                marks={i: f'{i}' for i in range(1950, 2091, 10)}
            )
        ])
    ),
    dbc.Row(
        dbc.Col([
            html.H3("Glaciar resultante: "),
            dcc.Graph(id='graph_glaciares')
        ])
    )
]
)
# Define callback to update graph
@app.callback(
    Output('graph_glaciares', 'figure'),
    Input('slider_anio', 'value')
)

def update_figure(anio):
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
    longitud = 40

    Z = generar_terreno(
            tamaño=(longitud, longitud),
            altura_min=altura_min,
            altura_max=altura_max,
            variabilidad=variabilidad,
            semilla=0
        )
    
    superficies = [go.Surface(z=Z)] 
    fila_base = np.full(longitud, altura_min)
    fila_de_valor_limite = np.full(longitud, longitud-1)
    fila_lineal = np.linspace(altura_min, longitud-1, longitud)

#   ---------- Pared 1:
    x = np.array([fila_base, fila_base])
    y = np.array([fila_lineal, fila_lineal])
    z = np.array([fila_base, Z[:,0]])
    
    superficies.append(go.Surface(x=x, y=y, z=z, opacity = 0.9))
#   ---------- Pared 2:
    x = np.array([fila_lineal, fila_lineal])
    y = np.array([fila_base, fila_base])
    z = np.array([fila_base, Z[0,:]])   

    superficies.append(go.Surface(x=x, y=y, z=z, opacity = 0.9))
#   ---------- Pared 3:
    x = np.array([fila_lineal, fila_lineal])
    y = np.array([fila_de_valor_limite, fila_de_valor_limite])
    z = np.array([fila_base, Z[longitud-1,:]])   

    superficies.append(go.Surface(x=x, y=y, z=z, opacity = 0.9))
#   ---------- Pared 4:
    x = np.array([fila_de_valor_limite, fila_de_valor_limite])
    y = np.array([fila_lineal, fila_lineal])
    z = np.array([fila_base, Z[:, longitud-1]]) 

    superficies.append(go.Surface(x=x, y=y, z=z, opacity = 0.9))
#   ----------- Piso:
    x, y = np.meshgrid(fila_lineal, fila_lineal)
    z = np.full((longitud, longitud), altura_min)
    superficies.append(go.Surface(x=x, y=y, z=z, opacity = 0.9))

    fig = go.Figure(data = superficies)
    return fig
