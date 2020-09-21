import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app
from apps import home, glaciares, experimentacion, retrocesos
from dash.dependencies import Input, Output

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Información General", href="/home", style={'font-size': '24px'}),
        dbc.DropdownMenuItem("Modelado del Derretimiento", href="/glaciares", style={'font-size': '24px'}),
        dbc.DropdownMenuItem("Modelado de Retrocesos", href="/retrocesos", style={'font-size': '24px'}),
        dbc.DropdownMenuItem("Experimentación", href="/experimentacion", style={'font-size': '24px'}),
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
    if pathname == '/glaciares':
        return glaciares.layout
    elif pathname == '/experimentacion':
        return experimentacion.layout
    elif pathname == '/retrocesos':
        return retrocesos.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)