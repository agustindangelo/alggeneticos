import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app
from apps import home, glaciares, experimentacion
from dash.dependencies import Input, Output

navbar = dbc.Navbar([
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='https://image.flaticon.com/icons/png/512/82/82990.png', width='70px')),
                        dbc.Col(dbc.NavbarBrand("Grupo 1", className="ml-2", style={'font-size': '32px'})),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            ),
            dbc.Col([
                dbc.NavLink("Información General", href="/home", style={'font-size': '20px'}, className='ml-auto'),              
                dbc.NavLink("Modelado de Glaciares", href="/glaciares", style={'font-size': '20px'}, className='ml-auto'),
                dbc.NavLink("Experimentación", href="/experimentacion", style={'font-size': '20px'}, className='ml-auto'), 
                ],
                width={'size':'4', 'order':'last'}
            )
           
        ],
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
    if pathname == '/glaciares':
        return glaciares.layout
    elif pathname == '/experimentacion':
        return experimentacion.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)