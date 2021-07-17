import warnings

import numpy as np
import pandas as pd

from FinMind.data import DataLoader
from FinMind.schema import (
    CompareMarketDetail,
    CompareMarketStats,
    FinalStats,
    TradeDetail,
)
from FinMind.schema.data import Dataset
from FinMind.strategies.utils import (
    calculate_datenbr,
    calculate_sharp_ratio,
    days2years,
    get_asset_underlying_type,
    get_underlying_trading_tax,
    period_return2annual_return,
)


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
        self.orderlists = []
        self.positionlists = [{"hold_volume":0, "trader_fund":self.trader_fund, "hold_cost":0}]

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

            order = {"trade_volume":trade_volume, "trade_price":trade_price, "trade_fee":buy_fee}
            last_postion = self.positionlists[-1]
            position = {
                "hold_volume":last_postion["hold_volume"]+trade_volume,
                "trader_fund":last_postion["trader_fund"]-buy_total_price,
                "hold_cost":(
                    last_postion["hold_cost"]*last_postion["hold_volume"] + buy_total_price) / (last_postion["hold_volume"] + trade_volume
                )
            }
            self.orderlists.append(order)
            self.positionlists.append(position)

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

            order = {"trade_volume": trade_lots * self.board_lot, "trade_price":trade_price, "trade_fee":sell_fee}
            last_postion = self.positionlists[-1]
            position = {
                "hold_volume":last_postion["hold_volume"]-trade_volume,
                "trader_fund":last_postion["trader_fund"]-sell_total_price,
                "hold_cost":(
                    last_postion["hold_cost"]*last_postion["hold_volume"] - sell_total_price) / (last_postion["hold_volume"] - trade_volume)
            }
            self.orderlists.append(order)
            self.positionlists.append(position)

        self.__compute_realtime_status()

    def no_action(self, trade_price: float):
        self.trade_price = trade_price
        self.__compute_realtime_status()
        order = {"trade_volume":0, "trade_price":trade_price, "trade_fee":0}
        position = self.positionlists[-1]
        self.orderlists.append(order)
        self.positionlists.append(position)

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

    def compute_div_income(self, cash_div: float, stock_div: float):
        position = self.positionlists.pop()

        gain_stock_div = stock_div * position["hold_volume"] / 10 #TODO: need check
        gain_cash = cash_div * position["hold_volume"]
        position["hold_volume"] += gain_stock_div
        origin_cost = position["hold_cost"] * position["hold_volume"]
        new_cost = origin_cost - gain_cash

        position["hold_cost"] = (
            new_cost / position["hold_volume"] if position["hold_volume"] != 0 else 0
        )
        self.positionlists.append(position)
        # trader.UnrealizedProfit = round(
        #     (
        #         trader.trade_price * (1 - trader.tax - trader.fee)
        #         - trader.hold_cost
        #     )
        #     * trader.hold_volume,
        #     2,
        # )
        # trader.RealizedProfit += gain_cash
        # trader.EverytimeProfit = trader.RealizedProfit + trader.UnrealizedProfit

    @property
    def position(self):
        return pd.DataFrame(self.positionlists[1:])

    @property
    def orders(self):
        return pd.DataFrame(self.orderlists)


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

    def buy(self, trade_price: float, trade_lots: float):
        self.trader.buy(trade_price, trade_lots)

    def sell(self, trade_price: float, trade_lots: float):
        self.trader.sell(trade_price, trade_lots)

    def no_action(self, trade_price: float):
        self.trader.no_action(trade_price)

    def next(self):
        pass

    @property
    def position(self):
        return pd.concat([self.indicator[["date", "stock_id"]], pd.DataFrame(self.trader.positionlists[1:])], axis=1)

    @property
    def orders(self):
        return pd.concat([self.indicator[["date", "stock_id"]], pd.DataFrame(self.trader.orderlists)], axis=1)


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
    ):
        self.data_loader = data_loader
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
        # self._trade_detail = pd.DataFrame()
        self.summary = pd.DataFrame()
        self._final_stats = pd.Series()
        self.__init_base_data()
        self._trade_period_years = days2years(
            calculate_datenbr(start_date, end_date) + 1
        )

        self._compare_market_detail = pd.DataFrame()
        self._compare_market_stats = pd.Series()

    def add_strategy(self, strategy: Strategy):
        self.strategy = strategy

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
        self.div = self.stock_price[["date", "stock_id"]].copy()
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

            self.div = pd.merge(
                self.div,
                cash_div,
                left_on=["stock_id", "date"],
                right_on=["stock_id", "date"],
                how="left",
            ).fillna(0)
            self.div = pd.merge(
                self.div,
                stock_div,
                left_on=["stock_id", "date"],
                right_on=["stock_id", "date"],
                how="left",
            ).fillna(0)
        else:
            self.div["StockEarningsDistribution"] = 0
            self.div["CashEarningsDistribution"] = 0

    def simulate(self):
        strategy = self.strategy(
            self.trader,
            self.stock_id,
            self.start_date,
            self.end_date,
            self.data_loader,
        )
        strategy.load_strategy_data()
        self.indicator = strategy.create_trade_sign(
            stock_price=self.stock_price.copy()
        )
        if not self.stock_price.index.is_monotonic_increasing:
            warnings.warn(
                "data index is not sorted in ascending order. Sorting.",
                stacklevel=2,
            )
            self.stock_price = self.stock_price.sort_index()
        for i in range(0, len(self.stock_price)):
            setattr(strategy, "stock_price", self.stock_price[i:i+1][["date", "stock_id", "open", "max", "min", "close"]])
            setattr(strategy, "indicator", self.indicator[:i]) # only have information before i day

            strategy.next()

            cash_div = self.div.loc[i, "CashEarningsDistribution"]
            stock_div = self.div.loc[i, "StockEarningsDistribution"]
            if cash_div or stock_div:
                strategy.trader.compute_div_income(cash_div, stock_div)

        '''
        summary
        # EverytimeProfit: stock_price + position
        # UnrealizedProfit: stock_price + position
        # RealizedProfit: order + position

        '''
        summary = pd.concat([self.indicator[["date", "stock_id", "close"]], self.trader.position], axis=1)
        sell_fee = np.maximum(20, summary["close"]*summary["hold_volume"]*0.001425)
        sell_tax = summary["close"]*summary["hold_volume"]* 0.001
        sell_feedback = summary["hold_volume"] * summary["close"]
        summary["EverytimeTotalProfit"] = (
            sell_feedback - sell_fee - sell_tax + summary["trader_fund"]
        )
        summary["UnrealizedProfit"] = (
            summary["hold_volume"] * (summary["close"]-summary["hold_cost"]) - sell_fee - sell_tax
        )

        summary = pd.concat([summary, self.trader.orders], axis=1)
        summary["RealizedProfit"] = abs(summary["trade_volume"]) * (summary["trade_price"]-summary["hold_cost"])
        summary["RealizedProfit"] = summary["RealizedProfit"] * (summary["trade_volume"] < 0).astype(int)

        summary["EverytimeProfit"] = summary["RealizedProfit"] + summary["UnrealizedProfit"]
        self.summary = summary

        self.__compute_final_stats()
        self.__compute_compare_market()

    def __compute_final_stats(self):
        self._final_stats["MeanProfit"] = np.mean(
            self.summary["EverytimeProfit"]
        )
        self._final_stats["MaxLoss"] = np.min(
            self.summary["EverytimeProfit"]
        )
        self._final_stats["FinalProfit"] = self.summary[
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
            self.summary["EverytimeProfit"]
            - self.summary["EverytimeProfit"].shift(1)
        ) / (self.summary["EverytimeProfit"].shift(1) + self.trader_fund)
        strategy_return = np.mean(time_step_returns)
        strategy_std = np.std(time_step_returns)
        self._final_stats["AnnualSharpRatio"] = calculate_sharp_ratio(
            strategy_return, strategy_std
        )

    # TODO:
    # future can compare with diff market, such as America, China
    # now only Taiwan
    def __compute_compare_market(self):
        self._compare_market_detail = self.summary[
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
    def final_stats(self) -> pd.Series():
        self._final_stats = pd.Series(
            FinalStats(**self._final_stats.to_dict()).dict()
        )
        return self._final_stats

    @property
    def trade_detail(self) -> pd.DataFrame():
        self.summary = pd.DataFrame(
            [
                TradeDetail(**row_dict).dict()
                for row_dict in self.summary.to_dict("records")
            ]
        )
        return self.summary

    @property
    def compare_market_detail(self) -> pd.DataFrame():
        self._compare_market_detail = pd.DataFrame(
            [
                CompareMarketDetail(**row_dict).dict()
                for row_dict in self._compare_market_detail.to_dict("records")
            ]
        )
        return self._compare_market_detail

    @property
    def compare_market_stats(self) -> pd.Series():
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
            import matplotlib.pyplot as plt
            import matplotlib.gridspec as gridspec
        except ImportError:
            raise ImportError("You must install matplotlib to plot importance")

        fig = plt.figure(figsize=(12, 8))
        gs = gridspec.GridSpec(4, 1, figure=fig)
        ax = fig.add_subplot(gs[:2, :])
        xpos = self.summary.index
        ax.plot(
            "UnrealizedProfit", data=self.summary, marker="", alpha=0.8
        )
        ax.plot("RealizedProfit", data=self.summary, marker="", alpha=0.8)
        ax.plot(
            "EverytimeProfit", data=self.summary, marker="", alpha=0.8
        )
        ax.grid(grid)
        ax.legend(loc=2)
        axx = ax.twinx()
        axx.bar(
            xpos,
            self.summary["hold_volume"],
            alpha=0.2,
            label="hold_volume",
            color="pink",
        )
        axx.legend(loc=3)
        ax2 = fig.add_subplot(gs[2:, :], sharex=ax)
        ax2.plot(
            "trade_price",
            data=self.summary,
            marker="",
            label="open",
            alpha=0.8,
        )
        ax2.plot(
            "hold_cost",
            data=self.summary,
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
