import typer
import json
from typing import Optional, List
from datetime import datetime
from src.parsers.valuecomputers import (
    ValueComputersLaptopParser,
    ValueComputersDesktopParser,
)
from src.parsers.backmarket import BackmarketLaptopParser, BackmarketTabletParser
from src.parsers.broadbandchoices import BroadbandchoicesDongleParser
from src.parsers.tabletmonkeys import TabletMonkeysTablets
from src.parsers.printerland import PrinterlandParser
from src.parsers.currys import CurrysLaptopParser, CurrysProjectorParser, CurrysDesktopParser
from src.summariser import Summary

app = typer.Typer()


@app.command()
def scrape(site: str, product: str):
    if site == "backmarket":
        if product == "laptop":
            blp = BackmarketLaptopParser()
            items = blp.parse()
        elif product == "tablet":
            btp = BackmarketTabletParser()
            items = btp.parse()
    elif site == "valuecomputers":
        if product == "laptop":
            vclp = ValueComputersLaptopParser()
            items = vclp.parse()
        elif product == "desktop":
            vcdt = ValueComputersDesktopParser()
            items = vcdt.parse()
            pass
    elif site == "broadbandchoices":
        if product == "dongle":
            bbc = BroadbandchoicesDongleParser()
            items = bbc.parse()
    elif site == "tabletmonkeys":
        if product == "tablet":
            tmt = TabletMonkeysTablets()
            items = tmt.parse()
    elif site == "printerland":
        if product == "printer":
            ppc = PrinterlandParser()
            items = ppc.parse()
    elif site == "currys":
        if product == "laptop":
            clp = CurrysLaptopParser()
            items = clp.parse()
        if product == "projector":
            cpp = CurrysProjectorParser()
            items = cpp.parse()
        if product == "Desktop":
            cdp = CurrysDesktopParser()
            items = cdp.parse()
    else:
        print(f"Product {product} not implemented for {site}")
        raise Exception

    json_file = [x.asdict() for x in items]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # TODO Add a function to write these json files
    with open(f"{site}_{product}_{timestamp}.json", "w") as f:
        json.dump(json_file, f)


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
