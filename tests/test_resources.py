import pytest
import datetime
from src.resources import Laptop


@pytest.fixture
def laptop():

    l = Laptop("apple", "macbook", "i5", 16, 256, 2020, 15, 2000, "gumtree", "url")

    return l


def test_laptop_init(laptop):
    assert laptop.__dict__ == {
        "brand": "apple",
        "model": "macbook",
        "processor": "i5",
        "ram": 16,
        "storage": 256,
        "release_year": 2020,
        "screen_size": 15,
        "price": 2000,
        "scrape_source": "gumtree",
        "scrape_date": datetime.datetime.today().date(),
        "scrape_url": "url",
    }


def test_laptop_todict(laptop):
    assert laptop.asdict() == {
        "brand": "apple",
        "model": "macbook",
        "processor": "i5",
        "ram": 16,
        "storage": 256,
        "release_year": 2020,
        "screen_size": 15,
        "price": 2000,
        "scrape_source": "gumtree",
        "scrape_date": datetime.datetime.today().date(),
        "scrape_url": "url",
    }


def test_laptop_totuple(laptop):
    assert laptop.astuple() == (
        "apple",
        "macbook",
        "i5",
        16,
        256,
        2020,
        15,
        2000,
        "gumtree",
        "url",
        datetime.datetime.today().date(),
    )
