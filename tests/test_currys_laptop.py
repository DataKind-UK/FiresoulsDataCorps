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
    assert len(items) == 20


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
    assert brand2 == "dell"


def test_parse_model_screen_size(products):
    clp = CurrysLaptopParser()
    res1a, res1b = clp._parse_model_screen_size(products[0])
    assert (res1a, res1b) == ("ideapad slim 1", 11.6)
    res2a, res2b = clp._parse_model_screen_size(products[5])
    assert (res2a, res2b) == ("inspiron 15 3000", 15.6)


def test_parse_processor(products):
    clp = CurrysLaptopParser()
    res1a = clp._parse_processor(products[0])
    assert res1a == "amd athlon silver 3050e"
    res2a = clp._parse_processor(products[5])
    assert res2a == "amd ryzen 5 3500u"


def test_parse_ram_storage(products):
    clp = CurrysLaptopParser()
    res1a, res1b = clp._parse_ram_storage(products[0])
    assert (res1a, res1b) == (4, 64)
    res2a, res2b = clp._parse_ram_storage(products[5])
    assert (res2a, res2b) == (8, 256)
    res3a, res3b = clp._parse_ram_storage(products[1])
    assert (res3a, res3b) == (None, 512)

def test_parse_price(products):
    clp = CurrysLaptopParser()
    res = clp._parse_price(products[0])
    assert res == 199.0
    res = clp._parse_price(products[5])
    assert res == 499.0

def test_parse_source():
    clp = CurrysLaptopParser()
    res = clp._scrape_source()
    assert res == "currys.co.uk"

def test_parse_scrape_url(products):
    clp = CurrysLaptopParser()
    res = clp._parse_scrape_url(products[0])
    assert res == "https://www.currys.co.uk/gbuk/computing/laptops/laptops/lenovo-ideapad-slim-1-11-6-laptop-amd-athlon-silver-64-gb-emmc-grey-10219103-pdt.html"
    res = clp._parse_scrape_url(products[5])
    assert res == "https://www.currys.co.uk/gbuk/computing/laptops/laptops/dell-inspiron-15-3000-15-6-laptop-amd-ryzen-5-256-gb-ssd-black-10214380-pdt.html"