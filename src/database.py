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
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
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
            scrape_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            for i, r in tqdm(df.iterrows(), total=len(df), desc="laptops"):
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
                    ),
                )
        connection.commit()


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
