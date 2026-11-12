import pandas as pd

def transform_fact_internet_sales(
    df_header: pd.DataFrame,
    df_detail: pd.DataFrame,
    df_cost_history: pd.DataFrame,
    df_currency_rate: pd.DataFrame,
    df_dim_currency: pd.DataFrame
) -> pd.DataFrame:
    """
    Transforma el datamart de FactInternetSales (OnlineOrderFlag = 1 / True) usando Pandas.
    Granularidad: Línea de pedido.
    """
    # Solo pedidos por internet
    df_h = df_header[df_header['OnlineOrderFlag'] == 1].copy()
    df = df_detail.merge(df_h, on='SalesOrderID', how='inner')

    # Número de línea dentro de cada pedido: 1, 2, 3...
    df = df.sort_values(['SalesOrderID', 'SalesOrderDetailID'])
    df['SalesOrderLineNumber'] = df.groupby('SalesOrderID').cumcount() + 1

    # Costo vigente en la fecha del pedido (historial de costos)
    df = df.sort_values('OrderDate')
    df_cost = df_cost_history[['ProductID', 'StartDate', 'StandardCost']].sort_values('StartDate')
    df = pd.merge_asof(df, df_cost, left_on='OrderDate', right_on='StartDate',
                       by='ProductID', direction='backward')
    df['ProductStandardCost'] = df['StandardCost']

    # Moneda de la venta. Si el pedido no tiene tasa (NULL), es USD.
    df = df.merge(df_currency_rate[['CurrencyRateID', 'ToCurrencyCode']],
                  on='CurrencyRateID', how='left')
    df['ToCurrencyCode'] = df['ToCurrencyCode'].fillna('USD')
    df = df.merge(df_dim_currency[['CurrencyKey', 'CurrencyAlternateKey']],
                  left_on='ToCurrencyCode', right_on='CurrencyAlternateKey', how='left')
    
    # Llaves de fecha (YYYYMMDD)
    df['OrderDateKey'] = pd.to_datetime(df['OrderDate']).dt.strftime('%Y%m%d').astype(int)
    df['DueDateKey'] = pd.to_datetime(df['DueDate']).dt.strftime('%Y%m%d').astype(int)
    df['ShipDateKey'] = pd.to_datetime(df['ShipDate']).dt.strftime('%Y%m%d').astype(int)

    # Llaves de las demás dimensiones
    df['ProductKey'] = df['ProductID']
    df['CustomerKey'] = df['CustomerID']
    df['PromotionKey'] = df['SpecialOfferID']
    df['SalesTerritoryKey'] = df['TerritoryID']
    df['CustomerPONumber'] = df['PurchaseOrderNumber']

    # Cantidad y medidas de la línea
    df['SalesOrderNumber'] = df['SalesOrderNumber']
    df['OrderQuantity'] = df['OrderQty']
    df['UnitPrice'] = df['UnitPrice']
    df['UnitPriceDiscountPct'] = df['UnitPriceDiscount']
    df['ExtendedAmount'] = df['OrderQuantity'] * df['UnitPrice']
    df['DiscountAmount'] = df['ExtendedAmount'] * df['UnitPriceDiscountPct']
    df['SalesAmount'] = df['ExtendedAmount'] - df['DiscountAmount']
    df['TotalProductCost'] = df['OrderQuantity'] * df['ProductStandardCost']
    
    # Flete e impuesto: están a nivel de pedido, así que se reparten entre sus líneas
    total_pedido = df.groupby('SalesOrderID')['LineTotal'].transform('sum')
    proporcion = df['LineTotal'] / total_pedido
    df['Freight'] = df['Freight'] * proporcion
    df['TaxAmt'] = df['TaxAmt'] * proporcion

    # Columnas finales esperadas en el modelo OLAP
    cols = [
        'ProductKey', 'OrderDateKey', 'DueDateKey', 'ShipDateKey',
        'CustomerKey', 'PromotionKey', 'CurrencyKey', 'SalesTerritoryKey',
        'SalesOrderNumber', 'SalesOrderLineNumber', 'RevisionNumber', 
        'OrderQuantity', 'UnitPrice', 'ExtendedAmount', 'UnitPriceDiscountPct', 
        'DiscountAmount', 'ProductStandardCost', 'TotalProductCost', 'SalesAmount', 
        'TaxAmt', 'Freight', 'CarrierTrackingNumber', 'CustomerPONumber',
        'OrderDate', 'DueDate', 'ShipDate'
    ]
    # existing_cols = [c for c in cols if c in df.columns]
    return df[cols]

def transform_fact_reseller_sales(
    df_header: pd.DataFrame,
    df_detail: pd.DataFrame,
    df_customer: pd.DataFrame,
    df_cost_history: pd.DataFrame,
    df_currency_rate: pd.DataFrame,
    df_dim_currency: pd.DataFrame,
    df_product: pd.DataFrame
) -> pd.DataFrame:
    """
    Transforma el datamart de FactResellerSales (OnlineOrderFlag = 0 / False) usando Pandas.
    Granularidad: Línea de pedido.
    """
    # Solo pedidos de revendedores
    df_h = df_header[df_header['OnlineOrderFlag'] == 0].copy()
    df = df_detail.merge(df_h, on='SalesOrderID', how='inner')

    # Entrega 3 solo incluye líneas vendidas durante la vigencia del producto.
    product_dates = df_product[
        ['ProductID', 'SellStartDate', 'SellEndDate']
    ].drop_duplicates('ProductID')
    df = df.merge(product_dates, on='ProductID', how='inner')
    valid_product_date = (
        (df['OrderDate'] >= df['SellStartDate'])
        & (df['SellEndDate'].isna() | (df['OrderDate'] <= df['SellEndDate']))
    )
    df = df[valid_product_date].copy()
    
    # Número de línea dentro de cada pedido: 1, 2, 3...
    df = df.sort_values(['SalesOrderID', 'SalesOrderDetailID'])
    df['SalesOrderLineNumber'] = df.groupby('SalesOrderID').cumcount() + 1

    # Revendedor: el StoreID del cliente es la llave del revendedor
    df = df.merge(df_customer[['CustomerID', 'StoreID']], on='CustomerID', how='left')
    df['ResellerKey'] = df['StoreID']

    # Costo vigente en la fecha del pedido (historial de costos)
    df = df.sort_values('OrderDate')
    df_cost = df_cost_history[['ProductID', 'StartDate', 'StandardCost']].sort_values('StartDate')
    df = pd.merge_asof(df, df_cost, left_on='OrderDate', right_on='StartDate',
                       by='ProductID', direction='backward')
    df['ProductStandardCost'] = df['StandardCost']

    # Moneda de la venta (igual que en internet). Si no hay tasa, USD.
    df = df.merge(df_currency_rate[['CurrencyRateID', 'ToCurrencyCode']],
                  on='CurrencyRateID', how='left')
    df['ToCurrencyCode'] = df['ToCurrencyCode'].fillna('USD')
    df = df.merge(df_dim_currency[['CurrencyKey', 'CurrencyAlternateKey']],
                  left_on='ToCurrencyCode', right_on='CurrencyAlternateKey', how='left')

    # Llaves de fecha (YYYYMMDD)
    df['OrderDateKey'] = pd.to_datetime(df['OrderDate']).dt.strftime('%Y%m%d').astype(int)
    df['DueDateKey'] = pd.to_datetime(df['DueDate']).dt.strftime('%Y%m%d').astype(int)
    df['ShipDateKey'] = pd.to_datetime(df['ShipDate']).dt.strftime('%Y%m%d').astype(int)

    # Llaves de las demás dimensiones
    df['ProductKey'] = df['ProductID']
    df['EmployeeKey'] = df['SalesPersonID']
    df['PromotionKey'] = df['SpecialOfferID']
    df['SalesTerritoryKey'] = df['TerritoryID']
    df['CustomerPONumber'] = df['PurchaseOrderNumber']

    # Cantidad y medidas de la línea
    df['SalesOrderNumber'] = df['SalesOrderNumber']
    df['OrderQuantity'] = df['OrderQty']
    df['UnitPrice'] = df['UnitPrice']
    df['UnitPriceDiscountPct'] = df['UnitPriceDiscount']
    df['ExtendedAmount'] = df['OrderQuantity'] * df['UnitPrice']
    df['DiscountAmount'] = df['ExtendedAmount'] * df['UnitPriceDiscountPct']
    df['SalesAmount'] = df['ExtendedAmount'] - df['DiscountAmount']
    df['TotalProductCost'] = df['OrderQuantity'] * df['ProductStandardCost']

    # Flete e impuesto: se reparten entre las líneas del pedido según LineTotal
    total_pedido = df.groupby('SalesOrderID')['LineTotal'].transform('sum')
    proporcion = df['LineTotal'] / total_pedido
    df['Freight'] = df['Freight'] * proporcion
    df['TaxAmt'] = df['TaxAmt'] * proporcion
    
    cols = [
        'ProductKey', 'OrderDateKey', 'DueDateKey', 'ShipDateKey',
        'ResellerKey', 'EmployeeKey', 'PromotionKey', 'CurrencyKey', 'SalesTerritoryKey',
        'SalesOrderNumber', 'SalesOrderLineNumber', 'RevisionNumber',
        'OrderQuantity', 'UnitPrice', 'ExtendedAmount', 'UnitPriceDiscountPct', 
        'DiscountAmount', 'ProductStandardCost', 'TotalProductCost', 'SalesAmount', 
        'TaxAmt', 'Freight', 'CarrierTrackingNumber', 'CustomerPONumber',
        'OrderDate', 'DueDate', 'ShipDate'
    ]
    #existing_cols = [c for c in cols if c in df.columns]
    return df[cols]

def transform_fact_internet_sales_reason(
    df_header: pd.DataFrame,
    df_detail: pd.DataFrame,
    df_header_reason: pd.DataFrame
) -> pd.DataFrame:
    """
    FactInternetSalesReason: una fila por línea de internet y motivo.
    La numeración de línea es la misma que usa FactInternetSales.
    """
    # Solo pedidos por internet, con su número de pedido
    df_h = df_header[df_header['OnlineOrderFlag'] == 1][['SalesOrderID', 'SalesOrderNumber']]
    df = df_detail.merge(df_h, on='SalesOrderID', how='inner')

    # Misma numeración de línea que en FactInternetSales
    df = df.sort_values(['SalesOrderID', 'SalesOrderDetailID'])
    df['SalesOrderLineNumber'] = df.groupby('SalesOrderID').cumcount() + 1

    # Cada línea recibe los motivos de su pedido
    df = df.merge(df_header_reason[['SalesOrderID', 'SalesReasonID']], on='SalesOrderID', how='inner')
    df['SalesReasonKey'] = df['SalesReasonID']

    df['SalesReasonAlternateKey'] = df['SalesReasonID']

    cols = ['SalesOrderNumber', 'SalesOrderLineNumber', 'SalesReasonKey']
    return df[cols]
