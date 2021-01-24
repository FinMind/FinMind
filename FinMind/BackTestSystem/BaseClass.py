import typing
import warnings

import numpy as np
import pandas as pd
from FinMind.BackTestSystem.utils import (
    get_asset_underlying_type,
    get_underlying_trading_tax,
    calculate_Datenbr,
    calculate_sharp_ratio,
    convert_Return2Annual,
    convert_period_days2years,
)
from FinMind.Data.Load import FinData
from FinMind.Schema import output


class Trader:
    def __init__(
        self,
        stock_id: str,
        trader_fund: int,
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
            buy_fee = max(20, self.trade_price * trade_volume * self.fee)
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
            sell_fee = max(20, trade_price * trade_volume * self.fee)
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

    def noaction(self, trade_price: float):
        self.trade_price = trade_price
        self.__compute_realtime_status()

    def __compute_realtime_status(self):
        sell_fee = max(20, self.trade_price * self.hold_volume * self.fee)
        sell_fee = sell_fee if self.hold_volume > 0 else 0
        sell_tax = self.trade_price * self.hold_volume * self.tax
        sell_price = self.trade_price * self.hold_volume
        capital_gains = sell_price - self.hold_cost * self.hold_volume
        self.UnrealizedProfit = capital_gains - sell_fee - sell_tax
        self.EverytimeProfit = self.UnrealizedProfit + self.RealizedProfit

    def __have_enough_money(
        self, trader_fund: int, trade_price: float, trade_volume: int
    ) -> bool:
        if trader_fund < (trade_price * trade_volume):
            return False
        else:
            return True

    def __have_enough_volume(
        self, hold_volume: float, trade_volume: int
    ) -> bool:
        if hold_volume < trade_volume:
            return False
        else:
            return True

    def __confirm_trade_lots(
        self, trade_lots: int, trade_price: float, trader_fund: int
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
        self, trader: Trader, stock_id: str, start_date: str, end_date: str
    ):
        self.trader = trader
        self.stock_id = stock_id
        self.start_date = start_date
        self.end_date = end_date

    def trade(self, signal: float, trade_price: float):
        if signal > 0:
            self.buy(trade_price=trade_price, trade_lots=signal)
        elif signal < 0:
            self.sell(trade_price=trade_price, trade_lots=signal)
        else:
            self.noaction(trade_price=trade_price)

    def buy(self, trade_price: float, trade_lots: float):
        self.trader.buy(trade_price, trade_lots)

    def sell(self, trade_price: float, trade_lots: float):
        self.trader.sell(trade_price, trade_lots)

    def noaction(self, trade_price: float):
        self.trader.noaction(trade_price)


class BackTest:
    def __init__(
        self,
        user_id: str = "",
        password: str = "",
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        trader_fund: float = 0,
        fee: float = 0.001425,
        strategy: Strategy = None,
    ):
        self.stock_id = stock_id
        self.start_date = start_date
        self.end_date = end_date
        self.trader_fund = trader_fund
        self.fee = fee
        underlying_type = get_asset_underlying_type(stock_id)
        self.tax = get_underlying_trading_tax(underlying_type)
        self.trader = Trader(
            stock_id=stock_id,
            hold_volume=0,
            hold_cost=0,
            trader_fund=trader_fund,
            fee=self.fee,
            tax=self.tax,
        )
        self.user_id = user_id
        self.password = password
        self.strategy = strategy
        self.stock_price = pd.DataFrame()
        self._trade_detail = pd.DataFrame()
        self._final_stats = pd.Series()
        self.__init_base_data()
        self._trade_period_years = convert_period_days2years(
            calculate_Datenbr(start_date, end_date) + 1
        )
        self._compare_market_detail = pd.DataFrame()
        self._compare_market_stats = pd.Series()

    def add_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def __init_base_data(self) -> pd.DataFrame:
        self.stock_price = FinData(
            dataset="TaiwanStockPrice",
            select=self.stock_id,
            date=self.start_date,
            end_date=self.end_date,
            user_id=self.user_id,
            password=self.password,
        )
        StockDividend = FinData(
            dataset="StockDividend",
            select=self.stock_id,
            date=self.start_date,
            end_date=self.end_date,
            user_id=self.user_id,
            password=self.password,
        )
        if not StockDividend.empty:
            cash_div = StockDividend[
                [
                    "stock_id",
                    "CashExDividendTradingDate",
                    "CashEarningsDistribution",
                ]
            ].rename(columns={"CashExDividendTradingDate": "date"})
            stock_div = StockDividend[
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
        trader = self.trader
        strategy = self.strategy(
            trader, self.stock_id, self.start_date, self.end_date
        )
        self.stock_price = strategy.create_trade_sign(
            stock_price=self.stock_price
        )
        assert (
            "signal" in self.stock_price.columns
        ), "Must be create signal columns in stock_price"
        if not self.stock_price.index.is_monotonic_increasing:
            warnings.warn(
                "Data index is not sorted in ascending order. Sorting.",
                stacklevel=2,
            )
            self.stock_price = self.stock_price.sort_index()
        for i in range(0, len(self.stock_price)):
            # use last date to decide buy or sell or nothing
            last_date_index = i - 1
            signal = (
                self.stock_price.loc[last_date_index, "signal"] if i != 0 else 0
            )
            trade_price = self.stock_price.loc[i, "open"]
            strategy.trade(signal, trade_price)
            cash_div = self.stock_price.loc[i, "CashEarningsDistribution"]
            stock_div = self.stock_price.loc[i, "StockEarningsDistribution"]
            self.__compute_div_income(strategy.trader, cash_div, stock_div)
            dic_value = strategy.trader.__dict__
            dic_value = {
                k: v for k, v in dic_value.items() if k not in ["tax", "fee"]
            }
            dic_value["date"] = self.stock_price.loc[i, "date"]
            dic_value["signal"] = self.stock_price.loc[i, "signal"]
            self._trade_detail = self._trade_detail.append(
                dic_value, ignore_index=True
            )

        self._trade_detail["EverytimeTotalProfit"] = (
            self._trade_detail["trader_fund"]
            + self._trade_detail["EverytimeProfit"]
        )
        self.__compute_final_stats()
        self.__compute_compare_market()

    def __compute_div_income(self, trader, cash_div: float, stock_div: float):
        gain_stock_div = stock_div * trader.hold_volume / 10
        gain_cash = cash_div * trader.hold_volume
        origin_cost = trader.hold_cost * trader.hold_volume
        trader.hold_volume += gain_stock_div
        new_cost = origin_cost - gain_cash
        trader.hold_cost = (
            new_cost / trader.hold_volume if trader.hold_volume != 0 else 0
        )
        trader.UnrealizedProfit = round(
            (
                trader.trade_price * (1 - trader.tax - trader.fee)
                - trader.hold_cost
            )
            * trader.hold_volume,
            2,
        )
        trader.RealizedProfit += gain_cash
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
            convert_Return2Annual(
                self._final_stats["FinalProfitPer"] / 100,
                self._trade_period_years,
            )
            * 100,
            2,
        )
        timestep_returns = (
            self._trade_detail["EverytimeProfit"]
            - self._trade_detail["EverytimeProfit"].shift(1)
        ) / (self._trade_detail["EverytimeProfit"].shift(1) + self.trader_fund)
        stratagy_return = np.mean(timestep_returns)
        stratagy_std = np.std(timestep_returns)
        self._final_stats["AnnualSharpRatio"] = calculate_sharp_ratio(
            stratagy_return, stratagy_std
        )

    # TODO:
    # future can compare with diff market, such as America, China
    # now only Taiwan
    def __compute_compare_market(self):
        self._compare_market_detail = self._trade_detail[
            ["date", "EverytimeTotalProfit"]
        ].copy()
        self._compare_market_detail["CumDailyRetrun"] = (
            np.log(self._compare_market_detail["EverytimeTotalProfit"])
            - np.log(
                self._compare_market_detail["EverytimeTotalProfit"].shift(1)
            )
        ).fillna(0)
        self._compare_market_detail["CumDailyRetrun"] = round(
            self._compare_market_detail["CumDailyRetrun"].cumsum(), 5
        )

        TAIEX = FinData(
            dataset="TaiwanStockPrice",
            select="TAIEX",
            date=self.start_date,
            end_date=self.end_date,
            user_id=self.user_id,
            password=self.password,
        )[["date", "close"]]
        TAIEX["CumTaiexDailyRetrun"] = (
            np.log(TAIEX["close"]) - np.log(TAIEX["close"].shift(1))
        ).fillna(0)
        TAIEX["CumTaiexDailyRetrun"] = round(
            TAIEX["CumTaiexDailyRetrun"].cumsum(), 5
        )
        self._compare_market_detail = pd.merge(
            self._compare_market_detail,
            TAIEX[["date", "CumTaiexDailyRetrun"]],
            on=["date"],
            how="left",
        )

        self._compare_market_stats = pd.Series()
        self._compare_market_stats["AnnualTaiexReturnPer"] = (
            convert_Return2Annual(
                self._compare_market_detail["CumTaiexDailyRetrun"].values[-1],
                self._trade_period_years,
            )
            * 100
        )
        self._compare_market_stats["AnnualReturnPer"] = self._final_stats[
            "AnnualReturnPer"
        ]

    @property
    def final_stats(self) -> pd.Series():
        self._final_stats = pd.Series(
            output.final_stats(**self._final_stats.to_dict()).dict()
        )
        return self._final_stats

    @property
    def trade_detail(self) -> pd.DataFrame():
        self._trade_detail = pd.DataFrame(
            [
                output.trade_detail(**row_dict).dict()
                for row_dict in self._trade_detail.to_dict("records")
            ]
        )
        return self._trade_detail

    @property
    def compare_market_detail(self) -> pd.DataFrame():
        self._compare_market_detail = pd.DataFrame(
            [
                output.compare_market_detail(**row_dict).dict()
                for row_dict in self._compare_market_detail.to_dict("records")
            ]
        )
        return self._compare_market_detail

    @property
    def compare_market_stats(self) -> pd.Series():
        self._compare_market_stats = pd.Series(
            output.compare_market_stats(
                **self._compare_market_stats.to_dict()
            ).dict()
        )
        return self._compare_market_stats

    def plot(
        self,
        title: str = "Backtest Result",
        xlabel: str = "Time",
        ylabel: str = "Profit",
        grid: bool = True,
    ):
        try:
            import matplotlib.pyplot as plt
            import matplotlib.gridspec as gridspec
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
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
        plt.show()
