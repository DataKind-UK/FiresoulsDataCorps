"""Curry's Laptop Parser Tests
"""

import pytest
import requests
from bs4 import BeautifulSoup

from src.parsers.currys import CurrysBaseParser

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