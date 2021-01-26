"""
Class to extract broadband dongle contracts from the Broadbandchoices price comparison site
"""
from typing import Tuple
import re
from bs4 import BeautifulSoup
from .base import BaseParser

class BroadbandchoicesDongleParser(BaseParser):
    URL = "https://www.broadbandchoices.co.uk/mobile-broadband/dongles?unlimitedData=true"


    def get_elements(self) -> BeautifulSoup:
        elements = self.soup.findAll('div', {'class':'deal-container'})
        return elements

    @staticmethod
    def get_provider_service(product: BeautifulSoup) -> Tuple[str]:
        header = product.find('div', {'class': 'deal-container__title'}).text
        provider = re.search(r"(.+)\s\d{1}G", header).group(1)
        service = header.replace(provider, "", 1).strip()
        return provider, service

    def parse(self):
        self.soup = self._make_soup(self.URL)