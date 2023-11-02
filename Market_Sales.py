import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px


df = pd.read_csv("C:/Users/reneb/OneDrive/Área de Trabalho/Python/Asimov/Dash/Market_sales/supermarket_sales.csv")
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H5("Cidades"),
    dcc.Checklist(df["City"].value_counts().index,
                  df["City"].value_counts().index,
                  inline=True,
                  id="checklist1"),
    html.H5("Variáveis"),
    dcc.RadioItems(options=["gross income", "Rating"], value="gross income", id="Radio1", inline=True),
    dcc.Graph(id="Grafico1"),
    dcc.Graph(id="Grafico2"),
    dcc.Graph(id="Grafico3"),
]
)


@app.callback([Output("Grafico1", "figure"),
               Output("Grafico2", "figure"),
               Output("Grafico3", "figure")],
              [Input("checklist1", "value"),
               Input("Radio1", "value")])
def fun(cidade, variavel):
    operacao = np.sum if variavel == "gross income" else np.mean
    df_filtrada = df[df["City"].isin(cidade)]
    df_cidade = df_filtrada.groupby("City")[variavel].apply(operacao).to_frame().reset_index()
    df_pagamento = df_filtrada.groupby("Payment")[variavel].apply(operacao).to_frame().reset_index()
    df_produtos = df_filtrada.groupby(["City", "Product line"])[variavel].apply(operacao).to_frame().reset_index()

    fig_cidade = px.bar(df_cidade, x="City", y=variavel)
    fig_pagamento = px.bar(df_pagamento, x=variavel, y="Payment", orientation="h")
    fig_produtos = px.bar(df_produtos, x=variavel, y="Product line", color="City", orientation="h", barmode="group")

    fig_cidade.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)
    fig_pagamento.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)
    fig_produtos.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=300)

    return fig_cidade, fig_pagamento, fig_produtos


if __name__ == "__main__":
    app.run_server(port=8050, debug=True)
