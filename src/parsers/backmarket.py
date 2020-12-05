import pdb
import re
from typing import Tuple, List
from bs4 import BeautifulSoup
from .base import BaseParser
from src.resources import Laptop


class BackmarketLaptopParser(BaseParser):
    scrape_source = "backmarket.co.uk"
    url = "https://www.backmarket.co.uk/refurbished-laptop-english.html"

    def _get_items(self) -> List[BeautifulSoup]:
        products = self.soup.findAll("a", {"data-qa": "productThumb"})
        return products

    def _get_num_pages(self) -> int:
        pages = len(
            self.soup.find("div", {"data-test": "pagination"}).findAll("button")
        )
        return pages

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
        try:
            release_year = re.search(r"([0-9]{4})", release_year).group(1)
        except AttributeError:
            print("\tRelease Year not specified for this laptop")
            release_year = "0"
        release_year = int(release_year)
        return release_year

    @staticmethod
    def _parse_screen_size(product: BeautifulSoup) -> float:
        screen_size = product.find("h2", {"data-test": "title"}).text
        screen_size = screen_size.strip()
        screen_size = re.search(r".*(\d{2}[.]{0,1}\d{0,2})”\s?", screen_size).group(1)
        screen_size = float(screen_size)
        return screen_size

    @staticmethod
    def _parse_price(product: BeautifulSoup) -> float:
        price = product.find("div", {"class": "price"}).text
        price = price.strip()
        price = price.replace(",", "")
        price = re.search(r".(\d{1,4}[.]{0,1}\d{0,2})", price).group(1)
        price = float(price)
        return price

    def _scrape_source(self) -> str:
        return self.scrape_source

    def _parse_scrape_url(self, product) -> str:
        return self.scrape_source + product["href"]

    def parse(self) -> List[Laptop]:
        self.soup = self._make_soup(self.url)
        num_pages = self._get_num_pages()
        laptops = []
        for i in range(num_pages):
            print(f"Downloading page: {i+1}/{num_pages}")
            self.soup = self._make_soup(f"{self.url}?page={i+1}")
            products = self._get_items()
            count = 0
            for product in products:
                count += 1
                print(f"Parsing laptop {count} of {len(products)}")
                brand, model = self._parse_brand_model(product)
                processor = self._parse_processor(product)
                ram = self._parse_ram(product)
                storage = self._parse_storage(product)
                release_year = self._parse_release_year(product)
                screen_size = self._parse_screen_size(product)
                price = self._parse_price(product)
                source = self._scrape_source()
                scrape_url = self._parse_scrape_url(product)
                l = Laptop(
                    brand,
                    model,
                    processor,
                    ram,
                    storage,
                    release_year,
                    screen_size,
                    price,
                    source,
                    scrape_url,
                )
                laptops.append(l)
        return laptops
