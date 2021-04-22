# Environment Setup

1. Download and install [Python 3.8](https://www.python.org/downloads/) or newer.
2. Clone this repository and change directory to the repository folder: 

```
git clone git@github.com:DataKind-UK/FiresoulsDataCorps.git
cd FiresoulsDataCorps
```

3. If the proxy service will be used, duplicate the `sample.env` file and update
it with the correct key value. It can be obtained from [ScraperAPI](https://www.scraperapi.com/).
Rename this file to `.env`

4. Add credentials to connect to the database. The required credentials are the same as those shown on the
`sample.env` file.

5. Install [`pipenv`](https://pipenv.pypa.io/en/latest/install/#installing-pipenv)

6. Install the packages using `pipenv`. From the terminal type:

```
pipenv shell
pipenv install Pipfile
```

If development packages are required, also run:

```
pipenv install --dev
```

This should install all the necessary python packages to work with this project.

6. The environment is installed and ready to use, develop and test.

-------

## To recreate the environment from scratch

The following commands were used to create the environment in the first place.
> **_NOTE:_** Do not try this if the step 6 was successful.

```
pipenv shell
pipenv install requests beautifulsoup4 scrapy pyodbc pandas selenium typer
pipenv install black pytest pytest-cov deon mypy autoflake --dev --pre
```

## Ethics checklist

An ethics checklist was generated for this project using `deon`. Ideally we can use DataKindUK's ethics checklist and [include](https://deon.drivendata.org/#command-line-options) it in the project. In the meantime we can use DataDriven's ethics checklist.

```
deon -o ETHICS.md
```

## Python packages

The following python packages are installed and ready to use from the environment:

- [pipenv](https://pipenv.pypa.io/) : to set up the dev environment.
- [requests](https://requests.readthedocs.io/en/master/) : to get the websites html code.
- [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/) : to parse the content of the webpages.
- [scrapy](https://scrapy.org) (just in case we need it)
- [selenium](https://selenium-python.readthedocs.io) (just in case we need it)
- [pyodbc](https://github.com/mkleehammer/pyodbc) : to connect to databases.
- [pandas](https://pandas.pydata.org) : for data analysis and pd.read_html() function.
- [typer](https://github.com/tiangolo/typer) : to create the Command Line Interface and running the scrapers.

### For development:
- [pytest](https://docs.pytest.org/en/latest/) : for testing the code.
- [pytest-cov](https://pypi.org/project/pytest-cov/) : for getting code coverage metrics.
- [black](https://github.com/psf/black) : For code formatting.
- [mypy](https://github.com/python/mypy) : For typing verification.
- [autoflake](https://github.com/myint/autoflake) : To remove unused imports.
- [deon](https://deon.drivendata.org) : For ethics checklist of the project.