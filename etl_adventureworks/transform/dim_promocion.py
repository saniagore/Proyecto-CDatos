import pandas as pd

def transform_dim_promotion(df_offer: pd.DataFrame) -> pd.DataFrame:
    """
    DimPromotion: una fila por oferta especial.
    La llave es SpecialOfferID, así que no hace falta generarla.
    """
    df = df_offer.copy()
    df['PromotionKey'] = df['SpecialOfferID']
    df['PromotionAlternateKey'] = df['SpecialOfferID']
    df['EnglishPromotionName'] = df['Description']
    df['EnglishPromotionType'] = df['Type']
    df['EnglishPromotionCategory'] = df['Category']
    cols = ['PromotionKey', 'PromotionAlternateKey', 'EnglishPromotionName', 'DiscountPct',
            'EnglishPromotionType', 'EnglishPromotionCategory', 'StartDate', 'EndDate',
            'MinQty', 'MaxQty']
    return df[cols]