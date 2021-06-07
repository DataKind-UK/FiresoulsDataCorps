import pytest
import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.parsers.ons import ONSPeopleParser


@pytest.fixture
def parser():
    with open("tests/fixtures/ons/download_page.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    b = ONSPeopleParser()
    b.soup = soup
    return b


def test_get_button_url(parser):
    url = parser._get_button_url()
    assert (
        url
        == "https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/regionbyoccupation4digitsoc2010ashetable15/2020provisional/table152020provisional1.zip"
    )


@pytest.fixture
def data():
    df = pd.read_excel("tests/fixtures/ons/data_file.xls", sheet_name="All")
    return df


def test_fix_file_headers(data):
    parser = ONSPeopleParser()
    df = parser._fix_headers(data)
    assert set(df.columns) == {
        "description",
        "code",
        "median",
        "mean",
        "first_decile",
        "first_quartile",
        "third_decile",
        "seventh_decile",
        "third_quartile",
        "ninth_decile"
    }


def test_split_region(data):
    parser = ONSPeopleParser()
    df = parser._fix_headers(data)
    df = parser._split_region(df)
    assert set(df.columns) == {
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
    }


def test_replace_nan_with_none(data):
    parser = ONSPeopleParser()
    df = parser._fix_headers(data)
    df = parser._split_region(df)
    df = parser._replace_nan_with_none(df)
