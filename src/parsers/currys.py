import math
import re
from datetime import datetime
from typing import Tuple, List, Dict, Optional
from bs4 import BeautifulSoup
from .base import BaseParser
from src.resources import Laptop, Projector, Desktop


class CurrysBaseParser(BaseParser):
    scrape_source = "currys.co.uk"

    def _get_items(self) -> List[BeautifulSoup]:
        products = self.soup.findAll("article", {"class": ["product", "result-prd"]})
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
    def _parse_brand(product: BeautifulSoup) -> str:
        brand = product.find("span", {"data-product": "brand"}).text
        brand = brand.strip().lower()
        return brand

    @staticmethod
    def _parse_model_screen_size(product: BeautifulSoup) -> Tuple[str, Optional[float]]:
        name = product.find("span", {"data-product": "name"}).text
        name = name.split(" - ")[0].strip().lower()
        name = name.replace("laptop", "")
        screen_size = re.search(r"[.+]?(\d{2}[.]?\d{0,2}\")[.+]?", name)
        if screen_size is not None:
            screen_size = screen_size.group(1)
            name = name.replace(screen_size, "")
            screen_size = float(screen_size.replace('"', ""))
        name = name.strip()
        return name, screen_size

    @staticmethod
    def _parse_processor(product: BeautifulSoup) -> str:
        processor = product.find("ul", {"class": "productDescription"}).findAll("li")
        processor = processor[1].text
        processor = processor.lower().replace("processor", "").strip()
        return processor

    @staticmethod
    def _parse_ram_storage(
        product: BeautifulSoup,
    ) -> Tuple[Optional[int], Optional[int]]:
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

    @staticmethod
    def _parse_price(product: BeautifulSoup) -> float:
        price = product.find("div", {"class": "productPrices"}).text
        price = price.strip()
        price = price.replace(",", "")
        price = re.search(r".(\d{1,4}[.]{0,1}\d{0,2})", price).group(1)
        price = float(price)
        return price

    def _scrape_source(self) -> str:
        return self.scrape_source

    def _parse_scrape_url(self, product) -> str:
        url = product.find("div", {"class": "desc"})
        url = url.find("a", {"class": "in"})["href"]
        return url

    def parse(self) -> List[Laptop]:
        self.soup = self._make_soup(self._structure_url())
        num_pages = self._get_num_pages()
        laptops = []
        for i in range(num_pages):
            print(f"Downloading page: {i+1}/{num_pages}")
            self.soup = self._make_soup(self._structure_url(i + 1))
            products = self._get_items()
            count = 0
            for product in products:
                count += 1
                try:
                    print(f"Parsing laptop {count} of {len(products)}")
                    scrape_url = self._parse_scrape_url(product)
                    brand = self._parse_brand(product)
                    model, screen_size = self._parse_model_screen_size(product)
                    processor = self._parse_processor(product)
                    ram, storage = self._parse_ram_storage(product)
                    release_year = datetime.now().year - 1
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
                except Exception as e:
                    print(f"Scraping of item {count} failed with error {e}")
        return laptops


class CurrysProjectorParser(CurrysBaseParser):
    url = "https://www.currys.co.uk/gbuk/computing/projectors/projectors/570_4432_32094_xx_xx/{}_50/relevance-desc/xx-criteria.html"

    def _structure_url(self, page: int = 1) -> str:
        return self.url.format(page)

    @staticmethod
    def _parse_brand(product: BeautifulSoup) -> Tuple[str, str]:
        brand = product.find("span", {"data-product": "brand"}).text
        brand = brand.strip().lower()
        return brand

    @staticmethod
    def _parse_model(product: BeautifulSoup) -> str:
        model = product.find("span", {"data-product": "name"}).text
        model = model.strip().lower()
        return model

    @staticmethod
    def _parse_price(product: BeautifulSoup) -> float:
        price = product.find("div", {"class": "productPrices"}).text
        price = price.strip()
        price = price.replace(",", "")
        price = re.search(r".(\d{1,4}[.]{0,1}\d{0,2})", price).group(1)
        price = float(price)
        return price

    @staticmethod
    def _parse_tech_specs(product_page: BeautifulSoup) -> Dict[str, str]:
        table = product_page.find("div", {"class": ["tab-tech-specs"]})
        keys = [x.text for x in table.findAll("th")]
        values = [x.text for x in table.findAll("td")]
        tech_specs = dict(zip(keys, values))
        return tech_specs

    @staticmethod
    def _parse_screen_size(tech_specs: Dict[str, str]) -> Optional[int]:
        screen = tech_specs.get("Screen size range")
        if screen is None:
            return screen
        size = re.search(r"(\d+)\"$", screen).group(1)
        return int(size)

    @staticmethod
    def _parse_projection_type(tech_specs: Dict[str, str]) -> Optional[str]:
        res = tech_specs.get("Projection type")
        if res is None:
            return res
        res = res.strip().lower()
        return res

    @staticmethod
    def _parse_resolution(tech_specs: Dict[str, str]) -> Optional[str]:
        res = tech_specs.get("Resolution")
        if res is None:
            return res
        res = res.strip().lower()
        return res

    @staticmethod
    def _parse_brightness(tech_specs: Dict[str, str]) -> Optional[int]:
        res = tech_specs.get("Brightness")
        if res is None:
            return res
        res = re.search(r"(\d+)", res.replace(",", "")).group(1)
        return int(res)

    @staticmethod
    def _parse_technology(tech_specs: Dict[str, str]) -> Optional[str]:
        res = tech_specs.get("Technology")
        if res is None:
            return res
        res = res.strip().lower()
        return res

    def _scrape_source(self) -> str:
        return self.scrape_source

    def _parse_scrape_url(self, product) -> str:
        url = product.find("header", {"class": "productTitle"})
        url = url.find("a")["href"]
        return url

    def parse(self) -> List[Projector]:
        self.soup = self._make_soup(self._structure_url())
        num_pages = self._get_num_pages()
        projectors = []
        for i in range(num_pages):
            print(f"Downloading page: {i+1}/{num_pages}")
            self.soup = self._make_soup(self._structure_url(i + 1))
            products = self._get_items()
            count = 0
            for product in products:
                count += 1
                try:
                    print(f"Parsing projector {count} of {len(products)}")
                    scrape_url = self._parse_scrape_url(product)
                    brand = self._parse_brand(product)
                    model = self._parse_model(product)
                    price = self._parse_price(product)
                    scrape_url = self._parse_scrape_url(product)
                    product_soup = self._make_soup(scrape_url)
                    product_tech_specs = self._parse_tech_specs(product_soup)
                    screen_size = self._parse_screen_size(product_tech_specs)
                    projection_type = self._parse_projection_type(product_tech_specs)
                    resolution = self._parse_resolution(product_tech_specs)
                    brightness = self._parse_brightness(product_tech_specs)
                    technology = self._parse_technology(product_tech_specs)
                    source = self._scrape_source()

                    p = Projector(
                        brand,
                        model,
                        screen_size,
                        projection_type,
                        resolution,
                        brightness,
                        technology,
                        price,
                        source,
                        scrape_url,
                    )
                    projectors.append(p)
                except Exception as e:
                    print(f"Scraping of item {count} failed with error {e}")
        return projectors


class CurrysDesktopParser(CurrysBaseParser):
    url = "https://www.currys.co.uk/gbuk/computing/desktop-pcs/desktop-pcs/317_3055_30057_xx_xx/{}_50/relevance-desc/xx-criteria.html"

    def _structure_url(self, page: int = 1) -> str:
        return self.url.format(page)

    @staticmethod
    def _parse_brand(product: BeautifulSoup) -> Tuple[str, str]:
        brand = product.find("span", {"data-product": "brand"}).text
        brand = brand.strip().lower()
        return brand

    @staticmethod
    def _parse_model(product: BeautifulSoup) -> str:
        model = product.find("span", {"data-product": "name"}).text
        model = model.split(" - ")[0].strip().lower()
        return model

    @staticmethod
    def _parse_price(product: BeautifulSoup) -> float:
        price = product.find("div", {"class": "productPrices"}).text
        price = price.strip()
        price = price.replace(",", "")
        price = re.search(r".(\d{1,4}[.]{0,1}\d{0,2})", price).group(1)
        price = float(price)
        return price

    @staticmethod
    def _parse_tech_specs(product_page: BeautifulSoup) -> Dict[str, str]:
        table = product_page.find("div", {"class": ["tab-tech-specs"]})
        keys = [x.text for x in table.findAll("th")]
        values = [x.text for x in table.findAll("td")]
        tech_specs = dict(zip(keys, values))
        return tech_specs

    @staticmethod
    def _parse_screen_size(tech_specs: Dict[str, str]) -> Optional[float]:
        screen = tech_specs.get("Screen size")
        if screen is None:
            return screen
        size = re.search(r"(\d{2}[.]{0,1}\d{0,2})\"$", screen)
        if size is None:
            return size
        size = size.group(1)
        return float(size)

    @staticmethod
    def _parse_ram(tech_specs: Dict[str, str]) -> Optional[int]:
        ram = tech_specs.get("RAM")
        if ram is None:
            return None
        ram = re.search(r"(\d+) GB", ram)
        if ram is None:
            return ram
        ram = ram.group(1)
        return int(ram)

    @staticmethod
    def _parse_processor(tech_specs: Dict[str, str]) -> Optional[str]:
        proc = tech_specs.get("Processor")
        if proc is None:
            return proc
        proc = proc.lower().split("\n")[0]
        proc = proc.replace("processor", "").replace("- ", "").strip()
        return proc

    @staticmethod
    def _parse_storage_hdd(tech_specs: Dict[str, str]) -> Optional[int]:
        storage = tech_specs.get("Storage")
        if storage is None:
            return storage
        storage = re.search(r"(\d+) (TB|GB) HDD", storage)
        if storage is None:
            return storage
        storage = storage.group(1)
        storage = int(storage)
        if storage < 10:
            storage = storage * 1000
        return storage

    @staticmethod
    def _parse_storage_ssd(tech_specs: Dict[str, str]) -> Optional[int]:
        storage = tech_specs.get("Storage")
        if storage is None:
            return storage
        storage = re.search(r"(\d+) (TB|GB) SSD", storage)
        if storage is None:
            return storage
        storage = storage.group(1)
        storage = int(storage)
        if storage < 10:
            storage = storage * 1000
        return storage

    @staticmethod
    def _parse_optical_drive(tech_specs: Dict[str, str]) -> Optional[str]:
        drive = tech_specs.get("Disc drive", "No")
        drive = drive.strip()
        return drive

    @staticmethod
    def _parse_operating_system(tech_specs: Dict[str, str]) -> Optional[str]:
        os = tech_specs.get("Operating system")
        return os

    def _scrape_source(self) -> str:
        return self.scrape_source

    def _parse_scrape_url(self, product) -> str:
        url = product.find("header", {"class": "productTitle"})
        url = url.find("a")["href"]
        return url

    def parse(self) -> List[Desktop]:
        self.soup = self._make_soup(self._structure_url())
        num_pages = self._get_num_pages()
        desktops = []
        for i in range(num_pages):
            print(f"Downloading page: {i+1}/{num_pages}")
            self.soup = self._make_soup(self._structure_url(i + 1))
            products = self._get_items()
            count = 0
            for product in products:
                count += 1
                print(f"Parsing desktop {count} of {len(products)}")
                try:
                    brand = self._parse_brand(product)
                    model = self._parse_model(product)
                    price = self._parse_price(product)
                    scrape_url = self._parse_scrape_url(product)
                    product_soup = self._make_soup(scrape_url)
                    product_tech_specs = self._parse_tech_specs(product_soup)
                    screen_size = self._parse_screen_size(product_tech_specs)
                    processor = self._parse_processor(product_tech_specs)
                    ram = self._parse_ram(product_tech_specs)
                    storage_hdd = self._parse_storage_hdd(product_tech_specs)
                    storage_ssd = self._parse_storage_ssd(product_tech_specs)
                    release_year = datetime.now().year - 1
                    optical_drive = self._parse_optical_drive(product_tech_specs)
                    os = self._parse_operating_system(product_tech_specs)
                    source = self._scrape_source()

                    p = Desktop(
                        brand,
                        model,
                        processor,
                        screen_size,
                        ram,
                        storage_hdd,
                        storage_ssd,
                        release_year,
                        optical_drive,
                        os,
                        price,
                        source,
                        scrape_url,
                    )
                    desktops.append(p)
                except Exception as e:
                    print(f"Scraping of item {count} failed with error {e}")
        return desktops
