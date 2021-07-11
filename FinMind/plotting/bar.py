import typing

from IPython.display import HTML, display
from pyecharts import options as opts
from pyecharts.charts import Bar

from FinMind.schema.plot import Labels, Series, convert_labels_series_schema


def bar(
    labels: typing.Union[typing.List[typing.Union[str, int]], Labels],
    series: typing.Union[typing.List[typing.Union[int, float]], Series],
    y_series_name: str = "",
    y_axis_name: str = "億",
    yaxis_color: str = "#dca540",
    title: str = "title",
    width: str = "800px",
    height: str = "600px",
    filename: str = "bar.html",
):
    """plot bar
    :param: bar_plot_data (:obj:FinMind.BarPlotSchema)
    BarPlotSchema(labels=labels, series=series)
    :param: y_series_name (str) default ''
    :param: y_axis_name (str) default "億"
    :param: yaxis_color (str) default "#dca540"
    :param: title (str) default "title"
    :param: width (str) default "800px"
    :param: height (str) default "600px"
    :param: filename (str) default "bar.html", output filename

    :return: display bar
    :rtype pyecharts.charts.Bar
    """
    labels, series = convert_labels_series_schema(labels, series)
    bar_plot = (
        Bar(opts.InitOpts(width=width, height=height))
        .add_xaxis(labels.labels)
        .add_yaxis(
            series_name=y_series_name,
            y_axis=series.series,
            itemstyle_opts=opts.ItemStyleOpts(color=yaxis_color),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            datazoom_opts=[
                opts.DataZoomOpts(xaxis_index=[0]),
                opts.DataZoomOpts(xaxis_index=[0], type_="inside"),
            ],
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    formatter=f"{{value}}{y_axis_name}"
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis", axis_pointer_type="cross"
            ),
        )
        .set_series_opts(
            markpoint_opts=opts.MarkPointOpts(),
        )
    )
    bar_plot.render(filename)
    display(HTML(filename=filename))
    return bar_plot
