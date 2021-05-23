from typing import List, Union

import numpy as np
import pandas as pd
from IPython.display import display, HTML
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Grid


def kline(stock_data: pd.DataFrame):
    """
    :input: column name ('date', 'open', 'close', 'min', 'max', 'Trading_Volume')
    """

    def calculate_ma(day_count: int, price: list):
        result: List[Union[float, str]] = []
        for i in range(len(price)):
            if i < day_count:
                result.append("-")
                continue
            sum_total = 0.0
            for j in range(day_count):
                sum_total += float(price[i - j])
            result.append(abs(float("%.3f" % (sum_total / day_count))))
        return result

    def process_stock_data(data):
        data = data[["date", "open", "close", "min", "max", "Trading_Volume"]]
        data.columns = ["date", "open", "close", "low", "high", "volume"]
        if is_datetime(data["date"]):
            data_times = data["date"].dt.strftime("%Y-%m-%d").to_list()
        else:
            data_times = data["date"].to_list()
        values = data.values.tolist()
        volumes = []
        for i, tick in enumerate(data.values.tolist()):
            volumes.append([i, tick[5], 1 if tick[1] > tick[2] else -1])
        return {
            "categoryData": data_times,
            "values": values,
            "volumes": volumes,
        }

    chart_data = process_stock_data(stock_data)

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

    bar = Bar(
        init_opts=opts.InitOpts(
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    bar.add_xaxis(xaxis_data=chart_data["categoryData"])
    bar.add_yaxis(
        series_name="Volume",
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

    overlap_kline_line = kline.overlap(line)

    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="1000px",
            height="800px",
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    grid_chart.add(
        overlap_kline_line,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
    )
    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="63%", height="16%"
        ),
    )
    grid_chart.render("kline.html")
    display(HTML(filename="kline.html"))
    return grid_chart
