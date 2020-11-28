"""downloader.py
"""
import os
import requests


class RequestFailedException(Exception):
    """Exception raised when an error occurs while making the get request to
    a site
    """

    pass


def downloadHTML(url: str, use_proxy: bool = True) -> str:
    """Function to make request to website and download HTML code.
    It will optionally use a proxy to make the request.
    It's currently set to use the ScraperAPI service.

    Parameters
    ----------
    url : str
        URL address to scrape
    use_proxy : bool, optional
        If True, will use proxy service to make request, by default True

    Returns
    -------
    str
        HTML code of the website requested

    Raises
    ------
    EnvironmentError
        Raised if use_proxy is True, but no key has been set in the .env file
    RequestFailedException
        Raised if any issues occur during the page request.
    """
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
