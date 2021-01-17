import pytest
import pandas as pd
from bs4 import BeautifulSoup
from src.parsers.valuecomputers import ValueComputersLaptopParser

@pytest.fixture
def soup():
    with open("tests/fixtures/valuecomputers/All refurbished laptops for sale.htm", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

@pytest.fixture
def soup_laptop():
    with open("tests/fixtures/valuecomputers/laptop_1.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def test_get_all_laptops_results(soup):
    df_results = ValueComputersLaptopParser.get_all_laptops_results(soup)
    assert isinstance(df_results, pd.DataFrame)

def test_parse_laptop_price(soup_laptop):
    price = ValueComputersLaptopParser._parse_laptop_price(soup_laptop)
    assert isinstance(price, float)

def test_parse_product_sku(soup_laptop):
    sku = ValueComputersLaptopParser._parse_product_sku(soup_laptop)
    assert isinstance(sku, str)

def test_parse_ram(soup_laptop):
    ram = ValueComputersLaptopParser._parse_ram(soup_laptop)
    assert not isinstance(ram, int)

def test_parse_screen_size(soup_laptop):
    pass

def test_parse_storage(soup_laptop):
    pass

def test_parse_brand(soup_laptop):
    pass
