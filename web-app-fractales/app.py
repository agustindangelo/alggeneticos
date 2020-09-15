import dash
import dash_bootstrap_components as dbc

theme = 'https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/materia/bootstrap.min.css'
app = dash.Dash(__name__, external_stylesheets=[theme], suppress_callback_exceptions=True)
server = app.server