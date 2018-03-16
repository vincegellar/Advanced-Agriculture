DROP DATABASE IF EXISTS AdvancedAgriculture;
CREATE DATABASE AdvancedAgriculture;
USE AdvancedAgriculture;

CREATE TABLE Plants (
	Id INT NOT NULL AUTO_INCREMENT,
	MACAddress CHAR(12) NOT NULL,
	Name VARCHAR(255) NOT NULL,
	SoilMoistureLowTreshold INT NOT NULL,
	SoilMoistureHighTreshold INT NOT NULL,
	TemperatureLowTreshold FLOAT(4,1) NOT NULL,
	TemperatureHighTreshold FLOAT(4,1) NOT NULL,
	HumidityLowTreshold INT NOT NULL,
	HumidityHighTreshold INT NOT NULL,
	LightLowTreshold INT NOT NULL,
	LightHighTreshold INT NOT NULL,
	PRIMARY KEY (Id),
	UNIQUE INDEX (MACAddress)
);

CREATE TABLE Measurements (
	MeasureTime DATETIME NOT NULL,
	PlantId INT NOT NULL,
	SoilMoisture INT NOT NULL,
	Temperature FLOAT(4,1) NOT NULL,
	Humidity INT NOT NULL,
	Light INT NOT NULL,
	WaterLevel INT NOT NULL,
	PRIMARY KEY (MeasureTime, PlantId),
	CONSTRAINT PlantId1
	FOREIGN KEY (PlantId)
	REFERENCES AdvancedAgriculture.Plants (Id)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE Settings (
	PlantId INT NOT NULL,
	Email VARCHAR(255) NOT NULL,
	DarkHoursStart TIME DEFAULT NULL,
	DarkHoursEnd TIME DEFAULT NULL,
	SilentHoursStart TIME DEFAULT NULL,
	SilentHoursEnd TIME DEFAULT NULL,
	PotSize INT DEFAULT 30,
	PRIMARY KEY (PlantId),
	CONSTRAINT PlantId2
	FOREIGN KEY (PlantId)
	REFERENCES AdvancedAgriculture.Plants (Id)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);