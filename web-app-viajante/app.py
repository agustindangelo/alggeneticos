import dash
import dash_bootstrap_components as dbc

stylesheet_url='https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/flatly/bootstrap.min.css'
app = dash.Dash(__name__, external_stylesheets=[stylesheet_url], suppress_callback_exceptions=True)
server = app.server