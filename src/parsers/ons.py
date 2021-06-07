from typing import List
import pandas as pd
from .base import BaseParser
from src.resources import People


class ONSPeopleParser(BaseParser):
    scrape_source = "ons.gov.uk"
    url = "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/regionbyoccupation4digitsoc2010ashetable15"

    def _get_button_url(self) -> str:
        path = (
            self.soup.find("div", {"class": "page-content"})
            .findAll("section")[1]
            .find("div")
            .find("a")["href"]
        )
        url = "https://www.ons.gov.uk" + path
        return url

    @staticmethod
    def _fix_headers(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        while True:
            if "Description" == df.columns[0]:
                break
            else:
                df.columns = df.iloc[0, :]
                df = df.iloc[1:, :]
        df = df[["Description", "Code", "Median", "Mean", 10, 25, 30, 70, 75, 90]]
        df = df.rename(columns={10: "first_decile", 25: "first_quartile",
                                30: "third_decile", 70: "seventh_decile",
                                75: "third_quartile", 90: "ninth_decile"})
        df.columns = [x.lower() for x in df.columns]
        return df

    @staticmethod
    def _split_region(df: pd.DataFrame) -> pd.DataFrame:
        REGIONS = [
            "North East",
            "North West",
            "Yorkshire and The Humber",
            "East Midlands",
            "West Midlands",
            "East",
            "London",
            "South East",
            "South West",
            "Wales",
            "Scotland",
        ]
        df = df.copy()
        df[["region", "job_title"]] = (
            df["description"].str.strip().str.split(",", 1, expand=True)
        )
        df = df[(df["region"].isin(REGIONS)) & (~df["job_title"].isna())]
        df = df[
            [
                "region",
                "job_title",
                "code",
                "median",
                "mean",
                "first_decile",
                "first_quartile",
                "third_decile",
                "seventh_decile",
                "third_quartile",
                "ninth_decile"
            ]
        ]
        return df

    @staticmethod
    def _replace_nan_with_none(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.loc[df["median"] == "x", "median"] = None
        df.loc[df["mean"] == "x", "mean"] = None
        df.loc[df["first_decile"] == "x", "first_decile"] = None
        df.loc[df["first_quartile"] == "x", "first_quartile"] = None
        df.loc[df["third_decile"] == "x", "third_decile"] = None
        df.loc[df["seventh_decile"] == "x", "seventh_decile"] = None
        df.loc[df["third_quartile"] == "x", "third_quartile"] = None
        df.loc[df["ninth_decile"] == "x", "ninth_decile"] = None
        df[df.isna()] = None
        return df

    def parse(self) -> List[People]:
        people = []
        self.soup = self._make_soup(self.url)
        button_url = self._get_button_url()
        df = self._download_excel_from_zip(button_url, "Table 15.6a", "All")
        df = self._fix_headers(df)
        df = self._split_region(df)
        df = self._replace_nan_with_none(df)
        for _, row in df.iterrows():
            person = People(
                row["region"],
                row["job_title"],
                row["code"],
                row["mean"],
                row["first_decile"],
                row["first_quartile"],
                row["third_decile"],
                row["median"],
                row["seventh_decile"],
                row["third_quartile"],
                row["ninth_decile"],
                self.scrape_source,
                self.scrape_source + row["code"] + row["region"],
            )
            people.append(person)
        return people
