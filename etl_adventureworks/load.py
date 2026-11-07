import pandas as pd
from .config import get_olap_engine, OLAP_SCHEMA

def load_to_postgres(df: pd.DataFrame, table_name: str, if_exists: str = 'append', chunksize: int = 5000):
    """
    Carga un DataFrame de Pandas a una tabla en PostgreSQL usando SQLAlchemy.
    """
    engine = get_olap_engine()
    print(f"-> Cargando {len(df)} registros en la tabla '{table_name}'...")
    df.to_sql(
        name=table_name.lower(),
        con=engine,
        schema=OLAP_SCHEMA,
        if_exists=if_exists,
        index=False,
        chunksize=chunksize,
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
