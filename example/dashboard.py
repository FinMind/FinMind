from pathlib import Path

from flask import Flask, render_template, request
from loguru import logger
from pyecharts.charts import Page

import FinMind
from FinMind import plotting
from FinMind.data import DataLoader


def get_path():
    path = Path(FinMind.__file__)
    path = path.parent.joinpath("templates")
    return path


PATH = get_path()


def kline(
    data_loader: DataLoader, stock_id: str, start_date: str, end_date: str
):
    stock_data = data_loader.taiwan_stock_daily(stock_id, start_date, end_date)
    stock_data = data_loader.feature.add_kline_institutional_investors(
        stock_data
    )
    stock_data = data_loader.feature.add_kline_margin_purchase_short_sale(
        stock_data
    )
    # 繪製k線圖
    kline_plot = plotting.kline(stock_data)
    return kline_plot


def bar(data_loader: DataLoader, stock_id: str, start_date: str, end_date: str):
    df = data_loader.taiwan_stock_month_revenue(
        stock_id=stock_id, start_date=start_date, end_date=end_date
    )
    df["labels"] = (
        df[["revenue_year", "revenue_month"]]
        .astype(str)
        .apply(lambda date: f"{date[0]}-{date[1]}M", axis=1)
    )
    df["series"] = df["revenue"].map(lambda value: round(value * 1e-8, 2))
    bar_plot = plotting.bar(
        labels=df["labels"],
        series=df["series"],
        title="月營收",
        yaxis_color="orange",
        y_axis_name="億",
    )
    return bar_plot


def line(
    data_loader: DataLoader, stock_id: str, start_date: str, end_date: str
):
    df = data_loader.taiwan_stock_shareholding(
        stock_id=stock_id, start_date=start_date, end_date=end_date
    )
    df["series"] = df["ForeignInvestmentSharesRatio"].map(
        lambda value: round(value * 1e-2, 2)
    )
    df["labels"] = df["date"]
    line_plot = plotting.line(
        labels=df["labels"],
        series=df["series"],
        title="外資持股比例",
        yaxis_color="blue",
        y_axis_name="",
    )
    return line_plot


def pie(data_loader: DataLoader, stock_id: str, start_date: str, end_date: str):
    df = data_loader.taiwan_stock_holding_shares_per(
        stock_id=stock_id, start_date=start_date, end_date=end_date
    )
    df = df[df["date"] == max(df["date"])]
    df = df[df["HoldingSharesLevel"] != "total"]
    df["labels"] = df["HoldingSharesLevel"]
    df["series"] = df["percent"]
    pie_plot = plotting.pie(
        labels=df["labels"], series=df["series"], title="股權分散表"
    )
    return pie_plot


def dashboard(stock_id: str, start_date: str, end_date: str):
    data_loader = DataLoader()
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        kline(data_loader, stock_id, start_date, end_date),
        bar(data_loader, stock_id, start_date, end_date),
        line(data_loader, stock_id, start_date, end_date),
        pie(data_loader, stock_id, start_date, end_date),
    )
    dashboard_html_path = str(PATH.joinpath("dashboard.html"))
    post_html_path = str(PATH.joinpath("post.html"))
    page.render(dashboard_html_path)
    post_html = open(post_html_path, "r", encoding="utf-8").read()
    dashboard_html = open(dashboard_html_path, "r", encoding="utf-8").read()
    html = post_html.replace("DASHBOARD", dashboard_html)
    with open(dashboard_html_path, "w", encoding="utf-8") as e:
        e.write(html)


app = Flask(__name__, template_folder=str(PATH))


@app.route("/", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        stock_id = request.form.get("stock_id")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        logger.info(stock_id)
        dashboard(stock_id=stock_id, start_date=start_date, end_date=end_date)
        return render_template("dashboard.html")
    return render_template("post.html")


app.run(host="0.0.0.0", debug=True)
