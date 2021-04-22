"""Broadband Dongle Tests
"""

import pytest
import requests
import json
from bs4 import BeautifulSoup

from src.parsers.broadbandchoices import BroadbandchoicesDongleParser


@pytest.fixture
def api_resp():
    with open("tests/fixtures/broadbandchoices/api_response.json", "r") as f:
        data = json.load(f)
    return data

def test_set_api_url():
    z = BroadbandchoicesDongleParser()
    z._set_api_url(1)
    assert z.api_url == "https://www.broadbandchoices.co.uk/mobile/results/devicescontracts?isDataOnlyDevice=true&page=1&deviceCondition=New&unlimitedData=true&unlimitedTexts=false&unlimitedMinutes=false&includeResellers=true&includeExistingCustomersHandset=false"

def test_get_deals(api_resp):
    z = BroadbandchoicesDongleParser()
    deals = z._get_deals(api_resp)
    assert len(deals) == 10

