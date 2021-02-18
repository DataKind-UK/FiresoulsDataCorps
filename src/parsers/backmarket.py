import pdb
import re
from typing import Tuple, List, Dict, Optional
from bs4 import BeautifulSoup
from .base import BaseParser
from src.resources import Laptop, Tablet


class BackmarketBaseParser(BaseParser):
    scrape_source = "backmarket.co.uk"

    def _get_items(self) -> List[BeautifulSoup]:
        products = self.soup.findAll("a", {"data-qa": "productThumb"})
        return products

    def _get_num_pages(self) -> int:
        try:
            pages = len(
                self.soup.find("nav", {"data-test": "pagination"}).findAll("button")
            )
        except AttributeError:
            pages = 1
            print(
                "Could not find a pagination object on the site, please make sure it's not due to a website change"
            )
        return pages


class BackmarketLaptopParser(BackmarketBaseParser):
    url = "https://www.backmarket.co.uk/refurbished-laptop-english.html"

    @staticmethod
    def _parse_brand_model(product: BeautifulSoup) -> Tuple[str, str]:
        title = product.find("p").text
        title = title.strip()
        brand_model = re.search(r"^(.+)?\s\d{2}[.]?\d{0,2}”", title).group(1)
        brand_model = brand_model.split(" ", 1)
        return brand_model[0], brand_model[1]

    @staticmethod
    def _parse_processor(product: BeautifulSoup) -> str:
        processor = product.find("ul").findAll("li")[1].findAll("span")[1].text
        processor = processor.strip()
        return processor

    @staticmethod
    def _parse_ram(product: BeautifulSoup) -> int:
        ram = product.find("ul").findAll("li")[4].findAll("span")[1].text
        ram = ram.strip()
        ram = ram.replace("GB", "")
        ram = int(ram)
        return ram

    @staticmethod
    def _parse_storage(product: BeautifulSoup) -> int:
        storage = product.find("ul").findAll("li")[3].findAll("span")[1].text
        storage = storage.strip()
        storage = storage.split()[0]
        storage = int(storage)
        return storage

    @staticmethod
    def _parse_release_year(product: BeautifulSoup) -> int:
        release_year = product.find("ul").findAll("li")[0].findAll("span")[1].text
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
        screen_size = product.find("p").text
        screen_size = screen_size.strip()
        screen_size = re.search(r".*(\d{2}[.]{0,1}\d{0,2})”\s?", screen_size).group(1)
        screen_size = float(screen_size)
        return screen_size

    @staticmethod
    def _parse_price(product: BeautifulSoup) -> float:
        price = product.find("div", {"data-qa": "prices"}).text
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


class BackmarketTabletParser(BackmarketBaseParser):
    url = "https://www.backmarket.co.uk/refurbished-tablets.html"

    @staticmethod
    def _parse_price(product: BeautifulSoup) -> float:
        price = product.find("div", {"class": "price primary large"}).text
        price = price.strip()
        price = price.replace("£", "").replace(",", "")
        price = float(price)
        return price

    @staticmethod
    def _parse_characteristics(product: BeautifulSoup) -> Dict[str, str]:
        chardict = {}
        chars = product.findAll("ul")[6].findAll("li")
        for char in chars:
            key = char.find("strong").text.replace(":", "").strip()
            chardict[key] = char.text.replace(key, "").replace(":", "").strip()
        return chardict

    @staticmethod
    def _parse_brand(chardict: Dict[str, str]) -> Optional[str]:
        return chardict.get("Brand").lower()

    @staticmethod
    def _parse_model(chardict: Dict[str, str]) -> Optional[str]:
        return chardict.get("Model").lower()

    @staticmethod
    def _parse_processor(chardict: Dict[str, str]) -> Optional[str]:
        processor = (
            chardict.get("Processor brand", "")
            + " "
            + chardict.get("Processor speed", "")
        )
        if processor == " ":
            return None
        return processor

    @staticmethod
    def _parse_screen_size(chardict: Dict[str, str]) -> float:
        screen_size = chardict.get("Screen size (in)", "0")
        screen_size = screen_size.replace(',', '.') if ',' in screen_size else screen_size
        return float(screen_size)

    @staticmethod
    def _parse_screen_resolution(chardict: Dict[str, str]) -> Optional[str]:
        return chardict.get("Resolution")

    @staticmethod
    def _parse_storage(chardict: Dict[str, str]) -> int:
        storage = chardict.get("Storage")
        storage = re.search(r"(\d+)", storage).group(1)
        return int(storage)

    @staticmethod
    def _parse_release_year(chardict: Dict[str, str]) -> int:
        year = chardict.get("Year of Release", "0")
        return int(year)

    def parse_single(self, url: str) -> Tablet:
        soup = self._make_soup(url)
        chardict = self._parse_characteristics(soup)
        brand = self._parse_brand(chardict)
        model = self._parse_model(chardict)
        processor = self._parse_processor(chardict)
        screen_size = self._parse_screen_size(chardict)
        screen_resolution = self._parse_screen_resolution(chardict)
        storage = self._parse_storage(chardict)
        release_year = self._parse_release_year(chardict)
        price = self._parse_price(soup)
        currency = "£"
        tablet = Tablet(
            brand,
            model,
            processor,
            screen_size,
            screen_resolution,
            storage,
            release_year,
            price,
            currency,
            self.scrape_source,
            url,
        )
        return tablet

    def parse(self) -> List[Tablet]:
        self.soup = self._make_soup(self.url)
        num_pages = self._get_num_pages()
        tablets = []
        for i in range(num_pages):
            print(f"Downloading page: {i+1}/{num_pages}")
            self.soup = self._make_soup(f"{self.url}?page={i+1}")
            products = self._get_items()
            count = 0
            for product in products:
                count += 1
                print(f"Parsing tablet {count} of {len(products)}")
                t = self.parse_single("www.backmarket.co.uk" + product["href"])
                tablets.append(t)
        return tablets
