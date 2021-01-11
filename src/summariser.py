"""summariser.py

Class to generate summary statistics based off a file of scraped data. It also
allows the generation of CSV files for easier exploration.
"""

import json
from typing import Optional, List
import pandas as pd


class Summary:
    def __init__(self, df: pd.DataFrame = pd.DataFrame()):
        self.df = df

    @classmethod
    def from_json(cls, path: str):
        data = cls._load_json(path)
        df = pd.DataFrame(data)
        return cls(df)

    @staticmethod
    def _load_json(path: str) -> dict:
        with open(path, "r") as f:
            data = json.load(f)
        return data

    def to_csv(self, path: str):
        self.df.to_csv(path)

    def summary_statistics(self, grouping: Optional[List[str]] = None):
        if grouping is None:
            summary = self.df["price"].describe()
        else:
            summary = self.df.groupby(grouping)["price"].describe()
        print(summary)
