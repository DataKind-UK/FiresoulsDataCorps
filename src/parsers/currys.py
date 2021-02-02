import math
import re
from typing import Tuple, List, Dict, Optional
from bs4 import BeautifulSoup
from .base import BaseParser
from src.resources import Laptop


class CurrysBaseParser(BaseParser):
    scrape_source = "currys.co.uk"

    def _get_items(self) -> List[BeautifulSoup]:
        products = self.soup.findAll("article", {"class": "product result-prd"})
        return products

    def _get_num_pages(self) -> int:
        text = self.soup.find(
            "div", {"data-component": "list-page-results-message"}
        ).text
        text = text.strip()
        match = re.search(r"^Showing \d - (\d+) of (\d+) results$", text)
        res_per_page = match.group(1)
        total_res = match.group(2)
        pages = math.ceil(float(total_res) / float(res_per_page))
        return int(pages)


class CurrysLaptopParser(CurrysBaseParser):
    url = "https://www.currys.co.uk/gbuk/computing/laptops/laptops/315_3226_30328_xx_xx/{}_50/relevance-desc/xx-criteria.html"

    def _structure_url(self, page: int = 1) -> str:
        return self.url.format(page)

    @staticmethod
    def _parse_brand(product: BeautifulSoup) -> Tuple[str, str]:
        brand = product.find("span", {"data-product": "brand"}).text
        brand = brand.strip().lower()
        return brand

    @staticmethod
    def _parse_model_screen_size(product: BeautifulSoup) -> Tuple[str, float]:
        name = product.find("span", {"data-product": "name"}).text
        name = name.split(" - ")[0].strip().lower()
        name = name.replace("laptop", "")
        screen_size = re.search(r".+(\d{2}[.]?\d{0,2}\").+", name).group(1)
        name = name.replace(screen_size, "").strip()
        screen_size = float(screen_size.replace('"', ""))
        return name, screen_size

    @staticmethod
    def _parse_processor(product: BeautifulSoup) -> str:
        processor = product.find("ul", {"class": "productDescription"}).findAll("li")
        processor = processor[1].text
        processor = processor.lower().replace("processor", "").strip()
        return processor

    @staticmethod
    def _parse_ram_storage(product: BeautifulSoup) -> Tuple[Optional[int], Optional[int]]:
        ram = None
        storage = None
        feats = product.find("ul", {"class": "productDescription"})
        feat = feats.text
        match = re.search(r"RAM: (\d+) GB", feat)
        if match is not None:
            ram = match.group(1)
            ram = int(ram)
        match = re.search(r"Storage: (\d+) GB", feat)
        if match is not None:
            storage = match.group(1)
            storage = int(storage)
        return ram, storage

    # @staticmethod
    # def _parse_storage(product: BeautifulSoup) -> int:
    #     storage = product.find("ul").findAll("li")[3].findAll("span")[1].text
    #     storage = storage.strip()
    #     storage = storage.split()[0]
    #     storage = int(storage)
    #     return storage

    # @staticmethod
    # def _parse_release_year(product: BeautifulSoup) -> int:
    #     release_year = product.find("ul").findAll("li")[0].findAll("span")[1].text
    #     release_year = release_year.strip()
    #     try:
    #         release_year = re.search(r"([0-9]{4})", release_year).group(1)
    #     except AttributeError:
    #         print("\tRelease Year not specified for this laptop")
    #         release_year = "0"
    #     release_year = int(release_year)
    #     return release_year

    # @staticmethod
    # def _parse_price(product: BeautifulSoup) -> float:
    #     price = product.find("div", {"data-qa": "prices"}).text
    #     price = price.strip()
    #     price = price.replace(",", "")
    #     price = re.search(r".(\d{1,4}[.]{0,1}\d{0,2})", price).group(1)
    #     price = float(price)
    #     return price

    # def _scrape_source(self) -> str:
    #     return self.scrape_source

    # def _parse_scrape_url(self, product) -> str:
    #     return self.scrape_source + product["href"]

    # def parse(self) -> List[Laptop]:
    #     self.soup = self._make_soup(self.url)
    #     num_pages = self._get_num_pages()
    #     laptops = []
    #     for i in range(num_pages):
    #         print(f"Downloading page: {i+1}/{num_pages}")
    #         self.soup = self._make_soup(f"{self.url}?page={i+1}")
    #         products = self._get_items()
    #         count = 0
    #         for product in products:
    #             count += 1
    #             print(f"Parsing laptop {count} of {len(products)}")
    #             brand, model = self._parse_brand_model(product)
    #             processor = self._parse_processor(product)
    #             ram = self._parse_ram(product)
    #             storage = self._parse_storage(product)
    #             release_year = self._parse_release_year(product)
    #             screen_size = self._parse_screen_size(product)
    #             price = self._parse_price(product)
    #             source = self._scrape_source()
    #             scrape_url = self._parse_scrape_url(product)
    #             l = Laptop(
    #                 brand,
    #                 model,
    #                 processor,
    #                 ram,
    #                 storage,
    #                 release_year,
    #                 screen_size,
    #                 price,
    #                 source,
    #                 scrape_url,
    #             )
    #             laptops.append(l)
    #     return laptops