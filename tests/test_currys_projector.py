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


def test_parse_price(products):
    clp = CurrysProjectorParser()
    res1a = clp._parse_price(products[0])
    assert res1a == 599.99
    res2a = clp._parse_price(products[5])
    assert res2a == 599.99


def test_parse_source():
    clp = CurrysProjectorParser()
    res = clp._scrape_source()
    assert res == "currys.co.uk"


def test_parse_scrape_url(products):
    clp = CurrysProjectorParser()
    res = clp._parse_scrape_url(products[0])
    assert (
        res
        == "https://www.currys.co.uk/gbuk/computing/projectors/projectors/optoma-gt1080e-full-hd-home-cinema-projector-10215801-pdt.html"
    )
    res = clp._parse_scrape_url(products[5])
    assert (
        res
        == "https://www.currys.co.uk/gbuk/computing/projectors/projectors/epson-eh-tw740-full-hd-home-cinema-projector-10218973-pdt.html"
    )


@pytest.fixture
def single_product_soup():
    with open("tests/fixtures/currys/projector_page.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


@pytest.fixture
def tech_specs():
    data = {
        "Type": "Home cinema projector",
        "Resolution": "1920 x 1080",
        "Technology": "DLP",
        "Projection type": "Short throw",
        "Screen size range": '45.3" - 300"',
        "Projection range": '- 300" at 3.35 m\n- 45.3" at 0.5 m',
        "Video standard": "- NTSC\n- SECAM\n- PAL",
        "Brightness": "3000 lumens",
        "Aspect ratio": "16:9",
        "Contrast ratio": "25000:1",
        "Keystone correction": "Yes",
        "3D ready": "Yes",
        "Other features": "- BrilliantColor\n- ISFccc\n- Game mode\n- ProJect Green\n- Security lock slot (cable lock sold separately)\n- Password protection\n- Security bar",
        "Number of speakers": "1",
        "Audio power": "10 W",
        "Wireless connectivity": "WiFi via adapter (sold separately)",
        "Video interface": "- HDMI x 2\n- MHL x 1",
        "USB": "Mini-USB Type B x 1",
        "Audio interface": "3.5 mm jack x 1",
        "Energy consumption": "233 W",
        "Lamp type and consumption": "190 W",
        "Lamp life": "5000 hours",
        "Energy saving features": "Eco mode",
        "Colour": "White",
        "Box contents": "- Optoma GT1080e Full HD Home Cinema Projector\n- Carrying case\n- Lens cover\n- AAA batteries x 2\n- Wireless remote control",
        "Dimensions": "114 x 315 x 224 mm (H x W x D)",
        "Weight": "2.65 kg",
        "Manufacturer’s guarantee": "1 year",
    }
    return data


def test_parse_tech_specs(single_product_soup, tech_specs):
    clp = CurrysProjectorParser()
    res1a = clp._parse_tech_specs(single_product_soup)
    assert res1a == tech_specs


def test_parse_screen_size(tech_specs):
    clp = CurrysProjectorParser()
    res1a = clp._parse_screen_size(tech_specs)
    assert res1a == 300


def test_parse_projection_type(tech_specs):
    clp = CurrysProjectorParser()
    res1a = clp._parse_projection_type(tech_specs)
    assert res1a == "short throw"


def test_parse_resolution(tech_specs):
    clp = CurrysProjectorParser()
    res1a = clp._parse_resolution(tech_specs)
    assert res1a == "1920 x 1080"


def test_parse_brightness(tech_specs):
    clp = CurrysProjectorParser()
    res1a = clp._parse_brightness(tech_specs)
    assert res1a == 3000


def test_parse_technology(tech_specs):
    clp = CurrysProjectorParser()
    res1a = clp._parse_technology(tech_specs)
    assert res1a == "dlp"
