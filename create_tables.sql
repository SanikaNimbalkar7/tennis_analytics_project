-- Create a new database
CREATE DATABASE tennis_analytics;
USE tennis_analytics;


-- Categories Table
CREATE TABLE Categories (
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    category_name NVARCHAR(100) NOT NULL
);
GO

-- Competitions Table
CREATE TABLE Competitions (
    competition_id INT IDENTITY(1,1) PRIMARY KEY,
    competition_name NVARCHAR(255),
    category_id INT,
    type NVARCHAR(50),
    gender NVARCHAR(20),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);
GO

-- Complexes Table
CREATE TABLE Complexes (
    complex_id INT IDENTITY(1,1) PRIMARY KEY,
    complex_name NVARCHAR(255)
);
GO

-- Venues Table
CREATE TABLE Venues (
    venue_id INT IDENTITY(1,1) PRIMARY KEY,
    venue_name NVARCHAR(255),
    city_name NVARCHAR(100),
    country_name NVARCHAR(100),
    timezone NVARCHAR(100),
    complex_id INT,
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
);
GO

-- Competitors Table
CREATE TABLE Competitors (
    competitor_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255),
    country NVARCHAR(100),
    country_code NVARCHAR(10)
);
GO

-- Competitor_Rankings Table
CREATE TABLE Competitor_Rankings (
    rank_id INT IDENTITY(1,1) PRIMARY KEY,
    competitor_id INT,
    rank INT,
    movement INT,
    points INT,
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
);
GO