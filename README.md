# FiresoulsDataCorps
mini DataCorps for Firesouls (Social Value Exchange)

## Documentation
- [Environment Setup](docs/environment.md)
- [Running Tests](docs/tests.md)
- [Ethics checklist](ETHICS.md)
- [Data Source Information](docs/datasources.md)

## Usage  

So far there is minimal version of the script, which only contains the dowloader
function. This can be run through the `main.py` script using the following:

```
python main.py <URL>
```

A quick test of this code is through the following command:  

```
python main.py https://api.myip.com
```

Which should output a JSON with the IP address and country. If using the Proxy service, this will not be your IP address.

