import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from app import app
from bitarray import bitarray
import pandas as pd 
import numpy as np 
import plotly.graph_objs as go


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    html.H4(children='MÉTODO EXHAUSTIVO',
                            className="text-center text-light bg-dark"),
                    body=True, color="dark")
                , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Cantidad de provincias"),
                    dbc.Input(type="number", value=4, id="input_cantidad"),
                ],
                id="styled-numeric-input",
                ),
                width=3
            ),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='graph')
            ])
        ])
    ])
])

# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    Input('input_cantidad', 'value')
)

def update_figure(input_cantidad):
    def permutacion_binaria(n, m):
    # función recursiva que genera permutaciones en cadenas binarias de longitud n, con m cantidad de unos
    # Detalle de implementacion en python: la palabra clave yield es el análogo de return, pero retorna un objeto generador
        if m < n:                                                  
            if m > 0:
                for x in permutacion_binaria(n-1,m-1):
                    yield bitarray([1]) + x
                for x in permutacion_binaria(n-1,m):
                    yield bitarray([0]) + x
            else:
                yield n * bitarray('0') 
        else:
            yield n * bitarray('1')

    def generar_combinaciones(n):
    
        # función que genera todas las cadenas binarias posibles de longitud n,
        # el valor de n debe indicarse como parámetro de la función.
        n = int(n)
        cadenas = []
        for i in range(n):
            for cadena in permutacion_binaria(n,i):
                cadenas.append((cadena))
    
        for index, cadena in enumerate(cadenas):
            cadenas[index] = [int(xi) for xi in cadena.tolist()]   # convertimos el arreglo de bits en una lista de python
        for index, cadena in enumerate(cadenas):
            cadenas[index] = ''.join([str(xi) for xi in cadena])   # convertimos la lista de python en un string
    
        cadenas.append('1' * n)
        #se devuelve una lista con las combinaciones posibles de '1's y '0's donde cada bit representa un elemento y si ese elemento se encuentra en la combinacion o no   
        return cadenas

    cap = pd.read_csv('apps/assets/capitales.csv')
    mantener_trazo = False
    frames = []
    if mantener_trazo:
        for k in range(len(cap)):
            frames.append(go.Frame(data=[go.Scattermapbox(mode='lines', lat=cap['latitud'][:k+1],  lon=cap['longitud'][:k+1])], name=f'frame{k}'))
    else:
        for k in range(len(cap)-1):
            frames.append(go.Frame(data=[go.Scattermapbox(mode='lines', lat=[cap['latitud'][k], cap['latitud'][k+1]],  lon=[cap['longitud'][k], cap['longitud'][k+1]])], name=f'frame{k}'))
    # dibujo la figura, y le asigno los cuadros
    fig = go.Figure(
        data=go.Scattermapbox(
            lat=cap['latitud'], 
            lon=cap['longitud'],
            text=cap['capital'],
            hoverinfo='text'
        ),
        layout=go.Layout(),
        frames=frames
    )


    updatemenus = [dict(
            buttons = [
                dict(
                    args = [None, {"frame": {"duration": 1000, "redraw": True},
                                    "fromcurrent": False, 
                                    "transition": {"duration": 500, 'easing': 'cubic-in-out'}
                                }],
                    label = "Recorrer",
                    method = "animate"
                    ),
                dict(
                    args = [[None], {"frame": {"duration": 0, "redraw": True},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    label = "Pausar",
                    method = "animate"
                    )
            ],
            direction = "left",
            pad = {"r": 10, "t": 87},
            showactive = False,
            type = "buttons",
            x = 0.14,
            xanchor = "right",
            y = 0.16,
            yanchor = "top"
        )]  

    sliders = [dict(steps = [dict(method= 'animate',
                                args= [[f'frame{k}'],                           
                                dict(mode= 'immediate',
                                    frame=dict(duration=400, redraw=True),
                                    transition=dict(duration= 0))
                                    ],
                                label=f'{cap["capital"][k]}'
                                ) for k in range(len(cap))], 
                    active=0,
                    transition={'duration':500 , 'easing': 'cubic-in-out'},
                    x=0, # slider starting position  
                    y=0, 
                    currentvalue=dict(
                        font=dict(size=25), 
                        visible=True, 
                        xanchor= 'center'
                    ),  
                    len=1) #slider length
            ]

    fig.update_layout(
        sliders = sliders,
        updatemenus = updatemenus,
        margin={"r":0,"t":50,"l":0,"b":0},
        mapbox_style="open-street-map",
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            center=dict(
                lat=-35.876958,
                lon=-65.293389
            ),
            zoom=3
        ),
        height=600
    )
    return fig

