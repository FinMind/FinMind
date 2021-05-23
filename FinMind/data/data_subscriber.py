import asyncio
import json
import sys
from enum import Enum
from threading import Thread

import aiohttp
from aiohttp import WSMsgType
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


class Stock(str, Enum):
    Tick = "taiwan_stock_price_tick"
    BidAsk = "taiwan_stock_price_bidask"


class FutureAndOption(str, Enum):
    Tick = "taiwan_futopt_price_tick"


class DataSubscriber:
    def __init__(self, testing: bool = False):
        '''
        :param: testing (bool) If true, test for websocket
        '''
        wss_url = "wss://api.finmindtrade.com/api/v4/websocket/"
        self._ws_main_url = f"{wss_url}test/" if testing else wss_url
        self._loop = asyncio.new_event_loop()
        self._event_thread = Thread(
            target=self._start_background_loop, args=(self._loop,)
        )
        self._event_thread.start()
        self._subscripting_product = {}

    @staticmethod
    def _start_background_loop(loop: asyncio.AbstractEventLoop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def _connect_ws(self, url: str, cb):
        session = aiohttp.ClientSession(loop=self._loop)
        try:
            async with session.ws_connect(url) as ws:
                async for msg in ws:
                    if msg.type == WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        cb(data)
                    elif msg.type == WSMsgType.ERROR:
                        break
                    elif msg.type == WSMsgType.CLOSE:
                        break
        except Exception as e:
            logger.error(e)
        finally:
            await session.close()

    def subscribe(
        self,
        product_id: str,
        product_type: Enum,
        cb=lambda message: print(message),
    ):
        """
        :param product_id: 商品代號("2330")
        :param product_type: 商品訂閱種類(Stock.Tick)
        :param cb: 回調函數
        """
        if product_id in self._subscripting_product:
            logger.warning(
                f"product:{product_id} {product_type.name} already subscribe"
            )
            return

        url = self._ws_main_url + product_type.value + "?data_id=" + product_id
        self._subscripting_product[
            product_id + product_type.value
        ] = asyncio.run_coroutine_threadsafe(
            self._connect_ws(url, cb), self._loop
        )
        logger.info(
            f"product:{product_id} {product_type.name} subscribe success"
        )

    def unsubscribe(self, product_id, product_type: Enum):
        """
        :param product_id: 商品代號("2330")
        :param product_type: 商品訂閱種類(Stock.Tick)
        """
        subscripting_id = product_id + product_type.value
        task = self._subscripting_product.get(subscripting_id)
        if task:
            task.cancel()
            self._subscripting_product.pop(subscripting_id)
            logger.info(
                f"product:{product_id} {product_type.name} unsubscribe success"
            )
        else:
            logger.warning(
                f"product:{product_id} {product_type.name} are not subscribe"
            )

    def close(self):
        for task in self._subscripting_product.values():
            task.cancel()
        self._subscripting_product = {}
        logger.info("DataSubscriber close")
