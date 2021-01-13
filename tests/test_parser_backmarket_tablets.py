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


@pytest.fixture
def tablet_chardict(tablet_soup):
    bls = BackmarketTabletParser()
    chars = bls._parse_characteristics(tablet_soup)
    return chars


def test_tablet_parse_brand(tablet_chardict):
    bls = BackmarketTabletParser()
    assert bls._parse_brand(tablet_chardict) == "samsung"


def test_tablet_parse_model(tablet_chardict):
    bls = BackmarketTabletParser()
    assert bls._parse_model(tablet_chardict) == "galaxy tab s2"


def test_tablet_parse_processor(tablet_chardict):
    bls = BackmarketTabletParser()
    assert bls._parse_processor(tablet_chardict) == None


def test_tablet_parse_processor_not_missing():
    bls = BackmarketTabletParser()
    chars = {
        "Colour": "Gold",
        "SIM card": "Without SIM Port",
        "Processor brand": "Intel",
        "Processor speed": "1.5 GHz",
    }
    assert bls._parse_processor(chars) == "Intel 1.5 GHz"


def test_tablet_parse_screen_size(tablet_chardict):
    bls = BackmarketTabletParser()
    assert bls._parse_screen_size(tablet_chardict) == 8


def test_tablet_parse_resolution(tablet_chardict):
    bls = BackmarketTabletParser()
    assert bls._parse_screen_resolution(tablet_chardict) == "2048x1536"


def test_tablet_parse_storage(tablet_chardict):
    bls = BackmarketTabletParser()
    assert bls._parse_storage(tablet_chardict) == 32


def test_tablet_parse_release_year(tablet_chardict):
    bls = BackmarketTabletParser()
    assert bls._parse_release_year(tablet_chardict) == 2015
