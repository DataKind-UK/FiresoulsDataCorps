# FiresoulsDataCorps
mini DataCorps for Firesouls (Social Value Exchange)

## Documentation
- [Environment Setup](docs/environment.md)
- [Running Tests](docs/tests.md)
- [Ethics checklist](ETHICS.md)
- [Data Source Information](docs/datasources.md)

## Usage  

So far there is basic version of the script, which contains the Backmarket
laptop scraper implementation. This can be run through the `main.py` script using the following:

```
python main.py <site_name>
```

A quick test of this code is through the following command:  

```
python main.py backmarket
```

This script will output a file called `file.json` which contains the data for
the scraped items.

