from abc import ABC, abstractmethod
from typing import Dict, Any
from bs4 import BeautifulSoup
from src.downloader import downloadHTML


class BaseParser(ABC):

    @staticmethod
    def _make_soup(url: str):
        html = downloadHTML(url)
        soup = BeautifulSoup(html, "html.parser")
        return soup

    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        pass
