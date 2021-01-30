import math
import re
from typing import Tuple, List, Dict, Optional
from bs4 import BeautifulSoup
from .base import BaseParser


class CurrysBaseParser(BaseParser):
    scrape_source = "currys.co.uk"

    def _get_items(self) -> List[BeautifulSoup]:
        products = self.soup.findAll("article", {"class": "product result-prd"})
        return products

    def _get_num_pages(self) -> int:
        text = self.soup.find('div', {"data-component": "list-page-results-message"}).text
        text = text.strip()
        match = re.search(r"^Showing \d - (\d+) of (\d+) results$", text)
        res_per_page = match.group(1)
        total_res = match.group(2)
        pages = math.ceil(float(total_res)/ float(res_per_page))
        return int(pages)
