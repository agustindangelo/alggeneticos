import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

card_agu = [
    dbc.CardHeader(           
        "Agustín D'Angelo",
        className="card-title",
        style={'font-size': 20}
    ),
    dbc.CardBody([
            html.P(
                "Legajo: 45822",
                className="card-text",
            ),
            html.P(
                "adangelo@frro.utn.edu.ar",
                className="card-text",
            ),
        ]
    ),
]
card_lu = [
    dbc.CardHeader(           
        "Lucía Fabbri",
        className="card-title",
        style={'font-size': 20}
    ),
    dbc.CardBody([
            html.P(
                "Legajo: 45703",
                className="card-text",
            ),
            html.P(
                "fabbriluciam@gmail.com",
                className="card-text",
            ),
        ]
    ),
]
card_juli = [
    dbc.CardHeader(           
        "Julián Lostumbo",
        className="card-title",
        style={'font-size': 20}
    ),
    dbc.CardBody([
            html.P(
                "Legajo: 46081",
                className="card-text",
            ),
            html.P(
                "julilostumbo.jl@gmail.com",
                className="card-text",
            ),
        ]
    ),
]
card_chucho = [
    dbc.CardHeader(           
        "Lucio Serenelli",
        className="card-title",
        style={'font-size': 20}
    ),
    dbc.CardBody([
            html.P(
                "Legajo: 44749",
                className="card-text",
            ),
            html.P(
                "lucioserenelli26@gmail.com",
                className="card-text",
            ),
        ]
    ),
]


# html.H6("D'Angelo Agustín - Leg. 45822 - agustindangelo2113@gmail.com"),
# html.H6("Fabbri Lucía - Leg. 45703 - fabbriluciam@gmail.com"),
# html.H6("Lostumbo Julián - Leg. 46081 - julilostumbo.jl@gmail.com"),
# html.H6("Serenelli Lucio - Leg. 44749 - lucioserenelli26@gmail.com"),

cards = html.Div([
    dbc.Row([
        dbc.Col([
                dbc.Col(dbc.Card(card_agu, color="light")),
            ],
            width=3
        ),
        dbc.Col([
                dbc.Col(dbc.Card(card_lu, color="light")),
            ],
            width=3
        ),
        dbc.Col([
                dbc.Col(dbc.Card(card_juli, color="light")),
            ],
            width=3
        ),
        dbc.Col([
                dbc.Col(dbc.Card(card_chucho, color="light")),
            ],
            width=3
        )
    ])
])

descripcion = "En este trabajo, implementamos el algoritmo del diamante cuadrado para la generación de terrenos. El algoritmo puede implementarse tomando un enfoque recursivo, sin embargo, nosotros llevamos a cabo su análogo procedural por ser más simple de leer e interpretar. Mediante el algoritmo, logramos modelar terrenos autosimilares de glaciares y presentamos de forma interactiva los efectos del calentamiento global sobre la dinámica del glaciar Perito Moreno en la Patagonia Argentina."

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    html.H4('ALGORITMOS GENÉTICOS - CICLO LECTIVO 2020', className="text-center text-light bg-dark"),
                    body=True, 
                    color="dark"
                )
                , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Descripcion", className='card-title', style={'font-size': 25}),
                    dbc.CardBody(
                        html.P(descripcion, style={'font-size': 15})
                    )
                ])
            )
        ]),
        dbc.Row(),
        cards,
    ])
])