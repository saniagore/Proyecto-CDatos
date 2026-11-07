import pandas as pd

def transform_fact_internet_sales(
    df_header: pd.DataFrame,
    df_detail: pd.DataFrame
) -> pd.DataFrame:
    """
    Transforma el datamart de FactInternetSales (OnlineOrderFlag = 1 / True) usando Pandas.
    Granularidad: Línea de pedido.
    """
    # Filtrar ventas por internet
    df_h = df_header[df_header['OnlineOrderFlag'] == 1].copy()
    
    # Unir encabezado y detalle
    df = df_detail.merge(df_h, on='SalesOrderID', how='inner')
    
    # Claves dimensionales (fechas a formato YYYYMMDD)
    df['OrderDateKey'] = pd.to_datetime(df['OrderDate']).dt.strftime('%Y%m%d').astype(int)
    df['DueDateKey'] = pd.to_datetime(df['DueDate']).dt.strftime('%Y%m%d').astype(int)
    df['ShipDateKey'] = pd.to_datetime(df['ShipDate']).dt.strftime('%Y%m%d').astype(int)
    
    df['ProductKey'] = df['ProductID']
    df['CustomerKey'] = df['CustomerID']
    df['PromotionKey'] = df['SpecialOfferID']
    df['CurrencyKey'] = df.get('CurrencyRateID', 100) # Por defecto o mapeo
    df['SalesTerritoryKey'] = df['TerritoryID']
    
    df['SalesOrderNumber'] = df['SalesOrderNumber']
    df['SalesOrderLineNumber'] = df['SalesOrderDetailID']
    df['OrderQuantity'] = df['OrderQty']
    df['UnitPrice'] = df['UnitPrice']
    df['UnitPriceDiscountPct'] = df['UnitPriceDiscount']
    
    # Medidas aditivas
    df['ExtendedAmount'] = df['OrderQuantity'] * df['UnitPrice']
    df['DiscountAmount'] = df['ExtendedAmount'] * df['UnitPriceDiscountPct']
    df['SalesAmount'] = df['ExtendedAmount'] - df['DiscountAmount']
    df['TotalProductCost'] = df.get('TotalProductCost', 0.0)
    df['TaxAmt'] = df['TaxAmt']
    df['Freight'] = df['Freight']
    
    cols = [
        'ProductKey', 'OrderDateKey', 'DueDateKey', 'ShipDateKey',
        'CustomerKey', 'PromotionKey', 'CurrencyKey', 'SalesTerritoryKey',
        'SalesOrderNumber', 'SalesOrderLineNumber', 'OrderQuantity',
        'UnitPrice', 'ExtendedAmount', 'UnitPriceDiscountPct', 'DiscountAmount',
        'TotalProductCost', 'SalesAmount', 'TaxAmt', 'Freight'
    ]
    existing_cols = [c for c in cols if c in df.columns]
    return df[existing_cols]

def transform_fact_reseller_sales(
    df_header: pd.DataFrame,
    df_detail: pd.DataFrame
) -> pd.DataFrame:
    """
    Transforma el datamart de FactResellerSales (OnlineOrderFlag = 0 / False) usando Pandas.
    Granularidad: Línea de pedido.
    """
    df_h = df_header[df_header['OnlineOrderFlag'] == 0].copy()
    df = df_detail.merge(df_h, on='SalesOrderID', how='inner')
    
    df['OrderDateKey'] = pd.to_datetime(df['OrderDate']).dt.strftime('%Y%m%d').astype(int)
    df['DueDateKey'] = pd.to_datetime(df['DueDate']).dt.strftime('%Y%m%d').astype(int)
    df['ShipDateKey'] = pd.to_datetime(df['ShipDate']).dt.strftime('%Y%m%d').astype(int)
    
    df['ProductKey'] = df['ProductID']
    df['ResellerKey'] = df['CustomerID']  # O CustomerID mapeado a ResellerKey
    df['EmployeeKey'] = df['SalesPersonID']
    df['PromotionKey'] = df['SpecialOfferID']
    df['CurrencyKey'] = df.get('CurrencyRateID', 100)
    df['SalesTerritoryKey'] = df['TerritoryID']
    
    df['SalesOrderNumber'] = df['SalesOrderNumber']
    df['SalesOrderLineNumber'] = df['SalesOrderDetailID']
    df['OrderQuantity'] = df['OrderQty']
    df['UnitPrice'] = df['UnitPrice']
    df['UnitPriceDiscountPct'] = df['UnitPriceDiscount']
    
    df['ExtendedAmount'] = df['OrderQuantity'] * df['UnitPrice']
    df['DiscountAmount'] = df['ExtendedAmount'] * df['UnitPriceDiscountPct']
    df['SalesAmount'] = df['ExtendedAmount'] - df['DiscountAmount']
    df['TotalProductCost'] = df.get('TotalProductCost', 0.0)
    df['TaxAmt'] = df['TaxAmt']
    df['Freight'] = df['Freight']
    
    cols = [
        'ProductKey', 'OrderDateKey', 'DueDateKey', 'ShipDateKey',
        'ResellerKey', 'EmployeeKey', 'PromotionKey', 'CurrencyKey', 'SalesTerritoryKey',
        'SalesOrderNumber', 'SalesOrderLineNumber', 'OrderQuantity',
        'UnitPrice', 'ExtendedAmount', 'UnitPriceDiscountPct', 'DiscountAmount',
        'TotalProductCost', 'SalesAmount', 'TaxAmt', 'Freight'
    ]
    existing_cols = [c for c in cols if c in df.columns]
    return df[existing_cols]
