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

This command kickstarts the scraping process for a given site.

```
python main.py scrape <site_name>
```

A quick test of this code is through the following command:  

```
python main.py scrape backmarket
```

This script will output a file called `file.json` which contains the data for
the scraped items.

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


