"""Regus meeting rooms
"""

import pytest
import json
from bs4 import BeautifulSoup

from src.parsers.regus import RegusParser


@pytest.fixture
def api_resp():
    with open("tests/fixtures/regus/London_Regus.htm", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "lxml")
    return soup


def test_init():
    r = RegusParser("london")
    assert r.url == "https://www.regus.com/en-gb/united-kingdom/london/listings"
    assert (
        r.api_url == "https://www.regus.com/en-gb/united-kingdom/london/listings?page=1"
    )
