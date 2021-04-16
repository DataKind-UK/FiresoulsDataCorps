"""
Class to extract broadband dongle contracts from the Broadbandchoices price comparison site
"""
from typing import Tuple, List, Dict, Any
import re
import tqdm
from bs4 import BeautifulSoup
from .base import BaseParser
from src.resources import WiFiDongle


class BroadbandchoicesDongleParser(BaseParser):
    scrape_source = "broadbandchoices.co.uk"
    URL = (
        "https://www.broadbandchoices.co.uk/mobile/results/devicescontracts?isDataOnlyDevice=true&page={}&deviceCondition=New&unlimitedData=true&unlimitedTexts=false&unlimitedMinutes=false&includeResellers=true&includeExistingCustomersHandset=false"
    )

    def _set_api_url(self, page: int):
        self.api_url = self.URL.format(page)

    def _get_data(self, page: int = 1):
        self._set_api_url(page)
        data = self._make_json(self.api_url)
        return data

    def _get_deals(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return data.get('deals', [])

    def parse(self) -> List[WiFiDongle]:
        dongles = []
        data = self._get_data()
        deals = self._get_deals(data)
        page = 1
        while len(deals) > 0:
            print(f"Scraping page {page} of {self.scrape_source}")
            for deal in tqdm.tqdm(deals):
                provider = deal.get('merchant', {}).get('name')
                service = deal.get('tariff', {}).get('connectionType', {}).get('label')
                upfront_cost = deal.get('tariff', {}).get('upfrontCosts', {}).get('sortValue')
                monthly_cost = deal.get('tariff', {}).get('totalMonthlyCost')
                total_cost = deal.get('tariff', {}).get('totalContractCost')
                data_allowance = deal.get('tariff', {}).get('data', {}).get('label')
                contract_months = deal.get('tariff', {}).get('contractLength', {}).get('sortValue')
                iden = deal.get('dealHash')
                prod = WiFiDongle(
                    provider,
                    service,
                    upfront_cost,
                    total_cost,
                    data_allowance,
                    contract_months,
                    monthly_cost,
                    self.scrape_source,
                    iden,
                )
                dongles.append(prod)
            page+=1
            data = self._get_data(page=page)
            deals = self._get_deals(data)
        return dongles
