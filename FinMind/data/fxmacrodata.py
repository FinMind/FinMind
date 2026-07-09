import json
import os
import typing
import urllib.error
import urllib.parse
import urllib.request

import pandas as pd


Params = typing.Mapping[str, typing.Any]


class FXMacroDataApi:
    """Small FXMacroData REST client that returns FinMind-friendly data frames."""

    DEFAULT_BASE_URL = "https://fxmacrodata.com/api/v1/"

    def __init__(
        self,
        api_key: str = "",
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 30,
    ):
        self.api_key = (
            api_key
            or os.getenv("FXMACRODATA_API_KEY", "")
            or os.getenv("FXMD_API_KEY", "")
        )
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout

    def request(
        self,
        path: str,
        params: typing.Optional[Params] = None,
        timeout: typing.Optional[int] = None,
    ) -> typing.Dict[str, typing.Any]:
        query = dict(params or {})
        if self.api_key:
            query["api_key"] = self.api_key
        url = urllib.parse.urljoin(self.base_url, path.lstrip("/"))
        if query:
            url = url + "?" + urllib.parse.urlencode(query)

        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as resp:
                payload = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                "FXMacroData request failed with HTTP {}: {}".format(
                    exc.code, body
                )
            )
        return json.loads(payload)

    def data_catalogue(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("data_catalogue/" + currency.lower(), params))

    def announcements(
        self, currency: str, indicator: str, **params
    ) -> pd.DataFrame:
        path = "announcements/{}/{}".format(currency.lower(), indicator)
        return self._frame(self.request(path, params))

    def latest_announcements(self, currency: str, **params) -> pd.DataFrame:
        path = "announcements/{}/latest".format(currency.lower())
        return self._frame(self.request(path, params))

    def announcement_changes(self, **params) -> pd.DataFrame:
        return self._frame(self.request("announcements/changes", params))

    def calendar(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("calendar/" + currency.lower(), params))

    def predictions(
        self, currency: str, indicator: str, **params
    ) -> pd.DataFrame:
        path = "predictions/{}/{}".format(currency.lower(), indicator)
        return self._frame(self.request(path, params))

    def forex(self, base: str, quote: str = "usd", **params) -> pd.DataFrame:
        path = "forex/{}/{}".format(base.lower(), quote.lower())
        return self._frame(self.request(path, params))

    def cot(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("cot/" + currency.lower(), params))

    def commodity(self, indicator: str, **params) -> pd.DataFrame:
        return self._frame(self.request("commodities/" + indicator, params))

    def commodities_latest(self, **params) -> pd.DataFrame:
        return self._frame(self.request("commodities/latest", params))

    def curves(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("curves/" + currency.lower(), params))

    def curve_proxies(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("curve_proxies/" + currency.lower(), params))

    def forward_curves(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("forward_curves/" + currency.lower(), params))

    def rate_differentials(
        self, base: str, quote: str = "usd", **params
    ) -> pd.DataFrame:
        path = "rate_differentials/{}/{}".format(base.lower(), quote.lower())
        return self._frame(self.request(path, params))

    def forward_differentials(
        self, base: str, quote: str = "usd", **params
    ) -> pd.DataFrame:
        path = "forward_differentials/{}/{}".format(base.lower(), quote.lower())
        return self._frame(self.request(path, params))

    def market_sessions(self, **params) -> pd.DataFrame:
        return self._frame(self.request("market_sessions", params))

    def risk_sentiment(self, **params) -> pd.DataFrame:
        return self._frame(self.request("risk_sentiment", params))

    def news(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("news/" + currency.lower(), params))

    def press_releases(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("press-releases/" + currency.lower(), params))

    def macro_context(
        self,
        base: str,
        quote: str = "usd",
        indicator: str = "policy_rate",
        limit: int = 10,
    ) -> typing.Dict[str, pd.DataFrame]:
        base = base.lower()
        quote = quote.lower()
        return {
            "base_catalogue": self.data_catalogue(base),
            "quote_catalogue": self.data_catalogue(quote),
            "base_calendar": self.calendar(base, limit=limit),
            "quote_calendar": self.calendar(quote, limit=limit),
            "base_announcements": self.announcements(base, indicator, limit=limit),
            "quote_announcements": self.announcements(quote, indicator, limit=limit),
            "forex": self.forex(base, quote, limit=limit),
        }

    @staticmethod
    def _frame(payload: typing.Any) -> pd.DataFrame:
        if isinstance(payload, dict):
            for key in ("data", "rows", "results", "items"):
                if isinstance(payload.get(key), list):
                    return pd.DataFrame(payload[key])
            return pd.DataFrame([payload])
        if isinstance(payload, list):
            return pd.DataFrame(payload)
        return pd.DataFrame({"value": [payload]})
