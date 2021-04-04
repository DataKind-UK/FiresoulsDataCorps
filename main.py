import sys
import typer
import json
from typing import Optional, List
from datetime import datetime
from src.parsers.base import BaseParser
from src.parsers.valuecomputers import (
    ValueComputersLaptopParser,
    ValueComputersDesktopParser,
)
from src.parsers.backmarket import BackmarketLaptopParser, BackmarketTabletParser
from src.parsers.broadbandchoices import BroadbandchoicesDongleParser
from src.parsers.tabletmonkeys import TabletMonkeysTablets
from src.parsers.printerland import PrinterlandParser
from src.parsers.currys import (
    CurrysLaptopParser,
    CurrysProjectorParser,
    CurrysDesktopParser,
)
from src.parsers.ons import ONSPeopleParser
from src.parsers.zipcube import ZipcubeParser
from src.parsers.regus import RegusParser
from src.summariser import Summary
from src.database import insert_into_database

app = typer.Typer()

def run_parser(parser: BaseParser):
    try:
        items = parser.parse()
    except Exception as e:
        print(f"Parser {str(parser)} errored out:\n{e}")
        return []
    return items

@app.command()
def scrape(product: str, sites: Optional[List[str]] = [], city: Optional[str] = None):
    all_items = []
    if product == "laptop":
        LAPTOP_SITES = ["backmarket", "valuecomputers", "currys"]
        if len(sites) > 0:
            LAPTOP_SITES = sites
        if "backmarket" in LAPTOP_SITES:
            items = run_parser(BackmarketLaptopParser())
            all_items.extend(items)
        if "valuecomputers" in LAPTOP_SITES:
            items = run_parser(ValueComputersLaptopParser())
            all_items.extend(items)
        if "currys" in LAPTOP_SITES:
            items = run_parser(CurrysLaptopParser())
            all_items.extend(items)
    
    elif product == "tablet":
        TABLET_SITES = ["backmarket", "tabletmonkeys", "currys"]
        if len(sites) > 0:
            TABLET_SITES = sites
        if "backmarket" in TABLET_SITES:
            items = run_parser(BackmarketTabletParser())
            all_items.extend(items)
        if "tabletmonkeys" in TABLET_SITES:
            items = run_parser(TabletMonkeysTablets())
            all_items.extend(items)

    elif product == "desktop":
        DESKTOP_SITES = ["valuecomputers", "currys"]
        if len(sites) > 0:
            DESKTOP_SITES = sites
        if "valuecomputers" in DESKTOP_SITES:
            items = run_parser(ValueComputersDesktopParser())
            all_items.extend(items)
        if "currys" in DESKTOP_SITES:
            items = run_parser(CurrysDesktopParser())
            all_items.extend(items)
    
    elif product == "printer":
        PRINTER_SITES = ["printerland"]
        if len(sites) > 0:
            PRINTER_SITES = sites
        if "printerland" in PRINTER_SITES:
            items = run_parser(PrinterlandParser())
            all_items.extend(items)

    elif product == "projector":
        PROJECTOR_SITES = ["currys"]
        if len(sites) > 0:
            PROJECTOR_SITES = sites
        if "printerland" in PROJECTOR_SITES:
            items = run_parser(CurrysProjectorParser())
            all_items.extend(items)

    elif product == "wifi_dongle":
        WIFI_SITES = ["broadbandchoices"]
        if len(sites) > 0:
            WIFI_SITES = sites
        if "broadbandchoices" in WIFI_SITES:
            items = run_parser(BroadbandchoicesDongleParser())
            all_items.extend(items)

    elif product == "people":
        PEOPLE_SITES = ["ons"]
        if len(sites) > 0:
            PEOPLE_SITES = sites
        if "ons" in PEOPLE_SITES:
            items = run_parser(ONSPeopleParser())
            all_items.extend(items)

    elif product == "meeting_rooms":
        MEETING_ROOM_SITES = ["zipcube"]
        if len(sites) > 0:
            MEETING_ROOM_SITES = sites
            print(sites)
        if "zipcube" in MEETING_ROOM_SITES:
            if city is None:
                raise Exception("City argument is required for Zipcube scraper")
            print("Scraping Zipcube for "+city)
            items = run_parser(ZipcubeParser(city))
            all_items.extend(items)
    elif site == "regus":
        if product == "meeting_rooms":
            if city is None:
                raise Exception("City argument is required for Regus scraper")
            print("Scraping Regus for "+city)
            r = RegusParser(city)
            items = r.parse()
    
    else:
        raise Exception(f"Product {product} not implemented")

    if len(all_items) == 0:
        raise Exception("No data was scraped. Verify that given sites have been set up for the product")

    json_file = [x.asdict() for x in items]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # TODO Add a function to write these json files
    print("Saving json file into folder")
    with open(f"json/{product}_{timestamp}.json", "w") as f:
        json.dump(json_file, f)
    
    print("Writing new data into database")
    insert_into_database(product, json_file)



@app.command()
def summarise(filepath: str, grouping: List[str] = [], save_csv: bool = False):
    s = Summary().from_json(filepath)
    if save_csv:
        s.to_csv("file.csv")
    print("### OVERALL PRICE SUMMARY STATISTICS ###\n")
    s.summary_statistics()
    if grouping:
        grouping = list(grouping)
        print(f"\n### PRICE SUMMARY STATISTICS WITH GROUPING {grouping}###\n")
        s.summary_statistics(grouping)


if __name__ == "__main__":
    app()
