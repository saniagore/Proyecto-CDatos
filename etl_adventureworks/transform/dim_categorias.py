import pandas as pd

def transform_dim_product_category(df_cat: pd.DataFrame) -> pd.DataFrame:
    df = df_cat.copy()
    df['ProductCategoryKey'] = df['ProductCategoryID']
    df['ProductCategoryAlternateKey'] = df['ProductCategoryID']
    df['EnglishProductCategoryName'] = df['Name']
    cols = ['ProductCategoryKey', 'ProductCategoryAlternateKey', 'EnglishProductCategoryName']
    return df[cols]

def transform_dim_product_subcategory(df_subcat: pd.DataFrame) -> pd.DataFrame:
    df = df_subcat.copy()
    df['ProductSubcategoryKey'] = df['ProductSubcategoryID']
    df['ProductSubcategoryAlternateKey'] = df['ProductSubcategoryID']
    df['EnglishProductSubcategoryName'] = df['Name']
    df['ProductCategoryKey'] = df['ProductCategoryID']
    cols = ['ProductSubcategoryKey', 'ProductSubcategoryAlternateKey', 'EnglishProductSubcategoryName', 'ProductCategoryKey']
    return df[cols]
