import typing

import pandas as pd
from pydantic import BaseModel, validator


class Labels(BaseModel):
    labels: typing.List[typing.Union[str, int]]

    @validator("labels", allow_reuse=True, each_item=True)
    def valid(cls, value):
        if isinstance(value, str):
            print("str pass")
        elif isinstance(value, int):
            print("int pass")
        else:
            raise Exception(
                "the type of labels must be list[int] for list[str]."
            )
        return value


class Series(BaseModel):
    series: typing.List[typing.Union[int, float]]

    @validator("series", allow_reuse=True, each_item=True)
    def valid(cls, value):
        if isinstance(value, int):
            pass
        elif isinstance(value, float):
            pass
        else:
            raise Exception(
                "the type of series must be list[int] for list[str]."
            )
        return value


def check_labels_series_schema(
    labels: typing.Union[typing.List[typing.Union[str, int]], Labels],
    series: typing.Union[typing.List[typing.Union[int, float]], Series],
):
    if isinstance(labels, Labels):
        pass
    elif isinstance(labels, pd.core.series.Series):
        labels = list(labels)
        labels = Labels(labels=labels)
    elif isinstance(labels, list):
        labels = Labels(labels=labels)

    if isinstance(series, Series):
        pass
    elif isinstance(series, pd.core.series.Series):
        series = list(series)
        series = Series(series=series)
    elif isinstance(series, list):
        series = Series(series=series)
    return labels, series
