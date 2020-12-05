import typer
import json
from src.parsers.backmarket import BackmarketLaptopParser


def main(site: str):
    if site == 'backmarket':
        blp = BackmarketLaptopParser()
        laptops = blp.parse()
        json_file = [x.asdict() for x in laptops]
        # TODO Add a function to write these json files
        with open("file.json", "w") as f:
            json.dump(json_file, f)
    else:
        print(f"Site {site} not implemented")


if __name__ == "__main__":
    typer.run(main)
