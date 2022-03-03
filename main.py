import json
import plotly.graph_objects as go

import numpy as np
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State


def main():
    xs = np.linspace(0, 10 * np.pi, 100)
    ys = np.sin(xs)

    default_colors = ["#a3a7e4"] * len(xs)
    default_sizes = [10] * len(xs)
    size = list(default_sizes)
    colors = list(default_colors)

    def plot(colors=None, size=None):
        if colors is None:
            colors = default_colors
        if size is None:
            size = default_sizes
        fig = go.Figure([go.Scatter(x=xs, y=ys, mode="markers")])
        scatter = fig.data[0]

        scatter.marker.color = colors
        scatter.marker.size = [10] * len(xs)

        return fig

    fig = plot()

    # fig.layout.hovermode = "closest"
    fig.update_layout(clickmode="event")

    app = dash.Dash()
    graph = dcc.Graph(figure=fig, id="graph")
    app.layout = html.Div(
        [
            html.Div([html.Div()], id="dummy", style={"display": "none"}),
            graph,
        ]
    )

    @app.callback(Output("graph", "figure"), Input("graph", "clickData"))
    def display_hover_data(clickData):
        if clickData is None:
            return plot(size, colors)
        for index in clickData["points"]:
            colors[index["pointIndex"]] = "#bae2be"
            size[index["pointIndex"]] = 20
        fig.update_traces()
        return plot(size, colors)

    app.run_server(debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
