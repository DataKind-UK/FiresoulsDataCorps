import pytest
import requests
from src.downloader import downloadHTML, RequestFailedException


class MockFailedResponse:
    text = "ERROR"
    ok = False
    status_code = 404


class MockSuccessfulResponse:
    text = "<html></html>"
    ok = True
    status_code = 200


def test_successful_make_request_method(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSuccessfulResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    a = downloadHTML("url")

    assert "<html></html>" == a


def test_failed_make_request_method(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockFailedResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(RequestFailedException) as e:
        _ = downloadHTML("url")
    assert str(e.value) == "Request for url failed with ERROR"


def test_proxy_key_not_set(monkeypatch):

    monkeypatch.delenv("SCRAPERAPI", raising=False)

    with pytest.raises(EnvironmentError) as e:
        _ = downloadHTML("url")
