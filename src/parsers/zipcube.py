from .base import BaseParser
from src.resources import MeetingRoom


class ZipcubeParser(BaseParser):
    scrape_source = "zipcube.com"
    url = "https://www.zipcube.com/uk/s/meeting-rooms/{city}--UK"
    api_url = "https://api.zipcube.com/api/search?page={page_num}&tag=meeting-rooms&location={city}--UK"

    def __init__(self, city: str):
        self.city = city
        self.url = self.url.format(city=city)
        self.api_url = self.api_url.format(page_num=1, city=city)

    @staticmethod
    def _get_rooms(data):
        return data["results"]["data"]

    @staticmethod
    def _get_num_pages(data):
        return data["results"]["last_page"]

    def parse(self):
        rooms = []
        page = 1
        while True:
            print(f"Scraping page {page}")
            url = self.api_url.format(page_num=page, city=self.city)
            data = self._make_json(url=url, use_proxy=True)
            data_rooms = self._get_rooms(data)
            for room in data_rooms:
                mr = MeetingRoom(
                    name=room.get("title"),
                    city=self.city,
                    capacity_people=room.get("max_capacity"),
                    cost_hour=room.get("listing_hourly_rate"),
                    scrape_source=self.scrape_source,
                    scrape_url=self.scrape_source + room.get("url"),
                )
                rooms.append(mr)
            if page == self._get_num_pages(data):
                break
            page += 1
        return rooms
