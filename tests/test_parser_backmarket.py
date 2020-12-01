import pytest
from bs4 import BeautifulSoup

from src.parsers.backmarket import BackmarketLaptopParser


@pytest.fixture
def html_code():
    with open("tests/fixtures/backmarket/laptops_page_1.html", "r") as f:
        html = f.read()
    return html


def test_laptop_get_items(html_code):
    bls = BackmarketLaptopParser(html_code)
    items = bls._get_items()
    assert len(items) == 30


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (0, ("Lenovo", "ThinkPad X240")),
        (4, ("Dell", "Latitude E7270")),
        (6, ("Dell", "G5 15 5590")),
    ],
)
def test_laptop_parse_brand_model(html_code, test_input, expected):
    bls = BackmarketLaptopParser(html_code)
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
def test_laptop_parse_processor(html_code, test_input, expected):
    bls = BackmarketLaptopParser(html_code)
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_processor(item) == expected


@pytest.mark.parametrize("test_input,expected", [(0, 4), (4, 8), (6, 8)])
def test_laptop_parse_ram(html_code, test_input, expected):
    bls = BackmarketLaptopParser(html_code)
    items = bls._get_items()
    item = items[test_input]
    assert bls._parse_ram(item) == expected
