import typer
import json
from src.parsers.backmarket import BackmarketLaptopParser
from src.parsers.valuecomputers import ValueComputersLaptopParser

def main(site: str):
    if site == 'backmarket':
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


if __name__ == "__main__":
    typer.run(main)
