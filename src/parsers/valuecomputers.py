from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
from typing import List
from src.parsers.base import BaseParser
from src.resources import Laptop


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
    def _parse_laptop_price(soup):
        price = soup.find(class_="product-price")
        price = price.text.split()[0]
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
            elif 'GB' in ram:
                return int(ram.replace('GB', '').strip())

    def _scrape_source(self) -> str:
        return self.scrape_source

    def get_laptop_specs(self, url):
        """
        Returns a dataframe
        """
        soup = self._make_soup(url, False)
        price = self._parse_laptop_price(soup)
        sku = self._parse_product_sku(soup)
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
        return df

    def get_all_laptops_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, r in tqdm(df.head().iterrows(), total=len(df)):
            time.sleep(1)
            if i == 0:
                df_specs = self.get_laptop_specs(r.url)
            else:
                df_specs = df_specs.append(self.get_laptop_specs(r.url))

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
            brand = ""
            model = ""
            processor = r["Processor"]
            ram = self._parse_ram(r["RAM"]),
            storage = r["Storage"]
            release_year = ""
            screen_size = r["Screen Size"]
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
        self.soup = self._make_soup(self.url, False)
        laptops = []
        df_results = self.get_all_laptops_results(self.soup)
        df_specs = self.get_all_laptops_specs(df_results)

        laptops = self.cast_laptops(df_specs)

        return laptops
