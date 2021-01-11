import typer
import json
from typing import Optional, List
from src.parsers.backmarket import BackmarketLaptopParser
<<<<<<< HEAD
from src.parsers.valuecomputers import ValueComputersLaptopParser
=======
from src.summariser import Summary

>>>>>>> dev

app = typer.Typer()


@app.command()
def scrape(site: str):
    if site == "backmarket":
        blp = BackmarketLaptopParser()
        laptops = blp.parse()
        json_file = [x.asdict() for x in laptops]
        # TODO Add a function to write these json files
        with open("file.json", "w") as f:
            json.dump(json_file, f)
    elif site == 'valucomputers':
        vclp = ValueComputersLaptopParser()
        laptops = vclp.parse()
        json_file = [x.asdict() for x in laptops]
        with open("valucomputers.json", "w") as f:
            json.dump(json_file, f)
    else:
        print(f"Site {site} not implemented")


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
