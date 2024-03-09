CREATE TABLE Cities (
    CityID INT AUTO_INCREMENT PRIMARY KEY,
    City/RegionName VARCHAR(100) UNIQUE
);

CREATE TABLE Districts (
    DistrictID INT AUTO_INCREMENT PRIMARY KEY,
    DistrictName VARCHAR(100),
    CityID INT,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID),
    UNIQUE (DistrictName, CityID)
);

CREATE TABLE Streets (
    StreetID INT AUTO_INCREMENT PRIMARY KEY,
    StreetName VARCHAR(100),
    DistrictID INT,
    FOREIGN KEY (DistrictID) REFERENCES Districts(DistrictID)
);

CREATE TABLE Locations (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    CityID INT,
    DistrictID INT,
    StreetID INT,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID),
    FOREIGN KEY (DistrictID) REFERENCES Districts(DistrictID),
    FOREIGN KEY (StreetID) REFERENCES Streets(StreetID)
);

CREATE TABLE Listings (
    ListingID INT AUTO_INCREMENT PRIMARY KEY,
    Price DECIMAL(10,2),
    LocationID INT,
    Area DECIMAL(8,2),
    Rooms INT,
    Floor INT,
    TotalFloors INT,
    Year INT,
    Heating VARCHAR(50),
    `Condition` VARCHAR(50),  
    Status ENUM('For Sale', 'Rent', 'Unknown'),  
    PostedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
);
