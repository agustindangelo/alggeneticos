import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

card_agu = [
    dbc.CardHeader(           
        "Agustín D'Angelo",
        className="card-title",
        style={'font-size': 20, 'font-weight': 'bold'}
    ),
    dbc.CardBody([
            html.P(
                "Legajo: 45822",
                className="card-text",
                style={'font-size': 20}
            ),
            html.P(
                "agustindangelo2113@gmail.co",
                className="card-text",
                style={'font-size': 20}
            ),
        ]
    ),
]
card_lu = [
    dbc.CardHeader(           
        "Lucía Fabbri",
        className="card-title",
        style={'font-size': 20, 'font-weight': 'bold'}
    ),
    dbc.CardBody([
            html.P(
                "Legajo: 45703",
                className="card-text",
                style={'font-size': 20}
            ),
            html.P(
                "fabbriluciam@gmail.com",
                className="card-text",
                style={'font-size': 20}
            ),
        ]
    ),
]
card_juli = [
    dbc.CardHeader(           
        "Julián Lostumbo",
        className="card-title",
        style={'font-size': 20, 'font-weight': 'bold'}
    ),
    dbc.CardBody([
            html.P(
                "Legajo: 46081",
                className="card-text",
                style={'font-size': '20px'}
            ),
            html.P(
                "julilostumbo.jl@gmail.com",
                className="card-text",
                style={'font-size': 20}
            ),
        ]
    ),
]
card_chucho = [
    dbc.CardHeader(           
        "Lucio Serenelli",
        className="card-title",
        style={'font-size': 20, 'font-weight': 'bold'}
    ),
    dbc.CardBody([
            html.P(
                "Legajo: 44749",
                className="card-text",
                style={'font-size': 20}
            ),
            html.P(
                "lucioserenelli26@gmail.com",
                className="card-text",
                style={'font-size': 20}
            ),
        ]
    ),
]


# html.H6("D'Angelo Agustín - Leg. 45822 - agustindangelo2113@gmail.com"),
# html.H6("Fabbri Lucía - Leg. 45703 - fabbriluciam@gmail.com"),
# html.H6("Lostumbo Julián - Leg. 46081 - julilostumbo.jl@gmail.com"),
# html.H6("Serenelli Lucio - Leg. 44749 - lucioserenelli26@gmail.com"),

cards = dbc.Container([
    dbc.Row([
        dbc.Col([
                dbc.Col(dbc.Card(card_agu, color="light", style={'width': '400', 'margin': '0px'})),
            ],
            width=3
        ),
        dbc.Col([
                dbc.Col(dbc.Card(card_lu, color="light", style={'width': '400', 'margin': '0px'})),
            ],
            width=3
        ),
        dbc.Col([
                dbc.Col(dbc.Card(card_juli, color="light", style={'width': '400', 'margin': '0px'})),
            ],
            width=3
        ),
        dbc.Col([
                dbc.Col(dbc.Card(card_chucho, color="light", style={'width': '400', 'margin': '0px'})),
            ],
            width=3
        )
    ])
],fluid=True)

descripcion = "En este trabajo, resolvemos el problema del viajante argentino. Implementamos distintas enfoques de resolver el problema: búsqueda exhaustiva, búsqueda heurística y algoritmos genéticos. En base a los resultados, analizamos las ventajas y desventajas de cada perspectiva para la solución de este reconocido problema."

layout = html.Div([
    dbc.Container([

        dbc.Row([
            dbc.Col(
                # dbc.Card([
                #     dbc.CardHeader("Descripcion", className='card-title', style={'font-size': 25}),
                #     dbc.CardBody(
                #         html.P(descripcion, style={'font-size': '20px'})
                #     )
                # ])
                dbc.Jumbotron([
                    html.H3('Problema del viajante argentino', className='display-4'),
                    html.H3('Algoritmos Genéticos, Ciclo Lectivo 2020', className='display-5'),
                    html.Hr(),
                    html.P(descripcion, style={'font-size': '20px'})
                    
                ])
            )
        ])
    ], fluid=True),
    cards,
])