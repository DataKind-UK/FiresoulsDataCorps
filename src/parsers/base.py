from typing import Dict, Any
from bs4 import BeautifulSoup
from src.downloader import downloadHTML


class BaseParser:
    @staticmethod
    def _make_soup(url: str, use_proxy: bool = True):
        html = downloadHTML(url, use_proxy)
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def parse(self) -> Dict[str, Any]:
        raise NotImplementedError(
            "This method needs to be implemented in child classes"
        )
