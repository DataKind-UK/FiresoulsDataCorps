"""Curry's Laptop Parser Tests
"""

import pytest
import requests
from bs4 import BeautifulSoup

from src.parsers.currys import CurrysDesktopParser


@pytest.fixture
def soup():
    with open("tests/fixtures/currys/desktops_page_1.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


def test_structure_url():
    clp = CurrysDesktopParser()
    url = clp._structure_url()
    assert (
        url
        == "https://www.currys.co.uk/gbuk/computing/desktop-pcs/desktop-pcs/317_3055_30057_xx_xx/1_50/relevance-desc/xx-criteria.html"
    )
    url = clp._structure_url(6)
    assert (
        url
        == "https://www.currys.co.uk/gbuk/computing/desktop-pcs/desktop-pcs/317_3055_30057_xx_xx/6_50/relevance-desc/xx-criteria.html"
    )


@pytest.fixture
def products(soup):
    bls = CurrysDesktopParser()
    bls.soup = soup
    items = bls._get_items()
    return items


def test_parse_brand(products):
    clp = CurrysDesktopParser()
    brand1 = clp._parse_brand(products[0])
    assert brand1 == "dell"
    brand2 = clp._parse_brand(products[4])
    assert brand2 == "hp"


def test_parse_model(products):
    clp = CurrysDesktopParser()
    res1a = clp._parse_model(products[0])
    assert res1a == "inspiron 3881 desktop pc"
    res2a = clp._parse_model(products[4])
    assert res2a == "pavilion 24-k0003na 23.8\" all-in-one pc"


def test_parse_price(products):
    clp = CurrysDesktopParser()
    res1a = clp._parse_price(products[0])
    assert res1a == 399.0
    res2a = clp._parse_price(products[4])
    assert res2a == 779.0


def test_parse_source():
    clp = CurrysDesktopParser()
    res = clp._scrape_source()
    assert res == "currys.co.uk"


def test_parse_scrape_url(products):
    clp = CurrysDesktopParser()
    res = clp._parse_scrape_url(products[0])
    assert (
        res
        == "https://www.currys.co.uk/gbuk/computing/desktop-pcs/desktop-pcs/dell-inspiron-3881-desktop-pc-intel-core-i3-1-tb-hdd-black-10211691-pdt.html"
    )
    res = clp._parse_scrape_url(products[4])
    assert (
        res
        == "https://www.currys.co.uk/gbuk/computing/desktop-pcs/desktop-pcs/hp-pavilion-24-k0003na-23-8-all-in-one-pc-amd-ryzen-5-512-gb-ssd-white-10207968-pdt.html"
    )


@pytest.fixture
def single_product_screen_soup():
    with open("tests/fixtures/currys/desktop_page_screen.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

@pytest.fixture
def single_product_no_screen_soup():
    with open("tests/fixtures/currys/desktop_page_no_screen.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

@pytest.fixture
def tech_specs_screen():
    data = {'Type': 'iMac', 'Operating system': 'macOS Catalina', 'Processor': '- Intel® Core™ i3 Processor\n- Quad-core\n- 3.2 GHz / 4.6 GHz', 'RAM': '8 GB DDR4 (2400 MHz)', 'Graphics card': '- AMD Radeon Pro 555X\n- 2 GB VRAM', 'Storage': '256 GB SSD', 'Touchscreen': 'No', 'Screen size': '21.5"', 'Screen type': 'Retina Display', 'Resolution': '4K Ultra HD 4096 x 2304p', 'Screen features': '- 500 nits brightness\n- Wide colour (P3)', 'WiFi': 'AC WiFi', 'Ethernet': 'Gigabit Ethernet port', 'Bluetooth': 'Bluetooth 4.2', 'USB': 'USB 3.0 x 4', 'Video connections': 'Thunderbolt 3 x 2', 'Audio connections': '3.5 mm jack', 'Speakers': 'Yes', 'Disc drive': 'No', 'Memory card reader': 'SDXC card reader', 'Camera': 'FaceTime HD camera', 'Mouse / trackpad': 'Apple Magic Mouse 2', 'Keyboard': 'Apple Magic Keyboard', 'Colour': 'Aluminium', 'Box contents': '- Apple iMac 4K 21.5" (2020)\n- Magic keyboard\n- Magic mouse 2\n- Power cable\n- Lightning to USB cable', 'Dimensions': '450 x 528 x 175 mm (H x W x D)', 'Weight': '5.60 kg', 'Manufacturer’s guarantee': '1 year', 'Software': '- Photos\n- iMovie\n- GarageBand\n- Pages\n- Numbers\n- Keynote\n- Siri\n- Safari\n- Mail\n- FaceTime\n- Messages\n- Maps\n- News\n- Stocks\n- Home\n- Voice Memos\n- Notes\n- Calendar\n- Contacts\n- Reminders\n- Photo Booth\n- Preview\n- iTunes\n- Books\n- App Store\n- Time Machine'}
    return data

@pytest.fixture
def tech_specs_no_screen():
    data = {'Type': 'Desktop PC', 'Operating system': 'Windows 10', 'Processor': '- Intel® Core™ i3-10100 Processor\n- Quad-core\n- 3.6 GHz / 4.3 GHz\n- 6 MB cache', 'RAM': '- 8 GB DDR4 (2666 MHz)\n- 64 GB maximum installable RAM', 'Storage': '1 TB HDD (7200 rpm)', 'WiFi': '- Dual-band AC WiFi\n- 1x1\n- Up to 433 Mbps', 'Ethernet': 'Gigabit Ethernet port', 'Bluetooth': 'Bluetooth 5.0', 'USB': '- USB Type-C x 1\n- USB 2.0 x 4', 'Video connections': '- HDMI 1.4 x 1\n- DisplayPort x 1\n- VGA x 1', 'Audio connections': '3.5 mm jack x 2', 'Audio software': 'Waves MaxxAudio Pro', 'Disc drive': 'DVD', 'Memory card reader': 'SD', 'Mouse / trackpad': 'USB mouse', 'Keyboard': 'USB keyboard with numeric keypad', 'Security features': '- Padlock ring security lock slot\n- Security cable wedge-shaped lock slot', 'Colour': 'Black', 'Box contents': '- Dell Inspiron 3881 Desktop PC (348P9)\n- Power adapter\n- Documentation', 'Dimensions': '324.3 x 154 x 293 mm (H x W x D)', 'Weight': '6.4 kg', 'Manufacturer’s guarantee': '1 year', 'Software': '* Full version of Microsoft Office not included\n* Full version of anti-virus / internet security not included\n\n- Office 2013 (30 day trial)\n- McAfee (30 day trial)'}
    return data

def test_parse_tech_specs_screen(single_product_screen_soup, tech_specs_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_tech_specs(single_product_screen_soup)
    assert res1a == tech_specs_screen

def test_parse_tech_specs(single_product_no_screen_soup, tech_specs_no_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_tech_specs(single_product_no_screen_soup)
    assert res1a == tech_specs_no_screen

def test_parse_screen_size(tech_specs_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_screen_size(tech_specs_screen)
    assert res1a == 21.5

def test_parse_screen_size_no_screen(tech_specs_no_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_screen_size(tech_specs_no_screen)
    assert res1a == None

def test_parse_ram(tech_specs_no_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_ram(tech_specs_no_screen)
    assert res1a == 8

def test_parse_processor(tech_specs_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_processor(tech_specs_screen)
    assert res1a == "intel® core™ i3"

def test_parse_storage_hdd(tech_specs_no_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_storage_hdd(tech_specs_no_screen)
    assert res1a == 1000

def test_parse_storage_hdd_missing(tech_specs_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_storage_hdd(tech_specs_screen)
    assert res1a == None

def test_parse_storage_ssd_missing(tech_specs_no_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_storage_ssd(tech_specs_no_screen)
    assert res1a == None

def test_parse_storage_ssd(tech_specs_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_storage_ssd(tech_specs_screen)
    assert res1a == 256

def test_parse_optical_drive_missing(tech_specs_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_optical_drive(tech_specs_screen)
    assert res1a == "No"

def test_parse_optical_drive(tech_specs_no_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_optical_drive(tech_specs_no_screen)
    assert res1a == "DVD"

def test_parse_operating_system(tech_specs_no_screen):
    clp = CurrysDesktopParser()
    res1a = clp._parse_operating_system(tech_specs_no_screen)
    assert res1a == "Windows 10"
