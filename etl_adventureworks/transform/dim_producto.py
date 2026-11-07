import pandas as pd

def transform_dim_producto(
    df_product: pd.DataFrame,
    df_subcategory: pd.DataFrame,
    df_category: pd.DataFrame
) -> pd.DataFrame:
    """
    Transforma y desnormaliza categorías y subcategorías para DimProduct usando Pandas.
    """
    df = df_product.copy()
    
    # Merge con subcategoría
    df = df.merge(
        df_subcategory, 
        how='left', 
        left_on='ProductSubcategoryID', 
        right_on='ProductSubcategoryID', 
        suffixes=('', '_sub')
    )
    
    # Merge con categoría
    df = df.merge(
        df_category, 
        how='left', 
        left_on='ProductCategoryID', 
        right_on='ProductCategoryID', 
        suffixes=('', '_cat')
    )
    
    # Asignación de surrogate keys y renombrado
    df['ProductKey'] = df['ProductID']
    df['ProductAlternateKey'] = df['ProductNumber']
    df['ProductSubcategoryKey'] = df['ProductSubcategoryID']
    df['EnglishProductName'] = df['Name']
    
    # Columnas esperadas en el modelo OLAP
    cols = [
        'ProductKey', 'ProductAlternateKey', 'ProductSubcategoryKey',
        'EnglishProductName', 'StandardCost', 'Color', 'SafetyStockLevel',
        'ReorderPoint', 'ListPrice', 'Size', 'Weight', 'DaysToManufacture',
        'ProductLine', 'Class', 'Style'
    ]
    
    # Asegurar que existan las columnas en el dataframe
    existing_cols = [c for c in cols if c in df.columns]
    return df[existing_cols]
