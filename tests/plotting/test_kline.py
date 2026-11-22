from FinMind import plotting
from FinMind.plotting.kline import (
    gen_kline_plot,
    gen_pos_top_height,
    process_stock_data,
)
from FinMind.data import DataLoader
import pytest
import pandas as pd
import json
import os

testdata_kline = [
    ("1220", "2015-01-01", "2020-05-19"),
    ("2330", "2018-01-01", "2021-03-03"),
]


@pytest.mark.parametrize("stock_id, start_date, end_date", testdata_kline)
def test_kline(stock_id, start_date, end_date):
    FINMIND_API_TOKEN = os.environ.get("FINMIND_API_TOKEN", "")
    data_loader = DataLoader()
    data_loader.login_by_token(FINMIND_API_TOKEN)
    stock_data = data_loader.taiwan_stock_daily_adj(
        stock_id=stock_id, start_date=start_date, end_date=end_date
    )
    assert plotting.kline(stock_data)
    stock_data = data_loader.feature.add_kline_institutional_investors(
        stock_data
    )
    assert plotting.kline(stock_data)
    stock_data = data_loader.feature.add_kline_margin_purchase_short_sale(
        stock_data
    )
    assert plotting.kline(stock_data)


@pytest.fixture(scope="module")
def stock_data():
    stock_data = pd.DataFrame(
        [
            {
                "date": "2018-01-03",
                "stock_id": "2330",
                "Trading_Volume": 31706091.0,
                "Trading_money": 7504382512.0,
                "open": 211.14,
                "max": 212.93,
                "min": 210.69,
                "close": 212.03,
                "spread": 4.02,
                "Trading_turnover": 13633.0,
            },
            {
                "date": "2018-01-04",
                "stock_id": "2330",
                "Trading_Volume": 29179613.0,
                "Trading_money": 6963192636.0,
                "open": 214.72,
                "max": 214.72,
                "min": 211.59,
                "close": 214.27,
                "spread": 2.24,
                "Trading_turnover": 10953.0,
            },
            {
                "date": "2018-01-05",
                "stock_id": "2330",
                "Trading_Volume": 23721255.0,
                "Trading_money": 5681934695.0,
                "open": 214.72,
                "max": 214.72,
                "min": 212.93,
                "close": 214.72,
                "spread": 0.45,
                "Trading_turnover": 8659.0,
            },
            {
                "date": "2018-01-08",
                "stock_id": "2330",
                "Trading_Volume": 21846692.0,
                "Trading_money": 5281823362.0,
                "open": 216.51,
                "max": 216.95,
                "min": 215.16,
                "close": 216.51,
                "spread": 1.79,
                "Trading_turnover": 10251.0,
            },
            {
                "date": "2018-01-09",
                "stock_id": "2330",
                "Trading_Volume": 19043123.0,
                "Trading_money": 4588314012.0,
                "open": 216.51,
                "max": 216.51,
                "min": 214.27,
                "close": 216.51,
                "spread": 0.0,
                "Trading_turnover": 7124.0,
            },
            {
                "date": "2018-01-10",
                "stock_id": "2330",
                "Trading_Volume": 25716220.0,
                "Trading_money": 6118683273.0,
                "open": 216.06,
                "max": 216.51,
                "min": 211.14,
                "close": 211.59,
                "spread": -4.92,
                "Trading_turnover": 10534.0,
            },
            {
                "date": "2018-01-11",
                "stock_id": "2330",
                "Trading_Volume": 32070338.0,
                "Trading_money": 7500674455.0,
                "open": 210.24,
                "max": 211.14,
                "min": 208.01,
                "close": 210.24,
                "spread": -1.35,
                "Trading_turnover": 9199.0,
            },
            {
                "date": "2018-01-12",
                "stock_id": "2330",
                "Trading_Volume": 23141291.0,
                "Trading_money": 5463302207.0,
                "open": 209.8,
                "max": 212.93,
                "min": 208.9,
                "close": 212.03,
                "spread": 1.79,
                "Trading_turnover": 7905.0,
            },
            {
                "date": "2018-01-15",
                "stock_id": "2330",
                "Trading_Volume": 28576533.0,
                "Trading_money": 6832851887.0,
                "open": 214.72,
                "max": 214.72,
                "min": 212.93,
                "close": 214.72,
                "spread": 2.69,
                "Trading_turnover": 9756.0,
            },
            {
                "date": "2018-01-16",
                "stock_id": "2330",
                "Trading_Volume": 23407632.0,
                "Trading_money": 5609009540.0,
                "open": 214.72,
                "max": 215.16,
                "min": 212.93,
                "close": 215.16,
                "spread": 0.44,
                "Trading_turnover": 8156.0,
            },
            {
                "date": "2018-01-17",
                "stock_id": "2330",
                "Trading_Volume": 38118119.0,
                "Trading_money": 9207582787.0,
                "open": 215.16,
                "max": 217.4,
                "min": 213.82,
                "close": 216.51,
                "spread": 1.35,
                "Trading_turnover": 12593.0,
            },
            {
                "date": "2018-01-18",
                "stock_id": "2330",
                "Trading_Volume": 50119952.0,
                "Trading_money": 12406562364.0,
                "open": 219.19,
                "max": 223.66,
                "min": 219.19,
                "close": 222.32,
                "spread": 5.81,
                "Trading_turnover": 19482.0,
            },
            {
                "date": "2018-01-19",
                "stock_id": "2330",
                "Trading_Volume": 55061292.0,
                "Trading_money": 13975174348.0,
                "open": 226.79,
                "max": 228.58,
                "min": 225.0,
                "close": 228.58,
                "spread": 6.26,
                "Trading_turnover": 18801.0,
            },
            {
                "date": "2018-01-22",
                "stock_id": "2330",
                "Trading_Volume": 45907509.0,
                "Trading_money": 11934882643.0,
                "open": 230.37,
                "max": 234.4,
                "min": 229.93,
                "close": 233.95,
                "spread": 5.37,
                "Trading_turnover": 13558.0,
            },
            {
                "date": "2018-01-23",
                "stock_id": "2330",
                "Trading_Volume": 34606444.0,
                "Trading_money": 9155080569.0,
                "open": 234.85,
                "max": 237.98,
                "min": 234.85,
                "close": 237.98,
                "spread": 4.03,
                "Trading_turnover": 13993.0,
            },
            {
                "date": "2018-01-24",
                "stock_id": "2330",
                "Trading_Volume": 42600813.0,
                "Trading_money": 11022372004.0,
                "open": 235.29,
                "max": 235.29,
                "min": 229.48,
                "close": 230.82,
                "spread": -7.16,
                "Trading_turnover": 17287.0,
            },
            {
                "date": "2018-01-25",
                "stock_id": "2330",
                "Trading_Volume": 46214756.0,
                "Trading_money": 11981089514.0,
                "open": 230.82,
                "max": 236.19,
                "min": 229.48,
                "close": 230.82,
                "spread": 0.0,
                "Trading_turnover": 15826.0,
            },
            {
                "date": "2018-01-26",
                "stock_id": "2330",
                "Trading_Volume": 43514523.0,
                "Trading_money": 11101977348.0,
                "open": 229.48,
                "max": 230.37,
                "min": 226.79,
                "close": 228.14,
                "spread": -2.68,
                "Trading_turnover": 12821.0,
            },
            {
                "date": "2018-01-29",
                "stock_id": "2330",
                "Trading_Volume": 31306234.0,
                "Trading_money": 8067780117.0,
                "open": 231.71,
                "max": 233.95,
                "min": 228.14,
                "close": 231.27,
                "spread": 3.13,
                "Trading_turnover": 12211.0,
            },
            {
                "date": "2018-01-30",
                "stock_id": "2330",
                "Trading_Volume": 37410591.0,
                "Trading_money": 9523980994.0,
                "open": 229.03,
                "max": 230.37,
                "min": 225.9,
                "close": 226.35,
                "spread": -4.92,
                "Trading_turnover": 12987.0,
            },
        ]
    )
    return stock_data


@pytest.fixture(scope="module")
def chart_data():
    chart_data = {
        "categoryData": [
            "2018-01-03",
            "2018-01-04",
            "2018-01-05",
            "2018-01-08",
            "2018-01-09",
            "2018-01-10",
            "2018-01-11",
            "2018-01-12",
            "2018-01-15",
            "2018-01-16",
            "2018-01-17",
            "2018-01-18",
            "2018-01-19",
            "2018-01-22",
            "2018-01-23",
            "2018-01-24",
            "2018-01-25",
            "2018-01-26",
            "2018-01-29",
            "2018-01-30",
        ],
        "values": [
            ["2018-01-03", 211.14, 212.03, 210.69, 212.93, 31706091.0],
            ["2018-01-04", 214.72, 214.27, 211.59, 214.72, 29179613.0],
            ["2018-01-05", 214.72, 214.72, 212.93, 214.72, 23721255.0],
            ["2018-01-08", 216.51, 216.51, 215.16, 216.95, 21846692.0],
            ["2018-01-09", 216.51, 216.51, 214.27, 216.51, 19043123.0],
            ["2018-01-10", 216.06, 211.59, 211.14, 216.51, 25716220.0],
            ["2018-01-11", 210.24, 210.24, 208.01, 211.14, 32070338.0],
            ["2018-01-12", 209.8, 212.03, 208.9, 212.93, 23141291.0],
            ["2018-01-15", 214.72, 214.72, 212.93, 214.72, 28576533.0],
            ["2018-01-16", 214.72, 215.16, 212.93, 215.16, 23407632.0],
            ["2018-01-17", 215.16, 216.51, 213.82, 217.4, 38118119.0],
            ["2018-01-18", 219.19, 222.32, 219.19, 223.66, 50119952.0],
            ["2018-01-19", 226.79, 228.58, 225.0, 228.58, 55061292.0],
            ["2018-01-22", 230.37, 233.95, 229.93, 234.4, 45907509.0],
            ["2018-01-23", 234.85, 237.98, 234.85, 237.98, 34606444.0],
            ["2018-01-24", 235.29, 230.82, 229.48, 235.29, 42600813.0],
            ["2018-01-25", 230.82, 230.82, 229.48, 236.19, 46214756.0],
            ["2018-01-26", 229.48, 228.14, 226.79, 230.37, 43514523.0],
            ["2018-01-29", 231.71, 231.27, 228.14, 233.95, 31306234.0],
            ["2018-01-30", 229.03, 226.35, 225.9, 230.37, 37410591.0],
        ],
        "volumes": [
            [0, 31706091.0, 1],
            [1, 29179613.0, -1],
            [2, 23721255.0, -1],
            [3, 21846692.0, -1],
            [4, 19043123.0, -1],
            [5, 25716220.0, -1],
            [6, 32070338.0, -1],
            [7, 23141291.0, 1],
            [8, 28576533.0, -1],
            [9, 23407632.0, 1],
            [10, 38118119.0, 1],
            [11, 50119952.0, 1],
            [12, 55061292.0, 1],
            [13, 45907509.0, 1],
            [14, 34606444.0, 1],
            [15, 42600813.0, -1],
            [16, 46214756.0, -1],
            [17, 43514523.0, -1],
            [18, 31306234.0, -1],
            [19, 37410591.0, -1],
        ],
    }
    return chart_data


def test_process_stock_data(stock_data, chart_data):
    result = process_stock_data(stock_data)
    expected = chart_data
    assert result == expected


# 子圖高度下限，預設圖高 800px 時約 56px
MIN_SUB_CHART_HEIGHT = 7
# 每張子圖上方要留給 y 軸名稱（例如「外資買賣(股)」）的空間
MIN_SUB_CHART_GAP = 3


def _percent(value: str) -> float:
    return float(value.rstrip("%"))


def _slider_pos_top(options: dict) -> float:
    (slider,) = [dz for dz in options["dataZoom"] if dz["type"] == "slider"]
    return _percent(slider["top"])


def _assert_sub_chart_layout(pos_top_list, height_list, slider_pos_top):
    assert len(pos_top_list) == len(height_list)
    for i in range(1, len(pos_top_list)):
        assert height_list[i] >= MIN_SUB_CHART_HEIGHT
        prev_bottom = pos_top_list[i - 1] + height_list[i - 1]
        assert round(pos_top_list[i] - prev_bottom, 6) >= MIN_SUB_CHART_GAP
    assert pos_top_list[-1] + height_list[-1] < slider_pos_top


@pytest.fixture(scope="module")
def stock_data_with_sub_charts(stock_data):
    diff = [(-1) ** i * 1000 * (i + 1) for i in range(len(stock_data))]
    return stock_data.assign(
        Foreign_Investor_diff=diff,
        Investment_Trust_diff=diff,
        Margin_Purchase_diff=diff,
        Short_Sale_diff=diff,
    )


@pytest.mark.parametrize("sub_graph_count", range(6))
def test_gen_pos_top_height(stock_data, sub_graph_count):
    plot_list = [object()] * sub_graph_count + [None] * (5 - sub_graph_count)
    pos_top_list, height_list = gen_pos_top_height(plot_list)
    assert len(pos_top_list) == sub_graph_count + 1

    kline_plot = gen_kline_plot(stock_data, process_stock_data(stock_data))
    slider_pos_top = _slider_pos_top(json.loads(kline_plot.dump_options()))
    _assert_sub_chart_layout(pos_top_list, height_list, slider_pos_top)


def test_kline_layout_with_all_sub_charts(stock_data_with_sub_charts, tmp_path):
    grid_chart = plotting.kline(
        stock_data_with_sub_charts, filename=str(tmp_path / "kline.html")
    )
    options = json.loads(grid_chart.dump_options())
    # 主圖 + 成交量、外資、投信、融資、融券
    assert len(options["grid"]) == 6
    _assert_sub_chart_layout(
        [_percent(grid["top"]) for grid in options["grid"]],
        [_percent(grid["height"]) for grid in options["grid"]],
        _slider_pos_top(options),
    )
