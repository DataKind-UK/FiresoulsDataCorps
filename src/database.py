import pymysql.cursors
from typing import Tuple, List, Any, Dict
import pandas as pd
import math
import datetime
from tqdm import tqdm
from .resources import (Laptop, Desktop, Tablet, Monitor, WiFiDongle, Printer,
                       Projector)


def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="scraper",
        password="firesouls",
        database="firesouls_db",
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection


def check_if_item_exists(table_name: str, url: str) -> Tuple[int, datetime.datetime.timestamp]:
    """
    Returns version and a timestamp for when the record is valid from.

    Parameters:
        url (str):

    Returns:
        version (int): version to be assigned to the record to be inserted.

        valid_from (datetime.timestamp):
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    valid_from = datetime.datetime.now()
    sql = """select scrape_url, version
            from {}
            where scrape_url = '{}'
                and valid_to is null;""".format(
        table_name, url
    )
    cursor.execute(sql)
    rows = cursor.fetchone()
    cursor.close()

    if rows is None:
        version = 1
    else:
        version = rows["version"]
        cursor2 = connection.cursor()
        update_query = """update {} set valid_to = '{}' 
                            where scrape_url = '{}'
                            and version = {};""".format(
            table_name, valid_from, url, version
        )
        cursor2.execute(update_query)
        connection.commit()
        version += 1
        cursor2.close()
    connection.close()
    return version, valid_from

def get_sql_script(table: str):
    pass


def insert_into_desktop(df: pd.DataFrame):
    """
    Insert new data in the `desktop` table.

    Parameters:
        df (pd.DataFrame):
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    df1 = df.where(pd.notnull(df), None)
    df1.drop_duplicates(inplace=True)

    sql = """insert into desktop (
        brand, 
        model, 
        processor, 
        screen_size,
        ram, 
        storage_hdd, 
        storage_ssd,
        release_year, 
        optical_drive,
        operative_system,
        price, 
        scrape_source, 
        scrape_url, 
        scrape_date,
        valid_from,
        version) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    for i, r in tqdm(df1.iterrows(), total=len(df1), desc="desktops"):
        version, valid_from = check_if_item_exists('desktop', r["scrape_url"])
        cursor.execute(
            sql,
            (
                r["brand"],
                r["model"],
                r["processor"],
                r["screen_size"],
                r["ram"],
                r["storage_hdd"],
                r["storage_ssd"],
                r["release_year"],
                r["optical_drive"],
                r["operative_system"],
                r["price"],
                r["scrape_source"],
                r["scrape_url"],
                r["scrape_date"],
                valid_from,
                version,
            ),
        )
        connection.commit()
    cursor.close()
    connection.close()


def insert_into_laptop(df: pd.DataFrame):
    """
    Insert new data in the `laptop` table.

    Parameters:
        df (pd.DataFrame):
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    df1 = df.where(pd.notnull(df), None)
    df1.drop_duplicates(inplace=True)

    sql = """insert into laptop (
        brand, 
        model, 
        processor, 
        ram, 
        storage, 
        release_year, 
        screen_size, 
        price, 
        scrape_source, 
        scrape_url, 
        scrape_date,
        valid_from,
        version) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    for i, r in tqdm(df.iterrows(), total=len(df), desc="laptops"):
        version, valid_from = check_if_item_exists('laptop', r["scrape_url"])
        cursor.execute(
            sql,
            (
                r["brand"],
                r["model"],
                r["processor"],
                r["ram"],
                r["storage"],
                r["release_year"],
                r["screen_size"],
                r["price"],
                r["scrape_source"],
                r["scrape_url"],
                r["scrape_date"],
                valid_from,
                version,
            ),
        )
        connection.commit()
    cursor.close()
    connection.close()


def insert_into_tablet(df):
    """
    Insert new data in the `tablet` table.

    Parameters:
        df (pd.DataFrame):
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    df1 = df.where(pd.notnull(df), None)
    df1.drop_duplicates(inplace=True)

    sql = """insert into tablet (
        brand, 
        model, 
        processor, 
        screen_size, 
        screen_resolution,
        storage, 
        release_year, 
        price,
        currency, 
        scrape_source, 
        scrape_url, 
        scrape_date,
        valid_from,
        version) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    for i, r in tqdm(df.iterrows(), total=len(df), desc="tablets"):
        version, valid_from = check_if_item_exists('tablet', r["scrape_url"])
        cursor.execute(
            sql,
            (
                r["brand"],
                r["model"],
                r["processor"],
                r["screen_size"],
                r["screen_resolution"],
                r["storage"],
                r["release_year"],
                r["price"],
                r.get('currency','GBP'),
                r["scrape_source"],
                r["scrape_url"],
                r["scrape_date"],
                valid_from,
                version,
            ),
        )
        connection.commit()
    cursor.close()
    connection.close()


def insert_into_monitor(df):
    pass


def insert_into_wifi_dongle(df):
    """
    Insert new data in the `wifi-dongle` table.

    Parameters:
        df (pd.DataFrame):
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    df1 = df.where(pd.notnull(df), None)
    df1.drop_duplicates(inplace=True)

    sql = """insert into wifi_dongle (
        provider, 
        service_name, 
        upfront_cost, 
        total_cost, 
        data_allowance,
        contract_months, 
        monthly_cost, 
        scrape_source, 
        scrape_url, 
        scrape_date,
        valid_from,
        version) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    for i, r in tqdm(df.iterrows(), total=len(df), desc="wifi_dongles"):
        version, valid_from = check_if_item_exists('wifi_dongle', r["scrape_url"])
        cursor.execute(
            sql,
            (
                r["provider"],
                r["service_name"],
                r["upfront_cost"],
                r["total_cost"],
                r["data_allowance"],
                r["contract_months"],
                r["monthly_cost"],
                r["scrape_source"],
                r["scrape_url"],
                r["scrape_date"],
                valid_from,
                version,
            ),
        )
        connection.commit()
    cursor.close()
    connection.close()


def insert_into_printer(df):
    """
    Insert new data in the `printer` table.

    Parameters:
        df (pd.DataFrame):
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    df1 = df.where(pd.notnull(df), None)
    df1.drop_duplicates(inplace=True)

    sql = """insert into printer (
        brand, 
        model, 
        functions, 
        printing_speed_ppm, 
        print_resolution,
        connectivity, 
        release_year,
        price, 
        scrape_source, 
        scrape_url, 
        scrape_date,
        valid_from,
        version) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    for i, r in tqdm(df.iterrows(), total=len(df), desc="printers"):
        version, valid_from = check_if_item_exists('printer', r["scrape_url"])
        cursor.execute(
            sql,
            (
                r["brand"],
                r["model"],
                r["functions"],
                r["printing_speed_ppm"],
                r["print_resolution"],
                r["connectivity"],
                r["release_year"],
                r["price"],
                r["scrape_source"],
                r["scrape_url"],
                r["scrape_date"],
                valid_from,
                version,
            ),
        )
        connection.commit()
    cursor.close()
    connection.close()


def insert_into_projector(df):
    pass



def insert_into_database(product_type: str, item_set: List[Dict[str, Any]]):
    """Channel the scraped products data into the correct insert_into_ method

    Parameters
    ----------
    product_type : str
        Product type of the item set
    item_set : List[Dict[str, Any]]
        List of scraped data

    Raises
    ------
    Exception
        When a product is not identified
    """

    df = pd.DataFrame(item_set)

    # This step is required since MySql doesn't know how to use NaN
    df = df.where(pd.notnull(df), None)

    if product_type == 'laptop':
        insert_into_laptop(df)
    elif product_type == 'desktop':
        insert_into_desktop(df)
    elif product_type == 'tablet':
        insert_into_tablet(df)
    elif product_type == 'monitor':
        insert_into_monitor(df)
    elif product_type == 'wifi_dongle':
        insert_into_wifi_dongle(df)
    elif product_type == 'printer':
        insert_into_printer(df)
    elif product_type == 'projector':
        insert_into_projector(df)
    else:
        raise Exception(f"Insert into database method not implemented for {product_type}")