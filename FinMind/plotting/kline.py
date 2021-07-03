import typing

import pandas as pd
import ta
from IPython.display import HTML, display
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Kline, Line


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
            "Margin_Purchase_diff",
            "Short_Sale_diff",
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
            "Margin_Purchase_diff": "Margin_Purchase_diff",
            "Short_Sale_diff": "Short_Sale_diff",
        }
    )
    return stock_data


def create_diff_data(
    stock_data: pd.DataFrame, column: str
) -> typing.Dict[str, typing.List[typing.List[int]]]:
    values = stock_data[column].values.tolist()
    _diff = [
        [i, value, 1 if value > 0 else -1] for i, value in enumerate(values)
    ]
    return {column: _diff}


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
        [i, tick[5], 1 if tick[1] < tick[2] else -1]
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
    for column in [
        "Foreign_Investor_diff",
        "Investment_Trust_diff",
        "Margin_Purchase_diff",
        "Short_Sale_diff",
    ]:
        if column in stock_data.columns:
            result.update(create_diff_data(stock_data, column=column))
    return result


def gen_line_plot(
    stock_data: pd.DataFrame,
    chart_data: typing.Dict[
        str, typing.List[typing.List[typing.Union[float, int]]]
    ],
) -> Line:
    ma_items = [5, 10, 20, 60]
    line = Line(
        init_opts=opts.InitOpts(
            animation_opts=opts.AnimationOpts(animation=False),
        )
    ).add_xaxis(xaxis_data=chart_data["categoryData"])
    for ma in ma_items:
        line.add_yaxis(
            series_name=f"MA{ma}",
            y_axis=ta.trend.sma_indicator(stock_data["close"], ma).round(2),
            is_smooth=True,
            is_symbol_show=False,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
    line.set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"))
    return line


def gen_bar_plot(
    chart_data: typing.Dict[
        str, typing.List[typing.List[typing.Union[float, int]]]
    ],
    index: int,
    column: str,
    label: str,
) -> typing.Tuple[Bar, int]:
    if column in chart_data.keys():
        bar = Bar(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(animation=False),
            )
        )
        xaxis_data = [label for i in range(len(chart_data[column]))]
        bar.add_xaxis(xaxis_data=xaxis_data)
        bar.add_yaxis(
            series_name="Value",
            y_axis=chart_data[column],
            xaxis_index=index,
            yaxis_index=index,
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
                name=label,
                name_textstyle_opts=opts.TextStyleOpts(
                    color="red",
                    font_style="normal",
                    font_weight="normal",
                    font_family="Arial",
                    font_size=12,
                ),
                grid_index=1,
                is_scale=True,
                split_number=2,
                name_gap=0,
                axislabel_opts=opts.LabelOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        return bar, index + 1
    else:
        return None, index


def gen_pos_top_height(plot_list: typing.List[typing.Any]):
    plot_list = [plot for plot in plot_list if plot]
    plot_index = [i + 1 for i in range(len(plot_list))]
    sub_graph_count = len(plot_index)
    border = 5
    if sub_graph_count == 1:
        pos_top_list = [5, 65]
        height_list = [50, 20]
    else:
        pos_top_list = [5]
        height_list = [30]
        split_count = int(50 / sub_graph_count) - border
        for i in range(sub_graph_count):
            pos_top_list.append(pos_top_list[-1] + height_list[-1] + border)
            height_list.append(split_count)
    return pos_top_list, height_list


def filter_bar_plot(bar_plot_list: typing.List[Bar]) -> typing.List[Bar]:
    return [bar_plot for bar_plot in bar_plot_list if bar_plot]


def gen_grid_chart(
    overlap_kline_line: Kline,
    width: str,
    height: str,
    bar_plot_list: typing.List[Bar],
    filename: str,
) -> Grid:
    index = 0
    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width=width,
            height=height,
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    pos_top_list, height_list = gen_pos_top_height(plot_list=bar_plot_list)
    grid_chart.add(
        overlap_kline_line,
        grid_opts=opts.GridOpts(
            pos_left="10%",
            pos_right="8%",
            pos_top=f"{pos_top_list[index]}%",
            height=f"{height_list[index]}%",
        ),
    )
    index += 1
    bar_plot_list = filter_bar_plot(bar_plot_list)
    for bar_plot in bar_plot_list:
        grid_chart.add(
            bar_plot,
            grid_opts=opts.GridOpts(
                pos_left="10%",
                pos_right="8%",
                pos_top=f"{pos_top_list[index]}%",
                height=f"{height_list[index]}%",
            ),
        )
        index += 1
    grid_chart.render(filename)
    return grid_chart


def get_subgraph_indices(
    chart_data: typing.Dict[
        str, typing.List[typing.List[typing.Union[float, int]]]
    ]
) -> typing.Tuple[typing.List[int], typing.List[int]]:
    x_axis_data_type = [
        key for key in list(chart_data.keys()) if key not in ["categoryData"]
    ]
    xaxis_index = [i for i in range(len(x_axis_data_type))]
    series_index = [5 + i for i in range(len(x_axis_data_type))]
    return xaxis_index, series_index


def gen_kline_plot(
    stock_data: pd.DataFrame,
    chart_data: typing.Dict[
        str, typing.List[typing.List[typing.Union[float, int]]]
    ],
) -> Kline:
    xaxis_index, series_index = get_subgraph_indices(chart_data)
    kline_data = [
        list(kline_dict.values())
        for kline_dict in stock_data[["open", "close", "min", "max"]].to_dict(
            "records"
        )
    ]
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
                xaxis_index=xaxis_index,
                range_start=85,
                range_end=100,
            ),
            opts.DataZoomOpts(
                is_show=True,
                xaxis_index=xaxis_index,
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
            series_index=series_index,
            is_piecewise=True,
            pieces=[
                {"value": 1, "color": "#ec0000"},
                {"value": -1, "color": "#00da3c"},
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


def gen_bar_plot_list(
    chart_data: typing.Dict[
        str, typing.List[typing.List[typing.Union[float, int]]]
    ]
) -> typing.List[Bar]:
    index = 1
    params_dict_list = [
        dict(column="volumes", label="成交量(股)"),
        dict(column="Foreign_Investor_diff", label="外資買賣(股)"),
        dict(column="Investment_Trust_diff", label="投信買賣(股)"),
        dict(column="Margin_Purchase_diff", label="融資買賣(股)"),
        dict(column="Short_Sale_diff", label="融券買賣(股)"),
    ]
    bar_plot_list = []
    for params_dict in params_dict_list:
        bar_plot, index = gen_bar_plot(
            chart_data,
            index=index,
            column=params_dict["column"],
            label=params_dict["label"],
        )
        bar_plot_list.append(bar_plot)
    return bar_plot_list


def kline(
    stock_data: pd.DataFrame,
    width: str = "1000px",
    height: str = "800px",
    filename: str = "kline.html",
) -> Grid:
    """plot kline
    :param: stock_data (pd.DataFrame) column name
    ('date', 'open', 'close', 'min', 'max', 'Trading_Volume')
    :param: width (str) default '1000px'
    :param: height (str) default '800px'
    :filename: output filename (str) default 'kline.html'

    :return: display kline
    :rtype Grid
    """
    chart_data = process_stock_data(stock_data.copy())
    kline_plot = gen_kline_plot(stock_data, chart_data)
    line_plot = gen_line_plot(stock_data, chart_data)
    bar_plot_list = gen_bar_plot_list(chart_data)
    overlap_kline_line = kline_plot.overlap(line_plot)
    grid_chart = gen_grid_chart(
        overlap_kline_line, width, height, bar_plot_list, filename
    )
    display(HTML(filename=filename))
    return grid_chart
