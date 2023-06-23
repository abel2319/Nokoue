-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS nokoue_dev_db;
CREATE USER IF NOT EXISTS 'nokoue_dev'@'localhost' IDENTIFIED BY 'nokoue_dev_pwd';
GRANT ALL PRIVILEGES ON `nokoue_dev_db`.* TO 'nokoue_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'nokoue_dev'@'localhost';
FLUSH PRIVILEGES;