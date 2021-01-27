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
    elems = parser.get_elements()
    assert len(elems) == 12