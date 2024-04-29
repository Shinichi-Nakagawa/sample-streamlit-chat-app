from typing import List, Tuple

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

WIDTH = 1400
HEIGHT = 700


def bar(df: pd.DataFrame, x: List[str], y: str, title: str, x_title: str, y_title: str,
        x_dtick: int, x_range: Tuple[int], autosize: bool = True) -> go.Figure:
    fig = px.bar(df, x=x, y=y, barmode='group', )
    """
    Bar chart
    :param df: DataFrame
    :param x: X column
    :param y: Y column
    :param title: Graph title
    :param x_title: x-axis title
    :param y_title: y-axis title
    :param x_dtick: x-axis tick interval
    :param x_range: x-axis range
    :param autosize: Auto size flag
    :return: Figure object
    """
    if autosize:
        # 画面に合わせるパターン
        fig.update_layout(
            title=title,
            autosize=True,
            legend_title=None
        )
    else:
        # 固定長
        fig.update_layout(
            title=title,
            width=WIDTH,
            height=HEIGHT,
            legend_title=None
        )
    fig.update_yaxes(title=y_title)
    fig.update_xaxes(title=x_title, dtick=x_dtick, range=x_range)
    return fig
