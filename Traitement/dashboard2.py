# -*- coding: utf-8 -*-
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
from Traitement.indicateurs import treat_modus
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
import plotly.graph_objects as go

df = treat_modus('scen', 'PPM')

fig1 = go.Figure(data=[go.Scatter(x=[t for t in range(22)], y=df['TC'])])
fig2 = go.Figure(data=[go.Scatter(x=[t for t in range(22)], y=df['VP'])])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children="Résultats du scénario"),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.H2(children="Part Modal TC"),
    dcc.Graph(
        id='Part Modal TC',
        figure=fig1
    ),
    html.H2(children="Part Modal VP"),
    dcc.Graph(
        id='Part Modal VP',
        figure=fig2
    )
])

if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload=False)
