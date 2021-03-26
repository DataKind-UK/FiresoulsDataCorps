CREATE DATABASE /*!32312 IF NOT EXISTS*/ firesouls_db /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE firesouls_db;

DROP TABLE IF EXISTS desktop;
CREATE TABLE `desktop` (
  `brand` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `processor` varchar(255) DEFAULT NULL,
  `screen_size` float DEFAULT NULL,
  `ram` int DEFAULT NULL,
  `storage_hdd` int DEFAULT NULL,
  `storage_ssd` int DEFAULT NULL,
  `release_year` int DEFAULT NULL,
  `optical_drive` varchar(255) DEFAULT NULL,
  `operative_system` varchar(255) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `scrape_source` varchar(255) DEFAULT NULL,
  `scrape_url` varchar(255) DEFAULT NULL,
  `scrape_date` timestamp NULL DEFAULT NULL,
  `version` int  NULL DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `valid_to` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS laptop;
CREATE TABLE `laptop` (
  `brand` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `processor` varchar(255) DEFAULT NULL,
  `ram` tinyint DEFAULT NULL,
  `storage` smallint DEFAULT NULL,
  `release_year` smallint DEFAULT NULL,
  `screen_size` float DEFAULT NULL,
  `price` float DEFAULT NULL,
  `scrape_source` varchar(255) DEFAULT NULL,
  `scrape_url` varchar(255) DEFAULT NULL,
  `scrape_date` date DEFAULT NULL,
  `version` int DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `valid_to` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS monitor;
CREATE TABLE `monitor` (
  `brand` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `screen_size` float DEFAULT NULL,
  `price` float DEFAULT NULL,
  `scrape_source` varchar(255) DEFAULT NULL,
  `scrape_url` varchar(255) DEFAULT NULL,
  `scrape_date` timestamp NULL DEFAULT NULL,
  `version` int  NULL DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `valid_to` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS printer;
CREATE TABLE `printer` (
  `brand` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `functions` varchar(255) DEFAULT NULL,
  `printing_speed_ppm` int DEFAULT NULL,
  `print_resolution` varchar(255) DEFAULT NULL,
  `connectivity` varchar(255) DEFAULT NULL,
  `release_year` int DEFAULT NULL,
  `price` float DEFAULT NULL,
  `scrape_source` varchar(255) DEFAULT NULL,
  `scrape_url` varchar(255) DEFAULT NULL,
  `scrape_date` timestamp NULL DEFAULT NULL,
  `version` int  NULL DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `valid_to` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS tablet;
CREATE TABLE `tablet` (
  `brand` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `processor` varchar(255) DEFAULT NULL,
  `screen_size` float DEFAULT NULL,
  `screen_resolution` varchar(255) DEFAULT NULL,
  `storage` int DEFAULT NULL,
  `release_year` int DEFAULT NULL,
  `price` float DEFAULT NULL,
  `currency` varchar(255) DEFAULT NULL,
  `scrape_source` varchar(255) DEFAULT NULL,
  `scrape_url` varchar(255) DEFAULT NULL,
  `scrape_date` timestamp NULL DEFAULT NULL,
  `version` int  NULL DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `valid_to` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS wifi_dongle;
CREATE TABLE `wifi_dongle` (
  `provider` varchar(255) DEFAULT NULL,
  `service_name` varchar(255) DEFAULT NULL,
  `upfront_cost` varchar(255) DEFAULT NULL,
  `total_cost` float DEFAULT NULL,
  `data_allowance` varchar(255) DEFAULT NULL,
  `contract_months` int DEFAULT NULL,
  `monthly_cost` float DEFAULT NULL,
  `scrape_source` varchar(255) DEFAULT NULL,
  `scrape_url` varchar(255) DEFAULT NULL,
  `scrape_date` timestamp NULL DEFAULT NULL,
  `version` int  NULL DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `valid_to` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS projector;
CREATE TABLE `projector` (
  `brand` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `screen_size` float DEFAULT NULL,
  `projection_type` varchar(255) DEFAULT NULL,
  `resolution` varchar(255) DEFAULT NULL,
  `brightness` int DEFAULT NULL,
  `technology` varchar(255) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `scrape_source` varchar(255) DEFAULT NULL,
  `scrape_url` varchar(255) DEFAULT NULL,
  `scrape_date` timestamp NULL DEFAULT NULL,
  `version` int  NULL DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `valid_to` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS people;
CREATE TABLE `people` (
  `region` varchar(255) DEFAULT NULL,
  `job_title` varchar(255) DEFAULT NULL,
  `soc_code` varchar(255) DEFAULT NULL,
  `hourly_pay` float DEFAULT NULL,
  `aggregation` varchar(255) DEFAULT NULL,
  `scrape_source` varchar(255) DEFAULT NULL,
  `scrape_url` varchar(255) DEFAULT NULL,
  `scrape_date` timestamp NULL DEFAULT NULL,
  `version` int  NULL DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `valid_to` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS meeting_rooms;
CREATE TABLE `meeting_rooms` (
  `name` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `capacity_people` int DEFAULT NULL,
  `cost_hour` float DEFAULT NULL,
  `scrape_source` varchar(255) DEFAULT NULL,
  `scrape_url` varchar(255) DEFAULT NULL,
  `scrape_date` timestamp NULL DEFAULT NULL,
  `version` int  NULL DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `valid_to` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

