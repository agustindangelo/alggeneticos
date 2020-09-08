import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([
         dbc.Row([
            dbc.Col(html.H1(children='ALGORITMOS GENÉTICOS: Problema del Viajante Argentino'), className="mb-2", align="center")
        ]),
    
        dbc.Row([
            dbc.Col(html.H6(children='Problema del Viajante Argentino'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children="Integrantes:  . . . . .. ."), className="mb-4")
        ]),


        dbc.Row([
            dbc.Col(
                dbc.Card(
                    children=[
                        html.H3(children='Ej. 1: Método exhaustivo', className="text-center"),                               
                        dbc.Row(html.P("El ejercicio consiste en tatata..")),
                    ],
                    body=True, outline=True
                )
                , width=3, className="mb-3"
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        html.H3(children='Ej. 2: Método ...', className="text-center"),                               
                        dbc.Row(html.P("El ejercicio consiste en tatata.."))
                    ],
                    body=True, outline=True
                )
                , width=3, className="mb-3"
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        html.H3(children='Ej. 3: Método ....', className="text-center"),                               
                        dbc.Row(html.P("El ejercicio consiste en tatata..")),
                    ],
                    body=True, outline=True
                )
                , width=3, className="mb-3"
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        html.H3(children='Ej. 4: Resolución mediante alg. geneticos', className="text-center"),                               
                        dbc.Row(html.P("El ejercicio consiste en tatata..")),
                    ],
                    body=True, outline=True
                )
                , width=3, className="mb-3"
            ),
        ], className="mb-5"),

    ])
])
