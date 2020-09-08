import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from app import app

layout = html.Div([
    html.Div(id="ejercicio3-content"),
    html.P("primera linea de la pagina 3")
])

@app.callback(
    Output('ejercicio3-content', 'children'),
    [Input('ejercicio3-dropdown', 'value')]
)
def display_value(value):
    return 'You have selected "{}"'.format(value)