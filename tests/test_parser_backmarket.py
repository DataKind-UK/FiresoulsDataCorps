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
    assert pages == 5


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (0, ("Lenovo", "ThinkPad X240")),
        (4, ("Dell", "Latitude E7270")),
        (6, ("Dell", "G5 15 5590")),
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
        (6, "Intel Core i7 1.8 GHz"),
    ],
)
def test_laptop_parse_processor(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_processor(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 4), (4, 8), (6, 8)])
def test_laptop_parse_ram(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_ram(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 500), (4, 128), (6, 256)])
def test_laptop_parse_storage(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_storage(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 2014), (4, 2016), (6, 2019)])
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
    "test_input,expected", [(0, 12.5), (2, 14), (4, 12.5), (6, 15.6)]
)
def test_laptop_parse_screen_size(soup, test_input, expected):
    bls = BackmarketLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_screen_size(item) == expected


@pytest.mark.parametrize(
    "test_input,expected", [(0, 299.0), (2, 280.0), (4, 425.0), (6, 879.0)]
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
            "backmarket.co.uk/second-hand-lenovo-thinkpad-x240-125-inch-2014-core-i5-4300u-4gb-hdd-500-gb-qwerty-english-us/351462.html#?l=2",
        ),
        (
            2,
            "backmarket.co.uk/second-hand-lenovo-thinkpad-t460-14-inch-2016-core-i3-6100u-8gb-ssd-128-gb-qwerty-english-us/405871.html#?l=2",
        ),
        (
            4,
            "backmarket.co.uk/second-hand-dell-latitude-e7270-125-inch-2016-core-i5-6300u-8gb-ssd-128-gb-qwerty-english-uk/404246.html#?l=0",
        ),
        (
            6,
            "backmarket.co.uk/second-hand-dell-g5-15-5590-156-inch-core-i7-10510u-8gb-256gb-nvidia-geforce-mx250-qwerty-english-us/412348.html#?l=2",
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
    assert len(laptops) == 150
