import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from app import app
from funciones import importar_tablas, main_genetico, formatear
import pandas as pd 
import numpy as np 
import plotly.graph_objs as go
import time

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    html.H4(children='RESOLUCIÓN FINAL CON ALG. GENÉTICOS',
                            className="text-center text-light bg-dark"),
                    body=True, color="dark")
                , className="mb-4")
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dcc.Checklist(
                    options=[
                        {'label': 'Elitismo', 'value': 'elitismo'}
                    ],
                    id='input_elitismo',
                    value=['elitismo'],
                    labelStyle={'font-size': 20},
                    inputStyle={'size': 10, 'margin': 10}
                ), width=3
            ),
            dbc.Col(
                dcc.Checklist(
                    options=[
                        {'label': 'Mantener trazos', 'value': 'trazos'}
                    ],
                    id='input_trazos',
                    value=['trazos'],
                    labelStyle={'font-size': 20},
                    inputStyle={'size': 10, 'margin': 10}
                ), width=3
            ),
            dbc.Col(
                dbc.Button("Ejecutar", id='ejecutar', color="primary", block=True)
            )
        ]),
        dbc.Row([
            dbc.Col([
                html.Hr(),
                dbc.Spinner([
                        dcc.Graph(id="mapa_genetico_ready")
                    ], size="lg", color="primary", type="grow", fullscreen=True, spinner_style={"width": "10rem", "height": "10rem"}),
            ])
        ]),
        html.Hr()
    ])
])

@app.callback(
    Output("mapa_genetico_ready", "figure"),
    Input('ejecutar', 'n_clicks')
)
def load_output(clicks):
    if clicks is None:
        return go.Figure()
    else:
        tabla_distancias, tabla_capitales = importar_tablas()
        mejor_cromosoma = [19, 15, 16, 1, 18, 6, 5, 14, 13, 21, 9, 3, 17, 20, 7, 23, 22, 12, 10, 4, 8, 11, 2, 19] 
        cap = formatear(tabla_capitales, mejor_cromosoma)

        # --------------------------- dibujado del mapa
        frames = []
        for k in range(len(cap)):
            frames.append(go.Frame(data=[
                go.Scattermapbox(
                    mode='markers+lines', 
                    lat=cap['latitud'][:k+1],  
                    lon=cap['longitud'][:k+1],
                    marker={'size': 8, 'color': 'red'},
                    line={'color': 'blue', 'width':2})
                ], name=f'frame{k}'))
     
        # dibujo la figura, y le asigno los cuadros
        fig = go.Figure(
            data=go.Scattermapbox(
                lat=cap['latitud'], 
                lon=cap['longitud'],
                text=cap['capital'],
                hoverinfo='text'
            ),
            layout=go.Layout(        
                title_text=f'Recorrido Mínimo: 12817 km    |   Tiempo Ejecución: 84.782 segundos', 
                hovermode="closest",
                font={'size': 18}
            ),
            frames=frames
        )

        updatemenus = [dict(
                buttons = [
                    dict(
                        args = [None, {"frame": {"duration": 1000, "redraw": True},
                                        "fromcurrent": True, 
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
                        borderwidth=2,
                        len=1) #slider length
                ]

        fig.update_layout(
            sliders = sliders,
            updatemenus = updatemenus,
            margin={"r":50,"t":50,"l":50,"b":50},
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