"""Printerland Tests
"""

import pytest
import requests
from bs4 import BeautifulSoup

from src.parsers.printerland import PrinterlandParser


@pytest.fixture
def parser():
    with open("tests/fixtures/printerland/page1.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    b = PrinterlandParser()
    b.soup = soup
    return b


def test_get_elements(parser):
    elems = parser._get_elements()
    assert len(elems) == 12


def test_get_num_pages(parser):
    num_pages = parser._get_num_pages()
    assert num_pages == 13


def test_get_brand_model(parser):
    elems = parser._get_elements()
    bm = parser._get_brand_model(elems[0])
    assert bm == ("Xerox", "VersaLink C405DN")
    bm = parser._get_brand_model(elems[4])
    assert bm == ("Xerox", "WorkCentre 6515DN")


def test_get_key_features(parser):
    elems = parser._get_elements()
    kf = parser._get_key_features(elems[0])
    assert kf == [
        "Print/Scan/Copy/Fax",
        "Continue printing in mono even if the printer is out of colour toners",
        "Benchmark Security Features with ConnectKey® Technology",
        "Automatic Double Sided Printing",
        "Up to 600 x 600 x 8 dpi Print",
        "USB, Network & NFC",
        "Up to 35ppm Colour Print",
        "Up to 35ppm Mono Print",
        "PCL5/6, Postscript 3, PDF, XPS, TIFF, JPEG, HP-GL",
        "550 Sheet Input Tray",
        "150 Sheet Bypass Tray",
        "1.05GHz Dual-Core Processor",
        "2GB RAM",
        "Up to 600 x 600 dpi Copy",
        "33.6Kbps Fax",
        "5 Inch Capacitive Colour Touch Screen",
        "5 Inch Colour Touch Screen",
    ]


def test_get_functions(parser):
    elems = parser._get_elements()
    kf = parser._get_key_features(elems[0])
    func = parser._get_functions(kf)
    assert func == "Print/Scan/Copy/Fax"
    kf = parser._get_key_features(elems[5])
    func = parser._get_functions(kf)
    assert func == "Print/Copy/Scan"


def test_get_printing_speed_ppm(parser):
    elems = parser._get_elements()
    kf = parser._get_key_features(elems[0])
    speed = parser._get_printing_speed_ppm(kf)
    assert speed == 35
    kf = parser._get_key_features(elems[5])
    speed = parser._get_printing_speed_ppm(kf)
    assert speed == 20


def test_get_print_resolution(parser):
    elems = parser._get_elements()
    kf = parser._get_key_features(elems[0])
    res = parser._get_print_resolution(kf)
    assert res == "600 x 600"
    kf = parser._get_key_features(elems[5])
    res = parser._get_print_resolution(kf)
    assert res == "1,200 x 2,400"


def test_get_connectivity(parser):
    elems = parser._get_elements()
    kf = parser._get_key_features(elems[0])
    res = parser._get_connectivity(kf)
    assert res == "USB, Network & NFC"
    kf = parser._get_key_features(elems[4])
    res = parser._get_connectivity(kf)
    assert res == "USB & Network"


def test_get_scrape_url(parser):
    elems = parser._get_elements()
    res = parser._get_scrape_url(elems[0])
    assert res == "printerland.co.uk/product/xerox-versalink-c405dn/138869"
