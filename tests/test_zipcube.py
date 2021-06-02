"""Zipcube meeting rooms
"""

import pytest
import json

from src.parsers.zipcube import ZipcubeParser


@pytest.fixture
def api_resp():
    with open("tests/fixtures/zipcube/fixtures.json", "r") as f:
        data = json.load(f)
    return data


def test_init():
    z = ZipcubeParser("London")
    assert z.url == "https://www.zipcube.com/uk/s/meeting-rooms/London--UK"
    assert (
        z.api_url
        == "https://api.zipcube.com/api/search?page=1&tag=meeting-rooms&location=London--UK"
    )


def test_get_rooms(api_resp):
    z = ZipcubeParser("")
    rooms = z._get_rooms(api_resp)
    assert len(rooms) == 24


def test_num_pages(api_resp):
    z = ZipcubeParser("")
    num_pages = z._get_num_pages(api_resp)
    assert num_pages == 10
