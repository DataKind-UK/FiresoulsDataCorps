"""Laptop Parser Tests
"""

import pytest
import requests
from bs4 import BeautifulSoup

from src.parsers.backmarket import BackmarketLaptopParser, BackmarketTabletParser


@pytest.fixture
def soup():
    with open("tests/fixtures/backmarket/laptops_page_1.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


def test_laptop_get_items(soup):
    bls = BackmarketLaptopParser()
    bls.soup = soup

    items = bls._get_items()
    assert len(items) == 26


def test_get_num_pages(soup):
    bls = BackmarketLaptopParser()
    bls.soup = soup

    pages = bls._get_num_pages()
    assert pages == 1


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (0, ("Microsoft", "Surface Pro 3")),
        (4, ("Dell", "Latitude E7270")),
        (6, ("HP", "EliteBook 840 G3")),
    ],
)
def test_laptop_parse_brand_model(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_brand_model(item) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (0, "Intel Core i5 1.9 GHz"),
        (4, "Intel Core i5 2.4 GHz"),
        (6, "Intel Core i5 2.3 GHz"),
    ],
)
def test_laptop_parse_processor(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_processor(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 8), (4, 8), (6, 8)])
def test_laptop_parse_ram(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_ram(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 256), (4, 512), (6, 240)])
def test_laptop_parse_storage(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_storage(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 2014), (4, 2016), (6, 2016)])
def test_laptop_parse_release_year(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_release_year(item) == expected


def test_laptop_parse_release_year_not_defined():
    bls = BackmarketLaptopParser()
    item = BeautifulSoup(
        "<html><ul><li><span></span><span></span></li></ul></html>", "html.parser"
    )
    bls._parse_release_year(item) == 0


@pytest.mark.parametrize(
    "test_input,expected", [(0, 12.0), (2, 14.0), (4, 12.5), (6, 14.0)]
)
def test_laptop_parse_screen_size(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_screen_size(item) == expected


@pytest.mark.parametrize(
    "test_input,expected", [(0, 399.0), (2, 325.0), (4, 465.0), (6, 445.0)]
)
def test_laptop_parse_price(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_price(item) == expected


def test_laptop_scrape_source(soup):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    assert bls._scrape_source() == "backmarket.co.uk"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            0,
            "backmarket.co.uk/second-hand-microsoft-surface-pro-3-12-inch-core-i5-4300u-ssd-256-gb-8gb-qwerty-english-us/442601.html#l=1",
        ),
        (
            2,
            "backmarket.co.uk/second-hand-hp-elitebook-840-g2-14-inch-2014-core-i5-5300u-4gb-hdd-500-gb-qwerty-english-uk/419200.html#l=1",
        ),
        (
            4,
            "backmarket.co.uk/second-hand-dell-latitude-e7270-125-inch-2016-core-i5-6300u-8gb-ssd-512-gb-qwerty-english-uk/408001.html#l=3",
        ),
        (
            6,
            "backmarket.co.uk/second-hand-hp-elitebook-840-g3-14-inch-2016-core-i5-6200u-8gb-ssd-240-gb-qwerty-english-us/413912.html#l=1",
        ),
    ],
)
def test_laptop_parse_url(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_scrape_url(item) == expected


class MockSuccessfulResponse:
    with open("tests/fixtures/backmarket/laptops_page_1.html", "r") as f:
        text = f.read()
    ok = True
    status_code = 200


def test_successful_make_request_method(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSuccessfulResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    bls = BackmarketLaptopParser()
    laptops = bls.parse()
    assert len(laptops) == 26
