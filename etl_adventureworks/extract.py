import pandas as pd
from .config import get_oltp_engine

def extract_table(query_or_table_name: str) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL en la base de datos operacional (SQL Server)
    y retorna un DataFrame de Pandas.
    """
    engine = get_oltp_engine()
    with engine.connect() as connection:
        if " " in query_or_table_name.strip():
            query = query_or_table_name
        else:
            query = f"SELECT * FROM {query_or_table_name}"
        df = pd.read_sql(query, con=connection)
    return df

def extract_sales_order_header() -> pd.DataFrame:
    return extract_table("Sales.SalesOrderHeader")

def extract_sales_order_detail() -> pd.DataFrame:
    return extract_table("Sales.SalesOrderDetail")

def extract_customer() -> pd.DataFrame:
    return extract_table("Sales.Customer")

def extract_person() -> pd.DataFrame:
    return extract_table("Person.Person")

def extract_store() -> pd.DataFrame:
    return extract_table("Sales.Store")

def extract_product() -> pd.DataFrame:
    return extract_table("Production.Product")

def extract_product_subcategory() -> pd.DataFrame:
    return extract_table("Production.ProductSubcategory")

def extract_product_category() -> pd.DataFrame:
    return extract_table("Production.ProductCategory")

# No pasamos todo porque genera error 
# Person.Address tiene SpatialLocation (tipo geography), que pyodbc no puede leer.
def extract_address():
    return extract_table("""
        SELECT AddressID, AddressLine1, AddressLine2, City, StateProvinceID, PostalCode
        FROM Person.Address
    """)

def extract_state_province() -> pd.DataFrame:
    return extract_table("Person.StateProvince")

def extract_country_region() -> pd.DataFrame:
    return extract_table("Person.CountryRegion")

def extract_sales_territory() -> pd.DataFrame:
    return extract_table("Sales.SalesTerritory")

# No pasamos todo porque genera error 
# HumanResources.Employee tiene un campo de tipo hierarchyid, que pyodbc no puede leer.
def extract_employee():
    return extract_table("""
        SELECT BusinessEntityID, NationalIDNumber, LoginID, JobTitle, BirthDate,
               MaritalStatus, Gender, HireDate, SalariedFlag, VacationHours,
               SickLeaveHours, CurrentFlag
        FROM HumanResources.Employee
    """)

def extract_sales_person() -> pd.DataFrame:
    return extract_table("Sales.SalesPerson")

def extract_special_offer() -> pd.DataFrame:
    return extract_table("Sales.SpecialOffer")

def extract_currency() -> pd.DataFrame:
    return extract_table("Sales.Currency")

def extract_currency_rate() -> pd.DataFrame:
    return extract_table("Sales.CurrencyRate")

def extract_sales_reason() -> pd.DataFrame:
    return extract_table("Sales.SalesReason")

def extract_sales_order_header_sales_reason() -> pd.DataFrame:
    return extract_table("Sales.SalesOrderHeaderSalesReason")

def extract_product_cost_history() -> pd.DataFrame:
    return extract_table("Production.ProductCostHistory")
