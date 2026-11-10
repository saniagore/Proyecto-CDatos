-- ====================================================================
-- DDL para el esquema dimensional de Ventas en PostgreSQL
-- Datamarts: Internet Sales y Reseller Sales (AdventureWorksDW)
-- ====================================================================

-- 1. DimDate
CREATE TABLE IF NOT EXISTS DimDate (
    DateKey INT PRIMARY KEY,
    FullDateAlternateKey DATE NOT NULL,
    DayNumberOfWeek SMALLINT,
    EnglishDayNameOfWeek VARCHAR(10),
    DayNumberOfMonth SMALLINT,
    DayNumberOfYear SMALLINT,
    WeekNumberOfYear SMALLINT,
    EnglishMonthName VARCHAR(10),
    MonthNumberOfYear SMALLINT,
    CalendarQuarter SMALLINT,
    CalendarYear SMALLINT,
    CalendarSemester SMALLINT
);

-- 2. DimSalesTerritory
CREATE TABLE IF NOT EXISTS DimSalesTerritory (
    SalesTerritoryKey INT PRIMARY KEY,
    SalesTerritoryAlternateKey INT,
    SalesTerritoryRegion VARCHAR(50),
    SalesTerritoryCountry VARCHAR(50),
    SalesTerritoryGroup VARCHAR(50)
);

-- 3. DimGeography
CREATE TABLE IF NOT EXISTS DimGeography (
    GeographyKey INT PRIMARY KEY,
    City VARCHAR(30),
    StateProvinceCode VARCHAR(3),
    StateProvinceName VARCHAR(50),
    CountryRegionCode VARCHAR(3),
    EnglishCountryRegionName VARCHAR(50),
    PostalCode VARCHAR(15),
    SalesTerritoryKey INT REFERENCES DimSalesTerritory(SalesTerritoryKey)
);

-- 4. DimCustomer
CREATE TABLE IF NOT EXISTS DimCustomer (
    CustomerKey INT PRIMARY KEY,
    GeographyKey INT REFERENCES DimGeography(GeographyKey),
    CustomerAlternateKey VARCHAR(15),
    Title VARCHAR(8),
    FirstName VARCHAR(50),
    MiddleName VARCHAR(50),
    LastName VARCHAR(50),
    NameStyle BOOLEAN,
    BirthDate DATE,
    MaritalStatus CHAR(1),
    Suffix VARCHAR(10),
    Gender VARCHAR(1),
    EmailAddress VARCHAR(50),
    YearlyIncome NUMERIC(15,2),
    TotalChildren SMALLINT,
    NumberChildrenAtHome SMALLINT,
    EnglishEducation VARCHAR(40),
    EnglishOccupation VARCHAR(100),
    HouseOwnerFlag CHAR(1),
    NumberCarsOwned SMALLINT,
    AddressLine1 VARCHAR(120),
    AddressLine2 VARCHAR(120),
    Phone VARCHAR(20),
    DateFirstPurchase DATE,
    CommuteDistance VARCHAR(15)
);

-- 5. DimProductCategory
CREATE TABLE IF NOT EXISTS DimProductCategory (
    ProductCategoryKey INT PRIMARY KEY,
    ProductCategoryAlternateKey INT,
    EnglishProductCategoryName VARCHAR(50)
);

-- 6. DimProductSubcategory
CREATE TABLE IF NOT EXISTS DimProductSubcategory (
    ProductSubcategoryKey INT PRIMARY KEY,
    ProductSubcategoryAlternateKey INT,
    EnglishProductSubcategoryName VARCHAR(50),
    ProductCategoryKey INT REFERENCES DimProductCategory(ProductCategoryKey)
);

-- 7. DimProduct
CREATE TABLE IF NOT EXISTS DimProduct (
    ProductKey INT PRIMARY KEY,
    ProductAlternateKey VARCHAR(25),
    ProductSubcategoryKey INT REFERENCES DimProductSubcategory(ProductSubcategoryKey),
    EnglishProductName VARCHAR(50),
    StandardCost NUMERIC(15,4),
    Color VARCHAR(15),
    SafetyStockLevel SMALLINT,
    ReorderPoint SMALLINT,
    ListPrice NUMERIC(15,4),
    Size VARCHAR(50),
    SizeRange VARCHAR(50),
    Weight NUMERIC(8,2),
    DaysToManufacture INT,
    ProductLine CHAR(2),
    DealerPrice NUMERIC(15,4),
    Class CHAR(2),
    Style CHAR(2),
    ModelName VARCHAR(50),
    StartDate TIMESTAMP,
    EndDate TIMESTAMP,
    Status VARCHAR(7)
);

-- 8. DimReseller
CREATE TABLE IF NOT EXISTS DimReseller (
    ResellerKey INT PRIMARY KEY,
    GeographyKey INT REFERENCES DimGeography(GeographyKey),
    ResellerAlternateKey VARCHAR(15),
    Phone VARCHAR(25),
    BusinessType VARCHAR(20),
    ResellerName VARCHAR(50),
    NumberEmployees INT,
    OrderFrequency CHAR(1),
    OrderMonth SMALLINT,
    FirstOrderYear INT,
    LastOrderYear INT,
    ProductLine VARCHAR(50),
    AddressLine1 VARCHAR(60),
    AddressLine2 VARCHAR(60),
    AnnualSales NUMERIC(15,2),
    BankName VARCHAR(50),
    MinPaymentType SMALLINT,
    MinPaymentAmount NUMERIC(15,2),
    AnnualRevenue NUMERIC(15,2),
    YearOpened INT
);

-- 9. DimEmployee
CREATE TABLE IF NOT EXISTS DimEmployee (
    EmployeeKey INT PRIMARY KEY,
    ParentEmployeeKey INT REFERENCES DimEmployee(EmployeeKey),
    EmployeeNationalIDAlternateKey VARCHAR(15),
    SalesTerritoryKey INT REFERENCES DimSalesTerritory(SalesTerritoryKey),
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    MiddleName VARCHAR(50),
    NameStyle BOOLEAN,
    Title VARCHAR(50),
    HireDate DATE,
    BirthDate DATE,
    LoginID VARCHAR(256),
    EmailAddress VARCHAR(50),
    Phone VARCHAR(25),
    MaritalStatus CHAR(1),
    EmergencyContactName VARCHAR(50),
    EmergencyContactPhone VARCHAR(25),
    SalariedFlag BOOLEAN,
    Gender CHAR(1),
    PayFrequency SMALLINT,
    BaseRate NUMERIC(15,4),
    VacationHours SMALLINT,
    SickLeaveHours SMALLINT,
    CurrentFlag BOOLEAN,
    SalesPersonFlag BOOLEAN,
    DepartmentName VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    Status VARCHAR(50)
);

-- 10. DimPromotion
CREATE TABLE IF NOT EXISTS DimPromotion (
    PromotionKey INT PRIMARY KEY,
    PromotionAlternateKey INT,
    EnglishPromotionName VARCHAR(255),
    DiscountPct NUMERIC(5,4),
    EnglishPromotionType VARCHAR(50),
    EnglishPromotionCategory VARCHAR(50),
    StartDate TIMESTAMP,
    EndDate TIMESTAMP,
    MinQty INT,
    MaxQty INT
);

-- 11. DimCurrency
CREATE TABLE IF NOT EXISTS DimCurrency (
    CurrencyKey INT PRIMARY KEY,
    CurrencyAlternateKey CHAR(3),
    CurrencyName VARCHAR(50)
);

-- 12. DimSalesReason
CREATE TABLE IF NOT EXISTS DimSalesReason (
    SalesReasonKey INT PRIMARY KEY,
    SalesReasonAlternateKey INT,
    SalesReasonName VARCHAR(50),
    SalesReasonReasonType VARCHAR(50)
);

-- 13. FactInternetSales (Datamart Ventas por Internet)
CREATE TABLE IF NOT EXISTS FactInternetSales (
    ProductKey INT NOT NULL REFERENCES DimProduct(ProductKey),
    OrderDateKey INT NOT NULL REFERENCES DimDate(DateKey),
    DueDateKey INT NOT NULL REFERENCES DimDate(DateKey),
    ShipDateKey INT NOT NULL REFERENCES DimDate(DateKey),
    CustomerKey INT NOT NULL REFERENCES DimCustomer(CustomerKey),
    PromotionKey INT NOT NULL REFERENCES DimPromotion(PromotionKey),
    CurrencyKey INT NOT NULL REFERENCES DimCurrency(CurrencyKey),
    SalesTerritoryKey INT NOT NULL REFERENCES DimSalesTerritory(SalesTerritoryKey),
    SalesOrderNumber VARCHAR(20) NOT NULL,
    SalesOrderLineNumber SMALLINT NOT NULL,
    RevisionNumber SMALLINT,
    OrderQuantity SMALLINT,
    UnitPrice NUMERIC(15,4),
    ExtendedAmount NUMERIC(15,4),
    UnitPriceDiscountPct NUMERIC(5,4),
    DiscountAmount FLOAT,
    ProductStandardCost NUMERIC(15,4),
    TotalProductCost NUMERIC(15,4),
    SalesAmount NUMERIC(15,4),
    TaxAmt NUMERIC(15,4),
    Freight NUMERIC(15,4),
    CarrierTrackingNumber VARCHAR(25),
    CustomerPONumber VARCHAR(25),
    OrderDate TIMESTAMP,
    DueDate TIMESTAMP,
    ShipDate TIMESTAMP,
    PRIMARY KEY (SalesOrderNumber, SalesOrderLineNumber)
);

-- 14. FactInternetSalesReason (Tabla puente)
CREATE TABLE IF NOT EXISTS FactInternetSalesReason (
    SalesOrderNumber VARCHAR(20) NOT NULL,
    SalesOrderLineNumber SMALLINT NOT NULL,
    SalesReasonKey INT NOT NULL REFERENCES DimSalesReason(SalesReasonKey),
    PRIMARY KEY (SalesOrderNumber, SalesOrderLineNumber, SalesReasonKey)
);

-- 15. FactResellerSales (Datamart Ventas por Revendedores)
CREATE TABLE IF NOT EXISTS FactResellerSales (
    ProductKey INT NOT NULL REFERENCES DimProduct(ProductKey),
    OrderDateKey INT NOT NULL REFERENCES DimDate(DateKey),
    DueDateKey INT NOT NULL REFERENCES DimDate(DateKey),
    ShipDateKey INT NOT NULL REFERENCES DimDate(DateKey),
    ResellerKey INT NOT NULL REFERENCES DimReseller(ResellerKey),
    EmployeeKey INT NOT NULL REFERENCES DimEmployee(EmployeeKey),
    PromotionKey INT NOT NULL REFERENCES DimPromotion(PromotionKey),
    CurrencyKey INT NOT NULL REFERENCES DimCurrency(CurrencyKey),
    SalesTerritoryKey INT NOT NULL REFERENCES DimSalesTerritory(SalesTerritoryKey),
    SalesOrderNumber VARCHAR(20) NOT NULL,
    SalesOrderLineNumber SMALLINT NOT NULL,
    RevisionNumber SMALLINT,
    OrderQuantity SMALLINT,
    UnitPrice NUMERIC(15,4),
    ExtendedAmount NUMERIC(15,4),
    UnitPriceDiscountPct NUMERIC(5,4),
    DiscountAmount FLOAT,
    ProductStandardCost NUMERIC(15,4),
    TotalProductCost NUMERIC(15,4),
    SalesAmount NUMERIC(15,4),
    TaxAmt NUMERIC(15,4),
    Freight NUMERIC(15,4),
    CarrierTrackingNumber VARCHAR(25),
    CustomerPONumber VARCHAR(25),
    OrderDate TIMESTAMP,
    DueDate TIMESTAMP,
    ShipDate TIMESTAMP,
    PRIMARY KEY (SalesOrderNumber, SalesOrderLineNumber)
);


-- Columna de control: última fecha de carga (en todas las tablas)
ALTER TABLE IF EXISTS DimDate ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimSalesTerritory ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimGeography ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimCustomer ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimProductCategory ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimProductSubcategory ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimProduct ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimReseller ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimEmployee ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimPromotion ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimCurrency ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS DimSalesReason ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS FactInternetSales ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS FactInternetSalesReason ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;
ALTER TABLE IF EXISTS FactResellerSales ADD COLUMN IF NOT EXISTS ultima_fecha_carga TIMESTAMP;