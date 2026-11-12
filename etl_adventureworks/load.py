import pandas as pd
from datetime import datetime
from .config import get_olap_engine, OLAP_SCHEMA
from sqlalchemy import text

def load_to_postgres(df: pd.DataFrame, table_name: str, if_exists: str = 'append', chunksize: int = 5000):
    """
    Carga un DataFrame de Pandas a una tabla en PostgreSQL usando SQLAlchemy.
    Si if_exists='truncate_first', vacía la tabla antes de insertar para evitar duplicados.
    """
    engine = get_olap_engine()
    print(f"-> Cargando {len(df)} registros en la tabla '{table_name}'...")
    
    # Normalizar nombres de columnas a minúsculas para coincidir exactamente con PostgreSQL
    df_to_load = df.copy()
    df_to_load.columns = [col.lower() for col in df_to_load.columns]
    df_to_load['ultima_fecha_carga'] = datetime.now()  
    tbl_name = table_name.lower()

    if if_exists == 'truncate_first':
        with engine.begin() as conn:
            conn.execute(
                text(
                    f'TRUNCATE TABLE "{OLAP_SCHEMA}"."{tbl_name}" '
                    "CASCADE"
                )
            )
        actual_if_exists = 'append'
    else:
        actual_if_exists = if_exists

    df_to_load.to_sql(
        name=tbl_name,
        con=engine,
        schema=OLAP_SCHEMA,
        if_exists=actual_if_exists,
        index=False,
        chunksize=min(chunksize, 1000),
        method='multi'
    )
    print(f"OK: Tabla '{table_name}' cargada exitosamente.")

def execute_sql_file(file_path: str):
    """
    Ejecuta un script SQL (por ejemplo el DDL) en la base de datos destino PostgreSQL.
    """
    engine = get_olap_engine()
    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    with engine.begin() as conn:
        conn.exec_driver_sql(sql)
    print(f"OK: Script SQL '{file_path}' ejecutado con exito.")
