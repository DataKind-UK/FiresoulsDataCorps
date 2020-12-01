from abc import ABC, abstractmethod
from typing import Dict, Any
from bs4 import BeautifulSoup


class BaseParser(ABC):
    def __init__(self, html: str):
        self.html = html
        self._make_soup()

    def _make_soup(self):
        soup = BeautifulSoup(self.html, "html.parser")
        self.soup = soup

    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        pass
