import pandas as pd
from .config import get_olap_engine

def get_row_count(engine, table_name: str) -> int:
    query = f"SELECT COUNT(*) FROM {table_name};"
    df = pd.read_sql(query, con=engine)
    return int(df.iloc[0, 0])

def validate_etl():
    """
    Realiza validaciones de conteos y sumas de control
    entre el Datamart construido y la bodega migrada en la entrega 3.
    """
    engine = get_olap_engine()
    print("==========================================")
    print("VALIDACIÓN DE DATAMARTS CON PANDAS / SQL")
    print("==========================================")
    
    tables_to_check = [
        "dimproduct",
        "dimcustomer",
        "dimreseller",
        "dimdate",
        "factinternetsales",
        "factresellersales"
    ]
    
    for table in tables_to_check:
        try:
            count = get_row_count(engine, table)
            print(f"[{table}] Total de registros cargados: {count}")
        except Exception as e:
            print(f"[{table}] Error al validar: {e}")

    # Validaciones de medidas de control (sumas de ventas)
    try:
        sales_query = """
            SELECT 
                SUM(SalesAmount) AS TotalSalesAmount,
                SUM(OrderQuantity) AS TotalOrderQuantity
            FROM factinternetsales;
        """
        df_metrics = pd.read_sql(sales_query, con=engine)
        print("\n--- Métricas de Control (Internet Sales) ---")
        print(df_metrics.to_string(index=False))
    except Exception as e:
        print(f"Error calculando métricas: {e}")

if __name__ == "__main__":
    validate_etl()
