import pandas as pd


def transform_dim_sales_reason(df_reason: pd.DataFrame) -> pd.DataFrame:
    """
    DimSalesReason: una fila por motivo de venta. La llave es SalesReasonID.
    """
    df = df_reason.copy()
    df['SalesReasonKey'] = df['SalesReasonID']
    df['SalesReasonAlternateKey'] = df['SalesReasonID']
    df['SalesReasonName'] = df['Name']
    df['SalesReasonReasonType'] = df['ReasonType']
    cols = ['SalesReasonKey', 'SalesReasonAlternateKey', 'SalesReasonName', 'SalesReasonReasonType']
    return df[cols]