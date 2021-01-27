"""
Class to extract printer prices from the Printerland.co.uk website
"""
from typing import Tuple, List
import re
from bs4 import BeautifulSoup
from .base import BaseParser


class PrinterlandParser(BaseParser):
    source = 'printerland.co.uk'
    URL = "https://www.printerland.co.uk/printers/multifunction/laser/colour"

    def get_elements(self) -> BeautifulSoup:
        elements = self.soup.findAll("li", {"class": "product__item"})
        return elements
