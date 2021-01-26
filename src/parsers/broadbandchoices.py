"""
Class to extract broadband dongle contracts from the Broadbandchoices price comparison site
"""
from typing import Tuple, List
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

    @staticmethod
    def _get_data(product: BeautifulSoup) -> List[BeautifulSoup]:
        data = product.findAll('div', {'class': 'deal-info__wrapper'})
        return data

    @staticmethod
    def _get_value(container: BeautifulSoup) -> str:
        value = container.find('span', {'class': 'deal-info__value'}).text
        return value

    def get_upfront_cost(self, data: List[BeautifulSoup]) -> float:
        upfront_cost = self._get_value(data[0])
        upfront_cost = upfront_cost.replace('£', '')
        return float(upfront_cost)

    def get_total_cost(self, data: List[BeautifulSoup]) -> float:
        total_cost = self._get_value(data[1])
        total_cost = total_cost.replace('£', '')
        return float(total_cost)

    def get_allowance(self, data: List[BeautifulSoup]) -> str:
        allowance = self._get_value(data[2])
        return allowance

    def get_contract_months(self, data: List[BeautifulSoup]) -> int:
        contract_months = self._get_value(data[3])
        return int(contract_months)

    def get_monthly_cost(self, data: List[BeautifulSoup]) -> int:
        monthly_cost = self._get_value(data[4])
        monthly_cost = monthly_cost.replace('£', '')
        return float(monthly_cost)

    def parse(self):
        self.soup = self._make_soup(self.URL)
        elems = self.get_elements()
        