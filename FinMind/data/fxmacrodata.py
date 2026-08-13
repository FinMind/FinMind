"""Optional client for the public FXMacroData v1 REST contract.

FXMacroData maintains the external API and this adapter. The always-free USD
catalogue, announcement history, and calendar do not require an API key;
protected datasets require a user-supplied key. Import this optional module
directly instead of relying on FinMind's top-level namespace.
"""

import json
import os
import typing
import urllib.error
import urllib.parse
import urllib.request

import pandas as pd


Params = typing.Mapping[str, typing.Any]


class FXMacroDataError(RuntimeError):
    """Raised when an FXMacroData request or response cannot be processed."""


class FXMacroDataApi:
    """FXMacroData v1 client that returns FinMind-friendly data frames."""

    API_VERSION = "v1"
    DEFAULT_BASE_URL = "https://api.fxmacrodata.com/v1/"

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
    ) -> typing.Any:
        query = dict(params or {})
        url = urllib.parse.urljoin(self.base_url, path.lstrip("/"))
        if query:
            url = url + "?" + urllib.parse.urlencode(query)

        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        req = urllib.request.Request(url, headers=headers)
        request_timeout = self.timeout if timeout is None else timeout
        try:
            with urllib.request.urlopen(req, timeout=request_timeout) as resp:
                payload = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raise FXMacroDataError(
                "FXMacroData request to {!r} failed with HTTP {}".format(
                    path, exc.code
                )
            ) from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise FXMacroDataError(
                "FXMacroData request to {!r} failed".format(path)
            ) from None
        except UnicodeError:
            raise FXMacroDataError(
                "FXMacroData response from {!r} was not UTF-8".format(path)
            ) from None

        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            raise FXMacroDataError(
                "FXMacroData response from {!r} was not valid JSON".format(path)
            ) from None

    def data_catalogue(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(
            self.request("data_catalogue/" + currency.lower(), params)
        )

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
        return self._predictions_frame(self.request(path, params))

    def forex(self, base: str, quote: str = "usd", **params) -> pd.DataFrame:
        path = "forex/{}/{}".format(base.lower(), quote.lower())
        return self._frame(self.request(path, params))

    def intraday_reference_rates(
        self, base: str, quote: str = "usd", **params
    ) -> pd.DataFrame:
        path = "fx/intraday-reference-rates/{}/{}".format(
            base.lower(), quote.lower()
        )
        return self._frame(self.request(path, params))

    def fx_sources(self, **params) -> pd.DataFrame:
        return self._frame(
            self.request("fx/sources", params), keys=("sources",)
        )

    def fx_source_universe(self, **params) -> pd.DataFrame:
        return self._frame(self.request("fx/source-universe", params))

    def cot(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("cot/" + currency.lower(), params))

    def commodity(self, indicator: str, **params) -> pd.DataFrame:
        return self._frame(self.request("commodities/" + indicator, params))

    def commodities_latest(self, **params) -> pd.DataFrame:
        return self._frame(self.request("commodities/latest", params))

    def curves(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(self.request("curves/" + currency.lower(), params))

    def factor(self, currency: str, factor: str, **params) -> pd.DataFrame:
        path = "factors/{}/{}".format(currency.lower(), factor)
        return self._frame(self.request(path, params))

    def rate_differentials(
        self, base: str, quote: str = "usd", **params
    ) -> pd.DataFrame:
        path = "rate_differentials/{}/{}".format(base.lower(), quote.lower())
        return self._frame(self.request(path, params))

    def market_sessions(self, **params) -> pd.DataFrame:
        return self._frame(self.request("market_sessions", params))

    def risk_sentiment(self, **params) -> pd.DataFrame:
        return self._frame(self.request("risk_sentiment", params))

    def press_releases(self, currency: str, **params) -> pd.DataFrame:
        return self._frame(
            self.request("press-releases/" + currency.lower(), params)
        )

    def ping(self) -> typing.Dict[str, typing.Any]:
        """Return the v1 health response without dataframe conversion."""

        return typing.cast(typing.Dict[str, typing.Any], self.request("ping"))

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
            "base_announcements": self.announcements(
                base, indicator, limit=limit
            ),
            "quote_announcements": self.announcements(
                quote, indicator, limit=limit
            ),
            "forex": self.forex(base, quote, limit=limit),
        }

    @staticmethod
    def _frame(
        payload: typing.Any,
        keys: typing.Tuple[str, ...] = ("data", "rows", "results", "items"),
    ) -> pd.DataFrame:
        if isinstance(payload, dict):
            for key in keys:
                if isinstance(payload.get(key), list):
                    return pd.DataFrame(payload[key])
            return pd.DataFrame([payload])
        if isinstance(payload, list):
            return pd.DataFrame(payload)
        return pd.DataFrame({"value": [payload]})

    @staticmethod
    def _predictions_frame(payload: typing.Any) -> pd.DataFrame:
        """Return one row per prediction while preserving release fields."""

        if not isinstance(payload, dict) or not isinstance(
            payload.get("data"), list
        ):
            return FXMacroDataApi._frame(payload)

        rows = []
        for group in payload["data"]:
            if not isinstance(group, dict):
                rows.append({"value": group})
                continue
            release = {
                key: value
                for key, value in group.items()
                if key != "predictions"
            }
            predictions = group.get("predictions")
            if not isinstance(predictions, list) or not predictions:
                rows.append(release)
                continue
            for prediction in predictions:
                row = dict(release)
                if isinstance(prediction, dict):
                    row.update(prediction)
                else:
                    row["prediction"] = prediction
                rows.append(row)
        return pd.DataFrame(rows)
