import pandas as pd

def transform_dim_cliente(
    df_customer: pd.DataFrame,
    df_person: pd.DataFrame,
    df_geography: pd.DataFrame = None
) -> pd.DataFrame:
    """
    Transforma clientes individuales para DimCustomer (Internet Sales) usando Pandas.
    """
    # Filtrar solo clientes individuales (PersonID not null)
    df_ind_cust = df_customer[df_customer['PersonID'].notnull()].copy()
    
    # Merge con Person
    df = df_ind_cust.merge(
        df_person, 
        how='left', 
        left_on='PersonID', 
        right_on='BusinessEntityID'
    )
    
    # Mapeo a las columnas dimensionales
    df['CustomerKey'] = df['CustomerID']
    df['CustomerAlternateKey'] = df['AccountNumber']
    df['Title'] = df.get('Title', None)
    df['FirstName'] = df['FirstName']
    df['MiddleName'] = df.get('MiddleName', None)
    df['LastName'] = df['LastName']
    df['Suffix'] = df.get('Suffix', None)
    df['GeographyKey'] = df.get('TerritoryID', None)
    
    cols = ['CustomerKey', 'CustomerAlternateKey', 'GeographyKey', 'Title', 'FirstName', 'MiddleName', 'LastName', 'Suffix']
    existing_cols = [c for c in cols if c in df.columns]
    return df[existing_cols]
