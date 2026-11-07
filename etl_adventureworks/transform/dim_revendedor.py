import pandas as pd

def transform_dim_revendedor(
    df_customer: pd.DataFrame,
    df_store: pd.DataFrame,
    df_geography: pd.DataFrame = None
) -> pd.DataFrame:
    """
    Transforma tiendas/revendedores para DimReseller (Reseller Sales) usando Pandas.
    """
    # Filtrar clientes tipo tienda (StoreID not null)
    df_store_cust = df_customer[df_customer['StoreID'].notnull()].copy()
    
    # Merge con Store
    df = df_store_cust.merge(
        df_store,
        how='inner',
        left_on='StoreID',
        right_on='BusinessEntityID'
    )
    
    df['ResellerKey'] = df['StoreID']
    df['ResellerAlternateKey'] = df['AccountNumber']
    df['ResellerName'] = df['Name']
    df['GeographyKey'] = df.get('TerritoryID', None)
    
    cols = ['ResellerKey', 'ResellerAlternateKey', 'ResellerName', 'GeographyKey']
    existing_cols = [c for c in cols if c in df.columns]
    return df[existing_cols]
