import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
load_figure_template("minty")


df = pd.read_csv("assets/supermarket_sales.csv")
print(df.columns)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            dbc.Card([
            html.H5("Cidades"),
            dcc.Checklist(df["City"].value_counts().index,
                          df["City"].value_counts().index,
                          inline=True,
                          id="checklist1",
                          inputStyle={"margin-right": "20px", "margin-left": "20px"}),
            html.Hr(),
            html.H5("Variáveis", style={"margin-top": "10px"}),
            dcc.RadioItems(options=["gross income", "Rating"], value="gross income", id="Radio1", inline=False)],
            style={"height": "100vh", "margin-right": "20px", "padding": "25px"})
        ], sm=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id="Grafico1")], sm=4),
                dbc.Col([dcc.Graph(id="Grafico2")], sm=4),
                dbc.Col([dcc.Graph(id="Grafico5")], sm=4)]),
            dbc.Row([dcc.Graph(id="Grafico4")]),
            dbc.Row([dcc.Graph(id="Grafico3")]),
        ], sm=10)
    ])
])

@app.callback([Output("Grafico1", "figure"),
               Output("Grafico2", "figure"),
               Output("Grafico5", "figure"),
               Output("Grafico4", "figure"),
               Output("Grafico3", "figure")],
              [Input("checklist1", "value"),
               Input("Radio1", "value")])
def fun(cidade, variavel):
    operacao = np.sum if variavel == "gross income" else np.mean
    df_filtrada = df[df["City"].isin(cidade)]
    df_cidade = df_filtrada.groupby("City")[variavel].apply(operacao).to_frame().reset_index()
    df_genero = df_filtrada.groupby(["Gender", "City"])[variavel].apply(operacao).to_frame().reset_index()
    df_pagamento = df_filtrada.groupby("Payment")[variavel].apply(operacao).to_frame().reset_index()
    df_data = df_filtrada.groupby("Date")[variavel].apply(operacao).to_frame().reset_index()
    df_produtos = df_filtrada.groupby(["City", "Product line"])[variavel].apply(operacao).to_frame().reset_index()

    fig_cidade = px.bar(df_cidade, x="City", y=variavel)
    fig_pagamento = px.bar(df_pagamento, x=variavel, y="Payment", orientation="h")
    fig_genero = px.bar(df_genero, y=variavel, x="Gender", color="City", barmode="group")
    fig_produtos = px.bar(df_produtos, x=variavel, y="Product line", color="City", orientation="h", barmode="group")
    fig_data = px.bar(df_data, y=variavel, x="Date")

    for fig in [fig_cidade, fig_pagamento, fig_genero, fig_data]:
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template="minty")

    fig_produtos.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=400)

    return fig_cidade, fig_pagamento, fig_genero, fig_data, fig_produtos


if __name__ == "__main__":
    app.run_server(port=8051, debug=True)

