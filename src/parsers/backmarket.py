import pdb
import re
from typing import Tuple
from bs4 import BeautifulSoup
from .base import BaseParser


class BackmarketLaptopParser(BaseParser):
    scrape_source = 'backmarket.com'

    def _get_items(self):
        products = self.soup.findAll("a", {"data-qa": "productThumb"})
        return products

    @staticmethod
    def _parse_brand_model(product: BeautifulSoup) -> Tuple[str, str]:
        title = product.find("h2", {"data-test": "title"}).text
        title = title.strip()
        brand_model = re.search(r"^(.+)?\s\d{2}[.]?\d{0,2}”", title).group(1)
        brand_model = brand_model.split(" ", 1)
        return brand_model[0], brand_model[1]

    @staticmethod
    def _parse_processor(product: BeautifulSoup) -> str:
        processor = product.find("ul").findAll("li")[1].find("b").text
        processor = processor.strip()
        return processor

    @staticmethod
    def _parse_ram(product: BeautifulSoup) -> int:
        ram = product.find("ul").findAll("li")[4].find("b").text
        ram = ram.strip()
        ram = ram.replace("GB", "")
        ram = int(ram)
        return ram

    @staticmethod
    def _parse_storage(product: BeautifulSoup) -> int:
        storage = product.find("ul").findAll("li")[3].find("b").text
        storage = storage.strip()
        storage = storage.split()[0]
        storage = int(storage)
        return storage

    @staticmethod
    def _parse_release_year(product: BeautifulSoup) -> int:
        release_year = product.find("ul").findAll("li")[0].find("b").text
        release_year = release_year.strip()
        release_year = re.search(r"([0-9]{4})", release_year).group(1)
        release_year = int(release_year)
        return release_year

    @staticmethod
    def _parse_screen_size(product: BeautifulSoup) -> float:
        screen_size = product.find("h2", {"data-test": "title"}).text
        screen_size = screen_size.strip()
        screen_size = re.search(r'.*(\d{2}[.]{0,1}\d{0,2})”\s',screen_size).group(1)
        screen_size = float(screen_size)
        return screen_size

    @staticmethod
    def _parse_price(product: BeautifulSoup) -> float:
        price = product.find('div',{'class':'price'}).text
        price = price.strip()
        price = re.search(r'.(\d{1,4}[.]{0,1}\d{0,2})',price).group(1)
        price = float(price)
        return price

    def _scrape_source(self) -> str:
        return self.scrape_source

    def _parse_scrape_url(self, product) -> str:
        return self.scrape_source + product['href']
    

    def parse(self):
        pass
