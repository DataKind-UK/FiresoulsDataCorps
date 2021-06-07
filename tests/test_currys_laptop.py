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
    assert len(items) == 50


def test_get_num_pages(soup):
    bls = CurrysBaseParser()
    bls.soup = soup

    pages = bls._get_num_pages()
    assert pages == 7


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
    assert (res1a, res1b) == ("ideapad flex 5i  2 in 1", 14.0)
    res2a, res2b = clp._parse_model_screen_size(products[5])
    assert (res2a, res2b) == ('14a  chromebook', 14.0)


def test_parse_processor(products):
    clp = CurrysLaptopParser()
    res1a = clp._parse_processor(products[0])
    assert res1a == "intel® core™ i3-1005g1"
    res2a = clp._parse_processor(products[5])
    assert res2a == "intel® celeron® n4020"


def test_parse_ram_storage(products):
    clp = CurrysLaptopParser()
    res1a, res1b = clp._parse_ram_storage(products[0])
    assert (res1a, res1b) == (4, 128)
    res2a, res2b = clp._parse_ram_storage(products[5])
    assert (res2a, res2b) == (4, 64)
    res3a, res3b = clp._parse_ram_storage(products[1])
    assert (res3a, res3b) == (8, 256)


def test_parse_price(products):
    clp = CurrysLaptopParser()
    res = clp._parse_price(products[0])
    assert res == 449.0
    res = clp._parse_price(products[5])
    assert res == 279.0


def test_parse_source():
    clp = CurrysLaptopParser()
    res = clp._scrape_source()
    assert res == "currys.co.uk"


def test_parse_scrape_url(products):
    clp = CurrysLaptopParser()
    res = clp._parse_scrape_url(products[0])
    assert (
        res
        == "https://www.currys.co.uk/gbuk/computing/laptops/laptops/lenovo-ideapad-flex-5i-14-2-in-1-laptop-intel-core-i3-128-gb-ssd-grey-10207981-pdt.html"
    )
    res = clp._parse_scrape_url(products[5])
    assert (
        res
        == "https://www.currys.co.uk/gbuk/computing/laptops/laptops/hp-14a-14-chromebook-intel-celeron-64-gb-emmc-white-10207665-pdt.html"
    )
