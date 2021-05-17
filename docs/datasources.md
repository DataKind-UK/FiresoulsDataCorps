# Data Sources Evaluated

Following is a list of the different data sources evaluated for the scrape as well as the features that are easy to obtain from the site.  

## **Equipment**

## Sources

The sources are described in the below:

| Source | Description | Requests per scrape |
|---|---|--|
| [BackMarket](https://www.backmarket.co.uk) | Supplier of refurbished technological products. Very detailed information and easy to access. | One per result item. |
| [Printerland](https://www.printerland.co.uk) | Printing equipment supplier.| One per results page. |
| [Broadbandchoices](https://www.broadbandchoices.co.uk/mobile-broadband/dongles) | Price comparison site for broadband services. They have a specific section for mobile broadband dongles. | One per results page. |
| [Currys](currys.co.uk) | Retailer of new technological products. Very detailed information.| One per result item. |
| [ValuComputers](https://www.valucomputers.co.uk/) | Computer retailer. Detailed information. | One per result item. |
| [TabletMonkeys](https://tabletmonkeys.com/) | Tablet price comparison site. Detailed information. | One per results page. |
| [ONS](https://www.ons.gov.uk/) | Office for National Statistics. Very detailed and reliable information. | Single |

_Note: All of the sources, except for the ONS data need to be aggregated in the database. The ONS data has been preaggregated by the ONS to mean and median calculations. In this project, we use the mean value because it's available for more regions and job roles that the median._

<br>


### 1. Laptop

| Source | Brand | Model | Processor | Memory (RAM) | HDD | Release Year | Screen Size | OS |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BackMarket | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Curry's | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | | :white_check_mark: | :white_check_mark: |
| ValuComputers | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | | :white_check_mark: | :white_check_mark: |

<br>

### 2. Mobile Broadband Dongles

| Source | Network Speed | Price per month | Data Allowance |
|---|:---:|:---:|:---:|
| Broadbandchoices* | :white_check_mark: | :white_check_mark: | :white_check_mark: |

<br>

### 3. Desktop
Desktop computers are often sold without a screen, keyboard and mouse. We might need to scrape these elements separately and obtain an average price for them. Then we can add the average component prices to get an estimate for a desktop.

<br>

#### 3.1 **Desktop Computer**

| Source     | Brand | Model | Processor | Memory (RAM) | HDD | Release Year | OS |
|------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BackMarket | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Curry's    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | | :white_check_mark: |
| Source 3 | | | | | | :white_check_mark: | :white_check_mark: |
| Source 4 | | | | | | :white_check_mark: | :white_check_mark: |
| Source 5 | | | | | | | |

#### 3.2 **PC Monitor**  

| Source | Brand | Model | Screen Size |
|------------|:---:|:---:|:---:|
| BackMarket | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Curry's | :white_check_mark: | :white_check_mark: | :white_check_mark: |

<br>

### 5. Projector

| Source | Brand | Model | Resolution |
|----------|:---:|:---:|:---:|
| Curry's | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Source 2 | :white_check_mark: | :white_check_mark: | :white_check_mark: |

Not sure what these are:
- "Min single-chip DLP
- Min 2100 AL

<br>

### 6. Laser Printer

| Source | Brand | Model | DPI Print Resolution |
|-------------|:---:|:---:|:---:|
| Printerland | :white_check_mark: | :white_check_mark: | :white_check_mark: |

<br>

### 7. Tablet

| Source | Brand | Model | Resolution | Processor | Screen Size | Battery Life | Release Year | Storage |
|------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BackMarket | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Tabletmonkeys | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |

<br>

## **People and Employment and Skills**


| Source | Description |
|---|---|
| [ONS](https://www.ons.gov.uk/) | Office for National Statistics. Very detailed and representative information.|

The following table shows the [SOC code](https://onsdigital.github.io/dp-classification-tools/standard-occupational-classification/ONS_SOC_hierarchy_view.html) mappings for each of the resource type:

| Category | Codes |
|---|---|
| People - Management Time | 1150, 113 |
| People - Executive Time | 111 |
| Employment - Local Recruitment | |
| Employment - Local Apprenticeship | |
| Employment - Employment Scheme | |
| Employment - Graduate Placement | |
| Employment - Supporting local job fairs | |
| Employment - Work experience placement for working age | |
| Employment - Work experience placement for learning difficulties| |

_Note: we use the mean value published by ONS rather than the median because it's available for more regions and job roles._
<br>

## **Space**


| Source | Description |
|---|---|
| [Regus](https://www.regus.com/en-gb) | Serviced office and meeting room space provicer accross the country. |
| [Zipcube](https://zipcube.com/uk) | Serviced office and meeting room space listings page. |
