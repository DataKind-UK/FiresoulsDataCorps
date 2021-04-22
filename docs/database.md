# Database

The scraped data is automatically inserted into the Database. There is a table for each one on the resources. Logic has been added to timestamp the addition of new data into the database. When it finds that an item had already been scraped previously (using the item's URL to identify them), it timestamps an `valid_to` for that record and assigns it a version number. This allows to track price changes accross time as well as making sure to only use the most recent data available for each item.

We used the [official MySQL 8.0] [Docker image](https://hub.docker.com/_/mysql) to test the database.

## PyMySQL

To connect to the MySQL database we are using [PyMySQL](https://github.com/PyMySQL/PyMySQL) Python library.

## MySQL
After installing docker or a MySQL server in the server that will host the database.

### For testing locally:

```sh
# To get the official image of MySQL
docker pull mysql:8.0
```

To start the server:
```sh
docker run \
--name firesouls_db \
-d \
-e MYSQL_ROOT_PASSWORD=scraping \
-e MYSQL_DATABASE=firesouls_db \
-e MYSQL_USER=scraper \
-e MYSQL_PASSWORD=firesouls \
-v firesouls_volume:/var/lib/mysql \
-p 3306:3306
mysql:8.0
```

Creating a database dump.

```sh
# For all databases
docker exec firesouls_db sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > src/firesouls/database/all-databases.sql

# For the firesouls_db database
docker exec -i firesouls_db sh -c 'exec mysql -uroot -pscraping' < src/firesouls/sql/firesouls_db.sql
```

Restoring data from a dump.

```sh
# Restore all databases
docker exec -i some-mysql sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < src/firesouls/database/all-databases.sql

# Restore the firesouls_db database
docker exec -i firesouls_db sh -c 'exec mysql -uroot -pscraping -t' < src/firesouls/sql/firesouls_db.sql
```

## Data Dictionary

### Desktop
| Column | Type |
|---|---|
| brand | VARCHAR(255) |
| model | VARCHAR(255)|
| processor | VARCHAR(255)|
| screen_size | FLOAT |
| ram | INT |
| storage_hdd | INT |
| storage_sdd | INT |
| release_year | INT |
| optical_drive | VARCHAR(255) |
| operative_system | VARCHAR(255) |
| price | FLOAT |
| scrape_source | VARCHAR(255) |
| scrape_url | VARCHAR(255) |
| scrape_date | VARCHAR(255) |
| version | INT |
| valid_from | TIMESTAMP |
| valid_to | TIMESTAMP |

<br>

### Laptop
| Column | Type |
|---|---|
| brand | VARCHAR(255) |
| model | VARCHAR(255)|
| processor | VARCHAR(255)|
| ram | INT |
| storage | INT |
| release_year | INT |
| screen_size | FLOAT |
| price | FLOAT |
| scrape_source | VARCHAR(255) |
| scrape_url | VARCHAR(255) |
| scrape_date | VARCHAR(255) |
| version | INT |
| valid_from | TIMESTAMP |
| valid_to | TIMESTAMP |

<br>  

### Printer
| Column | Type |
|---|---|
| brand | VARCHAR(255) |
| model | VARCHAR(255)|
| functions | VARCHAR(255)|
| printing_speed_ppm | INT |
| print_resolution | VARCHAR(255) |
| connectivity | VARCHAR(255) |
| release_year | INT |
| price | FLOAT |
| scrape_source | VARCHAR(255) |
| scrape_url | VARCHAR(255) |
| scrape_date | VARCHAR(255) |
| version | INT |
| valid_from | TIMESTAMP |
| valid_to | TIMESTAMP |

<br>  

### Tablet
| Column | Type |
|---|---|
| brand | VARCHAR(255) |
| model | VARCHAR(255)|
| processor | VARCHAR(255)|
| screen_size | FLOAT |
| screen_resolution | VARCHAR(255)|
| storage | INT |
| release_year | INT |
| price | FLOAT |
| scrape_source | VARCHAR(255) |
| scrape_url | VARCHAR(255) |
| scrape_date | VARCHAR(255) |
| version | INT |
| valid_from | TIMESTAMP |
| valid_to | TIMESTAMP |

<br>  

### Wifi Dongle
| Column | Type |
|---|---|
| provider | VARCHAR(255) |
| service_name | VARCHAR(255)|
| upfront_cost | VARCHAR(255)|
| total_cost | FLOAT |
| data_allowance | VARCHAR(255)|
| contract_months | INT |
| monthly_cost | FLOAT |
| scrape_source | VARCHAR(255) |
| scrape_url | VARCHAR(255) |
| scrape_date | VARCHAR(255) |
| version | INT |
| valid_from | TIMESTAMP |
| valid_to | TIMESTAMP |

<br>  

### Projector

| Column | Type |
|---|---|
| brand | VARCHAR(255) |
| model | VARCHAR(255)|
| screen_size | FLOAT |
| projection_type | VARCHAR(255)|
| resolution | VARCHAR(255) |
| brightness | INT|
| technology | VARCHAR(255) |
| price | FLOAT |
| scrape_source | VARCHAR(255) |
| scrape_url | VARCHAR(255) |
| scrape_date | VARCHAR(255) |
| version | INT |
| valid_from | TIMESTAMP |
| valid_to | TIMESTAMP |

<br>  

### People

| Column | Type |
|---|---|
| region | VARCHAR(255) |
| job_title | VARCHAR(255)|
| soc_code | VARCHAR(255) |
| hourly_pay | FLOAT |
| aggregation | VARCHAR(255) |
| scrape_source | VARCHAR(255) |
| scrape_url | VARCHAR(255) |
| scrape_date | VARCHAR(255) |
| version | INT |
| valid_from | TIMESTAMP |
| valid_to | TIMESTAMP |

<br>  

### Meeting Rooms

| Column | Type |
|---|---|
| name | VARCHAR(255) |
| city | VARCHAR(255)|
| capacity_people | INT |
| cost_hour | FLOAT |
| scrape_source | VARCHAR(255) |
| scrape_url | VARCHAR(255) |
| scrape_date | VARCHAR(255) |
| version | INT |
| valid_from | TIMESTAMP |
| valid_to | TIMESTAMP |
