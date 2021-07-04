from IPython.display import HTML, display
from pyecharts import options as opts
from pyecharts.charts import Line

from FinMind import LinePlotSchema


def line(
    line_plot_data: LinePlotSchema,
    y_series_name: str = "",
    y_axis_name: str = "億",
    yaxis_color: str = "#dca540",
    title: str = "title",
    width: str = "800px",
    height: str = "600px",
    filename: str = "line.html",
):
    """plot line
    :param: bar_plot_data (:obj:FinMind.LinePlotSchema)
    LinePlotSchema(labels=labels, series=series)
    :param: y_series_name (str) default ''
    :param: y_axis_name (str) default "億"
    :param: yaxis_color (str) default "#dca540"
    :param: title (str) default "title"
    :param: width (str) default "800px"
    :param: height (str) default "600px"
    :param: filename (str) default "line.html", output filename
    :return: display line
    :rtype pyecharts.charts.Line
    """
    plot_plot = (
        Line(opts.InitOpts(width=width, height=height))
        .add_xaxis(line_plot_data.labels)
        .add_yaxis(
            series_name=y_series_name,
            y_axis=line_plot_data.series,
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
    plot_plot.render(filename)
    display(HTML(filename=filename))
    return plot_plot
