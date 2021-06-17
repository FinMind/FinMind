import typing

import numpy as np
import pandas as pd
from IPython.display import display, HTML
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Grid


def calculate_ma(day_count: int, price: list):
    result: typing.List[typing.Union[float, str]] = []
    for i in range(len(price)):
        if i < day_count:
            result.append("-")
            continue
        sum_total = 0.0
        for j in range(day_count):
            sum_total += float(price[i - j])
        result.append(abs(float("%.3f" % (sum_total / day_count))))
    return result


def filter_stock_data(stock_data: pd.DataFrame) -> pd.DataFrame:
    colname = [
        col
        for col in [
            "date",
            "open",
            "close",
            "min",
            "max",
            "Trading_Volume",
            "Foreign_Investor_diff",
            "Investment_Trust_diff",
        ]
        if col in stock_data.columns
    ]
    stock_data = stock_data[colname]
    return stock_data


def column_mapping(stock_data: pd.DataFrame) -> pd.DataFrame:
    stock_data.columns = stock_data.columns.map(
        {
            "date": "date",
            "open": "open",
            "close": "close",
            "min": "low",
            "max": "high",
            "Trading_Volume": "volume",
            "Foreign_Investor_diff": "Foreign_Investor_diff",
            "Investment_Trust_diff": "Investment_Trust_diff",
        }
    )
    return stock_data


def add_foreign_investor(
    stock_data: pd.DataFrame,
) -> typing.Dict[str, typing.List[typing.List[typing.Union[float, int]]]]:
    values = stock_data["Foreign_Investor_diff"].values.tolist()
    foreign_investor_diff = [
        [i, value, 1 if value > 0 else -1] for i, value in enumerate(values)
    ]
    return dict(
        foreign_investor_diff=foreign_investor_diff,
    )


def add_investment_trust(
    stock_data: pd.DataFrame,
) -> typing.Dict[str, typing.List[typing.List[typing.Union[float, int]]]]:
    values = stock_data["Investment_Trust_diff"].values.tolist()
    investment_trust_diff = [
        [i, value, 1 if value > 0 else -1] for i, value in enumerate(values)
    ]
    return dict(
        investment_trust_diff=investment_trust_diff,
    )


def add_category_data(
    stock_data: pd.DataFrame,
) -> typing.Dict[str, typing.List[typing.List[typing.Union[float, int]]]]:
    if is_datetime(stock_data["date"]):
        data_times = stock_data["date"].dt.strftime("%Y-%m-%d").to_list()
    else:
        data_times = stock_data["date"].to_list()
    return dict(
        categoryData=data_times,
    )


def add_kline_volume(
    stock_data: pd.DataFrame,
) -> typing.Dict[str, typing.List[typing.List[typing.Union[float, int]]]]:
    values = stock_data.values.tolist()
    volumes = [
        [i, tick[5], 1 if tick[1] > tick[2] else -1]
        for i, tick in enumerate(values)
    ]
    return dict(
        values=values,
        volumes=volumes,
    )


def process_stock_data(
    stock_data: pd.DataFrame,
) -> typing.Dict[str, typing.List[typing.List[typing.Union[float, int]]]]:
    result = dict()
    stock_data = filter_stock_data(stock_data)
    stock_data = column_mapping(stock_data)
    result.update(add_category_data(stock_data))
    result.update(add_kline_volume(stock_data))
    if "Foreign_Investor_diff" in stock_data.columns:
        result.update(add_foreign_investor(stock_data))
    if "Investment_Trust_diff" in stock_data.columns:
        result.update(add_investment_trust(stock_data))

    return result


def gen_kline_plot(
    chart_data: typing.Dict[
        str, typing.List[typing.List[typing.Union[float, int]]]
    ]
) -> Kline:
    kline_data = [data[1:-1] for data in chart_data["values"]]
    kline = Kline(
        init_opts=opts.InitOpts(
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    kline.add_xaxis(xaxis_data=chart_data["categoryData"])
    kline.add_yaxis(
        series_name="kline",
        y_axis=kline_data,
        itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c"),
    )
    kline.set_global_opts(
        legend_opts=opts.LegendOpts(is_show=True, pos_left="center"),
        datazoom_opts=[
            opts.DataZoomOpts(
                is_show=False,
                type_="inside",
                xaxis_index=[0, 1],
                range_start=85,
                range_end=100,
            ),
            opts.DataZoomOpts(
                is_show=True,
                xaxis_index=[0, 1],
                type_="slider",
                pos_top="85%",
                range_start=85,
                range_end=100,
            ),
        ],
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross",
            background_color="rgba(245, 245, 245, 0.8)",
            border_width=1,
            border_color="#ccc",
            textstyle_opts=opts.TextStyleOpts(color="#000"),
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_show=False,
            dimension=2,
            series_index=5,
            is_piecewise=True,
            pieces=[
                {"value": 1, "color": "#00da3c"},
                {"value": -1, "color": "#ec0000"},
            ],
        ),
        axispointer_opts=opts.AxisPointerOpts(
            is_show=True,
            link=[{"xAxisIndex": "all"}],
            label=opts.LabelOpts(background_color="#777"),
        ),
        brush_opts=opts.BrushOpts(
            x_axis_index="all",
            brush_link="all",
            out_of_brush={"colorAlpha": 0.1},
            brush_type="lineX",
        ),
    )
    return kline


def gen_line_plot(
    chart_data: typing.Dict[
        str, typing.List[typing.List[typing.Union[float, int]]]
    ]
) -> Line:
    close = np.array(chart_data["values"])[:, 2]
    ma_items = [5, 10, 20, 60]
    line = Line(
        init_opts=opts.InitOpts(
            animation_opts=opts.AnimationOpts(animation=False),
        )
    ).add_xaxis(xaxis_data=chart_data["categoryData"])
    for ma in ma_items:
        line.add_yaxis(
            series_name="MA" + str(ma),
            y_axis=calculate_ma(day_count=ma, price=close),
            is_smooth=True,
            is_symbol_show=False,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
    line.set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"))
    return line


def gen_volume_bar_plot(
    chart_data: typing.Dict[
        str, typing.List[typing.List[typing.Union[float, int]]]
    ]
) -> Bar:
    bar = Bar(
        init_opts=opts.InitOpts(
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    xaxis_data = ["Volume" for i in range(len(chart_data["volumes"]))]
    bar.add_xaxis(xaxis_data=xaxis_data)
    bar.add_yaxis(
        series_name="Value",
        y_axis=chart_data["volumes"],
        xaxis_index=1,
        yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
    )
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            is_scale=True,
            grid_index=1,
            boundary_gap=False,
            axisline_opts=opts.AxisLineOpts(is_on_zero=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=False),
            split_number=20,
            min_="dataMin",
            max_="dataMax",
        ),
        yaxis_opts=opts.AxisOpts(
            grid_index=1,
            is_scale=True,
            split_number=2,
            axislabel_opts=opts.LabelOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(is_show=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    return bar


def gen_bar_plot(
    chart_data: typing.Dict[
        str, typing.List[typing.List[typing.Union[float, int]]]
    ],column:str
) -> Bar:
    bar = Bar(
        init_opts=opts.InitOpts(
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    xaxis_data = [
        column
        for i in range(len(chart_data[column]))
    ]
    bar.add_xaxis(xaxis_data=xaxis_data)
    bar.add_yaxis(
        series_name="Value",
        y_axis=chart_data[column],
        xaxis_index=1,
        yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
    )
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            is_scale=True,
            grid_index=1,
            boundary_gap=False,
            axisline_opts=opts.AxisLineOpts(is_on_zero=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=False),
            split_number=20,
            min_="dataMin",
            max_="dataMax",
        ),
        yaxis_opts=opts.AxisOpts(
            grid_index=1,
            is_scale=True,
            split_number=2,
            axislabel_opts=opts.LabelOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(is_show=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    return bar


def gen_grid_chart(
    overlap_kline_line: Kline,
    volume_bar_plot: Bar,
    institutional_investors_bar_plot: Bar = None,
) -> Grid:
    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="1000px",
            height="800px",
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    grid_chart.add(
        overlap_kline_line,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="40%"),
    )
    grid_chart.add(
        volume_bar_plot,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="53%", height="10%"
        ),
    )
    grid_chart.add(
        institutional_investors_bar_plot,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="63%", height="10%"
        ),
    )
    grid_chart.render("kline.html")
    return grid_chart


def kline(stock_data: pd.DataFrame) -> Grid:
    """plot kline
    :param: stock_data (pd.DataFrame) column name ('date', 'open', 'close', 'min', 'max', 'Trading_Volume')

    :return: display kline
    :rtype Grid
    """
    chart_data = process_stock_data(stock_data.copy())
    kline_plot = gen_kline_plot(chart_data)
    line_plot = gen_line_plot(chart_data)
    volume_bar_plot = gen_volume_bar_plot(chart_data)
    foreign_investor_bar_plot = gen_bar_plot(chart_data, "foreign_investor_diff")
    investment_trust_bar_plot = gen_bar_plot(chart_data, "investment_trust_diff")
    institutional_investors_bar_plot = foreign_investor_bar_plot.overlap(investment_trust_bar_plot)
    overlap_kline_line = kline_plot.overlap(line_plot)
    grid_chart = gen_grid_chart(
        overlap_kline_line,
        volume_bar_plot,
        institutional_investors_bar_plot=institutional_investors_bar_plot,
    )
    display(HTML(filename="kline.html"))
    return grid_chart
