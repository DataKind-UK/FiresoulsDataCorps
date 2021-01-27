"""
Class to extract printer prices from the Printerland.co.uk website
"""
from typing import Tuple, List
import re
from bs4 import BeautifulSoup
from .base import BaseParser


class PrinterlandParser(BaseParser):
    source = "printerland.co.uk"
    URL = "https://www.printerland.co.uk/printers/multifunction/laser/colour"

    def _get_elements(self) -> BeautifulSoup:
        elements = self.soup.findAll("li", {"class": "product__item"})
        return elements

    def _get_num_pages(self) -> int:
        num = self.soup.find("span", {"id": "lblPageCount"}).text
        num = num.replace("of ", "")
        return int(num)

    @staticmethod
    def _get_brand_model(item: BeautifulSoup) -> Tuple[str]:
        header = item.find("span", {"class": "header__text"}).text
        brand, model = header.strip().split(" ", 1)
        return brand, model

    @staticmethod
    def _get_key_features(item: BeautifulSoup) -> List[str]:
        key_features_cont = item.find("div", {"class": "key-features__container"})
        key_features = key_features_cont.findAll("li")
        key_features = [feat.text.strip() for feat in key_features]
        return key_features

    @staticmethod
    def _get_functions(key_features: List[str]) -> str:
        return key_features[0]

    @staticmethod
    def _get_printing_speed_ppm(key_features: List[str]) -> int:
        for feat in key_features:
            match = re.search(r"(\d+)ppm Colour", feat)
            if match is not None:
                break
        speed = match.group(1)
        return int(speed)

    @staticmethod
    def _get_print_resolution(key_features: List[str]) -> str:
        for feat in key_features:
            match = re.search(r"^Up to (\d*,?\d+ x \d*,?\d+).+Print$", feat)
            if match is not None:
                break
        res = match.group(1)
        return res

    @staticmethod
    def _get_connectivity(key_features: List[str]) -> str:
        possibles = ["USB", "Network", "NFC"]
        for feat in key_features:
            if any(pos in feat for pos in possibles):
                break
        return feat

    def _get_scrape_url(self, item: BeautifulSoup) -> str:
        return self.source + "/" + item.find("a")["href"]
