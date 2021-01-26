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

def test_get_data(parser):
    elems = parser.get_elements()
    data = parser._get_data(elems[0])
    assert len(data) == 5

def test_get_value(parser):
    elems = parser.get_elements()
    data = parser._get_data(elems[0])
    value = parser._get_value(data[0])
    assert value == "£0.00"
    value = parser._get_value(data[2])
    assert value == 'Unltd'

def test_get_upfront_cost(parser):
    elems = parser.get_elements()
    data = parser._get_data(elems[0])
    assert parser.get_upfront_cost(data) == 0
    data = parser._get_data(elems[1])
    assert parser.get_upfront_cost(data) == 18


def test_get_total_cost(parser):
    elems = parser.get_elements()
    data = parser._get_data(elems[0])
    assert parser.get_total_cost(data) == 408
    data = parser._get_data(elems[1])
    assert parser.get_total_cost(data) == 258


def test_get_allowance(parser):
    elems = parser.get_elements()
    data = parser._get_data(elems[0])
    assert parser.get_allowance(data) == 'Unltd'
    data = parser._get_data(elems[1])
    assert parser.get_allowance(data) == 'Unltd'


def test_get_contract_months(parser):
    elems = parser.get_elements()
    data = parser._get_data(elems[0])
    assert parser.get_contract_months(data) == 24
    data = parser._get_data(elems[1])
    assert parser.get_contract_months(data) == 12

def test_get_monthly_cost(parser):
    elems = parser.get_elements()
    data = parser._get_data(elems[0])
    assert parser.get_monthly_cost(data) == 17
    data = parser._get_data(elems[1])
    assert parser.get_monthly_cost(data) == 20