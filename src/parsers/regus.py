from .base import BaseParser
from src.resources import MeetingRoom
from tqdm import tqdm
import re

class RegusParser(BaseParser):
    scrape_source = 'regus.com'
    url = "https://www.regus.com/en-gb/united-kingdom/{city}/listings"
    api_url = "https://www.regus.com/en-gb/united-kingdom/{city}/listings?page={page_num}"

    def __init__(self, city: str):
        if ' ' in city:
            city = city.replace(' ', '-')
        self.city = city
        self.url = self.url.format(city=city)
        self.api_url = self.api_url.format(page_num=1, city=city)

    def _get_num_pages(self):
        num_pages = self.soup.find_all(class_ = 'css-9vlari')
        pages = int(num_pages[0].text.split()[-2]) // 12 + 1
        return pages

    @staticmethod
    def _get_name(soup):
        name = soup.find_all(class_ = 'css-12hqcib')
        name = name[0].text
        return name

    @staticmethod
    def _get_price(soup):
        try:
            price = re.search(r".(\d{1,4}[.]{0,1}\d{0,2})", soup.text).group(1)
            price = float(price)
            return price
        except:
            pass
        return None

    def parse(self):
        rooms = []
        self.soup = self._make_soup(self.api_url.format(city = self.city))
        pages = self._get_num_pages()

        for page in tqdm(range(1, pages), desc='pages'):
            self.soup = self._make_soup(self.api_url.format(city=self.city, page_num=page))
            results = self.soup.find_all(class_ = 'css-1n32xsl')
            for result in results:
                name = self._get_name(result)
                items = result.find_all(class_ = 'css-1xe3qid')
                for item in items:
                    if 'Meeting Rooms' in item.text:
                        price = self._get_price(item)

                room = MeetingRoom(name=name,
                                    city=self.city,
                                    capacity_people=None,
                                    cost_hour=price,
                                    scrape_source=self.scrape_source,
                                    scrape_url=self.api_url.format(self.city, page)
                )
                rooms.append(room)
        return rooms
