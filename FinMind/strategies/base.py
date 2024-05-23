import ast
import typing
import warnings
from enum import Enum

import numpy as np
import pandas as pd
from loguru import logger

from FinMind import indicators
from FinMind.data import DataLoader
from FinMind.schema import (
    CompareMarketDetail,
    CompareMarketStats,
    FinalStats,
    TradeDetail,
)
from FinMind.schema.data import Dataset
from FinMind.schema.indicators import (
    AddBuySellRule,
    AdditionalDataset,
    IndicatorsInfo,
    IndicatorsParams,
)
from FinMind.strategies.utils import (
    calculate_datenbr,
    calculate_sharp_ratio,
    days2years,
    get_asset_underlying_type,
    get_underlying_trading_tax,
    period_return2annual_return,
)
from FinMind.utility.rule import RULE_DICT


class Trader:
    def __init__(
        self,
        stock_id: str,
        trader_fund: float,
        hold_volume: float,
        hold_cost: float,
        fee: float,
        tax: float,
        board_lot: int = 1000,
    ):
        self.stock_id = stock_id
        self.trader_fund = trader_fund
        self.hold_volume = hold_volume
        self.hold_cost = hold_cost
        self.fee = fee
        self.tax = tax
        self.trade_price = None
        self.board_lot = board_lot
        self.UnrealizedProfit = 0
        self.RealizedProfit = 0
        self.EverytimeProfit = 0

    def buy(self, trade_price: float, trade_lots: float):
        self.trade_price = trade_price
        if (
            self.__confirm_trade_lots(trade_lots, trade_price, self.trader_fund)
            > 0
        ):
            trade_volume = trade_lots * self.board_lot
            buy_fee = max(20.0, self.trade_price * trade_volume * self.fee)
            buy_price = self.trade_price * trade_volume
            buy_total_price = buy_price + buy_fee
            self.trader_fund = self.trader_fund - buy_total_price
            origin_hold_cost = self.hold_volume * self.hold_cost
            self.hold_volume = self.hold_volume + trade_volume
            self.hold_cost = (
                origin_hold_cost + buy_total_price
            ) / self.hold_volume

        self.__compute_realtime_status()

    def sell(self, trade_price: float, trade_lots: float):
        self.trade_price = trade_price
        if (
            self.__confirm_trade_lots(trade_lots, trade_price, self.trader_fund)
            < 0
        ):
            trade_volume = abs(trade_lots) * self.board_lot
            sell_fee = max(20.0, trade_price * trade_volume * self.fee)
            sell_tax = trade_price * trade_volume * self.tax
            sell_price = trade_price * trade_volume
            sell_total_price = sell_price - sell_tax - sell_fee
            self.trader_fund = self.trader_fund + sell_total_price
            self.RealizedProfit = self.RealizedProfit + round(
                sell_total_price - (self.hold_cost * trade_volume),
                2,
            )
            self.hold_volume = self.hold_volume - trade_volume

        self.__compute_realtime_status()

    def no_action(self, trade_price: float):
        self.trade_price = trade_price
        self.__compute_realtime_status()

    def trade(self, signal: float, trade_price: float):
        if signal > 0:
            self.buy(trade_price=trade_price, trade_lots=signal)
        elif signal < 0:
            self.sell(trade_price=trade_price, trade_lots=signal)
        else:
            self.no_action(trade_price=trade_price)

    def __compute_realtime_status(self):
        sell_fee = max(20, self.trade_price * self.hold_volume * self.fee)
        sell_fee = sell_fee if self.hold_volume > 0 else 0
        sell_tax = self.trade_price * self.hold_volume * self.tax
        sell_price = self.trade_price * self.hold_volume
        capital_gains = sell_price - self.hold_cost * self.hold_volume
        self.UnrealizedProfit = capital_gains - sell_fee - sell_tax
        self.EverytimeProfit = self.UnrealizedProfit + self.RealizedProfit

    @staticmethod
    def __have_enough_money(
        trader_fund: int, trade_price: float, trade_volume: float
    ) -> bool:
        return trader_fund >= (trade_price * trade_volume)

    @staticmethod
    def __have_enough_volume(hold_volume: float, trade_volume: float) -> bool:
        if hold_volume < trade_volume:
            return False
        else:
            return True

    def __confirm_trade_lots(
        self, trade_lots: float, trade_price: float, trader_fund: int
    ):
        """
        do not have enough money --> not buy
        do not have enough lots --> not sell

        # TODO: in the future can expand
        if only have 4 los money, but buing 5 lots
            --> not buy, since money not enough, as the same as sell
        """
        final_trade_lots = 0
        trade_volume = abs(trade_lots) * self.board_lot
        if trade_lots > 0:
            if self.__have_enough_money(trader_fund, trade_price, trade_volume):
                final_trade_lots = trade_lots
            else:
                final_trade_lots = 0
        elif trade_lots < 0:
            hold_volume = self.hold_volume
            if self.__have_enough_volume(hold_volume, trade_volume):
                final_trade_lots = trade_lots
            else:
                final_trade_lots = 0
        return final_trade_lots


class Strategy:
    def __init__(
        self,
        trader: Trader,
        stock_id: str,
        start_date: str,
        end_date: str,
        data_loader: DataLoader,
    ):
        self.trader = trader
        self.stock_id = stock_id
        self.start_date = start_date
        self.end_date = end_date
        self.data_loader = data_loader
        self.load_strategy_data()

    def load_strategy_data(self):
        pass

    def trade(self, signal: float, trade_price: float):
        if signal > 0:
            self.buy(trade_price=trade_price, trade_lots=signal)
        elif signal < 0:
            self.sell(trade_price=trade_price, trade_lots=signal)
        else:
            self.no_action(trade_price=trade_price)

    def buy(self, trade_price: float, trade_lots: float):
        self.trader.buy(trade_price, trade_lots)

    def sell(self, trade_price: float, trade_lots: float):
        self.trader.sell(trade_price, trade_lots)

    def no_action(self, trade_price: float):
        self.trader.no_action(trade_price)


class BackTest:
    def __init__(
        self,
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        trader_fund: float = 0,
        fee: float = 0.001425,
        strategy: Strategy = None,
        data_loader: DataLoader = None,
        token: str = "",
    ):
        self.data_loader = data_loader if data_loader else DataLoader(token)
        self.stock_id = stock_id
        self.start_date = start_date
        self.end_date = end_date
        self.trader_fund = trader_fund
        self.fee = fee
        underlying_type = get_asset_underlying_type(stock_id, self.data_loader)
        self.tax = get_underlying_trading_tax(underlying_type)
        self.trader = Trader(
            stock_id=stock_id,
            hold_volume=0,
            hold_cost=0,
            trader_fund=trader_fund,
            fee=self.fee,
            tax=self.tax,
        )

        self.strategy = strategy
        self.stock_price = pd.DataFrame()
        self._trade_detail = pd.DataFrame()
        self._final_stats = pd.Series()
        self._sign_name_list = []
        self.buy_rule_list = []
        self.sell_rule_list = []
        self.__init_base_data()
        self._trade_period_years = days2years(
            calculate_datenbr(start_date, end_date) + 1
        )

        self._compare_market_detail = pd.DataFrame()
        self._compare_market_stats = pd.Series()

    def add_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def _add_indicators_formula(
        self,
        indicator: str,
        indicators_info: typing.Dict[str, typing.Union[str, int, float]],
    ):
        value = indicators_info.pop("formula_value", None)
        if value:
            if isinstance(value, list):
                params_list = ast.literal_eval(
                    getattr(IndicatorsParams, indicator).value
                )
                [
                    indicators_info.update({params: value.pop(0)})
                    for params in params_list
                ]
            else:
                indicators_info.update(
                    {getattr(IndicatorsParams, indicator).value: value}
                )
        return indicators_info

    def _convert_indicators_schema2dict(
        self,
        indicators_info: typing.Union[IndicatorsInfo, typing.Dict[str, str]],
    ):
        indicators_info = (
            indicators_info.dict()
            if isinstance(indicators_info, IndicatorsInfo)
            else indicators_info
        )
        indicator = (
            indicators_info["name"].name
            if isinstance(indicators_info["name"], Enum)
            else indicators_info["name"]
        )
        return indicators_info, indicator

    def add_indicators(
        self,
        indicators_info_list: typing.List[IndicatorsInfo],
    ):
        """add indicators
        :param indicators_info_list (List[FinMind.schema.indicators.IndicatorsInfo]):

        For example1: if add KD indicators, and set k_days=9

        [
            IndicatorsInfo(
                indicators=Indicators.KD,
                formula_value=9
            )
        ]

        For example2: if add BIAS indicators, and set ma_days=24

        [
            IndicatorsInfo(
                indicators=Indicators.BIAS,
                formula_value=24
            )
        ]
        """
        for indicators_info in indicators_info_list:
            indicators_info, indicator = self._convert_indicators_schema2dict(
                indicators_info
            )
            self._additional_dataset(indicator=indicator)
            logger.info(indicator)
            indicators_info = self._add_indicators_formula(
                indicator, indicators_info
            )
            func = indicators.INDICATORS_MAPPING.get(indicator)
            self.stock_price = func(
                self.stock_price, additional_dataset_obj=self, **indicators_info
            )

    def __convert_rule_schema2dict(
        self,
        rule_list: typing.List[
            typing.Union[AddBuySellRule, typing.Dict[str, str]]
        ],
    ):
        return [
            rule.dict() if isinstance(rule, AddBuySellRule) else rule
            for rule in rule_list
        ]

    def add_buy_rule(
        self,
        buy_rule_list: typing.List[AddBuySellRule],
    ):
        """add buy rule
        :param buy_rule_list (List[FinMind.schema.indicators.AddBuySellRule]):

        For example: if BIAS <= -7, then buy stock

        [
            AddBuySellRule(
                indicators=Indicators.BIAS,
                more_or_less_than=Rule.LessThan,
                threshold=-7,
            )
        ]

        or

        [
            AddBuySellRule(
                indicators=Indicators.BIAS,
                more_or_less_than="<",
                threshold=-7,
            )
        ]
        """
        self.buy_rule_list = self.__convert_rule_schema2dict(buy_rule_list)

    def add_sell_rule(
        self,
        sell_rule_list: typing.List[AddBuySellRule],
    ):
        """add sell rule
        :param sell_rule_list (List[FinMind.schema.indicators.AddBuySellRule]):

        For example: if BIAS >= 8, then sell stock

        [
            AddBuySellRule(
                indicators=Indicators.BIAS,
                more_or_less_than=Rule.MoreThan,
                threshold=8,
            )
        ]

        or

        [
            AddBuySellRule(
                indicators=Indicators.BIAS,
                more_or_less_than=">",
                threshold=8,
            )
        ]
        """
        self.sell_rule_list = self.__convert_rule_schema2dict(sell_rule_list)

    def _create_sign(
        self,
        sign_name: str,
        indicators: str,
        more_or_less_than: str,
        threshold: float,
    ):
        self.stock_price[sign_name] = 0
        self.stock_price.loc[
            self.stock_price[indicators].map(
                lambda _indicators: RULE_DICT[more_or_less_than](
                    _indicators, threshold
                )
            ),
            sign_name,
        ] = 1

    def _create_buy_sign(self):
        if len(self.buy_rule_list) > 0:
            self._sign_name_list.append("buy_sign")
            buy_sign_name_list = []
            for i in range(len(self.buy_rule_list)):
                sign_name = f"buy_signal_{i}"
                buy_sign_name_list.append(sign_name)
                self._create_sign(
                    sign_name=sign_name,
                    indicators=self.buy_rule_list[i]["indicators"],
                    more_or_less_than=self.buy_rule_list[i][
                        "more_or_less_than"
                    ],
                    threshold=self.buy_rule_list[i]["threshold"],
                )
            # if all of buy_sign_i are 1, then set buy_sign = 1
            self.stock_price["buy_sign"] = (
                self.stock_price[buy_sign_name_list].sum(axis=1)
                == len(buy_sign_name_list)
            ).astype(int)
            self.stock_price = self.stock_price.drop(buy_sign_name_list, axis=1)

    def _create_sell_sign(self):
        if len(self.sell_rule_list) > 0:
            self._sign_name_list.append("sell_sign")
            sell_sign_name_list = []
            for i in range(len(self.sell_rule_list)):
                sign_name = f"sell_signal_{i}"
                sell_sign_name_list.append(sign_name)
                self._create_sign(
                    sign_name=sign_name,
                    indicators=self.sell_rule_list[i]["indicators"],
                    more_or_less_than=self.sell_rule_list[i][
                        "more_or_less_than"
                    ],
                    threshold=self.sell_rule_list[i]["threshold"],
                )
            # if all of sell_sign_i are 1, then set sell_sign = 1
            self.stock_price["sell_sign"] = (
                self.stock_price[sell_sign_name_list].sum(axis=1)
                == len(sell_sign_name_list)
            ).astype(int) * -1
            self.stock_price = self.stock_price.drop(
                sell_sign_name_list, axis=1
            )

    def _create_trade_sign(self):
        logger.info("create_trade_sign")
        self._create_buy_sign()
        self._create_sell_sign()
        self.stock_price["signal"] = self.stock_price[self._sign_name_list].sum(
            axis=1
        )
        self.stock_price.loc[self.stock_price["signal"] >= 1, "signal"] = 1
        self.stock_price.loc[self.stock_price["signal"] <= -1, "signal"] = -1
        self.stock_price = self.stock_price.drop(self._sign_name_list, axis=1)

    def _additional_dataset(self, indicator: str):
        additional_dataset = getattr(AdditionalDataset, indicator, None)
        if additional_dataset:
            if getattr(self, additional_dataset.value, None) is None:
                df = self.data_loader.get_data(
                    dataset=additional_dataset,
                    data_id=self.stock_id,
                    start_date=self.start_date,
                    end_date=self.end_date,
                )
                setattr(self, additional_dataset.value, df)

    def __init_base_data(self):
        self.stock_price = self.data_loader.get_data(
            dataset=Dataset.TaiwanStockPrice,
            data_id=self.stock_id,
            start_date=self.start_date,
            end_date=self.end_date,
        )
        stock_dividend = self.data_loader.get_data(
            dataset=Dataset.TaiwanStockDividend,
            data_id=self.stock_id,
            start_date=self.start_date,
            end_date=self.end_date,
        )
        if not stock_dividend.empty:
            cash_div = stock_dividend[
                [
                    "stock_id",
                    "CashExDividendTradingDate",
                    "CashEarningsDistribution",
                ]
            ].rename(columns={"CashExDividendTradingDate": "date"})
            stock_div = stock_dividend[
                [
                    "stock_id",
                    "StockExDividendTradingDate",
                    "StockEarningsDistribution",
                ]
            ].rename(columns={"StockExDividendTradingDate": "date"})
            self.stock_price = pd.merge(
                self.stock_price,
                cash_div,
                left_on=["stock_id", "date"],
                right_on=["stock_id", "date"],
                how="left",
            ).fillna(0)
            self.stock_price = pd.merge(
                self.stock_price,
                stock_div,
                left_on=["stock_id", "date"],
                right_on=["stock_id", "date"],
                how="left",
            ).fillna(0)
        else:
            self.stock_price["StockEarningsDistribution"] = 0
            self.stock_price["CashEarningsDistribution"] = 0

    def simulate(self):
        if self.strategy:
            strategy = self.strategy(
                self.trader,
                self.stock_id,
                self.start_date,
                self.end_date,
                self.data_loader,
            )
            strategy.load_strategy_data()
            self.stock_price = strategy.create_trade_sign(
                stock_price=self.stock_price, additional_dataset_obj=self
            )
            assert (
                "signal" in self.stock_price.columns
            ), "Must be create signal columns in stock_price"
        else:
            self._create_trade_sign()
        if not self.stock_price.index.is_monotonic_increasing:
            warnings.warn(
                "data index is not sorted in ascending order. Sorting.",
                stacklevel=2,
            )
            self.stock_price = self.stock_price.sort_index()
        _trade_detail_dict_list = []
        for i in range(0, len(self.stock_price)):
            # use last date to decide buy or sell or nothing
            last_date_index = i - 1
            signal = (
                self.stock_price.loc[last_date_index, "signal"] if i != 0 else 0
            )
            trade_price = self.stock_price.loc[i, "open"]
            # 買賣之前，先進行配息配股
            cash_div = self.stock_price.loc[i, "CashEarningsDistribution"]
            stock_div = self.stock_price.loc[i, "StockEarningsDistribution"]
            self.__compute_div_income(self.trader, cash_div, stock_div)
            self.trader.trade(signal, trade_price)
            _trade_detail_dict_list.append(
                dict(
                    CashEarningsDistribution=cash_div,
                    StockEarningsDistribution=stock_div,
                    signal=signal,
                    **self.trader.__dict__,
                )
            )

        self._trade_detail = pd.DataFrame(_trade_detail_dict_list)
        self._trade_detail["date"] = self.stock_price["date"]
        self._trade_detail = self._trade_detail.drop(["fee", "tax"], axis=1)
        self._trade_detail["EverytimeTotalProfit"] = (
            self._trade_detail["trader_fund"]
            + self._trade_detail["EverytimeProfit"]
        )
        self.__compute_final_stats()
        self.__compute_compare_market()

    @staticmethod
    def __compute_div_income(trader, cash_div: float, stock_div: float):
        # 股票股利畸零股應被直接換算成現金
        gain_stock_div = stock_div * trader.hold_volume / 10
        gain_stock_frac = gain_stock_div % 1  # 取 gain_stock_div 小數部分
        gain_stock_div = (
            gain_stock_div - gain_stock_frac
        )  # gain_stock_div 只留整數部分
        gain_cash = (
            cash_div * trader.hold_volume + gain_stock_frac * 10
        )  # 將小數部分加進 gain_cash
        trader.hold_volume += gain_stock_div
        # 在 UnrealizedProfit & RealizedProfit
        # 避免重複計算 gain_cash
        origin_cost = trader.hold_cost * trader.hold_volume
        # 持有成本不變，將配息歸類在，已實現損益
        # new_cost = origin_cost - gain_cash
        trader.hold_cost = (
            origin_cost / trader.hold_volume if trader.hold_volume != 0 else 0
        )
        trader.UnrealizedProfit = (
            round(
                (
                    trader.trade_price * (1 - trader.tax - trader.fee)
                    - trader.hold_cost
                )
                * trader.hold_volume,
                2,
            )
            if trader.trade_price
            else 0
        )
        trader.RealizedProfit += gain_cash
        # 將配息也要增加資金池
        trader.trader_fund += gain_cash
        trader.EverytimeProfit = trader.RealizedProfit + trader.UnrealizedProfit

    def __compute_final_stats(self):
        self._final_stats["MeanProfit"] = np.mean(
            self._trade_detail["EverytimeProfit"]
        )
        self._final_stats["MaxLoss"] = np.min(
            self._trade_detail["EverytimeProfit"]
        )
        self._final_stats["FinalProfit"] = self._trade_detail[
            "EverytimeProfit"
        ].values[-1]
        self._final_stats["MeanProfitPer"] = round(
            self._final_stats["MeanProfit"] / self.trader_fund * 100, 2
        )
        self._final_stats["FinalProfitPer"] = round(
            self._final_stats["FinalProfit"] / self.trader_fund * 100, 2
        )
        self._final_stats["MaxLossPer"] = round(
            self._final_stats["MaxLoss"] / self.trader_fund * 100, 2
        )
        self._final_stats["AnnualReturnPer"] = round(
            period_return2annual_return(
                self._final_stats["FinalProfitPer"] / 100,
                self._trade_period_years,
            )
            * 100,
            2,
        )
        time_step_returns = (
            self._trade_detail["EverytimeProfit"]
            - self._trade_detail["EverytimeProfit"].shift(1)
        ) / (self._trade_detail["EverytimeProfit"].shift(1) + self.trader_fund)
        strategy_return = np.mean(time_step_returns)
        strategy_std = np.std(time_step_returns)
        self._final_stats["AnnualSharpRatio"] = calculate_sharp_ratio(
            strategy_return, strategy_std
        )

    # TODO:
    # future can compare with diff market, such as America, China
    # now only Taiwan
    def __compute_compare_market(self):
        self._compare_market_detail = self._trade_detail[
            ["date", "EverytimeTotalProfit"]
        ].copy()
        self._compare_market_detail["CumDailyReturn"] = (
            np.log(self._compare_market_detail["EverytimeTotalProfit"])
            - np.log(
                self._compare_market_detail["EverytimeTotalProfit"].shift(1)
            )
        ).fillna(0)
        self._compare_market_detail["CumDailyReturn"] = round(
            self._compare_market_detail["CumDailyReturn"].cumsum(), 5
        )
        tai_ex = self.data_loader.get_data(
            dataset="TaiwanStockPrice",
            data_id="TAIEX",
            start_date=self.start_date,
            end_date=self.end_date,
        )[["date", "close"]]

        tai_ex["CumTaiExDailyReturn"] = (
            np.log(tai_ex["close"]) - np.log(tai_ex["close"].shift(1))
        ).fillna(0)
        tai_ex["CumTaiExDailyReturn"] = round(
            tai_ex["CumTaiExDailyReturn"].cumsum(), 5
        )
        self._compare_market_detail = pd.merge(
            self._compare_market_detail,
            tai_ex[["date", "CumTaiExDailyReturn"]],
            on=["date"],
            how="left",
        )
        self._compare_market_detail = self._compare_market_detail.dropna()
        self._compare_market_stats = pd.Series()
        self._compare_market_stats["AnnualTaiexReturnPer"] = (
            period_return2annual_return(
                self._compare_market_detail["CumTaiExDailyReturn"].values[-1],
                self._trade_period_years,
            )
            * 100
        )
        self._compare_market_stats["AnnualReturnPer"] = self._final_stats[
            "AnnualReturnPer"
        ]

    @property
    def final_stats(self) -> pd.Series:
        self._final_stats = pd.Series(
            FinalStats(**self._final_stats.to_dict()).dict()
        )
        return self._final_stats

    @property
    def trade_detail(self) -> pd.DataFrame:
        self._trade_detail = pd.DataFrame(
            [
                TradeDetail(**row_dict).dict()
                for row_dict in self._trade_detail.to_dict("records")
            ]
        )
        return self._trade_detail

    @property
    def compare_market_detail(self) -> pd.DataFrame:
        self._compare_market_detail = pd.DataFrame(
            [
                CompareMarketDetail(**row_dict).dict()
                for row_dict in self._compare_market_detail.to_dict("records")
            ]
        )
        return self._compare_market_detail

    @property
    def compare_market_stats(self) -> pd.Series:
        self._compare_market_stats = pd.Series(
            CompareMarketStats(**self._compare_market_stats.to_dict()).dict()
        )
        return self._compare_market_stats

    def plot(
        self,
        title: str = "Backtest Result",
        x_label: str = "Time",
        y_label: str = "Profit",
        grid: bool = True,
    ):
        try:
            import matplotlib.gridspec as gridspec
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("You must install matplotlib to plot importance")

        fig = plt.figure(figsize=(12, 8))
        gs = gridspec.GridSpec(4, 1, figure=fig)
        ax = fig.add_subplot(gs[:2, :])
        xpos = self._trade_detail.index
        ax.plot(
            "UnrealizedProfit", data=self._trade_detail, marker="", alpha=0.8
        )
        ax.plot("RealizedProfit", data=self._trade_detail, marker="", alpha=0.8)
        ax.plot(
            "EverytimeProfit", data=self._trade_detail, marker="", alpha=0.8
        )
        ax.grid(grid)
        ax.legend(loc=2)
        axx = ax.twinx()
        axx.bar(
            xpos,
            self._trade_detail["hold_volume"],
            alpha=0.2,
            label="hold_volume",
            color="pink",
        )
        axx.legend(loc=3)
        ax2 = fig.add_subplot(gs[2:, :], sharex=ax)
        ax2.plot(
            "trade_price",
            data=self._trade_detail,
            marker="",
            label="open",
            alpha=0.8,
        )
        ax2.plot(
            "hold_cost",
            data=self._trade_detail,
            marker="",
            label="hold_cost",
            alpha=0.8,
        )
        # TODO: add signal plot
        ax2.legend(loc=2)
        ax2.grid(grid)
        if title is not None:
            ax.set_title(title)
        if x_label is not None:
            ax.set_xlabel(x_label)
        if y_label is not None:
            ax.set_ylabel(y_label)
        plt.show()
