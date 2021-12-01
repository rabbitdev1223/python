CREATE DATABASE Tarragon;
use Tarragon;

CREATE TABLE IF NOT EXISTS Users(
    id INT(6) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    UNIQUE (email)
);
CREATE TABLE IF NOT EXISTS Datas(
    id INT(6) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    date VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL
);
