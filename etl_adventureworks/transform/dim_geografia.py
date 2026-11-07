import pandas as pd

def transform_dim_sales_territory(df_territory: pd.DataFrame) -> pd.DataFrame:
    df = df_territory.copy()
    df['SalesTerritoryKey'] = df['TerritoryID']
    df['SalesTerritoryAlternateKey'] = df['TerritoryID']
    df['SalesTerritoryRegion'] = df['Name']
    df['SalesTerritoryCountry'] = df['CountryRegionCode']
    df['SalesTerritoryGroup'] = df['Group']
    cols = ['SalesTerritoryKey', 'SalesTerritoryAlternateKey', 'SalesTerritoryRegion', 'SalesTerritoryCountry', 'SalesTerritoryGroup']
    return df[cols]

def transform_dim_geography(df_address: pd.DataFrame, df_sp: pd.DataFrame, df_cr: pd.DataFrame) -> pd.DataFrame:
    df = df_address.merge(df_sp, on='StateProvinceID', how='inner')
    df = df.merge(df_cr, on='CountryRegionCode', how='inner')
    df['GeographyKey'] = df['AddressID']
    df['City'] = df['City']
    df['StateProvinceCode'] = df['StateProvinceCode']
    df['StateProvinceName'] = df['Name_x']
    df['CountryRegionCode'] = df['CountryRegionCode']
    df['EnglishCountryRegionName'] = df['Name_y']
    df['PostalCode'] = df['PostalCode']
    df['SalesTerritoryKey'] = df['TerritoryID']
    cols = ['GeographyKey', 'City', 'StateProvinceCode', 'StateProvinceName', 'CountryRegionCode', 'EnglishCountryRegionName', 'PostalCode', 'SalesTerritoryKey']
    return df[cols]
