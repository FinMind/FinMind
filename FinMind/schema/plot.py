import typing

import pandas as pd
from pydantic import BaseModel, field_validator


class Labels(BaseModel):
    labels: typing.List[typing.Union[str, int]]

    @field_validator("labels")
    @classmethod
    def valid(cls, value):
        for item in value:
            if not isinstance(item, (str, int)):
                raise Exception(
                    "the type of labels must be list[int] for list[str]."
                )
        return value


class Series(BaseModel):
    series: typing.List[typing.Union[int, float]]

    @field_validator("series")
    @classmethod
    def valid(cls, value):
        for item in value:
            if not isinstance(item, (int, float)):
                raise Exception(
                    "the type of series must be list[int] for list[str]."
                )
        return value


def convert_labels_series_schema(
    labels: typing.Union[typing.List[typing.Union[str, int]], Labels],
    series: typing.Union[typing.List[typing.Union[int, float]], Series],
):
    if isinstance(labels, Labels):
        pass
    elif isinstance(labels, pd.Series):
        labels = Labels(labels=labels.tolist())
    elif isinstance(labels, list):
        labels = Labels(labels=labels)

    if isinstance(series, Series):
        pass
    elif isinstance(series, pd.Series):
        series = Series(series=series.tolist())
    elif isinstance(series, list):
        series = Series(series=series)
    return labels, series
