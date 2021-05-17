"""
Class to extract printer prices from the Printerland.co.uk website
"""
from typing import Tuple, List, Optional
import re
from bs4 import BeautifulSoup
from .base import BaseParser
from src.resources import Printer


class PrinterlandParser(BaseParser):
    source = "printerland.co.uk"
    url = "https://www.printerland.co.uk/printers/multifunction/laser/colour"

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
    def _get_printing_speed_ppm(key_features: List[str]) -> Optional[int]:
        for feat in key_features:
            match = re.search(r"^Up to (\d+)ppm.+Print$", feat)
            if match is not None:
                break
        try:
            speed = match.group(1)
        except AttributeError:
            print("\t Printing speed not found")
            return None
        return int(speed)

    @staticmethod
    def _get_print_resolution(key_features: List[str]) -> Optional[str]:
        for feat in key_features:
            match = re.search(r"^Up to (\d*,?\d+ x \d*,?\d+).+Print$", feat)
            if match is not None:
                break
        try:
            res = match.group(1)
        except AttributeError:
            print("\tPrint resolution not found")
            return None
        return res

    @staticmethod
    def _get_connectivity(key_features: List[str]) -> str:
        possibles = ["USB", "Network", "NFC"]
        for feat in key_features:
            if any(pos in feat for pos in possibles):
                break
        return feat

    @staticmethod
    def _get_price(item: BeautifulSoup) -> float:
        price_box = item.find("span", {"class": "price-ex"})
        price = price_box.find("span", {"class": "price"}).text
        price = price.replace("£", "").replace(",", "")
        return float(price)

    def _get_scrape_url(self, item: BeautifulSoup) -> str:
        return self.source + "/" + item.find("a")["href"]

    def parse(self) -> List[Printer]:
        self.soup = self._make_soup(self.url)
        num_pages = self._get_num_pages()
        printers = []
        for i in range(num_pages):
            print(f"Downloading page: {i+1}/{num_pages}")
            self.soup = self._make_soup(f"{self.url}?page={i+1}")
            products = self._get_elements()
            count = 0
            for product in products:
                count += 1
                try:
                    print(f"Parsing printer {count} of {len(products)}")
                    brand, model = self._get_brand_model(product)
                    key_features = self._get_key_features(product)
                    functions = self._get_functions(key_features)
                    printing_speed_ppm = self._get_printing_speed_ppm(key_features)
                    print_resolution = self._get_print_resolution(key_features)
                    connectivity = self._get_connectivity(key_features)
                    release_year = None
                    try:
                        price = self._get_price(product)
                    except AttributeError:
                        print("\tPrice not available for item")
                        continue
                    source = self.source
                    scrape_url = self._get_scrape_url(product)
                    l = Printer(
                        brand,
                        model,
                        functions,
                        printing_speed_ppm,
                        print_resolution,
                        connectivity,
                        release_year,
                        price,
                        source,
                        scrape_url,
                    )
                    printers.append(l)
                except Exception as e:
                    print(f"Scraping of item {count} failed with error {e}")
        return printers
