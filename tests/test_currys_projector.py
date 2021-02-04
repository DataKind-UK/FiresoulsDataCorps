"""Curry's Laptop Parser Tests
"""

import pytest
import requests
from bs4 import BeautifulSoup

from src.parsers.currys import CurrysProjectorParser


@pytest.fixture
def soup():
    with open("tests/fixtures/currys/projectors_page_1.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def test_structure_url():
    clp = CurrysProjectorParser()
    url = clp._structure_url()
    assert (
        url
        == "https://www.currys.co.uk/gbuk/computing/projectors/projectors/570_4432_32094_xx_xx/1_50/relevance-desc/xx-criteria.html"
    )
    url = clp._structure_url(6)
    assert (
        url
        == "https://www.currys.co.uk/gbuk/computing/projectors/projectors/570_4432_32094_xx_xx/6_50/relevance-desc/xx-criteria.html"
    )


@pytest.fixture
def products(soup):
    bls = CurrysProjectorParser()
    bls.soup = soup
    items = bls._get_items()
    return items


def test_parse_brand(products):
    clp = CurrysProjectorParser()
    brand1 = clp._parse_brand(products[0])
    assert brand1 == "optoma"
    brand2 = clp._parse_brand(products[5])
    assert brand2 == "epson"


def test_parse_model(products):
    clp = CurrysProjectorParser()
    res1a = clp._parse_model(products[0])
    assert res1a == "gt1080e full hd home cinema projector"
    res2a = clp._parse_model(products[5])
    assert res2a == "eh-tw740 full hd home cinema projector"


# def test_parse_processor(products):
#     clp = CurrysProjectorParser()
#     res1a = clp._parse_processor(products[0])
#     assert res1a == "amd athlon silver 3050e"
#     res2a = clp._parse_processor(products[5])
#     assert res2a == "amd athlon silver 3050u"


# def test_parse_ram_storage(products):
#     clp = CurrysProjectorParser()
#     res1a, res1b = clp._parse_ram_storage(products[0])
#     assert (res1a, res1b) == (4, 64)
#     res2a, res2b = clp._parse_ram_storage(products[5])
#     assert (res2a, res2b) == (4, 128)
#     res3a, res3b = clp._parse_ram_storage(products[1])
#     assert (res3a, res3b) == (None, 512)

# def test_parse_price(products):
#     clp = CurrysProjectorParser()
#     res = clp._parse_price(products[0])
#     assert res == 199.0
#     res = clp._parse_price(products[5])
#     assert res == 299.0

# def test_parse_source():
#     clp = CurrysProjectorParser()
#     res = clp._scrape_source()
#     assert res == "currys.co.uk"

# def test_parse_scrape_url(products):
#     clp = CurrysProjectorParser()
#     res = clp._parse_scrape_url(products[0])
#     assert res == "https://www.currys.co.uk/gbuk/computing/laptops/laptops/lenovo-ideapad-slim-1-11-6-laptop-amd-athlon-silver-64-gb-emmc-grey-10219103-pdt.html"
#     res = clp._parse_scrape_url(products[5])
#     assert res == "https://www.currys.co.uk/gbuk/computing/laptops/laptops/hp-15s-eq1540na-15-6-laptop-amd-athlon-silver-128-gb-ssd-black-10220249-pdt.html"