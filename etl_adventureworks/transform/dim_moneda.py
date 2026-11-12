import pandas as pd

def transform_dim_currency(df_currency: pd.DataFrame) -> pd.DataFrame:
    """
    DimCurrency: una fila por moneda.
    En la OLTP no hay una llave numérica, así que la generamos como 1, 2, 3...
    (igual que el profesor, cuyas llaves sustitutas salen del índice).
    """
    df = df_currency.copy()
    df = df.sort_values('CurrencyCode').reset_index(drop=True)
    df['CurrencyKey'] = df.index + 1
    df['CurrencyAlternateKey'] = df['CurrencyCode']
    df['CurrencyName'] = df['Name']
    cols = ['CurrencyKey', 'CurrencyAlternateKey', 'CurrencyName']
    return df[cols]