"""Curry's Laptop Parser Tests
"""

import pytest
import requests
from bs4 import BeautifulSoup

from src.parsers.currys import CurrysBaseParser, CurrysLaptopParser


@pytest.fixture
def soup():
    with open("tests/fixtures/currys/laptops_page_1.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


def test_laptop_get_items(soup):
    bls = CurrysBaseParser()
    bls.soup = soup

    items = bls._get_items()
    assert len(items) == 12


def test_get_num_pages(soup):
    bls = CurrysBaseParser()
    bls.soup = soup

    pages = bls._get_num_pages()
    assert pages == 21


def test_structure_url():
    clp = CurrysLaptopParser()
    url = clp._structure_url()
    assert (
        url
        == "https://www.currys.co.uk/gbuk/computing/laptops/laptops/315_3226_30328_xx_xx/1_50/relevance-desc/xx-criteria.html"
    )
    url = clp._structure_url(6)
    assert (
        url
        == "https://www.currys.co.uk/gbuk/computing/laptops/laptops/315_3226_30328_xx_xx/6_50/relevance-desc/xx-criteria.html"
    )


@pytest.fixture
def products(soup):
    bls = CurrysLaptopParser()
    bls.soup = soup
    items = bls._get_items()
    return items


def test_parse_brand(products):
    clp = CurrysLaptopParser()
    brand1 = clp._parse_brand(products[0])
    assert brand1 == "lenovo"
    brand2 = clp._parse_brand(products[5])
    assert brand2 == "hp"


def test_parse_model_screen_size(products):
    clp = CurrysLaptopParser()
    res1a, res1b = clp._parse_model_screen_size(products[0])
    assert (res1a, res1b) == ("ideapad slim 1", 11.6)
    res2a, res2b = clp._parse_model_screen_size(products[5])
    assert (res2a, res2b) == ("15s-eq1540na", 15.6)


def test_parse_processor(products):
    clp = CurrysLaptopParser()
    res1a = clp._parse_processor(products[0])
    assert res1a == "amd athlon silver 3050e"
    res2a = clp._parse_processor(products[5])
    assert res2a == "amd athlon silver 3050u"


def test_parse_ram_storage(products):
    clp = CurrysLaptopParser()
    res1a, res1b = clp._parse_ram_storage(products[0])
    assert (res1a, res1b) == (4, 64)
    res2a, res2b = clp._parse_ram_storage(products[5])
    assert (res2a, res2b) == (4, 128)
    res3a, res3b = clp._parse_ram_storage(products[1])
    assert (res3a, res3b) == (None, 512)