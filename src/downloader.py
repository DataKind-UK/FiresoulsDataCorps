import os
import requests
from typing import Optional


class RequestFailedException(Exception):
    pass


def downloadHTML(url: str, use_proxy: bool = True) -> str:
    target_url = url
    if use_proxy:
        proxy_key = os.getenv("SCRAPERAPI")
        if proxy_key is None:
            raise EnvironmentError(
                "SCRAPERAPI key not found, please make sure it exists as an environmental variable"
            )
        url = f"http://api.scraperapi.com/?api_key={proxy_key}&url={url}"
    res = requests.get(url)
    if res.ok:
        return res.text
    else:
        raise RequestFailedException(f"Request for {target_url} failed with {res.text}")
