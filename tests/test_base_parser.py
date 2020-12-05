import pytest
import requests
from bs4 import BeautifulSoup
from src.parsers.base import BaseParser


class MockSuccessfulResponse:
    text = "<html></html>"
    ok = True
    status_code = 200


def test_make_soup(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSuccessfulResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    soup = BaseParser()._make_soup("url")

    expected = BeautifulSoup("<html></html>", "html.parser")

    assert soup == expected


def test_parse():
    with pytest.raises(NotImplementedError):
        BaseParser().parse()
