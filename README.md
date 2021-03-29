# FiresoulsDataCorps
mini DataCorps for Firesouls (Social Value Exchange)

## Documentation
- [Environment Setup](docs/environment.md)
- [Running Tests](docs/tests.md)
- [Ethics checklist](ETHICS.md)
- [Data Source Information](docs/datasources.md)

## Usage  

The `main.py` script is the primary interface to the tool. There are two commands
available:

- scrape
- summarise


### Scrape  

This command kickstarts the scraping process for a given resource type.

```
python main.py scrape <resource_type> --sites <site_name> --city <city_name>
```

The sites argument is optional, and is there to allow the scrape of only specific sites instead of all the ones that have been configured. 

The city argument is also optional and is used exclusively by the meeting_rooms scrapers.

A quick test of this code is through the following command:  

```
python main.py scrape laptop
```

This script will output a file called `{resource}_{timestamp}.json` which contains the data for the scraped items. The data is also automatically inserted into the database. The database credentials will have to have been configured through the `.env` file.

#### Commands

Currently the following commands are usable to download data about resources.

```
python main.py scrape laptop
python main.py scrape tablet
python main.py scrape desktop
python main.py scrape wifi_dongle
python main.py scrape printer
python main.py scrape projector
python main.py scrape people
python main.py scrape meeting_rooms
```

### Summarise  

This command allows for the automatic generation of summary statistics for the price.
At the moment it reads a JSON file saved locally (the output from the previous step)
and given a set of optional grouping variables, generates a statistical summary of the price.

It also allows to save the data to a CSV file for easier exploration in Excel. This is set
by adding the `--save-csv` flag to the command. If not added, it will not save the csv file.

```
python main.py summarise <json_file_name> --grouping <column_name_to_group_by> --save-csv
```

An example of this execution is the following:

```
python main.py summarise file.json --grouping release_year --grouping brand --save-csv
```

Which will print the summary statistics to the command line, as well as create a new file
called `file.csv` which contains the scraped data.


