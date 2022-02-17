import altair as alt
from dash import Dash, html, dcc, Input, Output
import pandas as pd

alt.data_transformers.enable("data_server")
alt.renderers.enable("mimetype")

df = pd.read_csv("athlete_events.csv")
filtered_df = df[df["Team"] == "Canada"]
filtered_df["Medal"].fillna(0)


def plot(xmax, ycol, filtered_df=filtered_df.copy()):
    chart = (
        alt.Chart(filtered_df[filtered_df["Year"] < xmax])
        .mark_point()
        .encode(y=alt.Y(ycol), x=alt.X("Year:O"))
    )
    return chart.to_html()


app = Dash(__name__)
server = app.server
app.layout = html.Div(
    [
        html.Iframe(
            id="scatter",
            srcDoc=plot(xmax=1900, ycol="mean(Weight)"),
            style={"border-width": "0", "width": "100%", "height": "400px"},
        ),
        dcc.Dropdown(
            id="ycol",
            value="mean(Weight)",
            options=[
                {"label": i, "value": i}
                for i in ["mean(Weight)", "mean(Age)", "mean(Height)"]
            ],
        ),
        dcc.Slider(id="xslider", min=1900, max=2016),
    ]
)


@app.callback(
    Output("scatter", "srcDoc"), Input("xslider", "value"), Input("ycol", "value")
)
def update_output(xmax, ycol):
    return plot(xmax, ycol)


if __name__ == "__main__":
    app.run_server(debug=True)
