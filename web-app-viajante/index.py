import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app
from apps import home, exhaustivo, heuristicoA, heuristicoB, geneticos, geneticosready
from dash.dependencies import Input, Output

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Información General", href="/home", style={'font-size': '24px'}),
        dbc.DropdownMenuItem("Enfoque Exhaustivo", href="/exhaustivo", style={'font-size': '24px'}),
        dbc.DropdownMenuItem("Enfoque Heurístico con Restricción", href="/heuristicoA", style={'font-size': '24px'}),
        dbc.DropdownMenuItem("Enfoque Heurístico", href="/heuristicoB", style={'font-size': '24px'}),
        dbc.DropdownMenuItem("Algoritmo Genético", href="/geneticos", style={'font-size': '24px'}),
        dbc.DropdownMenuItem("Final Algoritmo Genético", href="/geneticos-ready", style={'font-size': '24px'})
    ],
    nav = True,
    in_navbar = True,
    label = "Secciones",
    style={'font-size': '24px'}
)

navbar = dbc.Navbar(
    dbc.Container([
           html.A(
                dbc.Row([
                        dbc.Col(html.Img(src='https://image.flaticon.com/icons/png/512/82/82990.png', width='70px')),
                        dbc.Col(dbc.NavbarBrand("Grupo 1", className="ml-2", style={'font-size': '32px'})),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                style={'font-size': 25},
                navbar=True,
            ),
        ]
    ),
    color="primary",
    dark=True,
    className="mb-4",
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)

def display_page(pathname):
    if pathname == '/exhaustivo':
        return exhaustivo.layout
    elif pathname == '/heuristicoA':
        return heuristicoA.layout
    elif pathname == '/heuristicoB':
        return heuristicoB.layout
    elif pathname == '/geneticos':
        return geneticos.layout
    elif pathname == '/geneticos-ready':
        return geneticosready.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)