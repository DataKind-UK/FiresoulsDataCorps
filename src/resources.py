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


### EQUIPMENT ###


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
class Desktop(BaseResource):
    brand: str
    model: str
    processor: str
    screen_size: float
    ram: int
    storage_hdd: int
    storage_ssd: int
    release_year: int
    optical_drive: str
    operative_system: str
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
    currenty: str
    scrape_source: str
    scrape_url: str
    scrape_date: datetime.date = datetime.datetime.today().date()


@dataclass
class Monitor(BaseResource):
    brand: str
    model: str
    screen_size: float
    price: float
    scrape_source: str
    scrape_url: str
    scrape_date: datetime.date = datetime.datetime.today().date()


@dataclass
class WiFiDongle(BaseResource):
    provider: str
    service_name: str
    upfront_cost: float
    total_cost: float
    data_allowance: str
    contract_months: int
    monthly_cost: float
    scrape_source: str
    scrape_url: str
    scrape_date: datetime.date = datetime.datetime.today().date()


@dataclass
class Printer(BaseResource):
    brand: str
    model: str
    functions: str
    printing_speed_ppm: int
    print_resolution: str
    connectivity: str
    release_year: int
    price: float
    scrape_source: str
    scrape_url: str
    scrape_date: datetime.date = datetime.datetime.today().date()


@dataclass
class Projector(BaseResource):
    brand: str
    model: str
    screen_size: float
    projection_type: str
    resolution: str
    brightness: int
    technology: str
    price: float
    scrape_source: str
    scrape_url: str
    scrape_date: datetime.date = datetime.datetime.today().date()


### PEOPLE ###


@dataclass
class People(BaseResource):
    region: str
    job_title: str
    soc_code: str
    mean: float
    first_decile: float
    first_quartile: float
    third_decile: float
    median: float
    seventh_decile: float
    third_quartile: float
    ninth_decile: float
    scrape_source: str
    scrape_url: str
    scrape_date: datetime.date = datetime.datetime.today().date()


### SPACE ###


@dataclass
class MeetingRoom(BaseResource):
    name: str
    city: str
    capacity_people: str
    cost_hour: float
    scrape_source: str
    scrape_url: str
    scrape_date: datetime.date = datetime.datetime.today().date()
