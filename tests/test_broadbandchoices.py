"""Broadband Dongle Tests
"""

import pytest
import requests
from bs4 import BeautifulSoup

from src.parsers.broadbandchoices import BroadbandchoicesDongleParser


@pytest.fixture
def parser():
    with open("tests/fixtures/broadbandchoices/results_page.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    b = BroadbandchoicesDongleParser()
    b.soup = soup
    return b

def test_get_elements(parser):
    elems = parser.get_elements()
    assert len(elems) == 5

def test_get_provider_service(parser):
    elems = parser.get_elements()
    assert parser.get_provider_service(elems[0]) == ('Three', '4G Hub')
    assert parser.get_provider_service(elems[4]) == ('EE', '4GEE Mini Mobile WiFi')