import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app
from apps import home, ejercicio1, ejercicio2, ejercicio3, ejercicio4
from dash.dependencies import Input, Output

navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Información General", href="/home")),
            dbc.NavItem(dbc.NavLink("Ejercicio 1", href="/ejercicio1")),
            dbc.NavItem(dbc.NavLink("Ejercicio 2", href="/ejercicio2")),
            dbc.NavItem(dbc.NavLink("Ejercicio 3", href="/ejercicio3")),
            dbc.NavItem(dbc.NavLink("Ejercicio 4", href="/ejercicio4")),
        ],
        brand="GRUPO 1 - TP N°3",
        color="primary",
        dark=True,
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
    if pathname == '/ejercicio1':
        return ejercicio1.layout
    elif pathname == '/ejercicio2':
        return ejercicio2.layout
    elif pathname == '/ejercicio3':
        return ejercicio3.layout
    elif pathname == '/ejercicio4':
        return ejercicio4.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)