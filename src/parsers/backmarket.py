import pdb
import re
from typing import Tuple
from bs4 import BeautifulSoup
from .base import BaseParser

class BackmarketLaptopParser(BaseParser):
    
    def _get_items(self):
        products = self.soup.findAll("a", {"data-qa": "productThumb"})
        return products

    @staticmethod
    def _parse_brand_model(product: BeautifulSoup) -> Tuple[str, str]:
        title = product.find('h2',{'data-test':'title'}).text
        title = title.strip()
        brand_model = re.search(r'^(.+)?\s\d{2}[.]?\d{0,2}”', title).group(1)
        brand_model = brand_model.split(' ', 1)
        return brand_model[0], brand_model[1]


    def parse(self):
        pass