"""Tablet Parser Tests
"""
import pytest
from bs4 import BeautifulSoup
from src.parsers.backmarket import BackmarketTabletParser


@pytest.fixture
def tablet_soup():
    with open("tests/fixtures/backmarket/tablet_page.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


def test_tablet_parse_price(tablet_soup):
    bls = BackmarketTabletParser()
    price = bls._parse_price(tablet_soup)
    assert price == 186


def test_tablet_parse_chardict(tablet_soup):
    bls = BackmarketTabletParser()
    chars = bls._parse_characteristics(tablet_soup)
    expected_chars = {
        "Colour": "Gold",
        "SIM card": "Without SIM Port",
        "Screen size (in)": "8",
        "Storage": "32 GB",
        "Memory": "3 GB",
        "Model": "Galaxy Tab S2",
        "OS": "Android",
        "Resolution": "2048x1536",
        "Network": "WiFi",
        "Release Date": "September 2015",
        "Megapixels": "8",
        "Double SIM": "No",
        "Year of Release": "2015",
        "Brand": "Samsung",
        "Weight": "265 g",
    }
    assert chars == expected_chars
