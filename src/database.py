import pymysql.cursors
import pandas as pd
import math
import datetime


def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="scraper",
        password="firesouls",
        database="firesouls_db",
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection


def get_sql_script(table: str):
    pass


def insert_into_desktop(df: pd.DataFrame):
    """
    Insert new data in the `desktop` table.

    Parameters:
        df (pd.DataFrame):
    """

    def check_if_desktop_exists(url):
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
                from desktop
                where scrape_url = '{}'
                    and valid_to is null;""".format(
            url
        )
        cursor.execute(sql)
        rows = cursor.fetchone()
        cursor.close()

        if rows is None:
            version = 1
        else:
            version = rows["version"]
            cursor2 = connection.cursor()
            update_query = """update desktop set valid_to = '{}' 
                                where scrape_url = '{}'
                                and version = {};""".format(
                valid_from, url, version
            )
            cursor2.execute(update_query)
            connection.commit()
            version += 1
            cursor2.close()
        connection.close()
        return version, valid_from

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
        version, valid_from = check_if_desktop_exists(r["scrape_url"])
        cursor.execute(
            sql,
            (
                r["brand"],
                r["model"],
                r["processor"],
                str(r["screen_size"]),
                r["ram"],
                r["storage_hdd"],
                r["storage_ssd"],
                str(r["release_year"]),
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
    def check_if_laptop_exists(url):
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
                from laptop
                where scrape_url = '{}'
                    and valid_to is null;""".format(
            url
        )
        cursor.execute(sql)
        rows = cursor.fetchone()
        cursor.close()

        if rows is None:
            version = 1
        else:
            version = rows["version"]
            cursor2 = connection.cursor()
            update_query = """update laptop set valid_to = '{}' 
                                where scrape_url = '{}'
                                and version = {};""".format(
                valid_from, url, version
            )
            cursor2.execute(update_query)
            connection.commit()
            version += 1
            cursor2.close()
        connection.close()
        return version, valid_from

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
        version, valid_from = check_if_laptop_exists(r["scrape_url"])
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


def insert_into_tablet():
    pass


def insert_into_monitor():
    pass


def insert_into_wifi_dongle():
    pass


def insert_into_printer():
    pass


def insert_into_projector():
    pass



import pandas as pd
from tqdm import tqdm

laptop_test_file = pd.read_json(
    "/Users/darenasc/Documents/datakinduk/datacorps/firesouls/FiresoulsDataCorps/backmarket_laptop_2021-02-05_18-06-35.json"
)
desktop_test_file = pd.read_json(
    "/Users/darenasc/Documents/datakinduk/datacorps/firesouls/FiresoulsDataCorps/valuecomputers_desktop_2021-02-06_14-28-27.json"
)
#print(test_file.head())
insert_into_laptop(laptop_test_file)
#insert_into_desktop(desktop_test_file)