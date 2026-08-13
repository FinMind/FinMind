import asyncio
from unittest.mock import Mock

import pytest

from FinMind.data.data_subscriber import DataSubscriber, Stock


@pytest.fixture
def subscriber(monkeypatch):
    subscriber = DataSubscriber.__new__(DataSubscriber)
    subscriber._ws_main_url = "wss://example.test/"
    subscriber._loop = Mock()
    subscriber._subscripting_contract = {}
    scheduled_futures = []

    def schedule(coroutine, loop):
        coroutine.close()
        future = Mock()
        scheduled_futures.append(future)
        return future

    monkeypatch.setattr(asyncio, "run_coroutine_threadsafe", schedule)
    return subscriber, scheduled_futures


def test_subscribe_ignores_duplicate_contract_and_type(subscriber):
    data_subscriber, scheduled_futures = subscriber

    data_subscriber.subscribe("2330", Stock.Tick)
    data_subscriber.subscribe("2330", Stock.Tick)

    assert len(scheduled_futures) == 1
    assert list(data_subscriber._subscripting_contract) == [
        "2330taiwan_stock_price_tick"
    ]


def test_subscribe_allows_different_types_for_same_contract(subscriber):
    data_subscriber, scheduled_futures = subscriber

    data_subscriber.subscribe("2330", Stock.Tick)
    data_subscriber.subscribe("2330", Stock.BidAsk)

    assert len(scheduled_futures) == 2
    assert set(data_subscriber._subscripting_contract) == {
        "2330taiwan_stock_price_tick",
        "2330taiwan_stock_price_bidask",
    }


def test_unsubscribe_cancels_scheduled_future(subscriber):
    data_subscriber, scheduled_futures = subscriber
    data_subscriber.subscribe("2330", Stock.Tick)

    data_subscriber.unsubscribe("2330", Stock.Tick)

    scheduled_futures[0].cancel.assert_called_once_with()
    assert data_subscriber._subscripting_contract == {}
