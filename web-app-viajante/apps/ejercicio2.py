import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from app import app
from funciones import importar_tablas, heuristicoA, formatear
import pandas as pd 
import numpy as np 
import plotly.graph_objs as go


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    html.H4(children='MÉTODO HEURÍSTICO CON INGRESO DE CIUDAD',
                            className="text-center text-light bg-dark"),
                    body=True, color="dark")
                , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    options=[
                        {'label': 'Cdad de Bs. As.', 'value': 0},
                        {'label': 'Córdoba', 'value': 1},
                        {'label': 'Corrientes', 'value': 2},
                        {'label': 'Formosa', 'value': 3},
                        {'label': 'La Plata', 'value': 4},
                        {'label': 'La Rioja', 'value': 5},
                        {'label': 'Mendoza', 'value': 6},
                        {'label': 'Neuquén', 'value': 7},
                        {'label': 'Paraná', 'value': 8},
                        {'label': 'Posadas', 'value': 9},
                        {'label': 'Rawson', 'value': 10},
                        {'label': 'Resistencia', 'value': 11},
                        {'label': 'Río Gallegos', 'value': 12},
                        {'label': 'S.F.d.V.d. Catamarca', 'value': 13},
                        {'label': 'S.M. de Tucumán', 'value': 14},
                        {'label': 'S.S. de Jujuy', 'value': 15},
                        {'label': 'Salta', 'value': 16},
                        {'label': 'San Juan', 'value': 17},
                        {'label': 'San Luis', 'value': 18},
                        {'label': 'Santa Fe', 'value': 19},
                        {'label': 'Santa Rosa', 'value': 20},
                        {'label': 'Sgo. Del Estero', 'value': 21},
                        {'label': 'Ushuaia', 'value': 22},
                        {'label': 'Viedma', 'value': 23}
                    ],
                    value=0,
                    id='input_capital'
                ), 
            )
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='mapa_heuristicoA')
            ])
        ]),
        html.Hr()
    ])
])

# Define callback to update graph
@app.callback(
    Output('mapa_heuristicoA', 'figure'),
    Input('input_capital', 'value')
)

def update_figure(input_capital):

    tabla_distancias, tabla_capitales = importar_tablas()
    recorrido, distancia_recorrida, tiempo_ejecucion = heuristicoA(tabla_distancias, input_capital)
    cap = formatear(tabla_capitales, recorrido)

    # --------------------------- dibujado del mapa
    mantener_trazo = False
    frames = []
    if mantener_trazo:
        for k in range(len(cap)):
            frames.append(go.Frame(data=[go.Scattermapbox(mode='lines', lat=cap['latitud'][:k+1],  lon=cap['longitud'][:k+1])], name=f'frame{k}'))
    else:
        for k in range(len(cap)-1):
            frames.append(go.Frame(data=[go.Scattermapbox(mode='lines', lat=[cap.iloc[k]['latitud'], cap.iloc[k+1]['latitud']],  lon=[cap.iloc[k]['longitud'], cap.iloc[k+1]['longitud']])], name=f'frame{k}'))
    # dibujo la figura, y le asigno los cuadros
    fig = go.Figure(
        data=go.Scattermapbox(
            lat=cap['latitud'], 
            lon=cap['longitud'],
            text=cap['capital'],
            hoverinfo='text'
        ),
        layout=go.Layout(        
            title_text=f'Distancia Recorrida: {distancia_recorrida:8.0f} km  |   Tiempo Ejecución: {tiempo_ejecucion:5.5f} s', 
            hovermode="closest",
            font={'size': 18}

        ),
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
                                label=f'{cap.iloc[k]["capital"]}'
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
        margin={"r":0,"t":50,"l":0,"b":50},
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

