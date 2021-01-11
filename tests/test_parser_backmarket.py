import pytest
import requests
from bs4 import BeautifulSoup

from src.parsers.backmarket import BackmarketLaptopParser


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
    assert len(items) == 30


def test_get_num_pages(soup):
    bls = BackmarketLaptopParser()
    bls.soup = soup

    pages = bls._get_num_pages()
    assert pages == 4


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (0, ("Lenovo", "IdeaPad 3 15IIL05-81WE")),
        (4, ("HP", "EliteBook 840 G1")),
        (6, ("Dell", "Latitude E6530")),
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
        (0, "Intel Core i3 1.2 GHz"),
        (4, "Intel Core i5 2 GHz"),
        (6, "Intel Core i7 2.9 GHz"),
    ],
)
def test_laptop_parse_processor(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_processor(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 4), (4, 4), (6, 4)])
def test_laptop_parse_ram(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_ram(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 128), (4, 240), (6, 128)])
def test_laptop_parse_storage(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_storage(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 2019), (4, 2013), (6, 2012)])
def test_laptop_parse_release_year(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_release_year(item) == expected


def test_laptop_parse_release_year_not_defined():
    bls = BackmarketLaptopParser()
    item = BeautifulSoup("<html><ul><li><b></b></li></ul></html>", "html.parser")
    bls._parse_release_year(item) == 0


@pytest.mark.parametrize(
    "test_input,expected", [(0, 15.6), (2, 15.6), (4, 14.0), (6, 15.6)]
)
def test_laptop_parse_screen_size(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_screen_size(item) == expected


@pytest.mark.parametrize(
    "test_input,expected", [(0, 449.0), (2, 440.0), (4, 330.0), (6, 340.0)]
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
            "backmarket.co.uk/second-hand-lenovo-ideapad-3-15iil05-81we-156-inch-2019-core-i3-1005g1-4gb-ssd-128-gb-qwerty-english-uk/422090.html#?l=0",
        ),
        (
            2,
            "backmarket.co.uk/second-hand-dell-precision-m4800-156-inch-2013-core-i7-4800mq-8gb-ssd-128-gb-qwerty-english-us/432027.html#?l=3",
        ),
        (
            4,
            "backmarket.co.uk/second-hand-hp-elitebook-840-g1-14-inch-2013-core-i5-4310u-4gb-ssd-240-gb-qwerty-english-us/432297.html#?l=4",
        ),
        (
            6,
            "backmarket.co.uk/second-hand-dell-latitude-e6530-156-inch-2013-core-i7-3520m-4gb-ssd-128-gb-qwerty-english-us/432409.html#?l=4",
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
    assert len(laptops) == 120
