import pymysql.cursors
import pandas as pd
import math


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
    connection = get_db_connection()
    df1 = df.where(pd.notnull(df), None)
    with connection:
        with connection.cursor() as cursor:
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
            scrape_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            for i, r in tqdm(df1.iterrows(), total = len(df), desc = "desktops"):
                #print(r)
                #for c in df.columns:
                #    if isinstance(r[c], float):
                #        if math.isnan(r[c]):
                #            r[c] = None
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
                        r["scrape_date"]
                    )
                )
        connection.commit()


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
            for i, r in tqdm(df.iterrows(), total = len(df), desc = "laptops"):
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


import pandas as pd
from tqdm import tqdm

laptop_test_file = pd.read_json(
    "/Users/darenasc/Documents/datakinduk/datacorps/firesouls/FiresoulsDataCorps/backmarket_laptop_2021-02-05_18-06-35.json"
)
desktop_test_file = pd.read_json(
    "/Users/darenasc/Documents/datakinduk/datacorps/firesouls/FiresoulsDataCorps/valuecomputers_desktop_2021-02-06_14-28-27.json"
)
#print(test_file.head())
#insert_into_laptop(laptop_test_file)
insert_into_desktop(desktop_test_file)
