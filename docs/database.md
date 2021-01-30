# Database

We used the [official MySQL 8.0] [Docker image](https://hub.docker.com/_/mysql) to test the database.

## MySQL
After installing docker or a MySQL server in the server that will host the database.

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
-v /Users/darenasc/Documents/datakinduk/datacorps/firesouls/database:/var/lib/mysql \
mysql:8.0
```

Creating a database dump.

```sh
# For all databases
docker exec firesouls_db sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > /Users/darenasc/Documents/datakinduk/datacorps/firesouls/database/all-databases.sql

# For the firesouls_db database
docker exec -i firesouls_db sh -c 'exec mysql -uroot -pscraping' < /Users/darenasc/Documents/datakinduk/datacorps/firesouls/database/firesouls_db.sql
```

Restoring data from a dump.

```sh
# Restore all databases
docker exec -i some-mysql sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < /Users/darenasc/Documents/datakinduk/datacorps/firesouls/database/all-databases.sql

# Restore the firesouls_db database
docker exec -i firesouls_db sh -c 'exec mysql -uroot -pscraping -t' < /Users/darenasc/Documents/datakinduk/datacorps/firesouls/database/firesouls_db.sql
```