from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from typing import Optional
import time
import re
from typing import List
from src.parsers.base import BaseParser
from src.resources import Laptop, Desktop


class ValueComputersLaptopParser(BaseParser):
    scrape_source = "valucomputers.co.uk"
    url = "https://www.valucomputers.co.uk/acatalog/all-laptops.html"

    @staticmethod
    def get_all_laptops_results(soup: BeautifulSoup) -> pd.DataFrame:
        """
        Returns a dataframe with two columns: title and url. This is from
        the results page. The url takes to the webpage of the laptop and
        title is the description in the results page.

        Parameters:
            soup (BeautifulSoup): Parser of the html code of the results page.

        Returns:
            df (pd.DataFrame): A dataframe with description and url to the
                laptop in the results.
        """
        url_base = "https://www.valucomputers.co.uk/acatalog/{}"
        results = []
        for item in soup.find_all(class_="std-product-details"):
            for link in item.find_all("a", href=True):
                if len(link.text) > 0:
                    results.append((link.text, url_base.format(link["href"])))

        columns = ["title", "url"]
        df = pd.DataFrame(results, columns=columns)
        return df

    @staticmethod
    def _parse_price(soup):
        price = soup.find(class_="product-price")
        price = price.text.split()[0]
        price = re.search(r".(\d{1,4}[.]{0,1}\d{0,2})", price).group(
            1
        )  # code taken from backmarket.py
        price = float(price)  # code taken from backmarket.py
        return price

    @staticmethod
    def _parse_product_sku(soup):
        """
        Example: "Product ID: 1525white"
        """
        sku = soup.find(class_="sku")
        sku = sku.text.split(":")[1].strip()
        return sku

    @staticmethod
    def _parse_ram(ram: str):
        if len(str(ram)) > 0:
            if isinstance(ram, float):
                return None
            elif "GB" in ram:
                return int(ram.replace("GB", ""))

    @staticmethod
    def _parse_screen_size(screen_size: str) -> Optional[float]:
        screen_size = screen_size.replace('"', "")
        try:
            screen_size_res = float(screen_size)
        except:
            return None
        return screen_size_res

    @staticmethod
    def _parse_storage(storage: str):
        if storage == "nan":
            return None
        else:
            storage = re.search(r"([0-9]*)", storage).group(0)
            storage = float(storage)
            return storage

    @staticmethod
    def _parse_brand(title: str):
        brands = [
            "Acer",
            "Alienware",
            "Apple",
            "Asus",
            "Dell",
            "Google",
            "HP",
            "Lenovo",
            "Microsoft",
            "Razer",
            "Samsung",
        ]
        brand = [w for w in title.split() if w.lower() in [x.lower() for x in brands]]
        if len(brand) > 0:
            brand = brand[0]
            return brand
        elif "ProBook" in title:
            brand = "HP"
            return brand
        else:
            return "Brand not found"

    def _scrape_source(self) -> str:
        return self.scrape_source

    def get_laptop_specs(self, row):
        """
        Returns a dataframe
        """
        title, url = row
        soup = self._make_soup(url, False)
        price = self._parse_price(soup)
        sku = self._parse_product_sku(soup)
        brand = self._parse_brand(title)
        specs_list = []
        for item in soup.find_all(class_="tab-content"):
            specs = item.find(id="specs")
            table = specs.find("table")
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                specs_list.append((url, cols[0].text, cols[1].text))

        columns = ["url", "spec", "value"]
        df_laptop = pd.DataFrame(specs_list, columns=columns)

        df = df_laptop.pivot_table(
            columns="spec", values="value", aggfunc="max", index="url"
        )
        df["price"] = price
        df["sku"] = sku
        df["url"] = url
        df["brand"] = brand
        return df

    def get_all_laptops_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, r in tqdm(df.iterrows(), total=len(df)):
            time.sleep(1)
            if i == 0:
                df_specs = self.get_laptop_specs(r)
            else:
                df_specs = df_specs.append(self.get_laptop_specs(r))

        return df_specs

    def cast_laptops(self, df: pd.DataFrame):
        """
        Columns in specifications
        ['Processor',
        'RAM',
        'Storage',
        'Screen Size',
        'price',
        'url',

        'HDMI',
        'No. of USB Ports',
        'Operating System',
        'Optical Drive',
        'Ports',
        'Size/Weight',
        'Warranty',
        'Wireless',
        'sku',
        '5 in 1 Card Reader',
        'Firewire',
        'Display Resolution',
        'Serial Port',
        'Graphics Card',
        'Webcam']
        """
        laptops = []
        for i, r in df.iterrows():
            brand = r["brand"]
            model = ""
            processor = r["Processor"]
            ram = self._parse_ram(r["RAM"])
            storage = self._parse_storage(str(r["Storage"]))
            release_year = None
            screen_size = self._parse_screen_size(r["Screen Size"])
            price = r["price"]
            source = self._scrape_source()
            scrape_url = r["url"]

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

    def parse(self) -> List[Laptop]:
        self.soup = self._make_soup(self.url, use_proxy=False)
        laptops = []
        df_results = self.get_all_laptops_results(self.soup)
        df_specs = self.get_all_laptops_specs(df_results)

        laptops = self.cast_laptops(df_specs)

        return laptops


class ValueComputersDesktopParser(BaseParser):
    scrape_source = "valucomputers.co.uk"
    url = "https://www.valucomputers.co.uk/acatalog/Refurbished-Desktops.html"

    @staticmethod
    def get_all_desktops_results(soup: BeautifulSoup) -> pd.DataFrame:
        """"""
        url_base = "https://www.valucomputers.co.uk/acatalog/{}"
        results = []
        for item in soup.find_all(class_="product-list"):
            for link in item.find_all("a", href=True):
                if len(link.text) > 0:
                    results.append((link.text, url_base.format(link["href"])))

        columns = ["title", "url"]
        df = pd.DataFrame(results, columns=columns)
        return df

    @staticmethod
    def _parse_price(soup):
        price = soup.find(class_="product-price")
        price = price.text.split()[0]
        price = re.search(r".(\d{1,4}[.]{0,1}\d{0,2})", price).group(1)
        price = float(price)
        return price

    @staticmethod
    def _parse_brand(title: str):
        brands = [
            "Acer",
            "Alienware",
            "Apple",
            "Asus",
            "Dell",
            "Google",
            "HP",
            "Lenovo",
            "Microsoft",
            "Razer",
            "Samsung",
        ]
        brand = [w for w in title.split() if w.lower() in [x.lower() for x in brands]]
        if len(brand) > 0:
            brand = brand[0]
            return brand
        elif "ProBook" in title:
            brand = "HP"
            return brand
        else:
            return "Brand not found"

    @staticmethod
    def _parse_ram(ram: str):
        if len(str(ram)) > 0:
            if isinstance(ram, float):
                return None
            elif "GB" in ram:
                return int(ram.replace("GB", ""))

    def _scrape_source(self) -> str:
        return self.scrape_source

    @staticmethod
    def _parse_storage(storage: str):
        storage_hdd = None
        storage_ssd = None

        if storage == "nan":
            return None, None
        else:
            if "hdd" in storage.lower():
                storage_hdd = re.search(r"([0-9]*)", storage).group(1)
                storage_hdd = float(storage_hdd)
                if "tb" in storage.lower():
                    return storage_hdd * 1000, None
                else:
                    return storage_hdd, None
            elif "ssd" in storage.lower():
                storage_ssd = re.search(r"([0-9]*)", storage).group(1)
                storage_ssd = float(storage_ssd)
                if "tb" in storage.lower():
                    return None, storage_ssd * 1000
                else:
                    return None, storage_ssd
            else:
                return None, None

    def get_desktop_specs(self, row):_parse_storage
        """
        Returns a dataframe
        """
        title, url = row
        soup = self._make_soup(url, False)
        price = self._parse_price(soup)
        brand = self._parse_brand(title)
        specs_list = []
        for item in soup.find_all(class_="tab-content"):
            specs = item.find(id="specs")
            table = specs.find("table")
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                # There could be cases with a single cell describing the desktop.
                if len(cols) == 2:
                    specs_list.append((url, cols[0].text, cols[1].text))

        columns = ["url", "spec", "value"]
        df_laptop = pd.DataFrame(specs_list, columns=columns)

        df = df_laptop.pivot_table(
            columns="spec", values="value", aggfunc="max", index="url"
        )
        df["price"] = price
        df["url"] = url
        df["brand"] = brand
        return df

    def cast_desktops(self, df: pd.DataFrame):
        """"""
        desktops = []
        for i, r in df.iterrows():
            brand = r["brand"]
            model = ""
            processor = r["Processor"]
            ram = self._parse_ram(r["RAM"])
            storage_hdd, storage_ssd = self._parse_storage(str(r["Storage"]))
            optical_drive = r["Optical Drive"]
            operative_system = r["Operating System"]
            screen_size = r["Screen Size"]
            release_year = str("")
            price = r["price"]
            scrape_source = self._scrape_source()
            scrape_url = r["url"]

            d = Desktop(
                brand,
                model,
                processor,
                screen_size,
                ram,
                storage_hdd,
                storage_ssd,
                release_year,
                optical_drive,
                operative_system,
                price,
                scrape_source,
                scrape_url,
            )
            desktops.append(d)
        return desktops

    def get_all_desktops_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, r in tqdm(df.iterrows(), total=len(df)):
            time.sleep(1)
            if i == 0:
                df_specs = self.get_desktop_specs(r)
            else:
                df_specs = df_specs.append(self.get_desktop_specs(r))

        return df_specs

    def parse(self) -> List[Desktop]:
        self.soup = self._make_soup(self.url, use_proxy=False)
        desktops = []
        df_results = self.get_all_desktops_results(self.soup)
        df_specs = self.get_all_desktops_specs(df_results)

        desktops = self.cast_desktops(df_specs)

        return desktops
