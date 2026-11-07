import pandas as pd

def transform_dim_date(df_orders: pd.DataFrame) -> pd.DataFrame:
    """
    Genera el DataFrame para DimDate a partir del rango de fechas de las órdenes.
    """
    min_date = df_orders[['OrderDate', 'DueDate', 'ShipDate']].min().min()
    max_date = df_orders[['OrderDate', 'DueDate', 'ShipDate']].max().max()

    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    df_date = pd.DataFrame({'FullDateAlternateKey': date_range})

    df_date['DateKey'] = df_date['FullDateAlternateKey'].dt.strftime('%Y%m%d').astype(int)
    df_date['DayNumberOfWeek'] = df_date['FullDateAlternateKey'].dt.dayofweek + 1
    df_date['EnglishDayNameOfWeek'] = df_date['FullDateAlternateKey'].dt.day_name()
    df_date['DayNumberOfMonth'] = df_date['FullDateAlternateKey'].dt.day
    df_date['DayNumberOfYear'] = df_date['FullDateAlternateKey'].dt.dayofyear
    df_date['WeekNumberOfYear'] = df_date['FullDateAlternateKey'].dt.isocalendar().week
    df_date['EnglishMonthName'] = df_date['FullDateAlternateKey'].dt.month_name()
    df_date['MonthNumberOfYear'] = df_date['FullDateAlternateKey'].dt.month
    df_date['CalendarQuarter'] = df_date['FullDateAlternateKey'].dt.quarter
    df_date['CalendarYear'] = df_date['FullDateAlternateKey'].dt.year
    df_date['CalendarSemester'] = ((df_date['MonthNumberOfYear'] - 1) // 6) + 1

    return df_date
