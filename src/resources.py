"""resources.py
File to store the dataclasses for each of the resources being scraped.
"""
from dataclasses import dataclass, astuple, asdict
import datetime


class BaseResource:
    """Base class to define the basic methods shared throughout the objects"""

    def astuple(self):
        return astuple(self)

    def asdict(self):
        dictionary = asdict(self)
        dictionary["scrape_date"] = dictionary["scrape_date"].strftime("%Y-%m-%d")
        return dictionary


@dataclass
class Laptop(BaseResource):
    brand: str
    model: str
    processor: str
    ram: int
    storage: int
    release_year: int
    screen_size: float
    price: float
    scrape_source: str
    scrape_url: str
    scrape_date: datetime.date = datetime.datetime.today().date()


@dataclass
class Tablet(BaseResource):
    brand: str
    model: str
    processor: str
    screen_size: float
    screen_resolution: str
    storage: int
    release_year: int
    price: float
    scrape_source: str
    scrape_url: str
    scrape_date: datetime.date = datetime.datetime.today().date()
