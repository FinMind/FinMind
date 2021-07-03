from pydantic import BaseModel
import typing
import pandas as pd


class BarPlotSchema(BaseModel):
    labels: typing.List[typing.Union[str, int]] = None
    series: typing.List[typing.Union[int, float]] = None

    def __init__(
        self,
        labels: typing.List[typing.Union[str, int]] = None,
        series: typing.List[typing.Union[int, float]] = None,
        **kwargs
    ):
        super(BarPlotSchema, self).__init__(
            **{
                **dict(
                    labels=labels,
                    series=series,
                ),
                **kwargs,
            }
        )

    @staticmethod
    def df_convert(df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise Exception("df must be pd.DataFrame")
        if "labels" in df and "series" in df:
            result = BarPlotSchema(**df.to_dict("list"))
        else:
            raise Exception("df is missing labels or series column")
        return result
